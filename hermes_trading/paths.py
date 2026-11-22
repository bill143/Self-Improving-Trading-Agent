"""Filesystem layout for state files.

All state lives under a single directory so the worker can be pointed at a
persistent volume (e.g. /app/state on Railway) without touching anything else.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

_SEED_FILES = ("goal.yaml", "strategy.yaml")


def state_dir() -> Path:
    """Resolve the state directory.

    Order of precedence:
      1. HERMES_TRADING_STATE_DIR env var
      2. ./state relative to the repo root (the package's parent)
    """
    env = os.environ.get("HERMES_TRADING_STATE_DIR")
    base = Path(env) if env else Path(__file__).resolve().parent.parent / "state"
    return base


def seed_dir() -> Path | None:
    """Directory holding default goal/strategy files (HERMES_TRADING_SEED_DIR)."""
    env = os.environ.get("HERMES_TRADING_SEED_DIR")
    return Path(env) if env else None


def ensure_layout() -> Path:
    """Create the state directory tree if it does not yet exist.

    When a fresh (empty) persistent volume is mounted over the state dir, the
    default goal/strategy files are copied in from the seed dir. Existing files
    are never overwritten, so evolved strategies survive redeploys.
    """
    base = state_dir()
    (base / "history").mkdir(parents=True, exist_ok=True)
    seed = seed_dir()
    if seed is not None:
        for name in _SEED_FILES:
            src, dst = seed / name, base / name
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)
    for f in ("trades.jsonl", "hypotheses.jsonl"):
        p = base / f
        if not p.exists():
            p.touch()
    return base


def goal_file() -> Path:
    return state_dir() / "goal.yaml"


def strategy_file() -> Path:
    return state_dir() / "strategy.yaml"


def trades_file() -> Path:
    return state_dir() / "trades.jsonl"


def hypotheses_file() -> Path:
    return state_dir() / "hypotheses.jsonl"


def position_file() -> Path:
    return state_dir() / "position.json"


def heartbeat_file() -> Path:
    return state_dir() / "heartbeat.json"


def history_dir() -> Path:
    return state_dir() / "history"
