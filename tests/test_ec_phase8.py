"""Tests for Phase 8 — fleet, connectors, intake, reminders, dashboard."""

from __future__ import annotations

from datetime import datetime

from everlasting_compliance import connectors, intake, reminders
from everlasting_compliance.db import DB
from everlasting_compliance.fleet import load_fleet
from everlasting_compliance.submissions import SubmissionService
from everlasting_compliance.web.dashboard import render_dashboard


def test_fleet_loads_all_five_roles():
    roles = load_fleet()
    assert set(roles) == {"ec-orchestrator", "ec-scout", "ec-scribe", "ec-reach", "ec-dev"}
    for r in roles.values():
        assert r.description
        assert "Everlasting Care" in r.system_prompt


def test_connectors_queue_to_outbox_without_credentials(tmp_path, monkeypatch):
    for v in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_ALLOWED_CHAT_IDS"):
        monkeypatch.delenv(v, raising=False)
    db = DB(path=tmp_path / "c.db")
    res = connectors.telegram_send(db, "test reminder")
    assert res["status"] == "queued"
    assert connectors.pending_count(db) == 1


def test_intake_reportable_keyword_opens_incident_obligations(tmp_path):
    db = DB(path=tmp_path / "c.db")
    out = intake.handle_message(db, "Participant had a serious injury and went to hospital",
                                participant_id="P-1",
                                received_at=datetime(2026, 3, 2, 9, 0))
    assert out["type"] == "reportable_incident"
    assert "24h" in out["opened_obligations"]
    rule_keys = {o["rule_key"] for o in db.open_obligations()}
    assert "incident_24h_notification" in rule_keys


def test_intake_complaint_routes_to_complaints_register(tmp_path):
    db = DB(path=tmp_path / "c.db")
    out = intake.handle_message(db, "I have a complaint about a late visit", participant_id="P-2")
    assert out["type"] == "complaint"
    assert any(r["data"].get("register_key") == "complaints" for r in db.list_records("register_entry"))


def test_reminders_sweep_dispatches_for_overdue(tmp_path, monkeypatch):
    for v in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_ALLOWED_CHAT_IDS"):
        monkeypatch.delenv(v, raising=False)
    db = DB(path=tmp_path / "c.db")
    SubmissionService(db).record_reportable_incident(datetime(2026, 3, 2, 9, 0), "P-1")
    result = reminders.sweep(db, now=datetime(2026, 3, 20, 10, 0))
    assert result["audit_ready"] is False
    assert result["reminders_dispatched"]["overdue"] >= 2
    assert result["outbox_pending"] >= 2  # queued, since no telegram creds


def test_web_app_serves_dashboard_with_auth(tmp_path, monkeypatch):
    import pytest
    pytest.importorskip("fastapi")  # skipped when web extra isn't installed
    from fastapi.testclient import TestClient
    monkeypatch.setenv("EC_STATE_DIR", str(tmp_path))
    monkeypatch.setenv("EC_ADMIN_PASSWORD", "testpass")
    from everlasting_compliance.web.app import create_app

    db = DB(path=tmp_path / "compliance.db")
    SubmissionService(db).record_reportable_incident(datetime(2026, 3, 2, 9, 0), "P-1")
    db.close()

    client = TestClient(create_app())
    assert client.get("/healthz").json()["ok"] is True
    assert client.get("/").status_code == 401           # auth required
    ok = client.get("/", auth=("admin", "testpass"))
    assert ok.status_code == 200 and "Mission Control" in ok.text
    api = client.get("/api/status", auth=("admin", "testpass")).json()
    assert "readiness" in api and api["readiness"]["audit_ready"] is False


def test_dashboard_renders_html():
    readiness = {"audit_ready": False, "overdue_count": 2, "due_soon_count": 1,
                 "upcoming_count": 3, "generated_at": "2026-06-01T00:00:00",
                 "overdue": [{"name": "Incident 24h", "regulator": "NDIS Commission",
                              "subject": "incident:P-1", "due_at": "2026-05-30"}],
                 "due_soon": [], "upcoming": []}
    reg = {"registers": 15, "all_populated": False, "empty_registers": ["risk"]}
    pol = {"required_count": 43, "registered_count": 10, "missing_count": 33, "overdue_review": []}
    html = render_dashboard(readiness, reg, pol)
    assert "<!doctype html>" in html
    assert "NOT audit-ready" in html
    assert "Incident 24h" in html
    assert "10/43" in html
