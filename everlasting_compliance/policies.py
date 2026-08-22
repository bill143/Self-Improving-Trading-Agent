"""Phase 5 — the Core Module policy suite.

Auditors expect ~40-50 core policies across five domains, each with a version number,
owner, approval date, and review date, on an annual review cycle. This module encodes
the required-policy catalog, registers policies (version-controlled), schedules each
policy's annual review as an obligation, and reports which are missing or overdue.

The Scribe agent (`ec-scribe`) drafts the policy *content*; this module owns the
structure, version control, and review lifecycle.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from . import config, obligations as ob
from .db import DB


@dataclass(frozen=True)
class PolicySpec:
    key: str
    name: str
    domain: str
    owner_role: str = "Quality Manager"
    review_interval_months: int = 12
    requires_module_2a: bool = False
    requires_under_18: bool = False


# Minimum policy set from the compliance inventory (spec §2).
POLICY_CATALOG: list[PolicySpec] = [
    # Governance
    PolicySpec("governance_framework", "Governance framework", "Governance", "Board/Director"),
    PolicySpec("org_chart", "Organisational chart", "Governance", "Director"),
    PolicySpec("delegations_of_authority", "Delegations of authority", "Governance", "Director"),
    PolicySpec("key_personnel_register_policy", "Key personnel register policy", "Governance", "Director"),
    PolicySpec("conflict_of_interest", "Conflict of interest", "Governance"),
    PolicySpec("financial_management", "Financial management", "Governance", "Finance Manager"),
    PolicySpec("continuity_of_supports", "Continuity of supports / business continuity", "Governance"),
    PolicySpec("emergency_disaster_management", "Emergency and disaster management", "Governance"),
    PolicySpec("information_management", "Information management and record keeping", "Governance"),
    PolicySpec("quality_management", "Quality management and continuous improvement", "Governance"),
    PolicySpec("internal_audit_schedule", "Internal audit schedule", "Governance"),
    # Rights
    PolicySpec("participant_rights_dignity", "Participant rights and dignity", "Rights"),
    PolicySpec("supported_decision_making", "Supported decision-making", "Rights"),
    PolicySpec("independence_informed_choice", "Independence and informed choice", "Rights"),
    PolicySpec("privacy_confidentiality", "Privacy and confidentiality (Privacy Act + NDIS)", "Rights"),
    PolicySpec("freedom_from_abuse", "Freedom from violence, abuse, neglect, exploitation", "Rights"),
    PolicySpec("safeguarding", "Safeguarding", "Rights"),
    PolicySpec("advocacy_access", "Advocacy access", "Rights"),
    PolicySpec("participant_handbook", "Easy-read participant handbook", "Rights"),
    # Service Delivery
    PolicySpec("intake_access", "Intake and access to supports", "Service Delivery"),
    PolicySpec("support_planning", "Support planning", "Service Delivery"),
    PolicySpec("service_agreements", "Service agreements", "Service Delivery"),
    PolicySpec("responsive_support", "Responsive support provision", "Service Delivery"),
    PolicySpec("transitions", "Transitions to/from the provider", "Service Delivery"),
    PolicySpec("participant_money_property", "Participant money and property", "Service Delivery"),
    PolicySpec("medication_management", "Medication management", "Service Delivery", "Clinical Lead"),
    PolicySpec("safe_environment", "Safe environment", "Service Delivery"),
    PolicySpec("mealtime_management", "Mealtime management", "Service Delivery", "Clinical Lead"),
    # Workforce
    PolicySpec("recruitment_selection", "Recruitment and selection", "Workforce", "HR Manager"),
    PolicySpec("worker_screening_policy", "Worker screening", "Workforce", "HR Manager"),
    PolicySpec("induction_orientation", "Induction and orientation", "Workforce", "HR Manager"),
    PolicySpec("training_competency", "Training and competency", "Workforce", "HR Manager"),
    PolicySpec("supervision_performance", "Supervision and performance management", "Workforce", "HR Manager"),
    PolicySpec("code_of_conduct", "Code of Conduct", "Workforce"),
    PolicySpec("secondary_employment", "Secondary employment", "Workforce", "HR Manager"),
    PolicySpec("whs_infection_control", "WHS / infection control / PPE", "Workforce", "WHS Officer"),
    # Risk and Safeguarding
    PolicySpec("risk_management_framework", "Risk management framework", "Risk and Safeguarding"),
    PolicySpec("incident_management", "Incident management system", "Risk and Safeguarding"),
    PolicySpec("reportable_incident_procedure", "Reportable incident procedure", "Risk and Safeguarding"),
    PolicySpec("complaints_feedback", "Complaints and feedback management", "Risk and Safeguarding"),
    PolicySpec("whistleblower", "Whistleblower", "Risk and Safeguarding"),
    PolicySpec("child_safety", "Child safety", "Risk and Safeguarding", requires_under_18=True),
    PolicySpec("restrictive_practice", "Restrictive practice (Module 2A)", "Risk and Safeguarding",
               "Behaviour Support Lead", requires_module_2a=True),
]

POLICY_BY_KEY: dict[str, PolicySpec] = {p.key: p for p in POLICY_CATALOG}


def required_policies(scope: config.Scope | None = None) -> list[PolicySpec]:
    """The policies this provider must hold, filtered by scope toggles."""
    scope = scope or config.PROFILE.scope
    out = []
    for p in POLICY_CATALOG:
        if p.requires_module_2a and not scope.module_2a_restrictive_practices:
            continue
        if p.requires_under_18 and not scope.under_18_child_safety:
            continue
        out.append(p)
    return out


class PolicyService:
    def __init__(self, db: DB):
        self.db = db

    def register_policy(self, key: str, *, owner: str = "", version: int = 1,
                        approval_date: date | None = None, actor: str = "system") -> int:
        """Register/version a policy and schedule its annual review."""
        spec = POLICY_BY_KEY.get(key)
        if not spec:
            raise KeyError(f"unknown policy '{key}'")
        approved = approval_date or date.today()
        review_due = ob.add_months(approved, spec.review_interval_months)
        payload = {
            "key": key, "name": spec.name, "domain": spec.domain,
            "owner": owner or spec.owner_role, "version": version,
            "approval_date": approved.isoformat(), "review_date": review_due.isoformat(),
        }
        rid = self.db.add_record("policy", payload, ref=key, retention_class="default", actor=actor)
        # schedule the review as an obligation so it appears on the deadline calendar
        self.db.add_obligation("policy_annual_review", "policy",
                               ob._as_datetime(review_due).isoformat(),
                               subject_id=key, notes=f"Review: {spec.name}", actor=actor)
        self.db.audit(actor, "policy:registered", key, f"v{version}")
        return rid

    def current_policies(self) -> dict[str, dict]:
        """Latest registered version per policy key."""
        latest: dict[str, dict] = {}
        for rec in self.db.list_records("policy"):
            d = rec["data"]
            k = d["key"]
            if k not in latest or d["version"] >= latest[k]["version"]:
                latest[k] = d
        return latest

    def status(self, scope: config.Scope | None = None, today: date | None = None) -> dict:
        today = today or date.today()
        required = required_policies(scope)
        current = self.current_policies()
        missing = [p.key for p in required if p.key not in current]
        overdue_review = [
            k for k, d in current.items()
            if date.fromisoformat(d["review_date"]) < today
        ]
        by_domain: dict[str, int] = {}
        for p in required:
            by_domain[p.domain] = by_domain.get(p.domain, 0) + 1
        return {
            "required_count": len(required),
            "registered_count": len(current),
            "missing_count": len(missing),
            "missing": missing,
            "overdue_review": overdue_review,
            "complete": not missing,
            "by_domain": by_domain,
        }
