"""Deadline reminder sweep (the Reach agent's engine).

Refreshes obligation statuses, then dispatches a reminder for every due-soon item and
an escalation for every overdue item, via the connectors (queued to the outbox until
Telegram/email credentials are configured).
"""

from __future__ import annotations

from datetime import datetime

from . import connectors, service
from .db import DB
from . import obligations as ob


def sweep(db: DB, now: datetime | None = None, *, actor: str = "reach") -> dict:
    service.refresh_statuses(db, now=now, actor=actor)
    snap = service.audit_readiness(db, now=now)
    sent = {"overdue": 0, "due_soon": 0}

    for item in snap["overdue"]:
        connectors.telegram_send(
            db, f"🔴 OVERDUE: {item['name']} ({item['regulator']}) — was due {item['due_at']}. "
                f"Subject {item['subject']}. Act now.", actor=actor)
        sent["overdue"] += 1

    for item in snap["due_soon"]:
        connectors.telegram_send(
            db, f"🟠 Due soon: {item['name']} ({item['regulator']}) by {item['due_at']}. "
                f"Subject {item['subject']}.", actor=actor)
        sent["due_soon"] += 1

    db.audit(actor, "reminders:swept",
             detail=f"overdue={sent['overdue']} due_soon={sent['due_soon']}")
    return {"audit_ready": snap["audit_ready"], "reminders_dispatched": sent,
            "outbox_pending": connectors.pending_count(db)}
