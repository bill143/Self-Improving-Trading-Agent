"""The 24/7 reliability loop.

Every tick the worker:
  1. pulls data via the adapters (per-adapter retries with backoff),
  2. evaluates the strategy in strategy.yaml,
  3. opens or closes a paper position accordingly,
  4. appends any closed trade to state/trades.jsonl,
  5. writes a heartbeat.

After 5 consecutive failed ticks the loop circuit-breaks and exits non-zero so
the supervisor (Railway / Docker) restarts it cleanly rather than spinning.

Paper mode only. The live execution path is intentionally not implemented here;
flipping the env flags raises rather than silently risking real funds.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from pathlib import Path

import yaml
from rich.console import Console

from . import adapters, paths
from .adapters.base import SchemaError, with_retries
from .indicators import rsi

console = Console()

_MAX_CONSECUTIVE_FAILURES = 5


def _load_yaml(path: Path) -> dict:
    with open(path, "r") as fh:
        return yaml.safe_load(fh) or {}


def _append_jsonl(path: Path, obj: dict) -> None:
    with open(path, "a") as fh:
        fh.write(json.dumps(obj) + "\n")


def _read_position() -> dict | None:
    p = paths.position_file()
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _write_position(pos: dict | None) -> None:
    p = paths.position_file()
    if pos is None:
        p.unlink(missing_ok=True)
    else:
        p.write_text(json.dumps(pos))


def _write_heartbeat(**fields) -> None:
    hb = {"ts": time.time(), **fields}
    paths.heartbeat_file().write_text(json.dumps(hb))


def _classify_regime(candles: list[dict]) -> str:
    """Cheap 20-bar rolling-return regime label."""
    closes = [c["close"] for c in candles]
    if len(closes) < 21:
        return "unknown"
    change = (closes[-1] - closes[-21]) / closes[-21]
    if change > 0.01:
        return "bull"
    if change < -0.01:
        return "bear"
    return "chop"


class TradingWorker:
    def __init__(self, asset: str | None = None, tick_seconds: int | None = None):
        self.goal = _load_yaml(paths.goal_file())
        self.asset = asset or self.goal.get("asset", "BTC/USDT")
        self.tick_seconds = tick_seconds or int(
            os.environ.get("HERMES_TRADING_TICK_SECONDS", "60")
        )
        self.mode = os.environ.get("HERMES_TRADING_MODE", "paper").lower()
        self._consecutive_failures = 0

    def _assert_paper(self) -> None:
        accepted = os.environ.get("HERMES_TRADING_I_ACCEPT_RISK", "false").lower() == "true"
        if self.mode == "live" and accepted:
            raise NotImplementedError(
                "Live execution is not implemented in this build. This worker "
                "trades on paper only; no live order adapter is shipped."
            )
        if self.mode != "paper":
            console.print(
                f"[yellow]Unknown mode '{self.mode}', forcing paper.[/yellow]"
            )
            self.mode = "paper"

    async def _gather_data(self) -> dict:
        """Fetch every adapter with retries. Schema errors are fatal."""
        price = await with_retries(lambda: adapters.price.fetch(self.asset))
        data = {"price": price}
        # Auxiliary context: tolerate transient failure, never trade-blocking,
        # but a schema mismatch still halts (it signals an upstream break).
        for name in ("onchain", "news", "macro"):
            mod = adapters.ALL[name]
            try:
                data[name] = await with_retries(mod.fetch)
            except SchemaError:
                raise
            except Exception as exc:  # noqa: BLE001
                console.print(f"[dim]{name} adapter unavailable: {exc}[/dim]")
                data[name] = None
        return data

    def _evaluate(self, strategy: dict, data: dict) -> None:
        candles = data["price"]["candles"]
        closes = [c["close"] for c in candles]
        last = closes[-1]
        now = time.time()
        cur_rsi = rsi(closes)
        regime = _classify_regime(candles)

        entry = strategy.get("entry", {})
        exit_cfg = strategy.get("exit", {})
        threshold = float(entry.get("threshold", 30))
        direction = entry.get("direction", "long")
        stop_loss_pct = float(strategy.get("stop_loss_pct", 2.0))
        tp_rsi = float(exit_cfg.get("rsi_take_profit", 70))
        max_hold_min = float(exit_cfg.get("max_hold_minutes", 240))

        position = _read_position()

        if position is None:
            # Entry: long when RSI dips below threshold (oversold).
            if direction == "long" and cur_rsi < threshold:
                position = {
                    "id": uuid.uuid4().hex[:12],
                    "asset": self.asset,
                    "side": "long",
                    "entry_price": last,
                    "entry_time": now,
                    "entry_rsi": cur_rsi,
                    "stop_price": last * (1 - stop_loss_pct / 100.0),
                    "strategy_version": strategy.get("version"),
                    "regime": regime,
                }
                _write_position(position)
                console.print(
                    f"[green]OPEN long[/green] {self.asset} @ {last:.2f} "
                    f"(RSI {cur_rsi:.1f} < {threshold})"
                )
            return

        # Manage the open position: stop-loss, take-profit, or max hold.
        reason = None
        if last <= position["stop_price"]:
            reason = "stop_loss"
        elif cur_rsi >= tp_rsi:
            reason = "take_profit"
        elif (now - position["entry_time"]) >= max_hold_min * 60:
            reason = "max_hold"

        if reason is None:
            return

        ret = (last - position["entry_price"]) / position["entry_price"]
        if position["side"] == "short":
            ret = -ret

        trade = {
            **position,
            "exit_price": last,
            "exit_time": now,
            "exit_rsi": cur_rsi,
            "return_pct": ret,
            "exit_reason": reason,
            "mode": self.mode,
        }
        _append_jsonl(paths.trades_file(), trade)
        _write_position(None)
        color = "green" if ret >= 0 else "red"
        console.print(
            f"[{color}]CLOSE {position['side']}[/{color}] {self.asset} @ {last:.2f} "
            f"({reason}, return {ret*100:+.2f}%)"
        )

    async def tick(self) -> None:
        strategy = _load_yaml(paths.strategy_file())
        data = await self._gather_data()
        self._evaluate(strategy, data)
        _write_heartbeat(
            asset=self.asset,
            mode=self.mode,
            strategy_version=strategy.get("version"),
            last_price=data["price"]["last"],
            open_position=_read_position() is not None,
        )

    async def run(self) -> None:
        paths.ensure_layout()
        self._assert_paper()
        console.print(
            f"[bold]Booting hermes-trading worker[/bold] — {self.asset} "
            f"({self.mode} mode, tick {self.tick_seconds}s)"
        )
        while True:
            try:
                await self.tick()
                self._consecutive_failures = 0
            except SchemaError as exc:
                console.print(f"[bold red]Schema mismatch, halting:[/bold red] {exc}")
                raise
            except Exception as exc:  # noqa: BLE001
                self._consecutive_failures += 1
                console.print(
                    f"[red]tick failed "
                    f"({self._consecutive_failures}/{_MAX_CONSECUTIVE_FAILURES}):[/red] {exc}"
                )
                if self._consecutive_failures >= _MAX_CONSECUTIVE_FAILURES:
                    console.print("[bold red]Circuit breaker tripped. Exiting.[/bold red]")
                    raise
            await asyncio.sleep(self.tick_seconds)


async def run_worker(asset: str | None = None, tick_seconds: int | None = None) -> None:
    await TradingWorker(asset=asset, tick_seconds=tick_seconds).run()
