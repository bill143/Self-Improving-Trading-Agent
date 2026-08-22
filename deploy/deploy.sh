#!/usr/bin/env bash
# Deploy the Everlasting Care compliance platform on the hardened Sydney droplet.
# Installs the app, wires systemd services (dashboard + reminder sweep), and puts
# Caddy in front for automatic HTTPS. Run as root AFTER harden.sh.
set -euo pipefail

APP_USER="everlasting"
APP_DIR="/opt/everlasting"
REPO_URL="${REPO_URL:-https://github.com/bill143/Self-Improving-Trading-Agent.git}"
BRANCH="${BRANCH:-claude/ai-agency-agent-team-nis26o}"
DOMAIN="${DOMAIN:-}"   # e.g. compliance.everlastingcare.com.au (for TLS)

echo "[1/6] system deps"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3 python3-venv git curl debian-keyring debian-archive-keyring apt-transport-https

echo "[2/6] app user + code"
id -u "$APP_USER" &>/dev/null || useradd --system --create-home --home "$APP_DIR" "$APP_USER"
if [ -d "$APP_DIR/repo/.git" ]; then
  git -C "$APP_DIR/repo" fetch --all && git -C "$APP_DIR/repo" reset --hard "origin/$BRANCH"
else
  sudo -u "$APP_USER" git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR/repo"
fi
# .env must be uploaded to $APP_DIR/repo/.env (never committed). See DEPLOYMENT.md.
test -f "$APP_DIR/repo/.env" || echo "WARNING: $APP_DIR/repo/.env missing — create it before starting services."

echo "[3/6] python env (uv)"
sudo -u "$APP_USER" bash -lc "cd $APP_DIR/repo && (command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh) && ~/.local/bin/uv sync --extra compliance"

echo "[4/6] state dir (Postgres recommended for prod; SQLite default)"
mkdir -p "$APP_DIR/state" && chown -R "$APP_USER:$APP_USER" "$APP_DIR/state"

echo "[5/6] systemd services"
cp "$APP_DIR/repo/deploy/systemd/"*.service "$APP_DIR/repo/deploy/systemd/"*.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now everlasting-dashboard.service
systemctl enable --now everlasting-reminders.timer
systemctl status everlasting-dashboard.service --no-pager || true

echo "[6/6] TLS via Caddy (optional — needs a domain)"
if [ -n "$DOMAIN" ]; then
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list >/dev/null
  apt-get update -y && apt-get install -y caddy
  sed "s/__DOMAIN__/$DOMAIN/" "$APP_DIR/repo/deploy/Caddyfile" >/etc/caddy/Caddyfile
  systemctl restart caddy
  echo "Dashboard live at https://$DOMAIN"
else
  echo "No DOMAIN set — dashboard on http://<server-ip>:8080 (put behind Caddy/HTTPS before real use)."
fi
