import base64
import json
import threading
import time
import urllib.error
import urllib.request

import pytest

from hermes_trading import dashboard


@pytest.fixture()
def server(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_TRADING_STATE_DIR", str(tmp_path))
    monkeypatch.setenv("DASHBOARD_PASSWORD", "s3cret")
    (tmp_path / "goal.yaml").write_text("target_return_30d: 0.05\nmax_drawdown: 0.08\n")
    (tmp_path / "strategy.yaml").write_text('version: "03"\nentry:\n  threshold: 34\n')
    (tmp_path / "trades.jsonl").write_text(json.dumps({"return_pct": 0.01}) + "\nnot-json\n")
    (tmp_path / "hypotheses.jsonl").write_text("")
    (tmp_path / "heartbeat.json").write_text(
        json.dumps({"ts": time.time(), "tick_seconds": 60, "last_price": 100.0})
    )
    srv = dashboard.make_server("127.0.0.1", 0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}", tmp_path
    srv.shutdown()


def _get(url, auth=None):
    req = urllib.request.Request(url)
    if auth:
        req.add_header("Authorization", "Basic " + base64.b64encode(auth.encode()).decode())
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def test_requires_password(server):
    base, _ = server
    assert _get(base + "/")[0] == 401
    assert _get(base + "/api/status", "bill:wrong")[0] == 401


def test_status_and_page_with_password(server):
    base, _ = server
    code, body = _get(base + "/api/status", "bill:s3cret")
    data = json.loads(body)
    assert code == 200
    assert data["healthy"] is True
    assert data["strategy"]["version"] == "03"
    assert data["summary"]["n_trades"] == 1  # malformed line skipped
    code, page = _get(base + "/", "bill:s3cret")
    assert code == 200 and b"Hermes Trading" in page


def test_healthz_is_public_and_tracks_staleness(server):
    base, state = server
    assert _get(base + "/healthz") == (200, b"ok")
    (state / "heartbeat.json").write_text(json.dumps({"ts": time.time() - 3600, "tick_seconds": 60}))
    assert _get(base + "/healthz")[0] == 503


def test_is_healthy_without_heartbeat():
    assert dashboard.is_healthy(None) is False
