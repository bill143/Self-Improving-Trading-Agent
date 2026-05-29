from hermes_trading.indicators import rsi


def test_rsi_insufficient_data_is_neutral():
    assert rsi([1, 2, 3]) == 50.0


def test_rsi_all_gains_saturates_high():
    closes = list(range(1, 40))  # strictly increasing
    assert rsi(closes) > 99.0


def test_rsi_all_losses_saturates_low():
    closes = list(range(40, 1, -1))  # strictly decreasing
    assert rsi(closes) < 1.0


def test_rsi_in_range():
    closes = [10, 11, 10.5, 11.2, 10.8, 11.5, 11.1, 11.9, 11.3, 12.0,
              11.6, 12.2, 11.8, 12.4, 12.0, 12.6]
    val = rsi(closes)
    assert 0.0 <= val <= 100.0
