---
name: kimi-code
description: Open a new terminal window running the full Claude Code harness on Kimi K3 through OpenRouter, at roughly a third of the cost. Use when the user says "open kimmy", "open kimi", "kimi code", or asks to run Claude Code on Kimi K3 or route a Claude Code session through OpenRouter.
---

# Kimi Code — Run Claude Code on Kimi K3 (via OpenRouter)

Launches a **separate** terminal window running Claude Code with every API call
routed to `moonshotai/kimi-k3` through OpenRouter's Anthropic-compatible
endpoint (`https://openrouter.ai/api` → `/v1/messages`). Translation happens
server-side, so the full harness — tools, skills, file edits, bash — works
unchanged and no local proxy is needed.

**Hard rules — never violate these:**

- **Session-scoped only.** All routing lives in environment variables exported
  inside the launched window by `launch.sh`. Never write `ANTHROPIC_*`
  overrides into `~/.claude/settings.json`, project settings, or the current
  session's environment, and never run `/logout` on the user's main Anthropic
  login to fix routing (that would break their normal sessions).
- **Key hygiene.** The OpenRouter key is entered through a hidden prompt in the
  launched window and stored at `<skill-dir>/.openrouter_key` with mode 600.
  Never ask the user to paste the key into the chat, and never print, echo, or
  log it.

## Steps when triggered ("open kimmy" / "open kimi")

1. Resolve `SKILL_DIR` — the directory containing this SKILL.md — and make the
   launcher executable:

   ```bash
   chmod +x "$SKILL_DIR/launch.sh"
   ```

2. Open a new terminal window running the launcher (quote the path — it may
   contain spaces):

   **macOS:**

   ```bash
   osascript <<EOF
   tell application "Terminal"
       do script "exec bash '$SKILL_DIR/launch.sh'"
       activate
   end tell
   EOF
   ```

   **Windows:** open a new console window running the launcher under Git Bash
   (Claude Code on Windows requires Git for Windows, so `bash` is available):

   ```powershell
   Start-Process bash -ArgumentList "'$SKILL_DIR/launch.sh'"
   ```

   From cmd: `start "Kimi Code" bash "<skill-dir>/launch.sh"`.

   **Linux desktop:** `gnome-terminal -- bash "$SKILL_DIR/launch.sh"` (or
   `x-terminal-emulator -e`, `konsole -e`, whichever exists).

   **Headless / remote container (no GUI):** do not try to launch an
   interactive session; give the user the one-liner
   `bash "<skill-dir>/launch.sh"` to run in a terminal of their own.

3. Tell the user:
   - A new window is opening with Claude Code on `moonshotai/kimi-k3` via
     OpenRouter.
   - **First run only:** it prompts for an OpenRouter API key with hidden
     input (create one at https://openrouter.ai/settings/keys and add a few
     dollars of credit), then saves it locally so they are never asked again.
   - Closing the window ends the Kimi session; their normal Claude sessions
     are untouched.

## Configuration

- **Model:** defaults to `moonshotai/kimi-k3`. One-off override:
  `KIMI_CODE_MODEL=<openrouter-slug> bash launch.sh`. Permanent: edit the
  `MODEL` line in `launch.sh`.
- **Rotate or remove the key:** `rm "<skill-dir>/.openrouter_key"` — the next
  launch re-prompts.
- **If the launched window still talks to Anthropic** (or errors with
  model-not-found), a cached Anthropic login is overriding the env vars in
  that Claude Code version. Relaunch with `KIMI_CODE_ISOLATED=1`, which gives
  the Kimi instance its own private `CLAUDE_CONFIG_DIR` inside the skill
  folder. Trade-off: one-time onboarding in that window, and personal
  `~/.claude` skills won't load in isolated mode. Never fix this with
  `/logout`.

## What `launch.sh` exports (inside the new window only)

| Variable | Value | Why |
|---|---|---|
| `ANTHROPIC_BASE_URL` | `https://openrouter.ai/api` | Claude Code appends `/v1/messages`, hitting OpenRouter's Anthropic-compatible endpoint |
| `ANTHROPIC_AUTH_TOKEN` | the stored OpenRouter key | Sent as `Authorization: Bearer`, which OpenRouter expects |
| `ANTHROPIC_API_KEY` | empty string | Prevents any Anthropic key from being picked up |
| `ANTHROPIC_MODEL`, `ANTHROPIC_SMALL_FAST_MODEL`, `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` | the Kimi slug | Keeps the main loop *and* background/fast-path calls on Kimi, so nothing silently bills at Claude prices |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | `1` | No non-essential calls from the routed session |

## Troubleshooting

- **"API Error: 400 status code (no body)"** in the Kimi window — Claude Code
  hides the provider's error body. Run the diagnostic and read the real
  responses:

  ```bash
  bash "<skill-dir>/launch.sh" --check
  ```

  Common causes, in order of likelihood:
  1. A stray carriage return saved into `.openrouter_key` by a Windows
     console, which malforms the `Authorization` header. The launcher now
     strips whitespace on save and load; if the key was saved by an older
     version, delete `.openrouter_key` and relaunch to re-enter it.
  2. Key invalid, disabled, or out of credits — the `--check` key step shows
     usage and limits; top up at https://openrouter.ai/credits.
  3. If both `--check` steps return HTTP 200, the key is fine and the issue
     is request shape. Relaunch with `MAX_THINKING_TOKENS=0` (disables
     thinking blocks) and/or `KIMI_CODE_DEBUG=1` (sets `ANTHROPIC_LOG=debug`
     for wire logs), e.g. `MAX_THINKING_TOKENS=0 bash launch.sh`.
- **Bad key at launch:** the launcher preflights the stored key against
  OpenRouter and re-prompts automatically if it's rejected.

## Expectations to set

- Roughly ⅓ the cost of Claude on real builds; Kimi is 2–3× slower on heavy
  jobs — best suited to background builds.
- The key is only ever sent to `openrouter.ai`; it never appears in terminal
  scrollback, so the session is screen-recording safe.
