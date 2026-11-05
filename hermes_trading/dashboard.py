"""Read-only web dashboard for the worker.

Serves, from the same process as the trading loop:
  GET /             the dashboard page (polls /api/status)
  GET /api/status   JSON snapshot of heartbeat, position, strategy, trades, changes
  GET /healthz      200 while the loop heartbeat is fresh, else 503 (no auth)

Everything except /healthz sits behind HTTP Basic auth when DASHBOARD_PASSWORD
is set (username: DASHBOARD_USER, default "bill"). The dashboard never writes
state and exposes no controls, so it cannot move the strategy or place trades.
"""

from __future__ import annotations

import base64
import hmac
import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import Path

import yaml

from . import paths, score

_RECENT_TRADES = 50
_RECENT_CHANGES = 20


def _read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def _read_yaml(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text()) or {}
    except (OSError, yaml.YAMLError):
        return {}


def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    try:
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return rows


def heartbeat_age(hb: dict | None, now: float | None = None) -> float | None:
    if not hb or "ts" not in hb:
        return None
    return (now or time.time()) - float(hb["ts"])


def is_healthy(hb: dict | None, now: float | None = None) -> bool:
    """Healthy while the last heartbeat is within three ticks (min 3 minutes)."""
    age = heartbeat_age(hb, now)
    if age is None:
        return False
    limit = max(180.0, 3.0 * float(hb.get("tick_seconds") or 60))
    return age <= limit


def build_status() -> dict:
    goal = _read_yaml(paths.goal_file())
    trades = _read_jsonl(paths.trades_file())
    hb = _read_json(paths.heartbeat_file())
    return {
        "now": time.time(),
        "healthy": is_healthy(hb),
        "heartbeat_age_s": heartbeat_age(hb),
        "heartbeat": hb,
        "position": _read_json(paths.position_file()),
        "strategy": _read_yaml(paths.strategy_file()),
        "goal": goal,
        "summary": score.summary(trades, goal),
        "trades": trades[-_RECENT_TRADES:][::-1],
        "changes": _read_jsonl(paths.hypotheses_file())[-_RECENT_CHANGES:][::-1],
    }


def _page() -> bytes:
    return resources.files("hermes_trading").joinpath("dashboard.html").read_bytes()


class _Handler(BaseHTTPRequestHandler):
    server_version = "hermes-dashboard"
    sys_version = ""

    def log_message(self, fmt: str, *args) -> None:  # keep worker logs clean
        return

    def _send(self, code: int, body: bytes, ctype: str, extra: dict | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _authorized(self) -> bool:
        password = os.environ.get("DASHBOARD_PASSWORD")
        if not password:
            return True
        user = os.environ.get("DASHBOARD_USER", "bill")
        expected = base64.b64encode(f"{user}:{password}".encode()).decode()
        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            return False
        return hmac.compare_digest(header[6:].strip().encode(), expected.encode())

    def do_HEAD(self) -> None:
        self.do_GET()

    def do_GET(self) -> None:
        route = self.path.split("?", 1)[0]
        if route == "/healthz":
            ok = is_healthy(_read_json(paths.heartbeat_file()))
            self._send(200 if ok else 503, b"ok" if ok else b"stale", "text/plain")
            return
        if not self._authorized():
            self._send(
                401, b"authentication required", "text/plain",
                {"WWW-Authenticate": 'Basic realm="Hermes Trading", charset="UTF-8"'},
            )
            return
        if route == "/":
            self._send(200, _page(), "text/html; charset=utf-8")
        elif route == "/api/status":
            body = json.dumps(build_status(), default=str).encode()
            self._send(200, body, "application/json")
        else:
            self._send(404, b"not found", "text/plain")


def make_server(host: str = "0.0.0.0", port: int | None = None) -> ThreadingHTTPServer:
    port = port if port is not None else int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer((host, port), _Handler)
    server.daemon_threads = True
    return server


def start_in_background() -> ThreadingHTTPServer | None:
    """Start the dashboard on a daemon thread unless HERMES_DASHBOARD=off."""
    if os.environ.get("HERMES_DASHBOARD", "on").lower() in {"off", "0", "false"}:
        return None
    server = make_server()
    threading.Thread(target=server.serve_forever, name="dashboard", daemon=True).start()
    return server
