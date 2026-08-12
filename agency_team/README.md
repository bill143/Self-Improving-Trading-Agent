# agency_team — the 100% AI-driven agency runner

An autonomous agent team that executes JP Middleton's $5.4M AI-agency blueprint
(see [`docs/ai-agency-blueprint.md`](../docs/ai-agency-blueprint.md)) with no
human in the loop.

## How it works

- **Team members are Markdown files** in [`.claude/agents/`](../.claude/agents/) —
  one per role. Each file encodes the role's mission, its exact position in the
  blueprint's sequence, its operating prompts (adapted from JP's own), KPIs, and
  guardrails. The same files work as Claude Code subagents and as system prompts
  here — edit the MD file and the autonomous runner picks it up next cycle.
- **The orchestrator enforces the sequence.** Foundation phases run once, in
  order, each behind a gate that only passes when the phase's artifact really
  exists in state:
  1. Niche selection → 2. Franchise targeting → 3. Pillar 1 (reactivation) →
  4. Pillar 2 (reviews & referrals) → 5. Pillar 3 (speed-to-lead) →
  6. Ad intelligence → 7. Sales readiness.
  Then the operations loop runs every cycle: scrape → set appointments → close
  (7-step framework) → onboard → fulfill (reactivation → reviews → nurture →
  ads → voice AI) → client success & referrals.
- **State is durable JSON** under `state/agency/` (leads, clients, artifacts,
  metrics, activity log) — inspectable at any time with `status`.
- **External actions never block.** SMS/email/calls/payments/agreements go
  through `connectors.py`. With credentials configured they send (Twilio SMS is
  wired); without, they queue to a durable outbox and the loop keeps moving.

## Run it

```bash
uv sync --extra agency           # installs the anthropic SDK
export ANTHROPIC_API_KEY=...     # or `ant auth login`

python -m agency_team status     # inspect state
python -m agency_team run        # one autonomous cycle
python -m agency_team run --forever   # fully autonomous operation
```

Each cycle either advances the next foundation phase or runs a full operations
pass. Model defaults to `claude-opus-5` (override with `AGENCY_MODEL`).

## Configuration (`.env` / environment)

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | The brain. Required to run agents. |
| `AGENCY_MODEL` | Model override (default `claude-opus-5`). |
| `AGENCY_STATE_DIR` | State location (default `state/agency/`). |
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_FROM_NUMBER` | Live SMS sending. |
| *(planned)* GoHighLevel / Stripe / Dropbox Sign / Synthflow keys | Until wired, those actions queue to the outbox with an `integration` tag. |

## Guardrails baked in

- DNC is permanent; opt-outs are honored at the CRM level.
- Client fulfillment can only move forward through the fixed conveyor belt.
- Every external action is durably logged (sent, queued, or failed).
- Agents are instructed to never fabricate results, reviews, or claims, and to
  answer honestly when asked if they are AI.
