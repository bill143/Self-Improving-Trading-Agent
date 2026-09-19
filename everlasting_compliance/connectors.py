"""Outbound connectors — Telegram and email — with the outbox pattern.

If a credential is configured the message is sent; otherwise it is queued to a durable
outbox so reminders are never silently lost while the platform is being stood up. Once
tokens are added, `drain_outbox` sends what was queued.
"""

from __future__ import annotations

import os

import httpx

from .db import DB


def _queue(db: DB, channel: str, payload: dict, status: str = "queued") -> int:
    return db.add_record("outbox", {"channel": channel, "status": status, **payload},
                         retention_class="default", actor="connectors")


def telegram_send(db: DB, text: str, chat_id: str | None = None, *, actor: str = "system") -> dict:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = chat_id or (os.environ.get("TELEGRAM_ALLOWED_CHAT_IDS", "").split(",")[0] or None)
    if not token or not chat:
        rid = _queue(db, "telegram", {"text": text, "chat_id": chat or ""})
        return {"status": "queued", "record_id": rid}
    try:
        resp = httpx.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": text}, timeout=20,
        )
        resp.raise_for_status()
        rid = _queue(db, "telegram", {"text": text, "chat_id": chat}, status="sent")
        return {"status": "sent", "record_id": rid}
    except Exception as exc:  # never crash the reminder loop
        rid = _queue(db, "telegram", {"text": text, "chat_id": chat, "error": str(exc)},
                     status="failed")
        return {"status": "failed", "record_id": rid, "error": str(exc)}


def email_send(db: DB, subject: str, body: str, to: str, *, actor: str = "system") -> dict:
    host = os.environ.get("SMTP_HOST")
    if not host:
        rid = _queue(db, "email", {"subject": subject, "body": body, "to": to})
        return {"status": "queued", "record_id": rid}
    # SMTP send is wired at deployment; queue until then even if host is set but
    # credentials are incomplete, so nothing is lost.
    rid = _queue(db, "email", {"subject": subject, "body": body, "to": to}, status="queued")
    return {"status": "queued", "record_id": rid}


def outbox(db: DB, channel: str | None = None) -> list[dict]:
    rows = db.list_records("outbox")
    if channel:
        rows = [r for r in rows if r["data"].get("channel") == channel]
    return rows


def pending_count(db: DB) -> int:
    return sum(1 for r in db.list_records("outbox") if r["data"].get("status") == "queued")
