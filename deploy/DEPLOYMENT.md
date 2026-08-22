# Deployment Runbook — Everlasting Care Compliance Platform (Sydney)

The platform is built and tested. This is the sequence to put it live on a Sydney VPS.
Data residency is mandatory: **use a Sydney (AU) region and keep all backups onshore.**

## Prerequisites (the human steps I can't do for you)
1. A VPS in a **Sydney/AU** region (DigitalOcean SYD1, or any AU host). ~$12–24/mo,
   2–4 GB RAM. You get an **IP address** and a **root password/SSH key**.
2. (Recommended) A domain for the dashboard, e.g. `compliance.everlastingcare.com.au`,
   with an A record pointing at the server IP — enables automatic HTTPS.
3. Your filled-in `.env` (Anthropic key already set; add Telegram token, a strong
   `EC_ADMIN_PASSWORD`, and generated `EC_SECRET_KEY`/`EC_ENCRYPTION_KEY`).

## Steps
```bash
# 1. Connect (from your PC)
ssh root@YOUR_SERVER_IP

# 2. Harden the box (Fail2Ban + UFW + auto-updates)
curl -fsSL https://raw.githubusercontent.com/bill143/Self-Improving-Trading-Agent/claude/ai-agency-agent-team-nis26o/deploy/harden.sh | bash
#    ^ or scp the repo up and run deploy/harden.sh

# 3. Deploy the app (clones repo, installs, systemd services, TLS)
export DOMAIN=compliance.everlastingcare.com.au   # omit to skip HTTPS for now
curl -fsSL .../deploy/deploy.sh | bash

# 4. Upload your .env to the server (NEVER commit it)
scp .env root@YOUR_SERVER_IP:/opt/everlasting/repo/.env
systemctl restart everlasting-dashboard

# 5. Backups
crontab -e   # add:  0 2 * * *  EC_STATE_DIR=/opt/everlasting/state /opt/everlasting/repo/deploy/backup.sh
```

## Verify
- `systemctl status everlasting-dashboard` → active (running)
- Visit `https://your-domain/` → login with `EC_ADMIN_USERNAME` / `EC_ADMIN_PASSWORD`
- `systemctl list-timers everlasting-reminders` → next run scheduled
- Telegram bot responds (message it) once `TELEGRAM_BOT_TOKEN` is in `.env`

## Production notes
- Move from SQLite to **Postgres** (set `EC_DB_URL`) before real load.
- Keep the dashboard behind HTTPS (Caddy config included) — never expose `:8080` raw.
- Restrict `EC_ADMIN_*` to named accounts; rotate the Anthropic key (it passed
  through chat during the build).
- All participant data stays onshore; backups too.
