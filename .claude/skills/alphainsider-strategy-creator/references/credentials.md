# Credentials

## Prepare protected access

- Reuse working credentials through the current runtime's supported storage and
  access mechanism. When a credential is missing or needs replacement, use the
  easiest supported secure entry method, such as a masked secret card or settings
  form. A protected input displayed within chat is appropriate when the value
  stays outside the conversation transcript and model context. Never request the
  value in an ordinary chat message.
  - Keep one authoritative storage location for each credential. Prefer secure,
    persistent storage that future chats and scheduled runs can access.
  - Require root `plan.md`; record storage references and access methods there
    and in the runbook, never secret values. Verify protected access from future
    chats and scheduled runs; a saved secret alone does not prove runtime access.
  - Use supported credential injection or private runtime loading without
    creating additional persistent copies. Do not copy a working stored
    credential into `secrets/.env` or each project's `.env`.
  - Use a protected project `.env` only when no suitable supported credential
    storage and access method is available. Create fallback files only when that
    method is selected.
  - Never inspect or print existing API keys, `.env` values, or the process
    environment. Programs may load required values internally without exposure.
  - Use supported entry and storage without echoing values. Keep secrets out of
    arguments, shell interpolation, logs, plans, task prompts, version control,
    and exports; preserve unrelated credentials.
  - Restrict access to fallback `.env` files and exclude them from version
    control and exports.
  - Public strategy IDs may be shown and recorded in `plan.md`.

## Check existing access

- After implementation is chosen, [verify access](#verify-access-and-continue)
  without opening `.env`.
  - If access works, continue without requesting the key again.
  - For other services, verify access privately through their configured runtime.

## Request missing credentials

1. Choose the supported entry method and persistent storage for each missing
   secret. Give the user the actual entry method, storage location, required
   variable name, and completion signal.
   - Only when `.env` fallback is selected, create missing `.env` and
     `.env.example` files with empty assignments for the required names. Preserve
     existing files without reading them; never copy `.env` into `.env.example`.
2. Follow the [user action rule](workflow-contracts.md#resolve-the-current-decisions).
   For a missing AlphaInsider key, adapt this message to the chosen secure entry
   method. Offer project `.env` only when fallback is needed:

   ```markdown
   👉 **Action — AlphaInsider API key:** Open the [AlphaInsider developer page](https://alphainsider.com/settings/developers),
   select the **AI Agent** preset permissions button, and create an API key.
   Use <selected entry method> to paste it into <selected persistent storage>.
   Tell me when it is saved.
   ```

3. Wait for completion, then verify saved access before continuing.

## Verify access and continue

- Call the API directly with curl or any HTTP client at `https://alphainsider.com/api`.
  Send the raw `ALPHAINSIDER_API_KEY` in the `Authorization` header, with no
  `Bearer` prefix. Follow the hosted [API skill](https://api.alphainsider.com/skill.md)
  and [authentication guide](https://api.alphainsider.com/resources/introduction.md#authentication-and-requests).
- Verify saved access with `GET /verifyToken`, which shows the key's scopes,
  before implementation questions. Report only safe results.
  - Load the key from the runtime's injected environment without printing it or
    putting it in arguments, for example:

    ```bash
    printf 'Authorization: %s\n' "$ALPHAINSIDER_API_KEY" |
      curl -sS -H @- https://alphainsider.com/api/verifyToken
    ```

  - With `.env` fallback, load it in a subshell:
    `(set -a; . <project>/.env; set +a; <command>)`.
- Gotchas:
  - Plural reads such as `/getStrategyValues` and `/getStrategyTimelines` take
    `strategy_id[]`; a plain `strategy_id` returns 400.
  - Absence from `/getOrders` does not prove a fill.
  - Read endpoint pages for required fields before `/newStrategy` or `/updateStrategy`.

- Runtime code must use only required credentials through the recorded injection
  or private loading method, without additional persistent copies, and redact
  diagnostics.
  - Resolve authentication through the supported runtime mechanism without
    exposing secrets.

## Rotate credentials

- For a requested rotation, replace the credential through its authoritative
  store's supported entry method. Refresh or restart the affected runtime as
  required, then verify replacement access from the actual runtime, including
  scheduled runs, before continuing or retiring the previous key.
  - Keep the plan and runbook limited to storage references, access methods, and
    verification status; do not synchronize credential copies.
