"""Price adapter: OHLCV candles via ccxt against a free public exchange.

Premium credentials (EXCHANGE_API_KEY / EXCHANGE_API_SECRET) are picked up
automatically if present, but are not required — public market data is free.
"""

from __future__ import annotations

import asyncio
import os
import time

import ccxt

from .base import SchemaError

SCHEMA_VERSION = 1
_EXCHANGE_ID = os.environ.get("EXCHANGE_ID", "binance")


def _build_exchange() -> "ccxt.Exchange":
    klass = getattr(ccxt, _EXCHANGE_ID)
    params: dict = {"enableRateLimit": True}
    key = os.environ.get("EXCHANGE_API_KEY")
    secret = os.environ.get("EXCHANGE_API_SECRET")
    if key and secret:
        params["apiKey"] = key
        params["secret"] = secret
    return klass(params)


async def fetch(asset: str = "BTC/USDT", timeframe: str = "1m", limit: int = 100) -> dict:
    def _pull():
        ex = _build_exchange()
        return ex.fetch_ohlcv(asset, timeframe=timeframe, limit=limit)

    ohlcv = await asyncio.to_thread(_pull)

    if not ohlcv or not isinstance(ohlcv, list) or len(ohlcv[0]) != 6:
        raise SchemaError(f"price: unexpected OHLCV shape from {_EXCHANGE_ID}")

    candles = [
        {
            "ts": int(c[0]),
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5]),
        }
        for c in ohlcv
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "asset": asset,
        "timeframe": timeframe,
        "exchange": _EXCHANGE_ID,
        "candles": candles,
        "last": candles[-1]["close"],
        "fetched_at": time.time(),
    }
