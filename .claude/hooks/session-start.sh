#!/bin/bash
set -euo pipefail

# Only needed in remote (Claude Code on the web) sessions; local machines
# manage their own tooling.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"

# Project dependencies, including the dev extra (pytest), so tests run
# out of the box with `uv run pytest`.
uv sync --extra dev

# agent-reach: gives the agent read access to external sources (RSS feeds,
# YouTube transcripts). Idempotent — re-running reports "ready" and exits 0.
pip install --quiet agent-reach
agent-reach install rss
agent-reach install youtube

# Regenerate the skill file so the installed channels are discoverable.
mkdir -p ~/.claude/skills/agent-reach
agent-reach skill > ~/.claude/skills/agent-reach/SKILL.md
