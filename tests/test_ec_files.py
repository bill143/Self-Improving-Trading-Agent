"""Tests for participant and worker files (Phase 3-4)."""

from __future__ import annotations

from datetime import date

from everlasting_compliance.db import DB
from everlasting_compliance.files import (
    PARTICIPANT_DOCS,
    WORKER_DOCS,
    ParticipantFiles,
    WorkerFiles,
)


def test_document_catalogs_present():
    assert {d.key for d in PARTICIPANT_DOCS} >= {
        "intake", "consent", "service_agreement", "support_plan", "progress_notes"}
    assert {d.key for d in WORKER_DOCS} >= {
        "identity", "worker_screening", "first_aid", "cpr", "code_of_conduct"}


def test_participant_onboarding_schedules_recurring_reviews(tmp_path):
    db = DB(path=tmp_path / "c.db")
    pf = ParticipantFiles(db)
    pf.onboard("P-1", {"name": "REDACTED"}, plan_start=date(2026, 1, 1), actor="mgr")
    rule_keys = {o["rule_key"] for o in db.open_obligations()}
    assert {"participant_plan_review", "participant_risk_review",
            "participant_consent_refresh"} <= rule_keys
    assert any(e["action"] == "participant:onboarded" for e in db.audit_trail())


def test_worker_onboarding_schedules_credential_renewals(tmp_path):
    db = DB(path=tmp_path / "c.db")
    wf = WorkerFiles(db)
    wf.onboard("W-1", {"name": "REDACTED"},
               screening_expiry=date(2031, 1, 1),
               first_aid_expiry=date(2029, 1, 1),
               cpr_expiry=date(2027, 1, 1),
               actor="mgr")
    rule_keys = {o["rule_key"] for o in db.open_obligations()}
    assert {"worker_screening_renewal", "first_aid_renewal", "cpr_renewal"} <= rule_keys
    # screening also filed into the worker_screening register
    assert any(r["data"].get("register_key") == "worker_screening"
               for r in db.list_records("register_entry"))


def test_checklists_flag_missing_documents(tmp_path):
    db = DB(path=tmp_path / "c.db")
    wf = WorkerFiles(db)
    incomplete = wf.checklist({"identity": True, "worker_screening": True})
    assert incomplete["complete"] is False
    assert "code_of_conduct" in incomplete["missing"]

    pf = ParticipantFiles(db)
    complete = pf.checklist({d.key: True for d in PARTICIPANT_DOCS})
    assert complete["complete"] is True


def test_worker_and_participant_records_use_seven_year_retention(tmp_path):
    db = DB(path=tmp_path / "c.db")
    WorkerFiles(db).onboard("W-1", {"name": "x"}, actor="mgr")
    ParticipantFiles(db).onboard("P-1", {"name": "x"}, plan_start=date(2026, 1, 1), actor="mgr")
    assert db.list_records("worker")[0]["retention_class"] == "worker_record"
    assert db.list_records("participant")[0]["retention_class"] == "participant_record"
