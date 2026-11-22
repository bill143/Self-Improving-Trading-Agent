FROM python:3.11-slim
WORKDIR /app

# uv (pinned) for fast, reproducible installs from uv.lock
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# Optional build secret "ca": extra CA bundle for builds behind a TLS-inspecting
# proxy. Used only during install; never written into the image.
COPY pyproject.toml uv.lock README.md ./
RUN --mount=type=secret,id=ca,required=false \
    if [ -s /run/secrets/ca ]; then export SSL_CERT_FILE=/run/secrets/ca; fi; \
    uv sync --frozen --no-dev --no-install-project

COPY hermes_trading ./hermes_trading
RUN --mount=type=secret,id=ca,required=false \
    if [ -s /run/secrets/ca ]; then export SSL_CERT_FILE=/run/secrets/ca; fi; \
    uv sync --frozen --no-dev

# Default goal/strategy live in /app/seed; they are copied into the state dir
# on first boot so a fresh persistent volume at /app/state starts populated.
COPY state ./seed

# Paper mode only. Live execution is never imported unless the operator flips
# BOTH flags in .env (HERMES_TRADING_MODE=live AND HERMES_TRADING_I_ACCEPT_RISK=true).
ENV HERMES_TRADING_MODE=paper \
    HERMES_TRADING_STATE_DIR=/app/state \
    HERMES_TRADING_SEED_DIR=/app/seed

EXPOSE 8080
CMD ["uv", "run", "--no-sync", "python", "-m", "hermes_trading.run"]
