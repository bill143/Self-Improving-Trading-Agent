from hermes_trading import paths


def test_seed_populates_empty_volume_without_overwriting(tmp_path, monkeypatch):
    seed = tmp_path / "seed"
    seed.mkdir()
    (seed / "goal.yaml").write_text("asset: BTC/USDT\n")
    (seed / "strategy.yaml").write_text('version: "01"\n')
    state = tmp_path / "state"
    state.mkdir()
    (state / "strategy.yaml").write_text('version: "07"\n')
    monkeypatch.setenv("HERMES_TRADING_STATE_DIR", str(state))
    monkeypatch.setenv("HERMES_TRADING_SEED_DIR", str(seed))

    paths.ensure_layout()

    assert (state / "goal.yaml").read_text() == "asset: BTC/USDT\n"
    assert (state / "strategy.yaml").read_text() == 'version: "07"\n'
    assert (state / "trades.jsonl").exists()
    assert (state / "history").is_dir()
