"""The CEO loop: exact blueprint sequencing, fully autonomous.

Foundation phases run once, in order, each with a gate the CRM must show as
passed (the artifact/decision must actually exist). Then the operations loop
runs every cycle: scrape -> set -> close -> onboard -> fulfill -> success.

`run_agent` is injectable so the sequencing is testable without API calls.
"""

from __future__ import annotations

from collections.abc import Callable

from .agents import run_agent as _default_run_agent
from .crm import CRM, FOUNDATION_PHASES
from .roles import Role, load_roles

RunAgentFn = Callable[[Role, str, CRM], str]

# ---------------------------------------------------------------------------
# Foundation phase tasks (run once each, in this order) and their gate checks.
# ---------------------------------------------------------------------------

FOUNDATION_TASKS: dict[str, str] = {
    "niche_selected": (
        "Execute Phase 1 — niche selection. Apply your three non-negotiable "
        "filters, rank the top 3 markets, choose #1, call set_niche with the "
        "winner, and save the full ranked analysis with save_artifact as "
        "'phase1-niche-research'."
    ),
    "franchises_targeted": (
        "Execute Phase 2 — franchise targeting ('choose your ship') for the "
        "chosen niche (see get_state_summary). Identify the top 10 franchise "
        "brands per your filters and save the ranked list with save_artifact as "
        "'phase2-franchise-targets'."
    ),
    "pillar1_reactivation_built": (
        "Execute Phase 3 — build the master AI Database Reactivation campaign "
        "for the chosen niche (all deliverables in your exact order: offer, "
        "Day 1/2/3 SMS+email, YES handler, NO/STOP handler). Save it with "
        "save_artifact as 'pillar1-reactivation-campaign'."
    ),
    "pillar2_reviews_referrals_built": (
        "Execute Phase 4 — build the master Reviews & Referrals system for the "
        "chosen niche (all 5 messages, SMS + email versions, plus the 5 review "
        "auto-responses). Save it with save_artifact as "
        "'pillar2-reviews-referrals-system'."
    ),
    "pillar3_speed_to_lead_built": (
        "Execute Phase 5 — build the master 5-message website lead nurture "
        "sequence (5-minute instant response, 24h, 48h, booking confirmations, "
        "no-show win-back). Save it with save_artifact as "
        "'pillar3-speed-to-lead-sequence'."
    ),
    "ad_intelligence_built": (
        "Execute Phase 6 — ad intelligence. Research the winning ad patterns for "
        "the chosen niche (hooks, promises, CTAs, structure, visual style), "
        "derive the winning formula, write 3 ad variations for our offer, and "
        "save the full kit with save_artifact as 'phase6-ad-intelligence-kit'."
    ),
    "sales_readiness_passed": (
        "Execute Phase 7 — sales readiness. Write out the complete 7-step sales "
        "framework operationalized for the chosen niche (discovery questions "
        "with real numbers to collect, pitch lines per pillar weaving prospect "
        "words back in, temperature-check re-loop, close sequence with 12-month/"
        "30-day-out terms), run one full drill-mode self-test transcript against "
        "a realistic prospect, and save both with save_artifact as "
        "'phase7-sales-playbook'."
    ),
}

_GATE_ARTIFACTS: dict[str, str] = {
    "niche_selected": "phase1-niche-research",
    "franchises_targeted": "phase2-franchise-targets",
    "pillar1_reactivation_built": "pillar1-reactivation-campaign",
    "pillar2_reviews_referrals_built": "pillar2-reviews-referrals-system",
    "pillar3_speed_to_lead_built": "pillar3-speed-to-lead-sequence",
    "ad_intelligence_built": "phase6-ad-intelligence-kit",
    "sales_readiness_passed": "phase7-sales-playbook",
}


def gate_satisfied(crm: CRM, gate: str) -> bool:
    """A gate passes only when its artifact actually exists (plus the niche for
    Phase 1) — check, don't assume."""
    artifact = _GATE_ARTIFACTS[gate]
    if crm.read_artifact(artifact) is None:
        return False
    if gate == "niche_selected" and not crm.config.get("niche"):
        return False
    return True


# ---------------------------------------------------------------------------
# Operations loop (every cycle, fixed order).
# ---------------------------------------------------------------------------

