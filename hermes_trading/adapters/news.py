"""News adapter.

Free default: CryptoCompare's public news feed (no key required for the basic
endpoint). A NEWS_API_KEY, if set, is sent as an auth param.
"""

from __future__ import annotations

import os
import time

import httpx

from .base import SchemaError

SCHEMA_VERSION = 1
_URL = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"


async def fetch(limit: int = 10) -> dict:
    params = {}
    key = os.environ.get("NEWS_API_KEY")
    if key:
        params["api_key"] = key

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(_URL, params=params)
        resp.raise_for_status()
        payload = resp.json()

    items = payload.get("Data")
    if not isinstance(items, list):
        raise SchemaError("news: expected a 'Data' list in payload")

    headlines = [
        {"title": i.get("title"), "source": i.get("source"), "ts": i.get("published_on")}
        for i in items[:limit]
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "source": "cryptocompare",
        "count": len(headlines),
        "headlines": headlines,
        "fetched_at": time.time(),
    }
