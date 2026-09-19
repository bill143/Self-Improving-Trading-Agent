"""External-world connectors.

Every outward-facing action (SMS, email, call, payment, agreement) is dispatched
here. If the matching credential is configured, the action is sent for real;
otherwise it is queued to the CRM outbox so the autonomous loop never blocks on
a missing integration — the business keeps running and the sends drain once
credentials are added.

Currently implemented live: Twilio SMS. Everything else queues with a clear
`integration` tag (GoHighLevel, Stripe, Dropbox Sign, Synthflow) so wiring them
up later is a single function each.
"""

from __future__ import annotations

import os

import httpx

from .crm import CRM


def _twilio_creds() -> tuple[str, str, str] | None:
    sid = os.environ.get("TWILIO_ACCOUNT_SID")
    token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_ = os.environ.get("TWILIO_FROM_NUMBER")
    if sid and token and from_:
        return sid, token, from_
    return None


def send_sms(crm: CRM, to: str, body: str, on_behalf_of: str = "") -> dict:
    creds = _twilio_creds()
    payload = {"to": to, "body": body, "on_behalf_of": on_behalf_of, "integration": "twilio"}
    if not creds:
        return crm.queue_action("sms", payload)
    sid, token, from_ = creds
    try:
        resp = httpx.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
            auth=(sid, token),
            data={"To": to, "From": from_, "Body": body},
            timeout=30,
        )
        resp.raise_for_status()
        return crm.queue_action("sms", payload, status="sent")
    except Exception as exc:  # network/auth errors must never crash the loop
        payload["error"] = str(exc)
        return crm.queue_action("sms", payload, status="failed")


def send_email(crm: CRM, to: str, subject: str, body: str, on_behalf_of: str = "") -> dict:
    return crm.queue_action(
        "email",
        {"to": to, "subject": subject, "body": body, "on_behalf_of": on_behalf_of,
         "integration": "gohighlevel"},
    )


def place_call(crm: CRM, to: str, script_summary: str) -> dict:
    return crm.queue_action(
        "call",
        {"to": to, "script_summary": script_summary, "integration": "synthflow"},
    )


def process_payment(crm: CRM, client_ref: str, amount: float, description: str) -> dict:
    return crm.queue_action(
        "payment",
        {"client_ref": client_ref, "amount": amount, "description": description,
         "integration": "stripe"},
    )


def send_agreement(crm: CRM, client_ref: str, terms_summary: str) -> dict:
    return crm.queue_action(
        "agreement",
        {"client_ref": client_ref, "terms_summary": terms_summary,
         "integration": "dropbox_sign"},
    )