OPERATIONS_SEQUENCE: list[tuple[str, str]] = [
    (
        "lead-scraper-agent",
        "Operations step 1 — check get_state_summary. If uncontacted NEW leads "
        "are below 1,000, research and add a batch of new target businesses in "
        "the chosen niche with add_leads (franchise locations from "
        "'phase2-franchise-targets' first, scored per your method).",
    ),
    (
        "appointment-setter-agent",
        "Operations step 2 — work the pipeline: pull the top NEW leads "
        "(list_leads), run your outbound procedure (place_call / send_sms / "
        "send_email with the proven script), and record every outcome with "
        "update_lead. Book appointments by moving leads to BOOKED with the "
        "appointment details in a note, and send confirmation texts.",
    ),
    (
        "sales-closer-agent",
        "Operations step 3 — for each BOOKED lead (list_leads), run the "
        "appointment through the 7-step framework using the "
        "'phase7-sales-playbook' artifact. For every close: process_payment, "
        "send_agreement, then close_sale — all three on the call. Record "
        "declined outcomes honestly with update_lead.",
    ),
    (
        "onboarding-agent",
        "Operations step 4 — onboard every client in ONBOARDING (see "
        "get_state_summary): run your onboarding checklist, then advance_client "
        "to REACTIVATION with a note of what was collected and kicked off.",
    ),
    (
        "reactivation-agent",
        "Operations step 5a — for each client in REACTIVATION: run the "
        "reactivation campaign from 'pillar1-reactivation-campaign' adapted to "
        "the client (send_sms/send_email), record results with record_metric, "
        "and when the month-one campaign is delivered advance_client to "
        "REVIEWS_REFERRALS.",
    ),
    (
        "reviews-referrals-agent",
        "Operations step 5b — for each client in REVIEWS_REFERRALS: run the "
        "system from 'pillar2-reviews-referrals-system' (rating requests, review "
        "asks, referral asks, auto-responses), record metrics, and when live "
        "advance_client to SPEED_TO_LEAD.",
    ),
    (
        "lead-nurture-agent",
        "Operations step 5c — for each client in SPEED_TO_LEAD: attach the "
        "'pillar3-speed-to-lead-sequence', simulate/handle pending form leads "
        "within the 5-minute rule, record metrics, and when live advance_client "
        "to PAID_ADS.",
    ),
    (
        "ads-agent",
        "Operations step 5d — for each client in PAID_ADS: confirm reactivation "
        "cash was collected (gate), localize the 'phase6-ad-intelligence-kit', "
        "launch/iterate campaigns, route every ad lead to the nurture sequence, "
        "record cost metrics, and when stable advance_client to VOICE_AI.",
    ),
    (
        "voice-receptionist-agent",
        "Operations step 5e — for each client in VOICE_AI: produce the AI "
        "receptionist configuration (facts pack, routing rules, escalation "
        "rules) as an artifact 'voice-config-<client_id>', queue the deployment "
        "call, record before/after missed-call metrics, and advance_client to "
        "STEADY.",
    ),
    (
        "client-success-agent",
        "Operations step 6 — for every client: aggregate results, produce the "
        "weekly report artifact 'report-<client_id>', run 30-day reviews and "
        "upsells where due, make referral asks to demonstrably happy clients "
        "(franchise clients first), and feed referral leads back with add_leads.",
    ),
]


class Orchestrator:
    def __init__(
        self,
        crm: CRM | None = None,
        roles: dict[str, Role] | None = None,
        run_agent: RunAgentFn = _default_run_agent,
    ):
        self.crm = crm or CRM()
        self.roles = roles or load_roles()
        self.run_agent = run_agent
        missing = {owner for _, owner in FOUNDATION_PHASES} - set(self.roles)
        if missing:
            raise RuntimeError(f"missing agent definitions: {sorted(missing)}")

    def run_foundation_step(self) -> str | None:
        """Run the next incomplete foundation phase. Returns the gate name run,
        or None when the foundation is complete."""
        nxt = self.crm.next_foundation_phase()
        if nxt is None:
            return None
        gate, owner = nxt
        role = self.roles[owner]
        self.run_agent(role, FOUNDATION_TASKS[gate], self.crm)
        if gate_satisfied(self.crm, gate):
            self.crm.pass_gate(gate)
        else:
            self.crm.log("gate_not_satisfied", gate=gate, owner=owner)
        return gate

    def run_operations_cycle(self) -> list[str]:
        """Run one full pass of the operations loop, in the fixed order."""
        ran: list[str] = []
        for owner, task in OPERATIONS_SEQUENCE:
            role = self.roles[owner]
            self.run_agent(role, task, self.crm)
            ran.append(owner)
        self.crm.log("operations_cycle_complete", agents=len(ran))
        return ran

    def run_cycle(self) -> dict:
        """One autonomous cycle: advance the foundation if incomplete, otherwise
        run a full operations pass."""
        if self.crm.next_foundation_phase() is not None:
            gate = self.run_foundation_step()
            return {"mode": "foundation", "phase": gate, "summary": self.crm.summary()}
        ran = self.run_operations_cycle()
        return {"mode": "operations", "agents_run": ran, "summary": self.crm.summary()}
