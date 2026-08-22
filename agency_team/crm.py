"""Durable state for the autonomous agency: config, leads, clients, artifacts,
outbox, and activity log.

Everything is plain JSON/JSONL under a state directory so the pipeline is
inspectable and survives restarts. Writes are atomic (tmp file + rename).
"""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path

# Lead pipeline stages (in order).
LEAD_STAGES = ["NEW", "CONTACTED", "BOOKED", "CLOSED", "DECLINED", "DNC"]

# Client fulfillment stages — the fixed conveyor-belt order from the blueprint.
CLIENT_STAGES = [
    "ONBOARDING",
    "REACTIVATION",
    "REVIEWS_REFERRALS",
    "SPEED_TO_LEAD",
    "PAID_ADS",
    "VOICE_AI",
    "STEADY",
]

# Foundation phases — must complete in order, exactly once.
FOUNDATION_PHASES = [
    ("niche_selected", "market-research-agent"),
    ("franchises_targeted", "market-research-agent"),
    ("pillar1_reactivation_built", "reactivation-agent"),
    ("pillar2_reviews_referrals_built", "reviews-referrals-agent"),
    ("pillar3_speed_to_lead_built", "lead-nurture-agent"),
    ("ad_intelligence_built", "ads-agent"),
    ("sales_readiness_passed", "sales-closer-agent"),
]


