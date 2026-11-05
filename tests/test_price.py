import asyncio

import pytest

from hermes_trading.adapters import price


class _Blocked:
    def fetch_ohlcv(self, *a, **k):
        raise RuntimeError("451 restricted location")


class _Ok:
    def fetch_ohlcv(self, *a, **k):
        return [[1, 1.0, 2.0, 0.5, 1.5, 10.0], [2, 1.5, 2.5, 1.0, 2.0, 12.0]]


def test_fails_over_to_next_exchange(monkeypatch):
    monkeypatch.setenv("EXCHANGE_ID", "binance,okx")
    monkeypatch.setattr(price, "_EXCHANGES", {"binance": _Blocked(), "okx": _Ok()})
    out = asyncio.run(price.fetch("BTC/USDT"))
    assert out["exchange"] == "okx"
    assert out["last"] == 2.0


def test_all_exchanges_failing_raises_with_every_reason(monkeypatch):
    monkeypatch.setenv("EXCHANGE_ID", "binance,okx")
    monkeypatch.setattr(price, "_EXCHANGES", {"binance": _Blocked(), "okx": _Blocked()})
    with pytest.raises(ConnectionError, match="binance.*okx"):
        asyncio.run(price.fetch("BTC/USDT"))


def test_unknown_exchange_rejected(monkeypatch):
    monkeypatch.setenv("EXCHANGE_ID", "notanexchange")
    with pytest.raises(ValueError):
        price.exchange_chain()
