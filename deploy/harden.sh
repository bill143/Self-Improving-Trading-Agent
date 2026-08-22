#!/usr/bin/env bash
# Sydney VPS hardening for the Everlasting Care compliance server.
# Fail2Ban + UFW + automatic security updates. Run as root on a fresh
# Ubuntu/Debian droplet (Sydney region). Idempotent — safe to re-run.
set -euo pipefail

echo "[1/5] apt update + security tooling"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y fail2ban ufw unattended-upgrades

echo "[2/5] Fail2Ban (SSH brute-force protection)"
cat >/etc/fail2ban/jail.local <<'EOF'
[DEFAULT]
findtime = 10m
maxretry = 3
bantime  = 1h
[sshd]
enabled = true
EOF
systemctl enable --now fail2ban
systemctl restart fail2ban
fail2ban-client status sshd || true

echo "[3/5] UFW firewall — allow SSH + HTTP/HTTPS BEFORE enabling"
ufw allow 22/tcp        # SSH — never lock yourself out
ufw allow 80/tcp        # HTTP (Caddy ACME challenge)
ufw allow 443/tcp       # HTTPS (dashboard)
ufw --force enable
ufw status verbose

echo "[4/5] Automatic security updates"
dpkg-reconfigure -f noninteractive unattended-upgrades || true
systemctl enable --now unattended-upgrades

echo "[5/5] Done. Verify SSH still works from a SECOND terminal before closing this one."
