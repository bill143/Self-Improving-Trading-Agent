"""Tests for NDIA claiming + Commission submissions (Phase 6-7)."""

from __future__ import annotations

from datetime import date, datetime

from everlasting_compliance import claiming
from everlasting_compliance.claiming import ClaimLine, ClaimingService, build_bulk_csv, validate_abn
from everlasting_compliance.db import DB
from everlasting_compliance.submissions import SUBMISSION_TYPES, SubmissionService


# --- claiming ---

def test_abn_checksum():
    assert validate_abn("51 824 753 556")  # ATO's documented valid test ABN
    assert not validate_abn("51 824 753 557")
    assert not validate_abn("123")


def test_claim_line_90_day_window_enforced():
    today = date(2026, 6, 1)
    ok = ClaimLine("431234567", "01_011_0107_1_1", date(2026, 5, 1), 2, 65.47)
    late = ClaimLine("431234567", "01_011_0107_1_1", date(2026, 1, 1), 2, 65.47)
    assert claiming.validate_line(ok, today=today) == []
    assert any("90-day" in e for e in claiming.validate_line(late, today=today))


def test_plan_managed_requires_valid_abn():
    today = date(2026, 6, 1)
    line = ClaimLine("431234567", "01_011_0107_1_1", date(2026, 5, 1), 2, 65.47, abn="bad")
    errs = claiming.validate_line(line, today=today, plan_managed=True)
    assert any("ABN" in e for e in errs)


def test_bulk_csv_filename_and_row_rules():
    lines = [ClaimLine("431234567", "01_011_0107_1_1", date(2026, 5, 1), 1, 10.0)]
    csv_text, problems = build_bulk_csv(lines, "claim.CSV")
    assert problems == []
    assert "NDISNumber" in csv_text and "431234567" in csv_text
    # too-long filename is rejected
    _, problems2 = build_bulk_csv(lines, "a-very-long-filename.CSV")
    assert any("under 20" in p for p in problems2)


def test_booking_opens_90_day_payment_obligation(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = ClaimingService(db)
    svc.create_booking("431234567", "01_011_0107_1_1",
                       date(2026, 1, 1), date(2026, 3, 31), 5000.0, actor="mgr")
    assert any(o["rule_key"] == "ndia_payment_request" for o in db.open_obligations())


def test_rejected_claim_is_stored_not_dropped(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = ClaimingService(db)
    res = svc.record_claim(
        ClaimLine("431234567", "", date(2026, 5, 1), 1, 10.0),  # missing support item
        today=date(2026, 6, 1), actor="mgr")
    assert res["valid"] is False
    assert db.list_records("claim_line")[0]["data"]["valid"] is False


# --- submissions ---

def test_submission_catalog_covers_key_types():
    keys = {s.key for s in SUBMISSION_TYPES}
    assert {"reportable_incident_24h", "reportable_incident_5day", "urp_5day",
            "renewal", "mid_term_audit", "change_notification"} <= keys


def test_reportable_incident_opens_obligations_and_tracker(tmp_path):
    db = DB(path=tmp_path / "c.db")
    subs = SubmissionService(db)
    opened = subs.record_reportable_incident(datetime(2026, 3, 2, 9, 0), "P-1",
                                             final_report_required=True, actor="mgr")
    assert set(opened) == {"24h", "5day", "final"}
    rule_keys = {o["rule_key"] for o in db.open_obligations()}
    assert {"incident_24h_notification", "incident_5day_report", "incident_final_60day"} <= rule_keys
    # tracker entry filed in the reportable-incident register
    assert any(r["data"].get("register_key") == "reportable_incident"
               for r in db.list_records("register_entry"))


def test_marking_submission_closes_the_obligation(tmp_path):
    db = DB(path=tmp_path / "c.db")
    subs = SubmissionService(db)
    opened = subs.record_reportable_incident(datetime(2026, 3, 2, 9, 0), "P-1", actor="mgr")
    subs.mark_obligation_submitted(opened["24h"], reference="NDIS-REF-123", actor="mgr")
    assert all(o["id"] != opened["24h"] for o in db.open_obligations())
    assert any(e["detail"] == "NDIS-REF-123" for e in db.audit_trail())
