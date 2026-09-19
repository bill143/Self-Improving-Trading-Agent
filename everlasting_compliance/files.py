"""Participant files and worker files — the per-person records at the heart of NDIS
compliance, with their required-document checklists and cadence-driven obligations.

Onboarding a participant schedules their recurring reviews (support plan, risk
assessment, consent). Onboarding a worker schedules their credential expiries
(screening, First Aid, CPR) and files them into the relevant registers. Every record
carries a 7-year retention class and is audit-logged.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .db import DB
from . import service
from .registers import RegisterService


@dataclass(frozen=True)
class RequiredDoc:
    key: str
    name: str
    cadence: str  # onboarding | per_shift | annual | per_event | ongoing | as_applicable


# Spec §3 — participant file.
PARTICIPANT_DOCS: list[RequiredDoc] = [
    RequiredDoc("intake", "Referral/intake form + eligibility", "onboarding"),
    RequiredDoc("consent", "Consent forms (service, info-sharing, photo, plan access)", "annual"),
    RequiredDoc("service_agreement", "Signed service agreement", "onboarding"),
    RequiredDoc("plan_copy", "NDIS plan copy + budget breakdown", "per_plan_period"),
    RequiredDoc("service_booking", "Service booking confirmation (NDIA-managed)", "onboarding"),
    RequiredDoc("needs_risk_assessment", "Needs + risk assessment", "annual"),
    RequiredDoc("support_plan", "Individual support plan with goals", "annual"),
    RequiredDoc("progress_notes", "Progress/shift notes", "per_shift"),
    RequiredDoc("medication_records", "Medication chart + administration records", "as_applicable"),
    RequiredDoc("restrictive_practice", "Restrictive-practice register entries", "as_applicable"),
    RequiredDoc("money_property_log", "Participant money/property handling log", "as_applicable"),
    RequiredDoc("incidents", "Incident reports involving the participant", "per_event"),
    RequiredDoc("complaints", "Complaints/feedback from the participant", "per_event"),
    RequiredDoc("exit_plan", "Transition/exit plan + handover", "on_exit"),
]

# Spec §4 — worker file.
WORKER_DOCS: list[RequiredDoc] = [
    RequiredDoc("identity", "Proof of identity + right to work", "onboarding"),
    RequiredDoc("worker_screening", "NDIS Worker Screening Check (5yr, portable)", "ongoing"),
    RequiredDoc("wwcc", "Working With Children Check (if child-related)", "as_applicable"),
    RequiredDoc("orientation_module", "NDIS Worker Orientation Module certificate", "onboarding"),
    RequiredDoc("first_aid", "First Aid (HLTAID011, 3yr)", "ongoing"),
    RequiredDoc("cpr", "CPR (HLTAID009, annual)", "ongoing"),
    RequiredDoc("qualifications", "Qualifications (Cert III Individual Support etc.)", "onboarding"),
    RequiredDoc("code_of_conduct", "Signed Code of Conduct acknowledgment", "onboarding"),
    RequiredDoc("induction", "Induction checklist", "onboarding"),
    RequiredDoc("infection_control", "Infection control + PPE training", "ongoing"),
    RequiredDoc("role_competencies", "Manual handling / medication / behaviour / high-intensity", "as_applicable"),
    RequiredDoc("supervision", "Supervision records, performance reviews, CPD log", "ongoing"),
    RequiredDoc("secondary_employment", "Secondary employment declaration", "onboarding"),
]


def _checklist(required: list[RequiredDoc], held: dict) -> dict:
    present = [d.key for d in required if held.get(d.key)]
    missing = [d.key for d in required if not held.get(d.key)]
    return {
        "required": len(required),
        "present": present,
        "missing": missing,
        "complete": not missing,
    }


class ParticipantFiles:
    def __init__(self, db: DB):
        self.db = db

    def onboard(self, participant_id: str, data: dict, *, plan_start: date,
                actor: str = "system") -> int:
        """Create a participant record and schedule their recurring reviews."""
        rid = self.db.add_record("participant", {"participant_id": participant_id, **data},
                                 ref=participant_id, retention_class="participant_record",
                                 actor=actor)
        # Recurring compliance reviews anchored at plan start.
        service.schedule_recurring_next(self.db, "participant_plan_review", plan_start,
                                        subject_type="participant", subject_id=participant_id,
                                        on_or_after=date.today(), actor=actor)
        service.schedule_recurring_next(self.db, "participant_risk_review", plan_start,
                                        subject_type="participant", subject_id=participant_id,
                                        on_or_after=date.today(), actor=actor)
        service.schedule_recurring_next(self.db, "participant_consent_refresh", plan_start,
                                        subject_type="participant", subject_id=participant_id,
                                        on_or_after=date.today(), actor=actor)
        self.db.audit(actor, "participant:onboarded", participant_id)
        return rid

    def checklist(self, held: dict) -> dict:
        return _checklist(PARTICIPANT_DOCS, held)


class WorkerFiles:
    def __init__(self, db: DB):
        self.db = db
        self.registers = RegisterService(db)

    def onboard(self, worker_id: str, data: dict, *,
                screening_expiry: date | None = None,
                first_aid_expiry: date | None = None,
                cpr_expiry: date | None = None,
                actor: str = "system") -> int:
        """Create a worker record, file credentials into registers, and schedule
        every credential's renewal obligation."""
        rid = self.db.add_record("worker", {"worker_id": worker_id, **data},
                                 ref=worker_id, retention_class="worker_record", actor=actor)
        if screening_expiry:
            # register entry auto-opens the screening renewal obligation
            self.registers.add_entry("worker_screening",
                                     {"worker": worker_id, "expires_on": screening_expiry.isoformat()},
                                     ref=worker_id, subject_id=worker_id, actor=actor)
        if first_aid_expiry:
            service.schedule_expiry(self.db, "first_aid_renewal", first_aid_expiry,
                                    subject_type="worker", subject_id=worker_id, actor=actor)
        if cpr_expiry:
            service.schedule_expiry(self.db, "cpr_renewal", cpr_expiry,
                                    subject_type="worker", subject_id=worker_id, actor=actor)
        self.db.audit(actor, "worker:onboarded", worker_id)
        return rid

    def checklist(self, held: dict) -> dict:
        return _checklist(WORKER_DOCS, held)
