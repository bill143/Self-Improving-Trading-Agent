"""Price adapter: OHLCV candles via ccxt against a free public exchange.

EXCHANGE_ID may be a comma-separated failover chain (e.g. "binanceus,okx,kraken");
each exchange is tried in order and the first that returns data wins. This keeps
the worker alive when an exchange geo-blocks the host region (Binance returns
HTTP 451 to US data centres).

Premium credentials (EXCHANGE_API_KEY / EXCHANGE_API_SECRET) are applied to the
first exchange in the chain only, and are not required — public data is free.
"""

from __future__ import annotations

import asyncio
import os
import time

import ccxt

from .base import SchemaError

SCHEMA_VERSION = 1
_DEFAULT_CHAIN = "binance,binanceus,okx,kraken"

# Exchange instances are reused across ticks so markets load once, not per tick.
_EXCHANGES: dict[str, "ccxt.Exchange"] = {}


def exchange_chain() -> list[str]:
    raw = os.environ.get("EXCHANGE_ID", _DEFAULT_CHAIN)
    chain = [e.strip() for e in raw.split(",") if e.strip()]
    unknown = [e for e in chain if not hasattr(ccxt, e)]
    if unknown or not chain:
        raise ValueError(f"EXCHANGE_ID: unknown ccxt exchange(s) {unknown or raw!r}")
    return chain


def _build_exchange(exchange_id: str, *, primary: bool) -> "ccxt.Exchange":
    if exchange_id not in _EXCHANGES:
        params: dict = {"enableRateLimit": True}
        key = os.environ.get("EXCHANGE_API_KEY")
        secret = os.environ.get("EXCHANGE_API_SECRET")
        if primary and key and secret:
            params["apiKey"] = key
            params["secret"] = secret
        _EXCHANGES[exchange_id] = getattr(ccxt, exchange_id)(params)
    return _EXCHANGES[exchange_id]


def _pull(asset: str, timeframe: str, limit: int) -> tuple[str, list]:
    errors: list[str] = []
    for i, exchange_id in enumerate(exchange_chain()):
        try:
            ex = _build_exchange(exchange_id, primary=i == 0)
            return exchange_id, ex.fetch_ohlcv(asset, timeframe=timeframe, limit=limit)
        except Exception as exc:  # noqa: BLE001 - fail over to the next exchange
            errors.append(f"{exchange_id}: {type(exc).__name__}: {str(exc)[:160]}")
    raise ConnectionError("price: all exchanges failed — " + " | ".join(errors))


async def fetch(asset: str = "BTC/USDT", timeframe: str = "1m", limit: int = 100) -> dict:
    exchange_id, ohlcv = await asyncio.to_thread(_pull, asset, timeframe, limit)

    if not ohlcv or not isinstance(ohlcv, list) or len(ohlcv[0]) != 6:
        raise SchemaError(f"price: unexpected OHLCV shape from {exchange_id}")

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
        "exchange": exchange_id,
        "candles": candles,
        "last": candles[-1]["close"],
        "fetched_at": time.time(),
    }
