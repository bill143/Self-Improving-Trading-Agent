"""Entrypoint: load the goal, then start the reliability loop.

    python -m hermes_trading.run [--asset BTC/USDT] [--tick-seconds 60]

--asset overrides the asset in state/goal.yaml.
"""

from __future__ import annotations

import argparse
import asyncio

from . import loop, paths


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="hermes-trading", description=__doc__)
    parser.add_argument(
        "--asset",
        default=None,
        help="ccxt ticker to trade (overrides goal.yaml, e.g. BTC/USDT)",
    )
    parser.add_argument(
        "--tick-seconds",
        type=int,
        default=None,
        help="loop cadence in seconds (overrides HERMES_TRADING_TICK_SECONDS)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    paths.ensure_layout()
    try:
        asyncio.run(loop.run_worker(asset=args.asset, tick_seconds=args.tick_seconds))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
