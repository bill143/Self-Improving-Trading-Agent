"""Macro adapter: broad-market context via yfinance (free, no key).

Pulls recent closes for the S&P 500 and the US Dollar index as a simple
risk-on / risk-off backdrop. Used as context, not as a trade trigger.
"""

from __future__ import annotations

import asyncio
import time

import yfinance as yf

from .base import SchemaError

SCHEMA_VERSION = 1
_TICKERS = {"sp500": "^GSPC", "dxy": "DX-Y.NYB"}


def _last_close(ticker: str) -> float | None:
    hist = yf.Ticker(ticker).history(period="5d", interval="1d")
    if hist is None or hist.empty or "Close" not in hist:
        return None
    return float(hist["Close"].iloc[-1])


async def fetch() -> dict:
    def _pull():
        return {name: _last_close(sym) for name, sym in _TICKERS.items()}

    closes = await asyncio.to_thread(_pull)

    if not isinstance(closes, dict) or set(closes) != set(_TICKERS):
        raise SchemaError("macro: unexpected ticker set")

    return {
        "schema_version": SCHEMA_VERSION,
        "source": "yfinance",
        "closes": closes,
        "fetched_at": time.time(),
    }
