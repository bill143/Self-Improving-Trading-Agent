"""Tests for the autonomous agency team: role loading, CRM invariants, and —
most importantly — that the orchestrator enforces the blueprint's exact
sequencing (foundation gates in order, operations loop in order)."""

from __future__ import annotations

import pytest

from agency_team.crm import CLIENT_STAGES, CRM, FOUNDATION_PHASES
from agency_team.orchestrator import (
    FOUNDATION_TASKS,
    OPERATIONS_SEQUENCE,
    Orchestrator,
    _GATE_ARTIFACTS,
)
from agency_team.roles import load_roles

EXPECTED_ROLES = {
    "agency-ceo",
    "market-research-agent",
    "lead-scraper-agent",
    "appointment-setter-agent",
    "sales-closer-agent",
    "onboarding-agent",
    "reactivation-agent",
    "reviews-referrals-agent",
    "lead-nurture-agent",
    "ads-agent",
    "voice-receptionist-agent",
    "client-success-agent",
}


def test_all_team_member_md_files_load():
    roles = load_roles()
    assert EXPECTED_ROLES <= set(roles), (
        f"missing role MD files: {EXPECTED_ROLES - set(roles)}"
    )
    for name in EXPECTED_ROLES:
        role = roles[name]
        assert role.description, f"{name} has no frontmatter description"
        assert "## Mission" in role.body, f"{name} missing Mission section"
        assert "sequence" in role.body.lower(), f"{name} missing sequence section"
        assert name in role.system_prompt


def test_sales_closer_encodes_seven_steps():
    role = load_roles()["sales-closer-agent"]
    for step in ("INTRO", "DISCOVERY", "TRANSITION", "AUTHORITY POSITIONING",
                 "PITCH", "TEMPERATURE CHECK", "CLOSE"):
        assert step in role.body, f"7-step framework missing {step}"


def test_crm_lead_lifecycle_and_dnc(tmp_path):
    crm = CRM(state_dir=tmp_path)
    lead = crm.add_lead(business_name="Iron Gym", city="Austin", phone="+15550001")
    assert lead["stage"] == "NEW"
    # duplicate is not re-added
    dup = crm.add_lead(business_name="Iron Gym", city="Austin")
    assert dup["id"] == lead["id"]
    crm.update_lead(lead["id"], stage="CONTACTED", note="called")
    crm.update_lead(lead["id"], stage="DNC")
    with pytest.raises(ValueError):
        crm.update_lead(lead["id"], stage="NEW")  # DNC is permanent


def test_client_conveyor_belt_order(tmp_path):
    crm = CRM(state_dir=tmp_path)
    lead = crm.add_lead(business_name="Flex Fitness", city="Dallas")
    crm.update_lead(lead["id"], stage="CLOSED")
    client = crm.add_client(lead["id"], "Pillars 1+2", 1500.0, 1500.0)
    assert client["stage"] == "ONBOARDING"
    crm.advance_client(client["id"], "REACTIVATION")
    with pytest.raises(ValueError):
        crm.advance_client(client["id"], "ONBOARDING")  # no going backward
    # forward through the whole belt works
    for stage in CLIENT_STAGES[2:]:
        crm.advance_client(client["id"], stage)


def test_outbox_queues_without_credentials(tmp_path, monkeypatch):
    for var in ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER"):
        monkeypatch.delenv(var, raising=False)
    from agency_team import connectors

    crm = CRM(state_dir=tmp_path)
    action = connectors.send_sms(crm, "+15550002", "hello")
    assert action["status"] == "queued"
    assert crm.summary()["outbox_pending"] == 1


def test_every_foundation_phase_has_task_and_artifact_gate():
    gates = [g for g, _ in FOUNDATION_PHASES]
    assert gates == list(FOUNDATION_TASKS)
    assert gates == list(_GATE_ARTIFACTS)


def test_orchestrator_runs_foundation_in_exact_order(tmp_path):
    crm = CRM(state_dir=tmp_path)
    calls: list[str] = []

    def fake_run_agent(role, task, crm_):
        calls.append(role.name)
        gate, _ = crm_.next_foundation_phase()
        if gate == "niche_selected":
            crm_.set_config(niche="gyms & fitness studios")
        crm_.save_artifact(_GATE_ARTIFACTS[gate], f"artifact for {gate}")
        return "done"

    orch = Orchestrator(crm=crm, run_agent=fake_run_agent)
    ran_gates = []
    while (nxt := crm.next_foundation_phase()) is not None:
        ran_gates.append(orch.run_foundation_step())
    assert ran_gates == [g for g, _ in FOUNDATION_PHASES]
    # owners were invoked in the blueprint's order
    assert calls == [owner for _, owner in FOUNDATION_PHASES]
    assert crm.summary()["foundation_complete"] is True


def test_gate_does_not_pass_without_artifact(tmp_path):
    crm = CRM(state_dir=tmp_path)

    def lazy_agent(role, task, crm_):
        return "did nothing"  # produces no artifact

    orch = Orchestrator(crm=crm, run_agent=lazy_agent)
    gate = orch.run_foundation_step()
    assert gate == "niche_selected"
    assert not crm.gate_passed("niche_selected")  # gate held — check, don't assume
    assert crm.next_foundation_phase()[0] == "niche_selected"  # phase retries


def test_operations_cycle_runs_in_fixed_order(tmp_path):
    crm = CRM(state_dir=tmp_path)
    # complete the foundation first
    crm.set_config(niche="gyms")
    for gate, _ in FOUNDATION_PHASES:
        crm.save_artifact(_GATE_ARTIFACTS[gate], "x")
        crm.pass_gate(gate)

    calls: list[str] = []

    def fake_run_agent(role, task, crm_):
        calls.append(role.name)
        return "ok"

    orch = Orchestrator(crm=crm, run_agent=fake_run_agent)
    result = orch.run_cycle()
    assert result["mode"] == "operations"
    assert calls == [owner for owner, _ in OPERATIONS_SEQUENCE]
    # the loop is: scrape -> set -> close -> onboard -> fulfill(5) -> success
    assert calls[0] == "lead-scraper-agent"
    assert calls[1] == "appointment-setter-agent"
    assert calls[2] == "sales-closer-agent"
    assert calls[3] == "onboarding-agent"
    assert calls[-1] == "client-success-agent"
