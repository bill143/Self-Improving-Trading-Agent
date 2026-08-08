#!/usr/bin/env bash
# Kimi Code launcher — Claude Code on Kimi K3 via OpenRouter's
# Anthropic-compatible endpoint. Routing lives only in this shell's
# environment; ~/.claude/settings.json is never touched.
#
# Usage: launch.sh [--check]
#   --check  prints OpenRouter's real responses for a key check and a
#            minimal chat request — Claude Code hides these behind
#            "API Error: NNN (no body)".
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEY_FILE="$SKILL_DIR/.openrouter_key"
MODEL="${KIMI_CODE_MODEL:-moonshotai/kimi-k3}"
API_BASE="https://openrouter.ai/api"

command -v curl >/dev/null 2>&1 || {
    echo "kimi-code: 'curl' not found on PATH" >&2
    exit 1
}

prompt_key() {
    echo "Kimi Code needs an OpenRouter API key."
    echo "Create one at https://openrouter.ai/settings/keys (add a few dollars of credit)."
    echo "Input is hidden; the key is saved only to:"
    echo "    $KEY_FILE  (chmod 600)"
    read -rsp "OpenRouter API key: " key
    echo
    # Strip all whitespace — Windows consoles can smuggle a \r into read's
    # result, which malforms the Authorization header (bare 400, no body).
    key="$(printf '%s' "$key" | tr -d '[:space:]')"
    [[ -n "$key" ]] || { echo "kimi-code: no key entered, aborting." >&2; exit 1; }
    (umask 177 && printf '%s' "$key" > "$KEY_FILE")
    echo "Saved — you won't be asked again. (rm the file to rotate the key)"
}

[[ -s "$KEY_FILE" ]] || prompt_key
KEY="$(tr -d '[:space:]' < "$KEY_FILE")"

if [[ "${1:-}" == "--check" ]]; then
    echo "== 1/2 key validity: GET $API_BASE/v1/key =="
    curl -sS --max-time 20 -w '\nHTTP %{http_code}\n' \
        -H "Authorization: Bearer $KEY" "$API_BASE/v1/key" || true
    echo
    echo "== 2/2 minimal chat request: POST $API_BASE/v1/messages (model $MODEL) =="
    curl -sS --max-time 60 -w '\nHTTP %{http_code}\n' \
        -H "Authorization: Bearer $KEY" -H 'content-type: application/json' \
        -d "{\"model\":\"$MODEL\",\"max_tokens\":16,\"messages\":[{\"role\":\"user\",\"content\":\"Say ok\"}]}" \
        "$API_BASE/v1/messages" || true
    echo
    echo "Anything other than HTTP 200 above is the real error Claude Code hides."
    exit 0
fi

command -v claude >/dev/null 2>&1 || {
    echo "kimi-code: 'claude' CLI not found on PATH" >&2
    exit 1
}

# Preflight so a bad key fails here with a readable message instead of a
# bodyless 400 inside Claude Code. Network trouble (000) never blocks launch.
status="$(curl -sS --max-time 15 -o /dev/null -w '%{http_code}' \
    -H "Authorization: Bearer $KEY" "$API_BASE/v1/key" 2>/dev/null || echo 000)"
if [[ "$status" == "400" || "$status" == "401" || "$status" == "403" ]]; then
    echo "kimi-code: OpenRouter rejected the stored key (HTTP $status). Enter it again."
    rm -f "$KEY_FILE"
    prompt_key
    KEY="$(tr -d '[:space:]' < "$KEY_FILE")"
fi

export ANTHROPIC_BASE_URL="$API_BASE"
export ANTHROPIC_AUTH_TOKEN="$KEY"
export ANTHROPIC_API_KEY=""
export ANTHROPIC_MODEL="$MODEL"
export ANTHROPIC_SMALL_FAST_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$MODEL"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

# Anthropic-style thinking blocks don't survive translation to every
# provider; disabled by default. KIMI_CODE_THINKING=1 re-enables.
if [[ "${KIMI_CODE_THINKING:-0}" != "1" ]]; then
    export MAX_THINKING_TOKENS=0
fi

if [[ "${KIMI_CODE_DEBUG:-0}" == "1" ]]; then
    export ANTHROPIC_LOG=debug
fi

# Isolated by default: a cached Anthropic login in the shared config dir
# gets mixed into requests by some Claude Code versions, poisoning the auth
# header OpenRouter sees (bare 400s). A private config dir means one-time
# onboarding in this window and no personal ~/.claude skills, but the
# routing can never collide with the normal login. KIMI_CODE_ISOLATED=0
# opts back into the shared config.
if [[ "${KIMI_CODE_ISOLATED:-1}" != "0" ]]; then
    export CLAUDE_CONFIG_DIR="$SKILL_DIR/.claude-kimi"
    mkdir -p "$CLAUDE_CONFIG_DIR"
fi

echo "> Kimi Code: Claude Code -> $MODEL via OpenRouter (this window only — close it to end)"
exec claude
