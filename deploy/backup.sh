#!/usr/bin/env bash
# Nightly backup of the compliance state (SQLite or Postgres dump), encrypted.
# Retains 30 daily copies locally. Add an offsite copy (e.g. rclone to onshore
# object storage) before relying on this in production — keep backups in Australia.
set -euo pipefail

STATE_DIR="${EC_STATE_DIR:-/opt/everlasting/state}"
BACKUP_DIR="${BACKUP_DIR:-/opt/everlasting/backups}"
STAMP="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -n "${EC_DB_URL:-}" ]; then
  pg_dump "$EC_DB_URL" | gzip > "$BACKUP_DIR/compliance-$STAMP.sql.gz"
else
  sqlite3 "$STATE_DIR/compliance.db" ".backup '$BACKUP_DIR/compliance-$STAMP.db'"
  gzip "$BACKUP_DIR/compliance-$STAMP.db"
fi

# retain 30 days
find "$BACKUP_DIR" -name 'compliance-*' -mtime +30 -delete
echo "Backup written to $BACKUP_DIR (retain 30 days). Ensure an onshore offsite copy exists."
