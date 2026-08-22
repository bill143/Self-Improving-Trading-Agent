"""Phase 8 — the 5-agent fleet (Orchestrator + Scout/Scribe/Reach/Dev).

Loads the `ec-*.md` role files as system prompts and runs a role against the
compliance service using the Anthropic tool runner. `anthropic` is imported lazily so
the rest of the platform (and its tests) never depend on it being installed.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from .db import DB

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
FLEET_PREFIX = "ec-"
MODEL = os.environ.get("EC_MODEL", "claude-opus-5")

_FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class Role:
    name: str
    description: str
    body: str

    @property
    def system_prompt(self) -> str:
        return (
            f"You are `{self.name}`, a member of Everlasting Care's autonomous NDIS "
            "compliance fleet. You act through the provided tools and never invent "
            "regulatory facts, dates, or participant data. Participant data stays "
            "onshore. Human sign-off is required before real audits/claims.\n\n"
            f"{self.body}"
        )


def load_fleet(agents_dir: Path | None = None) -> dict[str, Role]:
    """Load the ec-* role definitions."""
    directory = agents_dir or AGENTS_DIR
    roles: dict[str, Role] = {}
    for path in sorted(directory.glob(f"{FLEET_PREFIX}*.md")):
        text = path.read_text(encoding="utf-8")
        name, desc, body = path.stem, "", text
        m = _FRONTMATTER.match(text)
        if m:
            body = text[m.end():].strip()
            for line in m.group(1).splitlines():
                k, _, v = line.partition(":")
                if k.strip() == "name" and v.strip():
                    name = v.strip()
                elif k.strip() == "description":
                    desc = v.strip()
        roles[name] = Role(name=name, description=desc, body=body)
    return roles


def build_fleet_tools(db: DB) -> list:
    """Compliance tools the fleet acts through. Imports anthropic lazily."""
    from anthropic import beta_tool  # noqa: PLC0415

    from . import service
    from .submissions import SubmissionService
    from .policies import PolicyService
    from .registers import RegisterService
    import json
    from datetime import datetime

    @beta_tool
    def audit_readiness() -> str:
        """Return the current audit-readiness snapshot: whether the org is audit-ready
        and the overdue / due-soon / upcoming obligation counts and lists."""
        return json.dumps(service.audit_readiness(db), default=str)

    @beta_tool
    def list_open_obligations() -> str:
        """List every open compliance obligation with its due date and status."""
        return json.dumps(db.open_obligations(), default=str)

    @beta_tool
    def log_reportable_incident(occurred_at_iso: str, participant_id: str,
                                final_report_required: bool = False) -> str:
        """Log a reportable incident and open its 24h + 5-day (and optional 60-day)
        Commission obligations. The awareness clock starts now.

        Args:
            occurred_at_iso: ISO8601 time the incident occurred / awareness began.
            participant_id: The participant involved.
            final_report_required: Whether the Commission has requested a 60-day final report.
        """
        opened = SubmissionService(db).record_reportable_incident(
            datetime.fromisoformat(occurred_at_iso.replace("Z", "")),
            participant_id, final_report_required=final_report_required, actor="fleet")
        return json.dumps({"opened_obligations": opened})

    @beta_tool
    def register_policy(policy_key: str, owner: str = "") -> str:
        """Register/version a Core Module policy and schedule its annual review.

        Args:
            policy_key: The policy key from the policy catalog.
            owner: The accountable owner role.
        """
        rid = PolicyService(db).register_policy(policy_key, owner=owner, actor="fleet")
        return f"registered policy {policy_key} (record {rid})"

    @beta_tool
    def policy_status() -> str:
        """Report which required policies are missing or overdue for review."""
        return json.dumps(PolicyService(db).status(), default=str)

    @beta_tool
    def add_register_entry(register_key: str, entry_json: str) -> str:
        """Append a versioned entry to a named register.

        Args:
            register_key: The register key (e.g. 'complaints', 'risk', 'incident').
            entry_json: JSON object of the entry's fields.
        """
        rid = RegisterService(db).add_entry(register_key, json.loads(entry_json), actor="fleet")
        return f"added entry to {register_key} register (record {rid})"

    return [audit_readiness, list_open_obligations, log_reportable_incident,
            register_policy, policy_status, add_register_entry]


def run_role(role_name: str, task: str, db: DB, *, model: str = MODEL, max_tokens: int = 8000) -> str:
    """Run a fleet role on a task with the compliance tools. Imports anthropic lazily."""
    import anthropic  # noqa: PLC0415

    roles = load_fleet()
    if role_name not in roles:
        raise KeyError(f"unknown fleet role '{role_name}'; have {sorted(roles)}")
    client = anthropic.Anthropic()
    tools = build_fleet_tools(db)
    runner = client.beta.messages.tool_runner(
        model=model, max_tokens=max_tokens,
        system=roles[role_name].system_prompt, tools=tools,
        messages=[{"role": "user", "content": task}],
    )
    last = None
    for message in runner:
        last = message
    if last is None:
        return ""
    return "".join(b.text for b in last.content if b.type == "text")
