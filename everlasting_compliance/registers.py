"""The registers — organisation-wide logs auditors read as proof that policy is
actually happening. A provider with polished policies but empty registers fails.

Each register entry is versioned and audit-logged. Registers that track expiries
(training, worker screening) auto-open the matching renewal obligation via the
deadline engine, so an expiring certificate can never silently lapse.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .db import DB
from . import service


@dataclass(frozen=True)
class Register:
    key: str
    name: str
    description: str
    expiry_field: str | None = None      # data key holding an ISO expiry date, if any
    linked_obligation: str | None = None  # obligations rule to open on expiry


REGISTERS: list[Register] = [
    Register("incident", "Incident register",
             "All incidents, reportable and not."),
    Register("reportable_incident", "Reportable-incident notification tracker",
             "Tracks 24h/5-day/60-day notifications to the Commission."),
    Register("complaints", "Complaints and feedback register",
             "Every complaint and feedback item, with resolution."),
    Register("continuous_improvement", "Continuous improvement register",
             "Improvements identified and actioned — audit evidence of a live QMS."),
    Register("risk", "Risk register",
             "Organisational and participant risks with controls and review dates."),
    Register("training", "Training register",
             "Worker training with expiry alerts.",
             expiry_field="expires_on", linked_obligation="first_aid_renewal"),
    Register("worker_screening", "Worker screening register",
             "NDIS Worker Screening status per worker.",
             expiry_field="expires_on", linked_obligation="worker_screening_renewal"),
    Register("restrictive_practice", "Restrictive practice register",
             "Every use of a restrictive practice (Module 2A)."),
    Register("medication_error", "Medication error register",
             "Medication errors and near-misses."),
    Register("whs_hazard", "Hazard / WHS register",
             "Workplace hazards and incidents (SafeWork NSW)."),
    Register("policy", "Policy register (version control)",
             "Every policy with version, owner, approval and review dates."),
    Register("asset_vehicle", "Asset and vehicle register",
             "Assets and vehicles, incl. registration/insurance for transport roles."),
    Register("conflict_of_interest", "Conflict of interest register",
             "Declared conflicts and how they are managed."),
    Register("consent", "Participant consent register",
             "Consents held and their refresh dates.",
             expiry_field="expires_on", linked_obligation="participant_consent_refresh"),
    Register("key_personnel", "Key personnel register",
             "Key personnel and delegations of authority."),
]

REGISTERS_BY_KEY: dict[str, Register] = {r.key: r for r in REGISTERS}


def register(key: str) -> Register:
    try:
        return REGISTERS_BY_KEY[key]
    except KeyError as exc:
        raise KeyError(f"unknown register '{key}'") from exc


class RegisterService:
    def __init__(self, db: DB):
        self.db = db

    def add_entry(self, register_key: str, data: dict, *, ref: str = "",
                  actor: str = "system", subject_id: str = "") -> int:
        """Append a versioned entry to a register. If the register tracks expiries and
        the entry carries an expiry date, auto-open the renewal obligation."""
        reg = register(register_key)
        version = 1 + sum(
            1 for e in self.db.list_records("register_entry")
            if e["data"].get("register_key") == register_key
            and (ref == "" or e["ref"] == ref)
        )
        payload = {"register_key": register_key, "version": version, **data}
        retention = "incident" if register_key in ("incident", "reportable_incident") else "default"
        rid = self.db.add_record("register_entry", payload, ref=ref,
                                 retention_class=retention, actor=actor)
        self.db.audit(actor, f"register:{register_key}:entry", str(rid), f"v{version}")

        if reg.expiry_field and reg.linked_obligation and data.get(reg.expiry_field):
            expires = date.fromisoformat(data[reg.expiry_field])
            service.schedule_expiry(self.db, reg.linked_obligation, expires,
                                    subject_type=register_key,
                                    subject_id=subject_id or ref, actor=actor)
        return rid

    def entries(self, register_key: str) -> list[dict]:
        register(register_key)  # validate
        return [e for e in self.db.list_records("register_entry")
                if e["data"].get("register_key") == register_key]

    def health(self) -> dict:
        """Register health for the dashboard: which registers have any entries.
        Empty registers are the classic audit red flag, so they are surfaced."""
        counts = {r.key: len(self.entries(r.key)) for r in REGISTERS}
        empty = [k for k, n in counts.items() if n == 0]
        return {
            "registers": len(REGISTERS),
            "entry_counts": counts,
            "empty_registers": empty,
            "all_populated": not empty,
        }
