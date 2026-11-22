"""News adapter.

With NEWS_API_KEY set: CryptoCompare's news API (the key is sent as api_key;
CryptoCompare no longer serves this endpoint without one).

Without a key: free public RSS feeds, tried in order until one returns
headlines (NEWS_RSS_FEEDS, comma-separated, overrides the default list).
"""

from __future__ import annotations

import os
import time
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

import httpx

from .base import SchemaError

SCHEMA_VERSION = 1
_CRYPTOCOMPARE_URL = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
_DEFAULT_FEEDS = (
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
)
_HEADERS = {"User-Agent": "hermes-trading/0.1 (+paper-trading research bot)"}


def rss_feeds() -> list[str]:
    raw = os.environ.get("NEWS_RSS_FEEDS")
    if raw:
        return [u.strip() for u in raw.split(",") if u.strip()]
    return list(_DEFAULT_FEEDS)


def _ts(pub_date: str | None) -> int | None:
    if not pub_date:
        return None
    try:
        return int(parsedate_to_datetime(pub_date).timestamp())
    except (TypeError, ValueError):
        return None


def parse_rss(xml_text: str, source: str, limit: int) -> list[dict]:
    """Extract headlines from an RSS 2.0 document. Empty list if none found."""
    root = ET.fromstring(xml_text)
    items = root.findall("./channel/item")
    headlines = []
    for item in items[:limit]:
        title = (item.findtext("title") or "").strip()
        if title:
            headlines.append({"title": title, "source": source, "ts": _ts(item.findtext("pubDate"))})
    return headlines


async def _fetch_cryptocompare(client: httpx.AsyncClient, key: str, limit: int) -> dict:
    resp = await client.get(_CRYPTOCOMPARE_URL, params={"api_key": key})
    resp.raise_for_status()
    items = resp.json().get("Data")
    if not isinstance(items, list):
        raise SchemaError("news: expected a 'Data' list in payload")
    return {
        "source": "cryptocompare",
        "headlines": [
            {"title": i.get("title"), "source": i.get("source"), "ts": i.get("published_on")}
            for i in items[:limit]
        ],
    }


async def _fetch_rss(client: httpx.AsyncClient, limit: int) -> dict:
    errors: list[str] = []
    for url in rss_feeds():
        source = httpx.URL(url).host
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            headlines = parse_rss(resp.text, source, limit)
            if headlines:
                return {"source": source, "headlines": headlines}
            errors.append(f"{source}: no items")
        except (httpx.HTTPError, ET.ParseError) as exc:
            errors.append(f"{source}: {type(exc).__name__}")
    raise ConnectionError("news: all RSS feeds failed — " + " | ".join(errors))


async def fetch(limit: int = 10) -> dict:
    key = os.environ.get("NEWS_API_KEY")
    async with httpx.AsyncClient(timeout=10.0, headers=_HEADERS, follow_redirects=True) as client:
        result = await (_fetch_cryptocompare(client, key, limit) if key else _fetch_rss(client, limit))
    return {
        "schema_version": SCHEMA_VERSION,
        "source": result["source"],
        "count": len(result["headlines"]),
        "headlines": result["headlines"],
        "fetched_at": time.time(),
    }
