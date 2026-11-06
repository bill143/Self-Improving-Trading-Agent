---
name: alphainsider-strategy-creator
description: Define, backtest, implement, schedule, resume, and update trading strategies with a persistent project plan, AlphaInsider forward testing, and optional automatic recovery.
---

# AlphaInsider Strategy Creator

Version: 1.1.1

## Updates

1. On first interactive use per conversation, inspect installed versions of this
   repository's `alphainsider` and `alphainsider-strategy-creator` skills, and read
   all pages of [public GitHub releases](https://api.github.com/repos/AlphaInsider/skills/releases?per_page=100)
   without authentication. Compare numerically with the highest published stable
   `vX.Y.Z`; ignore drafts, prereleases, bare tags, and Latest. For older/unknown
   copies, show installed/available versions, label unknowns, and pause:
   **Update all** or **Continue**. Share results/choices across skills; recheck
   on request. Skip unattended runs. Continue quietly on automatic lookup failure
   or no releases; explain explicit-check failures. The hosted API skill is
   maintained by Mintlify and is excluded from this GitHub release check.

2. On **Update all**, use available capabilities to update existing older/unknown
   copies from the selected release, preserving installation scope. Keep current/newer
   copies; install no missing skills. Reload updated instructions when supported
   and resume. If unable to update, report outcomes, link the release, and give
   suitable manual instructions; continue with available versions.

## Start or resume

1. Run the [platform and automation access check](references/workflow-contracts.md#check-platform-and-automation-access)
   before [project setup](references/workflow-contracts.md#start-or-resume-the-project)
   or strategy work.
   - Resume from its `plan.md` before new work; keep generated artifacts outside
     this skill repository.
   - Let user decisions govern strategy automation.
   - Use judgment for questions, guardrails, implementation, and checks.
2. Continue from recorded state.
   - Handle stops and updates whenever requested.
   - Number required sequences; use bullets for other notes, ranked by importance
     at each level.

## Define strategy

1. Research strategy and cadence constraints.
   - Check actual AI scheduling capabilities, data availability, and other
     relevant limits before recommending choices.
   - Explain conflicts, tradeoffs, and feasible alternatives.
   - For AlphaInsider API work, resolve its constraints and relevant API behavior.
     - Read the live [AlphaInsider API skill](https://api.alphainsider.com/skill.md),
       then follow its navigation, prerequisite guides, and exact operation pages.
       Use this source even if an older GitHub API skill is installed.
     - If required API guidance cannot be fetched, pause the dependent API work
       and report the missing source.
     - Verify intended actions' limits and side effects; do not invent rules or
       copy endpoint catalogs.
     - Apply AlphaInsider's [margin and liquidation](https://api.alphainsider.com/resources/trading.md#margin-and-liquidation)
       limits when designing and backtesting leveraged or short strategies.
2. [Ask high-level questions](references/workflow-contracts.md#resolve-the-current-decisions)
   until behavior is clear enough to test and implement.
   - Choose which details require user answers.
   - Use fixed code, scheduled AI judgment, or both; record their roles.
3. [Review the strategy and choose the next phase](references/workflow-contracts.md#choose-the-next-phase).

## Backtest

1. Assess feasibility before asking backtest questions.
   - Check information availability at each historical decision time.
   - Do not prefer `/getStockPriceHistory` as a data source; it may have gaps.
   - Explain material limitations. When faithful testing is unavailable, offer
     the closest useful alternatives (proxy, signal-only test, forward observation)
     and what each can establish.
2. Ask backtest questions; let the user choose a test, revise, or skip testing.
3. Build and run the chosen test.
   - Submit no orders.
   - Identify approximations and future information; do not portray them as
     faithful historical results.
4. Save and present results.
   - Save methodology, assumptions, limitations, results, reproducible outputs,
     reports including failures, and artifact links; summarize them in `plan.md`.
   - Explain results clearly with useful data-derived charts and visuals when
     possible; avoid a fixed chart count.
5. [Review the results and choose the next phase](references/workflow-contracts.md#choose-the-next-phase).

## Implement

1. Configure and verify AlphaInsider API access and other required secrets through
   [credentials](references/credentials.md).
   - Reuse the runtime's supported credential store without additional copies;
     use protected project `.env` only when no suitable storage/access method exists.
   - Complete any required user-action turn before implementation questions.
2. Ask relevant implementation questions.
   - Recommend a new AlphaInsider strategy and offer compatible
     owned strategies, explaining their state and reuse effects.
     - Before creating a new strategy, check available API parameters. Ask about
       options unresolved by prior answers or strategy context, recommending values
       with reasons; wait for answers.
       - Ask about strategy access: public, private, or paid,
         subject to account eligibility; confirm the monthly price if paid.
   - Resolve self-healing and notification preferences.
   - Ask whether to post [timeline updates](references/timeline-posts.md); default off.
3. Build the program command and runbook using
   [run and recover](references/run-and-recover.md).
   - Do not prefer `/getStockPriceHistory` as a data source; it may have gaps.
   - Support agreed code/AI roles, expected outcomes, persistent state, and one
     run at a time; choose the remaining project structure.
4. Verify implementation and establish setup scope.
   - Use meaningful checks and a dry run unable to submit, change, or cancel orders.
   - Clarify setup and ongoing order, repair, and notification authority; honor
     existing consent without a special approval phrase.
5. Create or configure the AlphaInsider strategy, then the selected scheduled task.
   - [Activate during setup](references/workflow-contracts.md#activate-the-schedule).
   - Record identities and outcomes as they occur; reconcile uncertain results
     before retrying resource creation or another external action.
6. Hand off actual strategy/scheduler status, project location, useful results,
   next scheduled run, and any required next action.

## Run and recover

- Follow current `plan.md` and the generated runbook for scheduled or manual runs.
  - The [runtime workflow](references/run-and-recover.md) covers execution,
    evaluation, recovery, and notifications.
