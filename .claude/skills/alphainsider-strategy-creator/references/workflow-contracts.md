# Workflow Contracts

## Check platform and automation access

1. Before creating files or starting strategy work, select persistent storage
   and native AI scheduling for the host runtime, independently of model
   provider or browser/desktop interface.
   - Native includes agent `cron`. Use OS cron/external schedulers only
     if native scheduling is unsupported or the user explicitly requests them.
     Missing tools warrant checking other host interfaces.
   - Web products with Projects must use them; reuse attached/user-confirmed
     Projects. Verify availability for the current account.

   | Runtime | Workspace and scheduler |
   | --- | --- |
   | ChatGPT cloud chat | Project + [Scheduled](https://learn.chatgpt.com/docs/automations?surface=web); saved files/connectors, temporary execution folders. |
   | Grok web | [Project](https://grok.com/project) + [Automation](https://grok.com/automations); verify scheduled project file access. |
   | Claude cloud chat | Project + [Cowork schedule](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork); writable account files/connectors. |
   | Claude Code cloud | [Claude Code Projects](https://code.claude.com/docs/en/claude-projects) + Library files + project memory + [project Routines](https://code.claude.com/docs/en/claude-projects#how-projects-relate-to-other-claude-code-features). |
   | OpenClaw | [Automations](https://docs.openclaw.ai/automation/cron-jobs) + owning agent's [workspace](https://docs.openclaw.ai/concepts/agent-workspace); keep Gateway running; verify scheduled [sandbox write access](https://docs.openclaw.ai/gateway/sandboxing#workspace-access). |
   | Hermes Agent | [`cronjob`](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) with absolute `workdir`; keep its profile's gateway running and [backend storage](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools#terminal-backends) persistent. |
   | Local CLI, IDE, desktop | Durable folder + native AI task ([OpenAI](https://learn.chatgpt.com/docs/automations?surface=app), [Claude Code](https://code.claude.com/docs/en/desktop-scheduled-tasks)); local execution needs host/app running. [Grok Build loops](https://docs.x.ai/build/features/background-tasks) are temporary. |
   | Hosted agents | Native tasks/routines; persist repository/state beyond disposable checkouts. [Codex cloud](https://learn.chatgpt.com/docs/environments/cloud-environment), [Claude Routines](https://code.claude.com/docs/en/routines), [Grok Bot `/workspace`](https://docs.x.ai/grok-bot/computer-and-apps). |

2. Verify plan/code/state and saved results survive the current chat and remain
   readable/writable from later chats and fresh scheduled runs. Verify scheduled
   runs can execute with protected credentials through the recorded storage
   references and access methods, and control pause/resume.
   Check actual storage and workspace bindings/permissions against official guidance.
   Cloud Projects may use durable writable storage without a permanent local folder 
   or trial schedule.
3. If persistence or any required access is unavailable or unverified, stop and
   resolve access on the current platform using the
   [user action rule](#resolve-the-current-decisions). Recheck before work;
   migration requires user choice.

## Start or resume the project

1. After the access check passes, resolve a dedicated persistent project available
   to later chats and scheduled runs.
   - Honor selected locations; resume clear matches and ask when ambiguous.
   - Keep authoritative files, user plans, and secrets outside the skill
     repository and temporary chat storage.
2. Read or initialize root `plan.md` using the [plan template](plan-template.md).
   - Keep high-level strategy, backtest, implementation, self-healing,
     notification, and planning decisions authoritative here.
   - Follow [protected credential storage](credentials.md#prepare-protected-access)
     for all setup secrets. Reuse each credential's authoritative store without
     additional project copies. Record only storage references and runtime
     access methods; exclude secret values from plans and reports.
   - Adapt the outline; it is neither a fixed schema nor a transcript.

- Maintain the resume point as answers, findings, actions, or failures change.
  - Record the current step, open decisions, last outcome, next action, resource
    identities, and actual scheduler state.
  - Save external action intentions before execution and results afterward for
    interrupted chats to reconcile.
  - Keep decisions and useful summaries in the plan; link code, detailed
    procedures, reports, and run history.

## Resolve the current decisions

1. Research facts with tools and documentation; identify user choices.
   - Honor existing answers and authority; revisit only changed or unclear
     material decisions. Choose routine technical details.
2. Request required user actions in a separate response and end the turn.
   - Include no interview questions, even independent ones or questions through tools.
   - Give instructions, alternatives, and a completion signal.
   - Record the waiting point in an existing accessible `plan.md`; if no usable
     project exists, provide a non-secret handoff in chat without creating files.
     Resume questions after completion and successful verification.
   - Use these markers:
     - `👉 **Action — Short title:**` required action and completion signal.
     - `↪️ **Alternative:**` another supported method.
     - `➡️ **Next:**` what happens next.
3. Ask the current round together, with prerequisites settled.
   - Skip settled questions; let answers determine the next round.
   - Give options on consecutive lines and a recommendation per question:

     ```markdown
     ❓ **Q1** - **Short title:** A question in plain language.

     A. First option
     B. Second option

     ➡️ **Recommended:** A — a short reason.

     ---

     ❓ **Q2** - **Short title:** The next independent question.

     A. First option
     B. Second option

     ➡️ **Recommended:** B — a short reason.
     ```

   - `Recommended all` accepts recommendations in the current round.
4. Summarize settled decisions at transitions and explain the next step.
   - Keep questions, results, and notifications understandable; include technical
     details only when useful to decisions.

## Choose the next phase

1. In a separate response, summarize the completed phase and ask one next-step question.
   - After strategy definition: summarize agreed behavior; offer Backtest Strategy,
     Skip Backtesting and Implement Strategy, Revise Strategy, or Save and Stop.
   - After backtesting: summarize results and limitations; offer Implement Strategy,
     Further/Corrected Backtesting, Revise and Retest, or Save and Stop.
   - Use `❓ **Next step:** What would you like to do?`, lettered options, and
     `➡️ **Recommended:**` with a reason.
   - Recommend useful backtesting; base post-test recommendations on evidence.
2. End the turn and wait for the choice; include no other questions or user actions.
3. Record the choice in `plan.md`, then enter that phase.
   - Choosing forward confirms the summary; require no separate agreement prompt.

## Prepare the implementation handoff

1. Generate a project runbook with the project location, file access methods,
   protected credential access methods, commands, expected outcomes, scheduler
   controls, and recovery/notification procedures.
   - Support fresh scheduled agents without chat history or this skill.
   - Refer to `plan.md` for decisions instead of duplicating them.
2. Link the runbook from `plan.md` and the scheduled task.

## Activate the schedule

1. Recheck [platform and automation access](#check-platform-and-automation-access)
   for the actual project and task; verify pause/resume support.
   - Leave inactive only for an explicit user pause or concrete setup failure;
     preserve user/error pauses and explain the blocker.
2. Enable new schedules automatically for the next scheduled run during agreed setup.
   - Require no separate activation confirmation.
   - If creation returns a paused task, enable it during the same setup.
3. Clear only setup-created execution blocks and verify the task is active.
4. Record task identity and next run in `plan.md`.

## Stop, update, or resume at any point

1. Establish the user's intent and save the exact handoff.
   - Record whether automation is still running; clarify an ambiguous stop
     request when existing automation would be affected.
2. For changes to running behavior, pause automation and coordinate with the
   run lock before changing files in use.
3. Apply the affected changes.
   - Preserve settled decisions and artifacts; revisit only affected questions.
   - Identify backtest results that no longer describe the current strategy.
4. Resume only when user intent and verified project state permit it.
