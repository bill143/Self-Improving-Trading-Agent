"""The reflection cycle: look at recent outcomes and change ONE variable.

Two modes:

  --fallback   Deterministic, risk-first rules judged on the current version's
               trades only: drawdown over max -> tighten the stop; losing ->
               tighten the entry; below target -> loosen the entry; else hold.
               Bounded, and exactly one variable changes.

  --hermes     Production mode. Formats recent trades + the current strategy
               into a prompt, calls the `hermes` CLI as a subprocess, parses the
               returned hypothesis, and applies it (still one variable only).

Either way: the prior strategy is archived to state/history/v{NNNN}.yaml, the
version is bumped, and the hypothesis is appended to state/hypotheses.jsonl.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import yaml

from . import paths, score


# --------------------------------------------------------------------------- #
# IO helpers
# --------------------------------------------------------------------------- #
def _load_yaml(path: Path) -> dict:
    with open(path, "r") as fh:
        return yaml.safe_load(fh) or {}


def _dump_yaml(path: Path, obj: dict) -> None:
    with open(path, "w") as fh:
        yaml.safe_dump(obj, fh, sort_keys=False)


def _read_trades(limit: int | None = None) -> list[dict]:
    p = paths.trades_file()
    if not p.exists():
        return []
    rows = [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
    return rows[-limit:] if limit else rows


def _append_hypothesis(h: dict) -> None:
    with open(paths.hypotheses_file(), "a") as fh:
        fh.write(json.dumps(h) + "\n")


def _set_nested(d: dict, dotted: str, value) -> None:
    keys = dotted.split(".")
    cur = d
    for k in keys[:-1]:
        cur = cur.setdefault(k, {})
    cur[keys[-1]] = value


def _get_nested(d: dict, dotted: str):
    cur = d
    for k in dotted.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


# --------------------------------------------------------------------------- #
# Applying a change (shared by both modes)
# --------------------------------------------------------------------------- #
def _bump_version(version: str) -> str:
    try:
        return f"{int(version) + 1:02d}"
    except (TypeError, ValueError):
        return "02"


def apply_change(strategy: dict, variable: str, new_value, hypothesis: dict) -> dict:
    """Archive the current strategy, change one variable, bump version, log."""
    prior = copy.deepcopy(strategy)
    old_version = str(prior.get("version", "01"))

    archive = paths.history_dir() / f"v{int(old_version):04d}.yaml"
    paths.history_dir().mkdir(parents=True, exist_ok=True)
    _dump_yaml(archive, prior)

    updated = copy.deepcopy(strategy)
    _set_nested(updated, variable, new_value)
    updated["version"] = _bump_version(old_version)
    _dump_yaml(paths.strategy_file(), updated)

    hypothesis = {
        **hypothesis,
        "ts": time.time(),
        "from_version": old_version,
        "to_version": updated["version"],
        "variable": variable,
        "old_value": _get_nested(prior, variable),
        "new_value": new_value,
        "archived": str(archive),
    }
    _append_hypothesis(hypothesis)
    return updated


# --------------------------------------------------------------------------- #
# Mode: deterministic fallback
# --------------------------------------------------------------------------- #
# Guardrails for the deterministic rules: the agent may tune itself, but never
# into a degenerate strategy (an RSI entry that fires constantly, or a stop so
# tight every trade is noise-stopped).
ENTRY_THRESHOLD_MIN = 15.0
ENTRY_THRESHOLD_MAX = 45.0
STOP_LOSS_MIN = 0.5
ENTRY_STEP = 2.0
STOP_STEP = 0.2


def trades_for_version(trades: list[dict], version) -> list[dict]:
    """Trades taken under one strategy version: the current experiment's evidence."""
    return [t for t in trades if str(t.get("strategy_version")) == str(version)]


