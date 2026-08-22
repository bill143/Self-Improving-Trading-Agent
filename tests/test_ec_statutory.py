"""Tests for adjacent statutory records (Phase 9)."""

from __future__ import annotations

from datetime import date

from everlasting_compliance.db import DB
from everlasting_compliance.statutory import STATUTORY_TYPES, StatutoryService


def test_statutory_catalog_covers_key_records():
    keys = {t.key for t in STATUTORY_TYPES}
    assert {"public_liability", "professional_indemnity", "workers_compensation",
            "schads_timesheets", "oaic_breach", "rp_authorisation"} <= keys


def test_insurance_with_expiry_schedules_renewal(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = StatutoryService(db)
    svc.record("public_liability", {"insurer": "Acme", "policy_no": "PL-1"},
               expires_on=date(2027, 1, 1), actor="mgr")
    assert any(o["rule_key"] == "insurance_renewal" for o in db.open_obligations())


def test_schads_timesheets_use_seven_year_retention(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = StatutoryService(db)
    svc.record("schads_timesheets", {"period": "2026-W10"}, actor="mgr")
    rec = db.list_records("statutory")[0]
    assert rec["retention_class"] == "schads_timesheet"


def test_status_flags_missing(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = StatutoryService(db)
    assert svc.status()["complete"] is False
    svc.record("abn_asic", {"abn": "51824753556"}, actor="mgr")
    assert "abn_asic" in svc.status()["held"]
