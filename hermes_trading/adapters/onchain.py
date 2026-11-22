"""On-chain / sentiment adapter.

Free default: the Crypto Fear & Greed index (alternative.me), no key required.
A GLASSNODE_API_KEY, if set, can be wired in here for richer on-chain metrics.
"""

from __future__ import annotations

import time

import httpx

from .base import SchemaError

SCHEMA_VERSION = 1
_URL = "https://api.alternative.me/fng/?limit=1&format=json"


async def fetch() -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(_URL)
        resp.raise_for_status()
        payload = resp.json()

    data = payload.get("data")
    if not isinstance(data, list) or not data or "value" not in data[0]:
        raise SchemaError("onchain: unexpected fear & greed payload")

    point = data[0]
    return {
        "schema_version": SCHEMA_VERSION,
        "source": "alternative.me/fng",
        "fear_greed": int(point["value"]),
        "classification": point.get("value_classification"),
        "fetched_at": time.time(),
    }
