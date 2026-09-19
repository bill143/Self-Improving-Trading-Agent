"""Tests for the compliance registers (Phase 2)."""

from __future__ import annotations

from datetime import date

from everlasting_compliance.db import DB
from everlasting_compliance.registers import REGISTERS, RegisterService, register


def test_all_fifteen_registers_defined():
    assert len(REGISTERS) >= 15
    keys = [r.key for r in REGISTERS]
    assert len(keys) == len(set(keys))
    for essential in ("incident", "reportable_incident", "complaints", "risk",
                      "training", "worker_screening", "restrictive_practice",
                      "policy", "consent", "key_personnel"):
        assert essential in keys


def test_add_entry_is_versioned_and_audited(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = RegisterService(db)
    r1 = db.get_record(svc.add_entry("risk", {"risk": "manual handling", "control": "training"},
                                     ref="R-1", actor="mgr"))
    r2 = db.get_record(svc.add_entry("risk", {"risk": "manual handling", "control": "hoist added"},
                                     ref="R-1", actor="mgr"))
    assert r1["data"]["version"] == 1
    assert r2["data"]["version"] == 2
    assert any(e["action"] == "register:risk:entry" for e in db.audit_trail())


def test_expiry_register_opens_renewal_obligation(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = RegisterService(db)
    # logging a worker screening with an expiry auto-opens the 5-year renewal obligation
    svc.add_entry("worker_screening",
                  {"worker": "W-1", "expires_on": date(2030, 6, 1).isoformat()},
                  ref="W-1", subject_id="W-1", actor="mgr")
    obligations = db.open_obligations()
    assert any(o["rule_key"] == "worker_screening_renewal" for o in obligations)


def test_register_health_flags_empty_registers(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = RegisterService(db)
    health = svc.health()
    assert health["all_populated"] is False
    assert "incident" in health["empty_registers"]

    svc.add_entry("incident", {"summary": "fall in bathroom", "reportable": False}, actor="mgr")
    health = svc.health()
    assert health["entry_counts"]["incident"] == 1
    assert "incident" not in health["empty_registers"]


def test_incident_register_uses_seven_year_retention(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = RegisterService(db)
    rid = svc.add_entry("incident", {"summary": "x"}, actor="mgr")
    rec = db.get_record(rid)
    assert rec["retention_class"] == "incident"
