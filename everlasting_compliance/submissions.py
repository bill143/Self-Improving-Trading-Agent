"""Phase 7 — submissions to the NDIS Commission.

The workflow that turns events (an incident, a restrictive practice, a change of key
personnel, a renewal) into tracked Commission submissions, each tied to its deadline
in the obligations engine and audit-logged with the portal reference once lodged.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from . import service
from .db import DB


@dataclass(frozen=True)
class SubmissionType:
    key: str
    name: str
    deadline_rule: str | None = None  # obligations rule that governs the deadline
    conditional: bool = False


SUBMISSION_TYPES: list[SubmissionType] = [
    SubmissionType("reportable_incident_24h", "Reportable incident — 24h notification",
                   "incident_24h_notification"),
    SubmissionType("reportable_incident_5day", "Reportable incident — 5-day report",
                   "incident_5day_report"),
    SubmissionType("reportable_incident_final", "Reportable incident — final report",
                   "incident_final_60day", conditional=True),
    SubmissionType("urp_5day", "Unauthorised restrictive practice — 5-day report", "urp_5day"),
    SubmissionType("rp_monthly", "Monthly restrictive-practice reporting",
                   "restrictive_practice_monthly"),
    SubmissionType("change_notification", "Notification of changes/events (key personnel, "
                   "ownership, structure, insolvency, adverse findings)"),
    SubmissionType("worker_screening_link", "Worker screening verification / linking"),
    SubmissionType("mid_term_audit", "Mid-term audit", "mid_term_audit"),
    SubmissionType("renewal", "Renewal application + self-assessment + audit",
                   "registration_renewal"),
    SubmissionType("conditional_audit", "Conditional audit", conditional=True),
    SubmissionType("compliance_notice_response", "Response to a compliance notice / info request"),
]

SUBMISSION_BY_KEY: dict[str, SubmissionType] = {s.key: s for s in SUBMISSION_TYPES}


class SubmissionService:
    def __init__(self, db: DB):
        self.db = db

    def record_reportable_incident(self, event_at: datetime, participant_id: str = "",
                                   *, final_report_required: bool = False,
                                   actor: str = "system") -> dict[str, int]:
        """Log a reportable incident and open its 24h + 5-day (and optional 60-day)
        obligations, plus a tracker entry in the reportable-incident register."""
        from .registers import RegisterService  # local import avoids a cycle
        RegisterService(self.db).add_entry(
            "reportable_incident",
            {"participant": participant_id, "occurred_at": event_at.isoformat(),
             "status": "notification_pending"},
            ref=f"INC:{participant_id}:{event_at.isoformat()}", actor=actor)
        opened = {
            "24h": service.schedule_event(self.db, "incident_24h_notification", event_at,
                                          subject_type="incident", subject_id=participant_id, actor=actor),
            "5day": service.schedule_event(self.db, "incident_5day_report", event_at,
                                           subject_type="incident", subject_id=participant_id, actor=actor),
        }
        if final_report_required:
            opened["final"] = service.schedule_event(
                self.db, "incident_final_60day", event_at,
                subject_type="incident", subject_id=participant_id, actor=actor)
        self.db.audit(actor, "submission:reportable_incident_opened", participant_id)
        return opened

    def log_submission(self, type_key: str, *, subject_id: str = "", reference: str = "",
                       status: str = "lodged", actor: str = "system") -> int:
        """Record that a submission was lodged with the Commission (with its portal
        reference), for the audit trail and portal reconciliation."""
        st = SUBMISSION_BY_KEY.get(type_key)
        if not st:
            raise KeyError(f"unknown submission type '{type_key}'")
        rid = self.db.add_record("submission", {
            "type": type_key, "name": st.name, "subject_id": subject_id,
            "reference": reference, "status": status,
            "lodged_at": datetime.utcnow().replace(microsecond=0).isoformat(),
        }, ref=reference, retention_class="incident", actor=actor)
        self.db.audit(actor, f"submission:{type_key}", reference or subject_id, status)
        return rid

    def mark_obligation_submitted(self, obligation_id: int, reference: str = "",
                                  actor: str = "system") -> None:
        """Close the loop: mark the deadline obligation submitted once lodged."""
        self.db.set_obligation_status(obligation_id, "submitted", actor=actor)
        if reference:
            self.db.audit(actor, "submission:reference", str(obligation_id), reference)

    def outstanding(self) -> list[dict]:
        """Open submission-type obligations still to be lodged."""
        rules = {s.deadline_rule for s in SUBMISSION_TYPES if s.deadline_rule}
        return [o for o in self.db.open_obligations() if o["rule_key"] in rules]
