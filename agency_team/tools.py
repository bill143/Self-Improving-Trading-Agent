"""Tools the agents use to act on the world and the CRM.

Built as a factory so every tool closes over the shared CRM instance. The tool
docstrings are what Claude reads — they say when to use each tool, per the
blueprint's sequencing.
"""

from __future__ import annotations

import json

from . import connectors
from .crm import CLIENT_STAGES, LEAD_STAGES, CRM


def build_tools(crm: CRM) -> list:
    from anthropic import beta_tool

    @beta_tool
    def set_niche(niche: str, rationale: str) -> str:
        """Record the agency's chosen niche (Phase 1 decision). Call exactly once,
        after ranking the top-3 markets, with the #1 market.

        Args:
            niche: The chosen market, e.g. "gyms & fitness studios".
            rationale: Why it won, referencing the three non-negotiable filters.
        """
        crm.set_config(niche=niche, niche_rationale=rationale)
        return f"Niche set to: {niche}"

    @beta_tool
    def save_artifact(name: str, content: str) -> str:
        """Save a durable work product (research report, franchise target list,
        campaign copy, ad kit, script) as a named Markdown artifact. Phase gates
        only pass when the phase's artifact exists.

        Args:
            name: Kebab-case artifact name, e.g. "pillar1-reactivation-campaign".
            content: Full Markdown content of the artifact.
        """
        path = crm.save_artifact(name, content)
        return f"Saved artifact {path.stem}"

    @beta_tool
    def read_artifact(name: str) -> str:
        """Read a previously saved artifact by name (see get_state_summary for the
        list). Use to load the niche research, campaigns, or scripts you need.

        Args:
            name: The artifact name.
        """
        content = crm.read_artifact(name)
        return content if content is not None else f"No artifact named {name}"

    @beta_tool
    def add_leads(leads_json: str) -> str:
        """Add scraped prospect businesses to the CRM (stage NEW). Duplicates and
        past-DNC businesses are silently skipped.

        Args:
            leads_json: JSON array of lead objects with keys: business_name, city,
                state, phone, website, franchise_brand, owner_name, email,
                google_reviews, score.
        """
        added = 0
        for fields in json.loads(leads_json):
            before = len(crm.leads)
            crm.add_lead(**fields)
            added += int(len(crm.leads) > before)
        return f"Added {added} new leads (total {len(crm.leads)})"

    @beta_tool
    def list_leads(stage: str, limit: int = 25) -> str:
        """List leads in a pipeline stage, highest score first.

        Args:
            stage: One of NEW, CONTACTED, BOOKED, CLOSED, DECLINED, DNC.
            limit: Max leads to return.
        """
        if stage not in LEAD_STAGES:
            return f"Invalid stage; valid: {LEAD_STAGES}"
        return json.dumps(crm.leads_in_stage(stage, limit), indent=2)

    @beta_tool
    def update_lead(lead_id: str, stage: str = "", note: str = "") -> str:
        """Move a lead through the pipeline and/or attach a note. DNC is permanent.

        Args:
            lead_id: The lead's id.
            stage: New stage (NEW/CONTACTED/BOOKED/CLOSED/DECLINED/DNC), or empty
                to leave unchanged.
            note: Outcome note, e.g. "no answer, retry Thursday".
        """
        lead = crm.update_lead(lead_id, stage=stage or None, note=note or None)
        return json.dumps(lead)

    @beta_tool
    def close_sale(lead_id: str, package: str, monthly_investment: float, cash_collected: float) -> str:
        """Record a closed sale (after the 7-step framework, with payment processed
        and agreement sent on the call). Creates the client in ONBOARDING.

        Args:
            lead_id: The lead that closed.
            package: What was sold, e.g. "Pillars 1+2 starter bundle".
            monthly_investment: Monthly amount agreed (12-mo term, 30-day out).
            cash_collected: Cash collected on the call.
        """
        crm.update_lead(lead_id, stage="CLOSED", note=f"Closed: {package}")
        client = crm.add_client(lead_id, package, monthly_investment, cash_collected)
        return f"Client {client['id']} created in ONBOARDING"

    @beta_tool
    def advance_client(client_id: str, stage: str, note: str = "") -> str:
        """Advance a client along the fixed fulfillment conveyor belt. Order is
        enforced: ONBOARDING -> REACTIVATION -> REVIEWS_REFERRALS -> SPEED_TO_LEAD
        -> PAID_ADS -> VOICE_AI -> STEADY. Never skip backward.

        Args:
            client_id: The client's id.
            stage: The next stage.
            note: What was delivered/started.
        """
        if stage not in CLIENT_STAGES:
            return f"Invalid stage; valid: {CLIENT_STAGES}"
        client = crm.advance_client(client_id, stage, note or None)
        return json.dumps(client)

    @beta_tool
    def send_sms(to: str, body: str, on_behalf_of: str = "") -> str:
        """Send an SMS (reactivation, nurture, review request, confirmation...).
        Queues to the outbox if no SMS credential is configured — never blocks.

        Args:
            to: E.164 phone number.
            body: Message text (obey the 160-char rules from your playbook).
            on_behalf_of: Client id when texting for a client; empty for agency.
        """
        action = connectors.send_sms(crm, to, body, on_behalf_of)
        return f"sms {action['status']} ({action['id']})"

    @beta_tool
    def send_email(to: str, subject: str, body: str, on_behalf_of: str = "") -> str:
        """Send an email counterpart of a campaign message. Queues to the outbox
        until the email integration is configured.

        Args:
            to: Recipient email.
            subject: Subject line.
            body: Email body (under 100 words for campaign emails).
            on_behalf_of: Client id when emailing for a client.
        """
        action = connectors.send_email(crm, to, subject, body, on_behalf_of)
        return f"email {action['status']} ({action['id']})"

    @beta_tool
    def place_call(to: str, script_summary: str) -> str:
        """Place an outbound voice call (cold call or AI receptionist callback).
        Queues to the outbox until the voice integration is configured.

        Args:
            to: E.164 phone number.
            script_summary: Which script/angle is used, e.g. "cold-call opener".
        """
        action = connectors.place_call(crm, to, script_summary)
        return f"call {action['status']} ({action['id']})"

    @beta_tool
    def process_payment(client_ref: str, amount: float, description: str) -> str:
        """Process a payment on the sales call (close step 1 of 3). Queues to the
        outbox until the payment integration is configured.

        Args:
            client_ref: Lead or client id being charged.
            amount: Amount in USD.
            description: e.g. "Month 1 — Pillars 1+2 starter bundle".
        """
        action = connectors.process_payment(crm, client_ref, amount, description)
        return f"payment {action['status']} ({action['id']})"

    @beta_tool
    def send_agreement(client_ref: str, terms_summary: str) -> str:
        """Send the service agreement (close step 2 of 3): 12-month term with a
        30-day out in the first month. Queues until the e-sign integration exists.

        Args:
            client_ref: Lead or client id.
            terms_summary: The exact terms as stated on the call.
        """
        action = connectors.send_agreement(crm, client_ref, terms_summary)
        return f"agreement {action['status']} ({action['id']})"

    @beta_tool
    def record_metric(name: str, value: float, context: str = "") -> str:
        """Record a KPI datapoint (booked, shows, closes, cash, reviews, referrals,
        response times...). Everything gets measured.

        Args:
            name: Metric name, e.g. "appointments_booked".
            value: Numeric value.
            context: Client id / campaign / phase.
        """
        crm.record_metric(name, value, context)
        return f"metric {name}={value} recorded"

    @beta_tool
    def get_state_summary() -> str:
        """Get the current business state: niche, next foundation phase, pipeline
        counts, client stages, artifacts, and pending outbox size. Call this first
        in any task to ground yourself."""
        return json.dumps(crm.summary(), indent=2)

    return [
        set_niche, save_artifact, read_artifact, add_leads, list_leads,
        update_lead, close_sale, advance_client, send_sms, send_email,
        place_call, process_payment, send_agreement, record_metric,
        get_state_summary,
    ]
