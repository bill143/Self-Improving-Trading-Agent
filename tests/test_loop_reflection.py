import asyncio
import importlib
import json

import yaml


def _worker(tmp_path, monkeypatch, every=2):
    monkeypatch.setenv("HERMES_TRADING_STATE_DIR", str(tmp_path))
    monkeypatch.setenv("HERMES_REFLECT_MODE", "fallback")
    import hermes_trading.paths as paths
    importlib.reload(paths)
    (tmp_path / "goal.yaml").write_text(yaml.safe_dump({"reflection_every": every}))
    (tmp_path / "strategy.yaml").write_text(
        yaml.safe_dump({"version": "01", "entry": {"threshold": 30}, "stop_loss_pct": 2.0})
    )
    (tmp_path / "hypotheses.jsonl").touch()
    (tmp_path / "history").mkdir()
    import hermes_trading.reflect as reflect
    import hermes_trading.loop as loop
    importlib.reload(reflect)
    importlib.reload(loop)
    return loop.TradingWorker()


def _close(tmp_path, worker, n):
    with open(tmp_path / "trades.jsonl", "a") as fh:
        for _ in range(n):
            fh.write(json.dumps({"return_pct": 0.001, "strategy_version": "01"}) + "\n")
    worker._closed_trade = True
    strategy = yaml.safe_load((tmp_path / "strategy.yaml").read_text())
    asyncio.run(worker._maybe_reflect(strategy))
    return yaml.safe_load((tmp_path / "strategy.yaml").read_text())


def test_reflects_after_every_n_closed_trades(tmp_path, monkeypatch):
    w = _worker(tmp_path, monkeypatch, every=2)
    (tmp_path / "trades.jsonl").touch()
    assert _close(tmp_path, w, 1)["version"] == "01"
    assert _close(tmp_path, w, 1)["version"] == "02"


def test_no_reflection_without_a_closed_trade(tmp_path, monkeypatch):
    w = _worker(tmp_path, monkeypatch, every=1)
    (tmp_path / "trades.jsonl").write_text(json.dumps({"return_pct": 0.0, "strategy_version": "01"}) + "\n")
    asyncio.run(w._maybe_reflect({"version": "01"}))
    assert yaml.safe_load((tmp_path / "strategy.yaml").read_text())["version"] == "01"
