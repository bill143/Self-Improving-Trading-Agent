"""Compliance service layer: schedule obligations, refresh statuses, and compute
audit-readiness. This is what the dashboard, the CLI, and the AI fleet all call.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

from . import obligations as ob
from .db import DB


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def schedule_event(db: DB, rule_key: str, event_at: date | datetime,
                   *, subject_type: str, subject_id: str = "", actor: str = "system") -> int:
    """Create a concrete obligation from an EVENT (e.g. an incident occurred)."""
    rule = ob.rule(rule_key)
    due = ob.event_due(rule, event_at)
    return db.add_obligation(rule_key, subject_type, due.isoformat(),
                             subject_id=subject_id, notes=rule.name, actor=actor)


def schedule_expiry(db: DB, rule_key: str, expires_on: date,
                    *, subject_type: str, subject_id: str = "", actor: str = "system") -> int:
    """Create a renewal obligation from a credential/registration expiry."""
    rule = ob.rule(rule_key)
    due = ob.expiry_renewal_opens(rule, expires_on)
    return db.add_obligation(rule_key, subject_type, ob._as_datetime(due).isoformat(),
                             subject_id=subject_id,
                             notes=f"{rule.name} — expires {expires_on.isoformat()}", actor=actor)


def schedule_recurring_next(db: DB, rule_key: str, anchor: date,
                            *, subject_type: str, subject_id: str = "",
                            on_or_after: date | None = None, actor: str = "system") -> int:
    """Create the next occurrence of a RECURRING obligation."""
    rule = ob.rule(rule_key)
    ref = on_or_after or date.today()
    due = ob.next_recurring_due(rule, anchor, ref)
    return db.add_obligation(rule_key, subject_type, ob._as_datetime(due).isoformat(),
                             subject_id=subject_id, notes=rule.name, actor=actor)


def refresh_statuses(db: DB, now: datetime | None = None, actor: str = "system") -> dict[str, int]:
    """Recompute status for every open obligation. Returns a count per status."""
    now = now or _now()
    counts = {s.value: 0 for s in ob.Status}
    for inst in db.open_obligations():
        rule = ob.CATALOG_BY_KEY.get(inst["rule_key"])
        lead = rule.lead_time_days if rule else 14
        due = datetime.fromisoformat(inst["due_at"])
        new_status = ob.status_for(due, now, lead)
        if new_status.value != inst["status"]:
            db.set_obligation_status(inst["id"], new_status.value, actor=actor)
        counts[new_status.value] += 1
    return counts


def audit_readiness(db: DB, now: datetime | None = None) -> dict:
    """A management-facing snapshot: are we audit-ready right now?"""
    now = now or _now()
    open_items = db.open_obligations()
    overdue, due_soon, upcoming = [], [], []
    for inst in open_items:
        rule = ob.CATALOG_BY_KEY.get(inst["rule_key"])
        lead = rule.lead_time_days if rule else 14
        due = datetime.fromisoformat(inst["due_at"])
        status = ob.status_for(due, now, lead)
        row = {
            "id": inst["id"],
            "rule_key": inst["rule_key"],
            "name": rule.name if rule else inst["rule_key"],
            "regulator": rule.regulator.value if rule else "",
            "subject": f'{inst["subject_type"]}:{inst["subject_id"]}'.rstrip(":"),
            "due_at": inst["due_at"],
        }
        if status is ob.Status.OVERDUE:
            overdue.append(row)
        elif status is ob.Status.DUE_SOON:
            due_soon.append(row)
        else:
            upcoming.append(row)
    ready = len(overdue) == 0
    return {
        "generated_at": now.isoformat(),
        "audit_ready": ready,
        "overdue_count": len(overdue),
        "due_soon_count": len(due_soon),
        "upcoming_count": len(upcoming),
        "overdue": overdue,
        "due_soon": due_soon,
        "upcoming": upcoming,
    }
