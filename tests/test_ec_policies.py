"""Tests for the Core Module policy suite (Phase 5)."""

from __future__ import annotations

from datetime import date

from everlasting_compliance import config
from everlasting_compliance.db import DB
from everlasting_compliance.policies import (
    POLICY_CATALOG,
    PolicyService,
    required_policies,
)


def test_catalog_covers_all_five_domains_and_is_sized_right():
    domains = {p.domain for p in POLICY_CATALOG}
    assert domains == {"Governance", "Rights", "Service Delivery", "Workforce",
                       "Risk and Safeguarding"}
    assert 40 <= len(POLICY_CATALOG) <= 50
    keys = [p.key for p in POLICY_CATALOG]
    assert len(keys) == len(set(keys))


def test_scope_toggles_filter_conditional_policies():
    full = config.Scope(module_2a_restrictive_practices=True, under_18_child_safety=True)
    minimal = config.Scope(module_2a_restrictive_practices=False, under_18_child_safety=False)
    full_keys = {p.key for p in required_policies(full)}
    min_keys = {p.key for p in required_policies(minimal)}
    assert "restrictive_practice" in full_keys and "child_safety" in full_keys
    assert "restrictive_practice" not in min_keys and "child_safety" not in min_keys


def test_registering_policy_schedules_annual_review(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = PolicyService(db)
    svc.register_policy("privacy_confidentiality", owner="Quality Manager",
                        approval_date=date(2026, 1, 1), actor="scribe")
    current = svc.current_policies()
    assert current["privacy_confidentiality"]["review_date"] == "2027-01-01"
    assert any(o["rule_key"] == "policy_annual_review" for o in db.open_obligations())


def test_status_reports_missing_and_overdue(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = PolicyService(db)
    # register one policy with a review date already in the past
    svc.register_policy("code_of_conduct", approval_date=date(2020, 1, 1), actor="scribe")
    st = svc.status(scope=config.Scope(module_2a_restrictive_practices=False,
                                       under_18_child_safety=False),
                    today=date(2026, 6, 1))
    assert st["registered_count"] == 1
    assert st["missing_count"] == st["required_count"] - 1
    assert "code_of_conduct" in st["overdue_review"]
    assert st["complete"] is False


def test_versioning_keeps_latest(tmp_path):
    db = DB(path=tmp_path / "c.db")
    svc = PolicyService(db)
    svc.register_policy("safeguarding", version=1, actor="scribe")
    svc.register_policy("safeguarding", version=2, actor="scribe")
    assert svc.current_policies()["safeguarding"]["version"] == 2
