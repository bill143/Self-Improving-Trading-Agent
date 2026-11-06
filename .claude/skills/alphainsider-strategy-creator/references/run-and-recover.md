# Run and Recover

## Prepare the runtime workflow

- Generate the executable workflow and runbook using mechanisms appropriate to
  the scheduler and implementation; verify them before activation.
  - Use required credentials through the recorded injection or private loading
    methods without additional persistent copies; verify access from a fresh
    scheduled run.
  - Make dry runs technically unable to submit, change, or cancel orders or
    advance trading state.
  - Distinguish known results from uncertain order outcomes and prevent duplicate
    execution, including sequential duplicate triggers.
  - Choose and test these protections for the actual design.

## Run the strategy

1. Read fresh `plan.md` and the project runbook; respect pauses and unresolved incidents.
2. Acquire shared exclusivity before order work.
   - Cover the command, AI decisions, evaluation, repair, and retries.
   - All scheduled and manual entry points participate; overlapping invocations exit.
3. Run the program command.
   - Follow any recorded role for scheduled AI judgment and pass its decisions
     through program execution controls.
   - Keep program entry points for execution and dry runs.
4. Evaluate expected outcomes from `plan.md` using saved evidence and exit status.
   - A planned no-trade result is success; poor returns alone are not an
     implementation failure.
   - On error, follow recovery below.
5. Record the outcome and apply selected notification settings.
6. Release exclusivity after evaluation and any recovery finish.

## Recover from an error

1. Stop order work, save the incident, and block new executions in project state.
2. Pause the scheduler and verify the pause.
   - If unverified, keep execution blocked and report the required action.
3. Diagnose against the plan and saved evidence.
4. Decide whether to self-heal and repair when eligible.
   - Require self-healing enabled, preservation of the plan's high-level
     decisions, and no human input or new authority.
   - Any implementation issue is eligible; no fixed list limits repairable files
     or components.
   - Update operational notes in `plan.md` without rewriting decisions to justify
     a repair.
   - Otherwise leave paused, record what the user must resolve, and end recovery.
5. Dry-run the fix and run meaningful checks without orders.
   - If checks fail or available execution time runs out, leave a coherent paused
     implementation and save the diagnosis and next action.
6. After checks pass, reconcile uncertain previous actions before allowing orders.
   - Leave paused if an outcome remains unresolved.
7. Choose an immediate rerun with current inputs or the next suitable scheduled run.
   - An immediate retry keeps the scheduler paused and admits only the recovery
     owner through this incident's execution block, under the same exclusivity
     and all other plan/order checks.
   - If the retry fails, keep paused and record the unresolved issue.
8. After recovery succeeds, clear this incident's block and resume the scheduler.
   - Never override a later user pause.
   - Verify and record actual scheduler state.
9. Record the outcome and send the selected incident/recovery notification.
   - Hand off unfinished recovery for any later user chat.
   - Leave paused when self-healing is disabled, needs human input, fails, or the
     agent is interrupted after pausing; preserve diagnosis and next action.
   - Do not rely on the paused scheduler for another attempt or create a separate
     recovery task.

## Send selected notifications

- Use the events, channels, and destinations agreed in `plan.md`.
- Select the exact strategy-run label:
  - `🚨 Error — Action Required`
    - Recovery awaits the user: explain the issue, recommended next step, and
      required information or decision.
  - `🔄 Retrying — No Action Required`
    - An automatic retry is underway or has an active scheduled trigger: explain
      what is being retried and what happens next.
  - `🛠️ Self-Healed — No Action Required`
    - The repair passed verification, safe operation is restored, and no user
      action is needed: explain what was restored, actual scheduler state, and
      next run.
  - `⚠️ Warning — No Action Required`
    - Useful information requiring no user action.
- Send a short, understandable message identifying the strategy, effect,
  automation state, and next step.
  - Keep technical diagnostics in project artifacts and secrets in the selected
    authoritative storage following [credentials](credentials.md).
- Record delivery failures honestly in the plan.
  - Never claim an unavailable channel notified the user.
