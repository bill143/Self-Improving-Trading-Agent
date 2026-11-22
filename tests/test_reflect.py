import importlib
import json

import yaml
import pytest


@pytest.fixture()
def state(tmp_path, monkeypatch):
    """Point the worker's state dir at a temp directory."""
    monkeypatch.setenv("HERMES_TRADING_STATE_DIR", str(tmp_path))
    # Reload modules so they re-read the env-driven paths.
    import hermes_trading.paths as paths
    importlib.reload(paths)

    (tmp_path / "goal.yaml").write_text(yaml.safe_dump({
        "target_return_30d": 0.05,
        "max_drawdown": 0.08,
        "min_sharpe": 1.2,
        "failure_below": -0.04,
    }))
    (tmp_path / "strategy.yaml").write_text(yaml.safe_dump({
        "version": "01",
        "entry": {"indicator": "rsi", "threshold": 30, "direction": "long"},
        "stop_loss_pct": 2.0,
        "position_size_r": 0.5,
    }, sort_keys=False))
    (tmp_path / "trades.jsonl").touch()
    (tmp_path / "hypotheses.jsonl").touch()
    (tmp_path / "history").mkdir()

    import hermes_trading.reflect as reflect
    importlib.reload(reflect)
    return tmp_path, reflect


def test_fallback_loosens_threshold_when_below_target(state):
    tmp_path, reflect = state
    # No trades -> realised return 0 < target -> threshold loosens by 2.
    reflect.reflect_fallback()

    strat = yaml.safe_load((tmp_path / "strategy.yaml").read_text())
    assert strat["version"] == "02"
    assert strat["entry"]["threshold"] == 32

    # Prior version archived.
    assert (tmp_path / "history" / "v0001.yaml").exists()

    # Hypothesis recorded with exactly one variable.
    lines = [l for l in (tmp_path / "hypotheses.jsonl").read_text().splitlines() if l]
    h = json.loads(lines[-1])
    assert h["variable"] == "entry.threshold"
    assert h["old_value"] == 30 and h["new_value"] == 32


def test_fallback_changes_exactly_one_variable(state):
    tmp_path, reflect = state
    before = yaml.safe_load((tmp_path / "strategy.yaml").read_text())
    reflect.reflect_fallback()
    after = yaml.safe_load((tmp_path / "strategy.yaml").read_text())

    # Only version + entry.threshold differ.
    assert after["stop_loss_pct"] == before["stop_loss_pct"]
    assert after["position_size_r"] == before["position_size_r"]
    assert after["entry"]["threshold"] != before["entry"]["threshold"]


def _write_trades(tmp_path, returns, version="01"):
    with open(tmp_path / "trades.jsonl", "w") as fh:
        for r in returns:
            fh.write(json.dumps({"return_pct": r, "strategy_version": version}) + "\n")


def test_fallback_tightens_stop_first_when_drawdown_exceeded(state):
    tmp_path, reflect = state
    _write_trades(tmp_path, [-0.05, -0.05])  # ~9.75% drawdown > 8% max
    reflect.reflect_fallback()
    strat = yaml.safe_load((tmp_path / "strategy.yaml").read_text())
    assert strat["stop_loss_pct"] == 1.8
    assert strat["entry"]["threshold"] == 30


def test_fallback_tightens_entry_when_losing_within_drawdown(state):
    tmp_path, reflect = state
    _write_trades(tmp_path, [0.01, -0.02])
    reflect.reflect_fallback()
    strat = yaml.safe_load((tmp_path / "strategy.yaml").read_text())
    assert strat["entry"]["threshold"] == 28
    assert strat["stop_loss_pct"] == 2.0


def test_fallback_judges_only_current_version_trades(state):
    tmp_path, reflect = state
    # Heavy losses under an older version must not drive this version's change.
    with open(tmp_path / "trades.jsonl", "w") as fh:
        for _ in range(5):
            fh.write(json.dumps({"return_pct": -0.05, "strategy_version": "00"}) + "\n")
    reflect.reflect_fallback()
    strat = yaml.safe_load((tmp_path / "strategy.yaml").read_text())
    assert strat["entry"]["threshold"] == 32  # no v01 trades -> return 0 -> loosen


def test_fallback_holds_at_guardrail_bound(state):
    tmp_path, reflect = state
    s = yaml.safe_load((tmp_path / "strategy.yaml").read_text())
    s["entry"]["threshold"] = reflect.ENTRY_THRESHOLD_MIN
    (tmp_path / "strategy.yaml").write_text(yaml.safe_dump(s, sort_keys=False))
    _write_trades(tmp_path, [0.01, -0.02])
    reflect.reflect_fallback()
    after = yaml.safe_load((tmp_path / "strategy.yaml").read_text())
    assert after["version"] == "01"
    h = json.loads((tmp_path / "hypotheses.jsonl").read_text().splitlines()[-1])
    assert h["rule"] == "hold"