def reflect_fallback() -> None:
    """Deterministic one-variable rules, judged only on the current version's trades.

    Priority (risk first):
      1. drawdown above max         -> tighten stop_loss_pct
      2. losing (return < 0)        -> tighten entry.threshold (be more selective)
      3. 0 <= return < target       -> loosen entry.threshold (take more trades)
      4. otherwise, or at a bound   -> hold (no change, recorded)
    """
    goal = _load_yaml(paths.goal_file())
    strategy = _load_yaml(paths.strategy_file())
    version = strategy.get("version", "01")
    trades = trades_for_version(_read_trades(), version)
    s = score.summary(trades, goal)

    target = float(goal.get("target_return_30d", 0.05))
    max_dd = float(goal.get("max_drawdown", 0.08))
    threshold = float(_get_nested(strategy, "entry.threshold") or 30)
    stop = float(_get_nested(strategy, "stop_loss_pct") or 2.0)

    print(f"[reflect:fallback] v{version} {json.dumps(s)}")

    change = None
    if s["max_drawdown"] > max_dd and stop > STOP_LOSS_MIN:
        new = round(max(STOP_LOSS_MIN, stop - STOP_STEP), 4)
        change = ("stop_loss_pct", stop, new, "drawdown_above_max",
                  f"drawdown {s['max_drawdown']:.4f} > max {max_dd}; "
                  f"tighten stop_loss_pct {stop} -> {new} to cap losses")
    elif s["realised_return"] < 0 and threshold > ENTRY_THRESHOLD_MIN:
        new = max(ENTRY_THRESHOLD_MIN, threshold - ENTRY_STEP)
        change = ("entry.threshold", threshold, new, "losing_tighten_entry",
                  f"realised return {s['realised_return']:.4f} < 0; tighten "
                  f"entry.threshold {threshold} -> {new} to only buy deeper dips")
    elif 0 <= s["realised_return"] < target and threshold < ENTRY_THRESHOLD_MAX:
        new = min(ENTRY_THRESHOLD_MAX, threshold + ENTRY_STEP)
        change = ("entry.threshold", threshold, new, "return_below_target",
                  f"realised return {s['realised_return']:.4f} < target {target}; "
                  f"loosen entry.threshold {threshold} -> {new} to take more trades")

    if change is None:
        _append_hypothesis(
            {
                "ts": time.time(),
                "mode": "fallback",
                "rule": "hold",
                "rationale": "metrics within goal or at a guardrail bound; no variable changed",
                "summary": s,
            }
        )
        print("[reflect:fallback] holding strategy (no change)")
        return

    variable, old, new, rule, rationale = change
    apply_change(
        strategy,
        variable,
        new,
        {
            "mode": "fallback",
            "rule": rule,
            "rationale": rationale,
            "summary": s,
            "predicted_score_direction": "up",
        },
    )
    print(f"[reflect:fallback] {variable} {old} -> {new}")


def reflect_auto() -> None:
    """Run the configured reflection mode (HERMES_REFLECT_MODE).

    auto (default): the Hermes CLI when it is on PATH, else the fallback rules.
    """
    mode = os.environ.get("HERMES_REFLECT_MODE", "auto").lower()
    if mode == "hermes" or (mode == "auto" and shutil.which("hermes")):
        reflect_hermes()
    else:
        reflect_fallback()


# --------------------------------------------------------------------------- #
# Mode: hermes (production)
# --------------------------------------------------------------------------- #
_HERMES_PROMPT = """\
You are the reflection brain of a self-improving trading agent.

Goal:
{goal}

Current strategy:
{strategy}

The last {n} closed trades (JSONL):
{trades}

Propose exactly ONE change to a single variable in the strategy. Respond with
ONLY a JSON object, no prose:
{{"variable": "<dotted.path>", "new_value": <value>,
  "rationale": "<one sentence>", "predicted_score_direction": "up|down"}}
"""


def reflect_hermes() -> None:
    if shutil.which("hermes") is None:
        print(
            "[reflect:hermes] `hermes` CLI not found on PATH. Install Hermes, "
            "or use --fallback. No change made."
        )
        return

    goal = _load_yaml(paths.goal_file())
    strategy = _load_yaml(paths.strategy_file())
    trades = _read_trades(limit=25)

    prompt = _HERMES_PROMPT.format(
        goal=yaml.safe_dump(goal, sort_keys=False),
        strategy=yaml.safe_dump(strategy, sort_keys=False),
        n=len(trades),
        trades="\n".join(json.dumps(t) for t in trades) or "(none yet)",
    )

    try:
        proc = subprocess.run(
            ["hermes", "--prompt", prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        print(f"[reflect:hermes] subprocess error: {exc}. No change made.")
        return

    out = (proc.stdout or "").strip()
    hypothesis = _extract_json(out)
    if not hypothesis or "variable" not in hypothesis or "new_value" not in hypothesis:
        print(f"[reflect:hermes] could not parse a hypothesis from output:\n{out}")
        return

    apply_change(
        strategy,
        hypothesis["variable"],
        hypothesis["new_value"],
        {
            "mode": "hermes",
            "rationale": hypothesis.get("rationale", ""),
            "predicted_score_direction": hypothesis.get("predicted_score_direction"),
        },
    )
    print(
        f"[reflect:hermes] {hypothesis['variable']} -> {hypothesis['new_value']} "
        f"({hypothesis.get('rationale', '')})"
    )


def _extract_json(text: str) -> dict | None:
    """Pull the first {...} JSON object out of arbitrary CLI output."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        return None
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="hermes-trading.reflect", description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fallback", action="store_true", help="deterministic rules")
    group.add_argument("--hermes", action="store_true", help="call the Hermes CLI")
    args = parser.parse_args(argv)

    paths.ensure_layout()
    if args.fallback:
        reflect_fallback()
    else:
        reflect_hermes()


if __name__ == "__main__":
    main()
