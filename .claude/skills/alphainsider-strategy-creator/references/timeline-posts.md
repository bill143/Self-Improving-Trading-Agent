# Timeline Posts

Optional updates on the strategy's AlphaInsider timeline. Off by default; post
only when the user or calling agent opts in.

## Decide whether to post

- Ask when creating or updating a strategy, or accept the user's or calling
  agent's choice. Record the decision and any style guidance in `plan.md`.

## Post an update

- Send `POST /newPost` (`https://alphainsider.com/api/newPost`) with JSON
  `{"strategy_id": "<strategy-id>", "description": "<text>"}`.
  - Put the raw `ALPHAINSIDER_API_KEY` in the `Authorization` header with no
    `Bearer` prefix. Load it as described in [credentials](credentials.md);
    never expose it.
  - The key's account must own the strategy, and the key needs the `newPost`
    permission; [verifying access](credentials.md#verify-access-and-continue)
    shows its scopes.
  - Use the hosted [newPost](https://api.alphainsider.com/resources/timelines/newpost.md),
    [getStrategyTimelines](https://api.alphainsider.com/resources/timelines/getstrategytimelines.md),
    and [limits](https://api.alphainsider.com/resources/limits.md#operation-specific-limits)
    pages for current fields and behavior.
- AlphaInsider allows 100 successful `/newPost` requests per strategy per day;
  avoid posting loops.
- A posting failure should not affect trading.

## Suggestions

These are light suggestions, not rules. Users and calling agents can override
anything here.

- Post when something meaningful happens, such as trades or strategy changes.
- Keep numbers accurate to what actually happened.
- Check the timeline with `/getStrategyTimelines` and `type[]=post` to avoid
  duplicate posts.
- Wait for orders to leave `/getOrders` before describing positions; leaving the
  open-order list does not prove a fill.
- Plural reads such as `/getStrategyValues` and `/getStrategyTimelines` take
  `strategy_id[]`.
- Default style: write in a "we" voice and do not mention AI or bots.
