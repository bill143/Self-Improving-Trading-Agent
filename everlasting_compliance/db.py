"""SQLite persistence with an immutable audit log and retention enforcement.

SQLite now, Postgres-shaped later (parameterised SQL, no SQLite-only features in the
domain layer). Every mutation writes an append-only audit_log row — auditors require
evidence of *who did what when*, and nothing may be silently deleted before its
retention period elapses.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS obligation_instances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_key TEXT NOT NULL,
    subject_type TEXT NOT NULL,      -- organisation | participant | worker | claim | incident
    subject_id TEXT,
    due_at TEXT NOT NULL,            -- ISO8601
    status TEXT NOT NULL DEFAULT 'upcoming',
    evidence_id INTEGER,
    submitted_at TEXT,
    closed_at TEXT,
    created_at TEXT NOT NULL,
    notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_oblig_due ON obligation_instances(due_at);
CREATE INDEX IF NOT EXISTS idx_oblig_status ON obligation_instances(status);

CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,             -- participant | worker | policy | incident | claim | register_entry ...
    ref TEXT,                       -- external/business id
    data TEXT NOT NULL,             -- JSON payload
    retention_class TEXT NOT NULL DEFAULT 'default',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    retain_until TEXT               -- ISO date; nothing purged before this
);
CREATE INDEX IF NOT EXISTS idx_records_kind ON records(kind);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT,
    detail TEXT
);
"""


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class DB:
    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path else config.state_dir() / "compliance.db"
        self._conn = sqlite3.connect(self.path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    @contextmanager
    def _tx(self):
        try:
            yield self._conn
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise

    def close(self) -> None:
        self._conn.close()

    # --- audit log (append-only) ---
    def audit(self, actor: str, action: str, target: str = "", detail: str = "") -> None:
        with self._tx() as c:
            c.execute(
                "INSERT INTO audit_log(ts, actor, action, target, detail) VALUES (?,?,?,?,?)",
                (_now_iso(), actor, action, target, detail),
            )

    def audit_trail(self, limit: int = 100) -> list[dict]:
        rows = self._conn.execute(
            "SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    # --- records ---
    def add_record(self, kind: str, data: dict, *, ref: str = "",
                   retention_class: str = "default", actor: str = "system") -> int:
        years = config.RETENTION_YEARS.get(retention_class, config.RETENTION_YEARS["default"])
        retain_until = date.today().replace(year=date.today().year + years).isoformat()
        now = _now_iso()
        with self._tx() as c:
            cur = c.execute(
                "INSERT INTO records(kind, ref, data, retention_class, created_at, updated_at, retain_until)"
                " VALUES (?,?,?,?,?,?,?)",
                (kind, ref, json.dumps(data), retention_class, now, now, retain_until),
            )
            rid = cur.lastrowid
        self.audit(actor, f"create:{kind}", str(rid), ref)
        return rid

    def get_record(self, record_id: int) -> dict | None:
        row = self._conn.execute("SELECT * FROM records WHERE id=?", (record_id,)).fetchone()
        if not row:
            return None
        d = dict(row)
        d["data"] = json.loads(d["data"])
        return d

    def list_records(self, kind: str) -> list[dict]:
        rows = self._conn.execute(
            "SELECT * FROM records WHERE kind=? ORDER BY id", (kind,)
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["data"] = json.loads(d["data"])
            out.append(d)
        return out

    def purge_expired(self, actor: str = "system") -> int:
        """Delete only records whose retention period has fully elapsed."""
        today = date.today().isoformat()
        with self._tx() as c:
            rows = c.execute(
                "SELECT id FROM records WHERE retain_until IS NOT NULL AND retain_until < ?",
                (today,),
            ).fetchall()
            ids = [r["id"] for r in rows]
            for rid in ids:
                c.execute("DELETE FROM records WHERE id=?", (rid,))
        for rid in ids:
            self.audit(actor, "purge:retention_elapsed", str(rid))
        return len(ids)

    # --- obligation instances ---
    def add_obligation(self, rule_key: str, subject_type: str, due_at: str,
                       *, subject_id: str = "", status: str = "upcoming",
                       notes: str = "", actor: str = "system") -> int:
        with self._tx() as c:
            cur = c.execute(
                "INSERT INTO obligation_instances"
                "(rule_key, subject_type, subject_id, due_at, status, created_at, notes)"
                " VALUES (?,?,?,?,?,?,?)",
                (rule_key, subject_type, subject_id, due_at, status, _now_iso(), notes),
            )
            oid = cur.lastrowid
        self.audit(actor, "obligation:create", str(oid), rule_key)
        return oid

    def set_obligation_status(self, obligation_id: int, status: str, actor: str = "system") -> None:
        stamp = _now_iso()
        col = {"submitted": "submitted_at", "closed": "closed_at"}.get(status)
        with self._tx() as c:
            if col:
                c.execute(
                    f"UPDATE obligation_instances SET status=?, {col}=? WHERE id=?",
                    (status, stamp, obligation_id),
                )
            else:
                c.execute(
                    "UPDATE obligation_instances SET status=? WHERE id=?",
                    (status, obligation_id),
                )
        self.audit(actor, f"obligation:{status}", str(obligation_id))

    def open_obligations(self) -> list[dict]:
        rows = self._conn.execute(
            "SELECT * FROM obligation_instances WHERE status NOT IN ('submitted','closed')"
            " ORDER BY due_at"
        ).fetchall()
        return [dict(r) for r in rows]

    def all_obligations(self) -> list[dict]:
        rows = self._conn.execute(
            "SELECT * FROM obligation_instances ORDER BY due_at"
        ).fetchall()
        return [dict(r) for r in rows]