def _default_state_dir() -> Path:
    env = os.environ.get("AGENCY_STATE_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parent.parent / "state" / "agency"


def _atomic_write(path: Path, data: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(data, encoding="utf-8")
    tmp.replace(path)


class CRM:
    def __init__(self, state_dir: Path | None = None):
        self.dir = Path(state_dir) if state_dir else _default_state_dir()
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "artifacts").mkdir(exist_ok=True)

    # ---------- generic json helpers ----------
    def _load(self, name: str, default):
        path = self.dir / name
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def _save(self, name: str, obj) -> None:
        _atomic_write(self.dir / name, json.dumps(obj, indent=2, sort_keys=True))

    def _append(self, name: str, obj: dict) -> None:
        obj = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **obj}
        with open(self.dir / name, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj) + "\n")

    # ---------- config & phase gates ----------
    @property
    def config(self) -> dict:
        return self._load("config.json", {"phase_gates": {}})

    def set_config(self, **kwargs) -> dict:
        cfg = self.config
        cfg.update(kwargs)
        self._save("config.json", cfg)
        return cfg

    def pass_gate(self, gate: str) -> None:
        cfg = self.config
        cfg.setdefault("phase_gates", {})[gate] = True
        self._save("config.json", cfg)
        self.log("gate_passed", gate=gate)

    def gate_passed(self, gate: str) -> bool:
        return bool(self.config.get("phase_gates", {}).get(gate))

    def next_foundation_phase(self) -> tuple[str, str] | None:
        for gate, owner in FOUNDATION_PHASES:
            if not self.gate_passed(gate):
                return gate, owner
        return None

    # ---------- artifacts (campaigns, research, scripts) ----------
    def save_artifact(self, name: str, content: str) -> Path:
        safe = "".join(c if c.isalnum() or c in "-_." else "-" for c in name)
        path = self.dir / "artifacts" / f"{safe}.md"
        _atomic_write(path, content)
        self.log("artifact_saved", name=safe)
        return path

    def list_artifacts(self) -> list[str]:
        return sorted(p.stem for p in (self.dir / "artifacts").glob("*.md"))

    def read_artifact(self, name: str) -> str | None:
        path = self.dir / "artifacts" / f"{name}.md"
        return path.read_text(encoding="utf-8") if path.exists() else None

    # ---------- leads ----------
    @property
    def leads(self) -> dict:
        return self._load("leads.json", {})

    def add_lead(self, **fields) -> dict:
        leads = self.leads
        # de-dupe on (business_name, city) or phone
        key_new = (
            str(fields.get("business_name", "")).lower().strip(),
            str(fields.get("city", "")).lower().strip(),
        )
        phone_new = str(fields.get("phone", "")).strip()
        for lead in leads.values():
            key_old = (
                str(lead.get("business_name", "")).lower().strip(),
                str(lead.get("city", "")).lower().strip(),
            )
            if key_new == key_old or (phone_new and phone_new == lead.get("phone")):
                return lead  # already known — never re-add (protects DNC)
        lead = {
            "id": uuid.uuid4().hex[:12],
            "stage": "NEW",
            "score": 0,
            "notes": [],
            **fields,
        }
        leads[lead["id"]] = lead
        self._save("leads.json", leads)
        return lead

    def update_lead(self, lead_id: str, stage: str | None = None, note: str | None = None, **fields) -> dict:
        leads = self.leads
        if lead_id not in leads:
            raise KeyError(f"unknown lead {lead_id}")
        lead = leads[lead_id]
        if stage:
            if stage not in LEAD_STAGES:
                raise ValueError(f"invalid stage {stage}; valid: {LEAD_STAGES}")
            if lead["stage"] == "DNC" and stage != "DNC":
                raise ValueError("DNC is permanent — lead cannot leave DNC")
            lead["stage"] = stage
        if note:
            lead.setdefault("notes", []).append(note)
        lead.update(fields)
        self._save("leads.json", leads)
        self.log("lead_updated", lead_id=lead_id, stage=lead["stage"])
        return lead

    def leads_in_stage(self, stage: str, limit: int = 25) -> list[dict]:
        pool = [l for l in self.leads.values() if l["stage"] == stage]
        pool.sort(key=lambda l: -int(l.get("score", 0)))
        return pool[:limit]

    # ---------- clients ----------
    @property
    def clients(self) -> dict:
        return self._load("clients.json", {})

    def add_client(self, lead_id: str, package: str, monthly_investment: float, cash_collected: float) -> dict:
        clients = self.clients
        client = {
            "id": uuid.uuid4().hex[:12],
            "lead_id": lead_id,
            "package": package,
            "monthly_investment": monthly_investment,
            "cash_collected": cash_collected,
            "stage": "ONBOARDING",
            "results": {},
            "notes": [],
        }
        clients[client["id"]] = client
        self._save("clients.json", clients)
        self.log("client_closed", client_id=client["id"], package=package, cash=cash_collected)
        return client

    def advance_client(self, client_id: str, stage: str, note: str | None = None) -> dict:
        clients = self.clients
        if client_id not in clients:
            raise KeyError(f"unknown client {client_id}")
        if stage not in CLIENT_STAGES:
            raise ValueError(f"invalid client stage {stage}; valid: {CLIENT_STAGES}")
        client = clients[client_id]
        # Enforce the conveyor-belt order: a client can only move forward.
        if CLIENT_STAGES.index(stage) < CLIENT_STAGES.index(client["stage"]):
            raise ValueError(
                f"fulfillment order violation: {client['stage']} -> {stage}"
            )
        client["stage"] = stage
        if note:
            client.setdefault("notes", []).append(note)
        self._save("clients.json", clients)
        self.log("client_advanced", client_id=client_id, stage=stage)
        return client

    # ---------- outbox (external actions) ----------
    def queue_action(self, kind: str, payload: dict, status: str = "queued") -> dict:
        action = {"id": uuid.uuid4().hex[:12], "kind": kind, "status": status, "payload": payload}
        self._append("outbox.jsonl", action)
        return action

    def outbox(self) -> list[dict]:
        path = self.dir / "outbox.jsonl"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    # ---------- metrics & log ----------
    def record_metric(self, name: str, value: float, context: str = "") -> None:
        self._append("metrics.jsonl", {"metric": name, "value": value, "context": context})

    def log(self, event: str, **fields) -> None:
        self._append("activity.jsonl", {"event": event, **fields})

    # ---------- summary ----------
    def summary(self) -> dict:
        leads = self.leads
        clients = self.clients
        by_stage = {s: 0 for s in LEAD_STAGES}
        for lead in leads.values():
            by_stage[lead["stage"]] = by_stage.get(lead["stage"], 0) + 1
        client_stages = {s: 0 for s in CLIENT_STAGES}
        for c in clients.values():
            client_stages[c["stage"]] = client_stages.get(c["stage"], 0) + 1
        nxt = self.next_foundation_phase()
        return {
            "niche": self.config.get("niche"),
            "owner_context": self.config.get("owner_context"),
            "next_foundation_phase": nxt[0] if nxt else None,
            "foundation_complete": nxt is None,
            "leads_total": len(leads),
            "leads_by_stage": by_stage,
            "clients_total": len(clients),
            "clients_by_stage": client_stages,
            "artifacts": self.list_artifacts(),
            "outbox_pending": sum(1 for a in self.outbox() if a["status"] == "queued"),
        }
