#!/usr/bin/env bash
# Kimi Code launcher — Claude Code on Kimi K3 via OpenRouter's
# Anthropic-compatible endpoint. Routing lives only in this shell's
# environment; ~/.claude/settings.json is never touched.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEY_FILE="$SKILL_DIR/.openrouter_key"
MODEL="${KIMI_CODE_MODEL:-moonshotai/kimi-k3}"

command -v claude >/dev/null 2>&1 || {
    echo "kimi-code: 'claude' CLI not found on PATH" >&2
    exit 1
}

if [[ ! -s "$KEY_FILE" ]]; then
    echo "First run — Kimi Code needs an OpenRouter API key."
    echo "Create one at https://openrouter.ai/settings/keys (add a few dollars of credit)."
    echo "Input is hidden; the key is saved only to:"
    echo "    $KEY_FILE  (chmod 600)"
    read -rsp "OpenRouter API key: " key
    echo
    [[ -n "$key" ]] || { echo "kimi-code: no key entered, aborting." >&2; exit 1; }
    (umask 177 && printf '%s' "$key" > "$KEY_FILE")
    echo "Saved — you won't be asked again. (rm the file to rotate the key)"
fi

export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$(<"$KEY_FILE")"
export ANTHROPIC_API_KEY=""
export ANTHROPIC_MODEL="$MODEL"
export ANTHROPIC_SMALL_FAST_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$MODEL"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

# Some Claude Code versions let a cached Anthropic login override env routing.
# KIMI_CODE_ISOLATED=1 sidesteps that with a private config dir (one-time
# onboarding there; personal ~/.claude skills won't load in that mode).
if [[ "${KIMI_CODE_ISOLATED:-0}" == "1" ]]; then
    export CLAUDE_CONFIG_DIR="$SKILL_DIR/.claude-kimi"
    mkdir -p "$CLAUDE_CONFIG_DIR"
fi

echo "> Kimi Code: Claude Code -> $MODEL via OpenRouter (this window only — close it to end)"
exec claude
