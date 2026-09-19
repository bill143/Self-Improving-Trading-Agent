from hermes_trading import score

GOAL = {
    "target_return_30d": 0.05,
    "max_drawdown": 0.08,
    "min_sharpe": 1.2,
    "failure_below": -0.04,
}


def _trades(returns):
    return [{"return_pct": r} for r in returns]


def test_empty_trades_score_zero():
    assert score.score([], GOAL) == 0.0


def test_score_bounded():
    s = score.score(_trades([0.5, 0.5, 0.5]), GOAL)
    assert -1.0 <= s <= 1.0


def test_failure_floor_is_steeply_negative():
    s = score.score(_trades([-0.10, -0.05]), GOAL)
    assert s < -0.5


def test_positive_returns_score_positive():
    s = score.score(_trades([0.02, 0.02, 0.02]), GOAL)
    assert s > 0.0


def test_drawdown_math():
    dd = score.max_drawdown([0.1, -0.2, 0.05])
    assert 0.0 < dd < 1.0


def test_cumulative_return_compounds():
    cr = score.cumulative_return([0.1, 0.1])
    assert abs(cr - 0.21) < 1e-9
