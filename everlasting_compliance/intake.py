"""Incident/complaint intake — turns a field message (e.g. from Telegram) into a
compliance record. Reportable-incident keywords open the 24h/5-day obligations; the
awareness clock starts when the message arrives.
"""

from __future__ import annotations

from datetime import datetime

from .db import DB
from .registers import RegisterService
from .submissions import SubmissionService

# Keywords that make an incident reportable to the Commission (spec §6).
REPORTABLE_KEYWORDS = (
    "death", "died", "serious injury", "hospital", "abuse", "neglect",
    "assault", "sexual", "unlawful", "misconduct", "restrictive practice",
    "unauthorised restrictive",
)


def classify(text: str) -> dict:
    """Best-effort classification of an intake message."""
    low = text.lower()
    reportable = any(k in low for k in REPORTABLE_KEYWORDS)
    is_complaint = any(k in low for k in ("complaint", "unhappy", "dissatisfied", "concern"))
    return {
        "reportable": reportable,
        "is_complaint": is_complaint,
        "matched": [k for k in REPORTABLE_KEYWORDS if k in low],
    }


def handle_message(db: DB, text: str, *, participant_id: str = "",
                   received_at: datetime | None = None, actor: str = "intake") -> dict:
    """Route an intake message to the right record/obligation."""
    received_at = received_at or datetime.utcnow().replace(microsecond=0)
    cls = classify(text)

    if cls["reportable"]:
        opened = SubmissionService(db).record_reportable_incident(
            received_at, participant_id, actor=actor)
        return {"type": "reportable_incident", "opened_obligations": opened, **cls}

    reg = RegisterService(db)
    if cls["is_complaint"]:
        rid = reg.add_entry("complaints",
                            {"participant": participant_id, "text": text,
                             "received_at": received_at.isoformat(), "status": "open"},
                            actor=actor)
        return {"type": "complaint", "record_id": rid, **cls}

    rid = reg.add_entry("incident",
                        {"participant": participant_id, "text": text, "reportable": False,
                         "received_at": received_at.isoformat()},
                        actor=actor)
    return {"type": "incident", "record_id": rid, **cls}
