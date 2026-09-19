"""The deadline engine — the spine of the platform.

Encodes the real NDIS obligations and hard deadlines as a rule catalog, plus the
date math to turn a trigger (an incident time, a certificate expiry, an anchor date)
into a concrete due date and a live status. Missed deadlines are what deregister
providers, so this module is pure, deterministic, and heavily tested.

All rules trace to docs/everlasting-compliance-plan.md and the owner's inventory.
`now` is always injectable so behaviour is testable without wall-clock dependence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum


class Regulator(str, Enum):
    NDIS_COMMISSION = "NDIS Quality and Safeguards Commission"
    NDIA = "National Disability Insurance Agency"
    OCG_NSW = "NSW Office of the Children's Guardian"
    STATUTORY = "ATO / Fair Work / SafeWork NSW / OAIC"


class Trigger(str, Enum):
    EVENT = "event"        # due a fixed offset after a one-off event (incident, booking end)
    EXPIRY = "expiry"      # renew before a credential/registration expires
    RECURRING = "recurring"  # repeats on a fixed cadence from an anchor date


class Status(str, Enum):
    UPCOMING = "upcoming"
    DUE_SOON = "due_soon"
    OVERDUE = "overdue"
    SUBMITTED = "submitted"
    CLOSED = "closed"


@dataclass(frozen=True)
class ObligationRule:
    key: str
    name: str
    category: str
    regulator: Regulator
    trigger: Trigger
    # EVENT: offset in hours OR business days (exactly one set)
    offset_hours: int | None = None
    offset_business_days: int | None = None
    offset_calendar_days: int | None = None
    # EXPIRY / RECURRING: interval in months
    interval_months: int | None = None
    # EXPIRY: how far before expiry the renewal opens (also the alert lead)
    renewal_window_days: int | None = None
    # alert lead time (days before due) for DUE_SOON — defaults sensibly per trigger
    lead_time_days: int = 14
    conditional: bool = False
    notes: str = ""


# --------------------------------------------------------------------------
# Date math
# --------------------------------------------------------------------------

def add_business_days(start: date, n: int) -> date:
    """Add n business days (Mon–Fri), skipping weekends. Public holidays are not
    yet modelled — flagged for the NSW holiday calendar in a later phase."""
    d = start
    added = 0
    step = 1 if n >= 0 else -1
    while added < abs(n):
        d += timedelta(days=step)
        if d.weekday() < 5:
            added += 1
    return d


def add_months(anchor: date, months: int) -> date:
    """Add whole months, clamping the day to the target month's last day."""
    m = anchor.month - 1 + months
    year = anchor.year + m // 12
    month = m % 12 + 1
    # clamp day
    for day in (anchor.day, 28, 29, 30, 31):
        try:
            return date(year, month, min(day, _days_in_month(year, month)))
        except ValueError:  # pragma: no cover
            continue
    return date(year, month, 28)  # pragma: no cover


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        nxt = date(year + 1, 1, 1)
    else:
        nxt = date(year, month + 1, 1)
    return (nxt - date(year, month, 1)).days


def _as_datetime(d: date | datetime) -> datetime:
    if isinstance(d, datetime):
        return d
    return datetime(d.year, d.month, d.day)


def event_due(rule: ObligationRule, event_at: date | datetime) -> datetime:
    """Concrete due datetime for an EVENT-triggered obligation."""
    if rule.trigger is not Trigger.EVENT:
        raise ValueError(f"{rule.key} is not an EVENT rule")
    if rule.offset_hours is not None:
        return _as_datetime(event_at) + timedelta(hours=rule.offset_hours)
    if rule.offset_business_days is not None:
        base = event_at.date() if isinstance(event_at, datetime) else event_at
        return _as_datetime(add_business_days(base, rule.offset_business_days))
    if rule.offset_calendar_days is not None:
        return _as_datetime(event_at) + timedelta(days=rule.offset_calendar_days)
    raise ValueError(f"{rule.key} EVENT rule has no offset")


def expiry_renewal_opens(rule: ObligationRule, expires_on: date) -> date:
    """When the renewal window opens for an EXPIRY obligation."""
    window = rule.renewal_window_days or rule.lead_time_days
    return expires_on - timedelta(days=window)


def next_recurring_due(rule: ObligationRule, anchor: date, on_or_after: date) -> date:
    """Next occurrence of a RECURRING obligation on/after a reference date."""
    if rule.trigger is not Trigger.RECURRING or not rule.interval_months:
        raise ValueError(f"{rule.key} is not a RECURRING rule with an interval")
    due = anchor
    guard = 0
    while due < on_or_after and guard < 10_000:
        due = add_months(due, rule.interval_months)
        guard += 1
    return due


def status_for(
    due: date | datetime,
    now: date | datetime,
    lead_time_days: int,
    *,
    submitted: bool = False,
    closed: bool = False,
) -> Status:
    """Live status of a concrete obligation instance."""
    if closed:
        return Status.CLOSED
    if submitted:
        return Status.SUBMITTED
    due_dt = _as_datetime(due)
    now_dt = _as_datetime(now)
    if now_dt > due_dt:
        return Status.OVERDUE
    if now_dt >= due_dt - timedelta(days=lead_time_days):
        return Status.DUE_SOON
    return Status.UPCOMING


# --------------------------------------------------------------------------
# The rule catalog — spec as code
# --------------------------------------------------------------------------
R = Regulator

