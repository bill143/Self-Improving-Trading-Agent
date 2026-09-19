"""Score closed trades against the goal.

score(trades, goal) -> float in [-1, +1]

The composite blends three components, each normalised to roughly [-1, +1]:
  * realised cumulative return vs target_return_30d
  * max drawdown vs max_drawdown   (lower drawdown scores higher)
  * Sharpe ratio vs min_sharpe

A returns figure below goal["failure_below"] is treated as failure and pulls
the composite steeply negative regardless of the other components.
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence


def _clamp(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def cumulative_return(returns: Sequence[float]) -> float:
    """Compound a series of per-trade fractional returns into one figure."""
    equity = 1.0
    for r in returns:
        equity *= (1.0 + r)
    return equity - 1.0


def max_drawdown(returns: Sequence[float]) -> float:
    """Peak-to-trough drawdown of the equity curve, as a positive fraction."""
    equity = 1.0
    peak = 1.0
    worst = 0.0
    for r in returns:
        equity *= (1.0 + r)
        peak = max(peak, equity)
        dd = (peak - equity) / peak if peak > 0 else 0.0
        worst = max(worst, dd)
    return worst


def sharpe(returns: Sequence[float]) -> float:
    """Per-trade Sharpe (risk-free assumed 0). Returns 0 when undefined."""
    n = len(returns)
    if n < 2:
        return 0.0
    mean = sum(returns) / n
    var = sum((r - mean) ** 2 for r in returns) / (n - 1)
    sd = math.sqrt(var)
    if sd == 0:
        return 0.0
    return mean / sd


def _returns_of(trades: Iterable[dict]) -> list[float]:
    out: list[float] = []
    for t in trades:
        r = t.get("return_pct")
        if r is None:
            continue
        out.append(float(r))
    return out


def score(trades: Iterable[dict], goal: dict) -> float:
    """Composite score in [-1, +1]. Empty input scores 0 (no information)."""
    returns = _returns_of(trades)
    if not returns:
        return 0.0

    target = float(goal.get("target_return_30d", 0.05)) or 0.05
    max_dd = float(goal.get("max_drawdown", 0.08)) or 0.08
    min_s = float(goal.get("min_sharpe", 1.2)) or 1.2
    failure_below = float(goal.get("failure_below", -0.04))

    realised = cumulative_return(returns)
    dd = max_drawdown(returns)
    s = sharpe(returns)

    # Failure floor: steeply negative, dominates everything else.
    if realised < failure_below:
        return _clamp(-1.0 + (realised - failure_below) / abs(failure_below or 1.0))

    return_component = _clamp(realised / target)
    # 1.0 when no drawdown, 0.0 at the limit, negative when exceeded.
    dd_component = _clamp(1.0 - (dd / max_dd))
    sharpe_component = _clamp(s / min_s)

    composite = (
        0.45 * return_component
        + 0.30 * dd_component
        + 0.25 * sharpe_component
    )
    return _clamp(composite)


def summary(trades: Iterable[dict], goal: dict) -> dict:
    """Human-readable breakdown of the score components."""
    returns = _returns_of(trades)
    return {
        "n_trades": len(returns),
        "realised_return": cumulative_return(returns),
        "max_drawdown": max_drawdown(returns),
        "sharpe": sharpe(returns),
        "score": score(trades, goal),
    }
