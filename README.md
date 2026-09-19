# Hermes Trading — self-improving paper-trading worker

A small, runnable trading agent that:

1. **pulls market data** through pluggable adapters (price, on-chain sentiment, news, macro),
2. **takes paper trades** against a versioned strategy (`state/strategy.yaml`),
3. **scores** every closed trade against a goal (`state/goal.yaml`), and
4. **reflects** on recent outcomes to evolve the strategy **one variable at a time**.

> **Paper mode only.** This build never places real orders. No live-execution
> adapter is shipped; setting the live flags raises instead of risking funds.

## Layout

```
hermes_trading/
  run.py          entrypoint  (python -m hermes_trading.run)
  loop.py         24/7 reliability loop: fetch -> evaluate -> trade -> log
  reflect.py      reflection cycle (--fallback deterministic, --hermes via CLI)
  score.py        score(trades, goal) -> float in [-1, +1]
  indicators.py   pure TA helpers (RSI)
  adapters/       price · onchain · news · macro  (each: async fetch() -> dict)
state/
  goal.yaml       success / failure definition  (edit this for your strategy)
  strategy.yaml   current strategy, starts at v01 and evolves
  trades.jsonl    every closed paper trade
  hypotheses.jsonl  one line per reflection decision
  history/        archived strategy versions (vNNNN.yaml)
```

## Quick start

```bash
uv sync                                   # or: pip install -e .
cp .env.example .env                      # optional; defaults are fine for paper

python -m hermes_trading.run              # start the worker (Ctrl-C to stop)
python -m hermes_trading.run --asset ETH/USDT --tick-seconds 30
```

Force a reflection cycle and watch the strategy version bump:

```bash
python -m hermes_trading.reflect --fallback
cat state/strategy.yaml          # version 01 -> 02, exactly one variable changed
cat state/hypotheses.jsonl       # the reasoning
ls state/history/                # the archived prior version
```

## Configuration

`state/goal.yaml` defines what success and failure mean:

| key                  | meaning                                            |
| -------------------- | -------------------------------------------------- |
| `asset`              | ccxt ticker to trade (e.g. `BTC/USDT`)             |
| `target_return_30d`  | success threshold (fraction, e.g. `0.05` = +5%)    |
| `max_drawdown`       | failure threshold (fraction)                       |
| `min_sharpe`         | quality bar                                        |
| `failure_below`      | score floor — returns under this are punished hard |
| `reflection_every`   | reflect after this many closed trades              |
| `one_variable_only`  | guardrail: change exactly one variable per cycle   |

Secrets and overrides live in `.env` (gitignored). All adapters fall back to
free public endpoints, so API keys are optional.

## Reflection modes

- **`--fallback`** — deterministic. If realised return is below target it loosens
  `entry.threshold`; else if drawdown exceeds the max it tightens `stop_loss_pct`.
  One variable per cycle. Proves the mechanism with no external dependency.
- **`--hermes`** — formats recent trades + the strategy into a prompt, calls the
  `hermes` CLI as a subprocess, parses the returned single-variable hypothesis,
  and applies it. Falls back gracefully if `hermes` is not on `PATH`.

## Tests

```bash
uv run pytest          # or: pytest
```

## Deploying (optional)

A `Dockerfile` is included; it builds with `uv` and runs the worker in paper
mode with state at `/app/state`. Mount a persistent volume at `/app/state` so
trades and strategy history survive restarts. Going live is intentionally **not**
a supported path in this build.
