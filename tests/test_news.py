import asyncio

import httpx
import pytest

from hermes_trading.adapters import news

RSS = """<?xml version="1.0"?><rss version="2.0"><channel><title>x</title>
<item><title>BTC rallies</title><pubDate>Thu, 05 Nov 2026 17:00:00 +0000</pubDate></item>
<item><title> ETF inflows </title><pubDate>not a date</pubDate></item>
</channel></rss>"""


def test_parse_rss_extracts_titles_and_timestamps():
    out = news.parse_rss(RSS, "example.com", 10)
    assert [h["title"] for h in out] == ["BTC rallies", "ETF inflows"]
    assert out[0]["ts"] == 1793898000
    assert out[1]["ts"] is None


def _mock(monkeypatch, handler):
    real = httpx.AsyncClient

    def factory(*a, **k):
        k["transport"] = httpx.MockTransport(handler)
        return real(*a, **k)

    monkeypatch.setattr(news.httpx, "AsyncClient", factory)


def test_rss_fails_over_to_next_feed(monkeypatch):
    monkeypatch.delenv("NEWS_API_KEY", raising=False)
    monkeypatch.setenv("NEWS_RSS_FEEDS", "https://down.example/rss,https://up.example/rss")
    _mock(monkeypatch, lambda req: httpx.Response(503) if req.url.host == "down.example"
          else httpx.Response(200, text=RSS))
    out = asyncio.run(news.fetch(limit=1))
    assert out["source"] == "up.example"
    assert out["count"] == 1


def test_all_feeds_failing_raises(monkeypatch):
    monkeypatch.delenv("NEWS_API_KEY", raising=False)
    monkeypatch.setenv("NEWS_RSS_FEEDS", "https://a.example/rss")
    _mock(monkeypatch, lambda req: httpx.Response(200, text="<html>nope"))
    with pytest.raises(ConnectionError):
        asyncio.run(news.fetch())


def test_api_key_uses_cryptocompare(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "k")
    seen = {}

    def handler(req):
        seen["key"] = req.url.params.get("api_key")
        return httpx.Response(200, json={"Data": [{"title": "t", "source": "s", "published_on": 1}]})

    _mock(monkeypatch, handler)
    out = asyncio.run(news.fetch())
    assert out["source"] == "cryptocompare" and seen["key"] == "k"
