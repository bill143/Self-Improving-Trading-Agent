# Strategy Plan

## Current state

- Keep enough high-level and operational context to resume.
  - Never include secret values.
  - Host/runtime/profile, persistent project location/file references, automation
    runner and its workspace/backend binding,
    [access status/evidence](workflow-contracts.md#check-platform-and-automation-access), and outstanding setup.
  - Actual scheduler state, pause reasons, and unresolved actions/incidents.
  - Current work, last completed action, open questions and next-phase
    choices, what is waiting, next step, and last update.
  - Adapt as decisions emerge; keep unanswered items open and link detailed artifacts.

## Define strategy

- Intended behavior and governing decisions.
  - Objective, trading behavior, code/AI roles, schedule, constraints, and
    chosen guardrails.
  - Distinguish agreements from proposals; explain consequential tradeoffs.

## Backtest

- Feasibility, selected approach, or decision to skip.
- Methodology, assumptions, limitations, and findings.
  - Identify strategy decisions evaluated by each test.
  - Link saved results, charts, and reproducible artifacts.

## Implement

- AlphaInsider strategy/settings, visibility, and public ID/link.
- Agreed setup and ongoing authority.
- Program/dry-run commands, expected outcomes, and runbook/artifact locations.
- Each credential's authoritative storage reference and runtime access method
  for future chats and scheduled runs, verification status, and missing access;
  never secret values.
- Scheduler/task identity and selection reason, timing, setup verification, and incomplete work.
- Self-healing decisions and recovery state.
  - Enabled/disabled, relevant user decisions, and what preserving this plan means.
  - Latest incident, repair, verification, and resume action; link diagnostic history.
- Notification decisions and delivery state.
  - Enabled/disabled, selected events, channels, and safe destination references.
  - Delivery status/limitations; keep private destinations and credentials in
    the selected authoritative storage following [credentials](credentials.md).
- Timeline post decision (on/off) and any style guidance; see
  [timeline posts](timeline-posts.md).
