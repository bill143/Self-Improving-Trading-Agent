"""Tests for the Everlasting Care compliance deadline engine and persistence.

The deadline engine is the spine of the platform — a missed deadline deregisters a
provider — so these tests pin the exact NDIS rules from the supplied inventory.
"""

from __future__ import annotations

from datetime import date, datetime

import pytest

from everlasting_compliance import obligations as ob
from everlasting_compliance import service
from everlasting_compliance.db import DB


# --- date math ---

def test_add_business_days_skips_weekend():
    # Friday + 5 business days = next Friday
    assert ob.add_business_days(date(2026, 1, 2), 5) == date(2026, 1, 9)  # 2 Jan 2026 is a Fri
    # Thursday + 1 business day = Friday
    assert ob.add_business_days(date(2026, 1, 1), 1) == date(2026, 1, 2)
    # Friday + 1 business day = Monday
    assert ob.add_business_days(date(2026, 1, 2), 1) == date(2026, 1, 5)


def test_add_months_clamps_end_of_month():
    assert ob.add_months(date(2026, 1, 31), 1) == date(2026, 2, 28)  # no 31 Feb
    assert ob.add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)  # leap year
    assert ob.add_months(date(2026, 10, 24), 36) == date(2029, 10, 24)


# --- the real NDIS deadlines ---

def test_incident_24h_notification():
    rule = ob.rule("incident_24h_notification")
    awareness = datetime(2026, 3, 1, 17, 0)  # became aware Sun 5pm
    assert ob.event_due(rule, awareness) == datetime(2026, 3, 2, 17, 0)  # +24h


def test_incident_5_business_day_report():
    rule = ob.rule("incident_5day_report")
    # incident on a Monday → 5 business days = the following Monday
    due = ob.event_due(rule, date(2026, 3, 2))  # 2 Mar 2026 is a Monday
    assert due.date() == date(2026, 3, 9)


def test_ndia_payment_90_day_window():
    rule = ob.rule("ndia_payment_request")
    booking_end = date(2026, 1, 1)
    assert ob.event_due(rule, booking_end).date() == date(2026, 4, 1)  # +90 calendar days


def test_worker_screening_renewal_window_opens_90_days_before_expiry():
    rule = ob.rule("worker_screening_renewal")
    expires = date(2030, 6, 1)
    assert ob.expiry_renewal_opens(rule, expires) == date(2030, 3, 3)  # 90 days prior


def test_registration_renewal_uses_six_month_window():
    rule = ob.rule("registration_renewal")
    opens = ob.expiry_renewal_opens(rule, date(2027, 10, 24))
    assert opens < date(2027, 5, 1)  # prep well before the Oct 2027 deadline


def test_next_recurring_due_advances_past_reference():
    rule = ob.rule("policy_annual_review")
    nxt = ob.next_recurring_due(rule, anchor=date(2020, 1, 1), on_or_after=date(2026, 6, 1))
    assert nxt == date(2027, 1, 1)


# --- status transitions ---

def test_status_progression():
    due = datetime(2026, 6, 15, 12, 0)
    lead = 14
    assert ob.status_for(due, datetime(2026, 5, 1), lead) is ob.Status.UPCOMING
    assert ob.status_for(due, datetime(2026, 6, 10), lead) is ob.Status.DUE_SOON
    assert ob.status_for(due, datetime(2026, 6, 16), lead) is ob.Status.OVERDUE
    assert ob.status_for(due, datetime(2026, 6, 16), lead, submitted=True) is ob.Status.SUBMITTED
    assert ob.status_for(due, datetime(2026, 6, 16), lead, closed=True) is ob.Status.CLOSED


def test_catalog_is_complete_and_unique():
    keys = [r.key for r in ob.CATALOG]
    assert len(keys) == len(set(keys)), "duplicate rule keys"
    # the deadlines that get providers deregistered must all exist
    for key in ("incident_24h_notification", "incident_5day_report", "urp_5day",
                "ndia_payment_request", "worker_screening_renewal", "registration_renewal"):
        assert key in ob.CATALOG_BY_KEY


# --- persistence, audit log, retention ---

def test_db_records_audit_log_and_retention(tmp_path):
    db = DB(path=tmp_path / "c.db")
    rid = db.add_record("participant", {"name": "REDACTED"}, ref="P-1",
                        retention_class="participant_record", actor="tester")
    rec = db.get_record(rid)
    assert rec["data"]["name"] == "REDACTED"
    assert rec["retain_until"] is not None  # 7 years out — not purgeable now
    # audit log captured who did what
    trail = db.audit_trail()
    assert any(e["action"] == "create:participant" and e["actor"] == "tester" for e in trail)
    # retention: nothing purged while within window
    assert db.purge_expired() == 0


def test_schedule_and_audit_readiness(tmp_path):
    db = DB(path=tmp_path / "c.db")
    # an incident just occurred → 24h + 5-day obligations
    event_at = datetime(2026, 3, 2, 9, 0)
    service.schedule_event(db, "incident_24h_notification", event_at,
                           subject_type="incident", subject_id="INC-1")
    service.schedule_event(db, "incident_5day_report", event_at,
                           subject_type="incident", subject_id="INC-1")
    # a worker screening that expires in 5 years
    service.schedule_expiry(db, "worker_screening_renewal", date(2031, 3, 2),
                            subject_type="worker", subject_id="W-1")

    # Right after the incident: nothing overdue yet → audit ready
    snap = service.audit_readiness(db, now=datetime(2026, 3, 2, 10, 0))
    assert snap["audit_ready"] is True

    # A week later, both incident reports are overdue → NOT audit ready
    snap = service.audit_readiness(db, now=datetime(2026, 3, 20, 10, 0))
    assert snap["audit_ready"] is False
    assert snap["overdue_count"] >= 2

    # refresh persists the computed statuses
    counts = service.refresh_statuses(db, now=datetime(2026, 3, 20, 10, 0))
    assert counts["overdue"] >= 2


def test_submitting_obligation_clears_it_from_open(tmp_path):
    db = DB(path=tmp_path / "c.db")
    oid = service.schedule_event(db, "incident_24h_notification", datetime(2026, 3, 2, 9, 0),
                                 subject_type="incident", subject_id="INC-1")
    db.set_obligation_status(oid, "submitted", actor="manager")
    assert all(o["id"] != oid for o in db.open_obligations())
    assert any(e["action"] == "obligation:submitted" for e in db.audit_trail())
