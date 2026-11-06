---
name: alphainsider-api
description: Navigate and use the AlphaInsider REST and WebSocket APIs. Use for authentication, endpoint requests, normalized trading calculations, orders, positions, strategies, bots, market data, accounts, and streams.
---

# AlphaInsider API

Use this skill for AlphaInsider API work, including the API portion of a Strategy Creator project. It supplies instructions and verified calculation examples; it does not ship executable request helpers or grant permission to trade or change an account.

- REST: `https://alphainsider.com/api`
- WebSocket: `wss://alphainsider.com/ws`
- Canonical skill: https://api.alphainsider.com/skill.md

## Navigate a task

1. Open the [API navigation index](https://api.alphainsider.com/resources/agent-skill.md#api-navigation). Choose the task group and exact operation or message. Do not load all endpoint references.
2. Read the prerequisite guide linked by that group, then the exact endpoint or message. For any normalized value, read the relevant [calculation section](https://api.alphainsider.com/resources/trading.md#calculation-map) before displaying or sizing it.
3. Follow the method, field locations, required fields, types, units, limits, and side effects in that focused page. REST pages include their OpenAPI contract; the WebSocket page includes AsyncAPI. Use the full [OpenAPI](https://api.alphainsider.com/openapi.yaml) or [AsyncAPI](https://api.alphainsider.com/asyncapi.yaml) only when the focused export leaves a contract question unresolved.
4. For additional or newly published guidance, search [llms.txt](https://api.alphainsider.com/llms.txt). Use [llms-full.txt](https://api.alphainsider.com/llms-full.txt) only if focused discovery fails. Never guess a page URL, field, accepted session, or operation from its name.
5. If focused prose states a stricter compatible rule than the schema, follow the prose and record the documentation discrepancy. If sources conflict in a way that changes the action, resolve it before making that action. If required guidance cannot be fetched, pause only the dependent API work.

## Construct requests privately

Read [authentication and requests](https://api.alphainsider.com/resources/introduction.md#authentication-and-requests) before the first request.

- Protected REST operations use `Authorization: <api-token>`, without `Bearer`. `GET /verifyToken` uses this header; `/newOrderWebhook` uses `api_token` in its JSON body. WebSocket authentication belongs in the subscribe payload specified by AsyncAPI.
- Let request code read `ALPHAINSIDER_API_KEY` privately from the selected project's environment or configured secret storage. Never inspect, print, request in chat, echo, or inline an existing key; never dump `.env` or the process environment. A separate user-authorized credential-entry workflow may collect and store a new value without echoing it.
- `ALPHAINSIDER_STRATEGY_ID` and `ALPHAINSIDER_BOT_ID` are optional, non-secret defaults. Explicit request IDs win. Apply a default only to the matching field the endpoint accepts; ask when a required ID remains unresolved.
- Keep secrets out of command arguments, URLs, plans, source, logs, exceptions, dry-run output, and returned data. Redact nested credential fields and occurrences of known secret values, including broker keys and webhook tokens. A runtime reading a key privately is different from revealing it to the agent.
- Check HTTP status and the JSON `success` flag. Handle non-JSON/binary responses according to the endpoint. Do not automatically replay a mutation after a timeout or uncertain result; reconcile current state first.
- Use the project's language and tools to implement the exact documented requests. No installed GitHub API skill, helper download, or fixed SDK is required.

## Calculate before displaying or ordering

- Strategy values, position amounts, order amounts/totals, and timeline trades can be normalized. Resolve the correct user's and strategy's `input_multiplier`; never reuse another context's multiplier or silently assume `1`.
- Owners require their multiplier. If missing, refresh their subscription/calculation context before displaying dollars/shares or sizing a user-denominated order. Subscribers may use a saved/calculated multiplier or the explicitly labeled percent fallback described in the guide.
- Multiply normalized values by the multiplier for display; divide user-visible amounts by it for fixed `newOrder` inputs. Use decimal arithmetic, validate inputs, and follow the worked examples for price selection, shorts, cash, performance baselines, and zero denominators.
- Market prices, allocation percentages, webhook signals, and real bot broker values do not receive multiplier conversion. `getMaxOrderSize` quantities/cash capacities and nested strategy positions in bot allocation responses are normalized. Compare normalized capacities with normalized order inputs; multiply them only for display. Follow the guide's fixed-order reserve guidance; use returned multipliers, trade totals/fees, and adjusted bot weights for the calculations AlphaInsider performs.

## Choose an action

- [Fixed orders, allocation targets, and webhooks](https://api.alphainsider.com/resources/trading.md#execution-choice) have different inputs and side effects. Send exactly one of `amount` or `total` for a fixed order. Allocation targets are the complete desired position set; omitted positions close. Allocation and webhook requests cancel existing open strategy orders before submitting new ones.
- `order_dependencies` lists prerequisite order IDs in responses and is an optional `newOrder` input. Use only confirmed same-strategy order IDs; allocation/webhook requests do not accept it. Cancelling a prerequisite releases its dependents. An empty list or disappearance from open orders does not prove a fill; follow [order reconciliation](https://api.alphainsider.com/resources/trading.md#order-requirements-and-lifecycle).
- [Limits](https://api.alphainsider.com/resources/limits.md#operation-specific-limits) apply only to the named operations. The current order limiter is shared by fixed, allocation, and webhook routes; follow the guide rather than inferring independent allowances.
- [Submission and execution](https://api.alphainsider.com/resources/trading.md#sessions-and-availability) are separate: valid orders can be accepted while closed; market updates trigger order processing when exchange status is `open`. An accepted order is not a fill. Preserve Strategy Creator's independently confirmed schedule policy.
- [Bots](https://api.alphainsider.com/resources/bots.md#agent-bot-workflow) execute in broker accounts; AlphaInsider strategies are normalized virtual portfolios. Respect the user's chosen scope.
- [WebSockets](https://api.alphainsider.com/resources/websockets.md#connection-and-recovery) require a complete subscription list, heartbeat handling, safe recovery, and the same normalized-value rules as REST.
