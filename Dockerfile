FROM python:3.11-slim
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# uv for fast, reproducible installs
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}" \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY hermes_trading ./hermes_trading
RUN uv sync --frozen --no-dev

# Default goal/strategy live in /app/seed; they are copied into the state dir
# on first boot so a fresh persistent volume at /app/state starts populated.
COPY state ./seed

# Paper mode only. Live execution is never imported unless the operator flips
# BOTH flags in .env (HERMES_TRADING_MODE=live AND HERMES_TRADING_I_ACCEPT_RISK=true).
ENV HERMES_TRADING_MODE=paper \
    HERMES_TRADING_STATE_DIR=/app/state \
    HERMES_TRADING_SEED_DIR=/app/seed

CMD ["uv", "run", "--no-sync", "python", "-m", "hermes_trading.run"]
