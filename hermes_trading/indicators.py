"""Pure technical-indicator helpers. No I/O, easy to unit-test."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def rsi(closes: Sequence[float], period: int = 14) -> float:
    """Wilder's RSI over a series of closing prices.

    Returns the most recent RSI value in [0, 100]. Returns 50.0 (neutral) when
    there is not enough data to compute a meaningful value.
    """
    arr = np.asarray(closes, dtype=float)
    if arr.size < period + 1:
        return 50.0

    deltas = np.diff(arr)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)

    # Seed with a simple average, then apply Wilder's smoothing.
    avg_gain = gains[:period].mean()
    avg_loss = losses[:period].mean()
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return float(100.0 - (100.0 / (1.0 + rs)))