CATALOG: list[ObligationRule] = [
    # --- Reportable incidents (Commission) ---
    ObligationRule(
        "incident_24h_notification", "Reportable incident — 24h notification",
        "Incidents", R.NDIS_COMMISSION, Trigger.EVENT, offset_hours=24, lead_time_days=1,
        notes="Death, serious injury, abuse/neglect, unlawful sexual/physical contact, "
              "sexual misconduct. Clock starts at awareness, not occurrence.",
    ),
    ObligationRule(
        "incident_5day_report", "Reportable incident — 5-business-day report",
        "Incidents", R.NDIS_COMMISSION, Trigger.EVENT, offset_business_days=5, lead_time_days=2,
        notes="Root cause + corrective actions.",
    ),
    ObligationRule(
        "incident_final_60day", "Reportable incident — final report (if requested)",
        "Incidents", R.NDIS_COMMISSION, Trigger.EVENT, offset_calendar_days=60,
        lead_time_days=10, conditional=True,
        notes="May be required within 60 days of the 5-day report, if the Commission requests it.",
    ),
    ObligationRule(
        "urp_5day", "Unauthorised restrictive practice — 5-business-day report",
        "Restrictive Practices", R.NDIS_COMMISSION, Trigger.EVENT, offset_business_days=5,
        lead_time_days=2, notes="5-day form only where no harm.",
    ),
    # --- Recurring Commission ---
    ObligationRule(
        "restrictive_practice_monthly", "Monthly restrictive-practice reporting",
        "Restrictive Practices", R.NDIS_COMMISSION, Trigger.RECURRING, interval_months=1,
        lead_time_days=5, notes="If implementing behaviour support plans (Module 2A).",
    ),
    ObligationRule(
        "register_reconciliation_quarterly",
        "Quarterly incident-register reconciliation vs Commission portal",
        "Governance", R.NDIS_COMMISSION, Trigger.RECURRING, interval_months=3, lead_time_days=10,
    ),
    # --- Registration lifecycle (Commission) ---
    ObligationRule(
        "registration_renewal", "Registration renewal + self-assessment + audit",
        "Registration", R.NDIS_COMMISSION, Trigger.EXPIRY, interval_months=36,
        renewal_window_days=183, lead_time_days=183,
        notes="Commission notifies ~6 months before expiry. Everlasting Care due before 2027-10-24.",
    ),
    ObligationRule(
        "mid_term_audit", "Mid-term audit (Certification providers)",
        "Registration", R.NDIS_COMMISSION, Trigger.RECURRING, interval_months=18, lead_time_days=30,
        notes="Approx. 18 months into the 3-year cycle.",
    ),
    # --- Worker credentials (OCG / Commission) ---
    ObligationRule(
        "worker_screening_renewal", "NDIS Worker Screening renewal",
        "Workforce", R.OCG_NSW, Trigger.EXPIRY, interval_months=60, renewal_window_days=90,
        lead_time_days=90, notes="Valid 5 years, portable. Renew up to 90 days before expiry.",
    ),
    ObligationRule(
        "first_aid_renewal", "First Aid (HLTAID011) renewal",
        "Workforce", R.STATUTORY, Trigger.EXPIRY, interval_months=36, renewal_window_days=45,
        lead_time_days=45,
    ),
    ObligationRule(
        "cpr_renewal", "CPR (HLTAID009) renewal",
        "Workforce", R.STATUTORY, Trigger.EXPIRY, interval_months=12, renewal_window_days=30,
        lead_time_days=30,
    ),
    # --- NDIA claiming ---
    ObligationRule(
        "ndia_payment_request", "NDIA payment request window",
        "Claiming", R.NDIA, Trigger.EVENT, offset_calendar_days=90, lead_time_days=14,
        notes="Within 90 days from the end of a service booking.",
    ),
    # --- Recurring governance / participant / statutory ---
    ObligationRule(
        "policy_annual_review", "Policy review cycle",
        "Governance", R.NDIS_COMMISSION, Trigger.RECURRING, interval_months=12, lead_time_days=30,
        notes="At least annually or on legislation/standard/procedure change.",
    ),
    ObligationRule(
        "participant_plan_review", "Individual support plan review",
        "Service Delivery", R.NDIS_COMMISSION, Trigger.RECURRING, interval_months=12,
        lead_time_days=30,
    ),
    ObligationRule(
        "participant_risk_review", "Participant needs/risk assessment review",
        "Service Delivery", R.NDIS_COMMISSION, Trigger.RECURRING, interval_months=6,
        lead_time_days=21, notes="6–12 monthly or on change; 6-monthly used to be safe.",
    ),
    ObligationRule(
        "participant_consent_refresh", "Participant consent refresh",
        "Rights", R.NDIS_COMMISSION, Trigger.RECURRING, interval_months=12, lead_time_days=21,
    ),
    ObligationRule(
        "insurance_renewal", "Insurance renewals (PL/PI, workers comp)",
        "Statutory", R.STATUTORY, Trigger.RECURRING, interval_months=12, lead_time_days=30,
    ),
    ObligationRule(
        "whs_audit_annual", "WHS audit",
        "Statutory", R.STATUTORY, Trigger.RECURRING, interval_months=12, lead_time_days=30,
    ),
]

CATALOG_BY_KEY: dict[str, ObligationRule] = {r.key: r for r in CATALOG}


def rule(key: str) -> ObligationRule:
    try:
        return CATALOG_BY_KEY[key]
    except KeyError as exc:
        raise KeyError(f"unknown obligation rule '{key}'") from exc
