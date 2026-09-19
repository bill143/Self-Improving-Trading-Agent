# Pillar 3 — Activation Readiness & Dry-Run QA
**Agent:** lead-nurture-agent · **Op:** Operations step 5c · **Result: NO-OP (blocked upstream), 2 defects found and fixed**

## 1. Why step 5c did not execute

| Check | Value |
|---|---|
| Clients in SPEED_TO_LEAD | **0** |
| Clients in any stage | **0** |
| Leads BOOKED / CLOSED | **0 / 0** |
| Leads CONTACTED / NEW | 29 / 3 |

Step 5c iterates over clients in SPEED_TO_LEAD. That set is empty, and it is empty because **no sale has closed** — the pipeline has not produced a first client. Pillar 3 is a fulfillment pillar; it has no independent trigger. There is nothing to attach, no client forms to instrument, and no consumer leads pending.

**No client was fabricated and no messages were sent.** Two specific refusals, recorded so they are not quietly retried later:

- **No synthetic close.** Creating a client requires `close_sale`, which writes cash-collected into agency revenue. A fake close to satisfy a fulfillment gate corrupts the single metric the blueprint is measured on.
- **No simulated sends.** The outbox is live (37 pending) and flushes on credential configuration. Texting invented numbers on behalf of a non-existent client is unsolicited automated messaging — TCPA statutory exposure $500–$1,500 per message, with no consent record to defend it (§9.3). Simulation was therefore run as offline validation with zero send calls.

## 2. Dry-run QA against the master sequence — 2 defects

Rendered every SMS at both the worked-example and maximum variable lengths.

**DEFECT 1 — Message 2 character count understated (was: 152, actual: 154).**
Recount of "Karen - Bill again at Miller Heating. Did you get the AC sorted? If you're still collecting quotes, mine's free and takes 20 min: go.millerheating.co/bk12" = **154 chars**. Fine at example lengths, but at max variables (`[FIRST]` 8, `[SENDER]` 5, `[BUSINESS]` 16) it renders **~163 — over the 160 limit**, which forces a carrier split. Per §1, a split message arrives out of order and reads instantly as a bot, on the follow-up that carries the highest engagement burden.
**Fix:** trim to "Karen - Bill again at Miller Heating. Get the AC sorted? If you're still collecting quotes, mine's free, 20 min: go.millerheating.co/bk12" (**138**, 25 chars of headroom). Re-verify at swap time per §1.

**DEFECT 2 — Opt-out language missing from 5 of 9 outbound SMS.**
`STOP to end` appears in Message 1 and Message 3 only. It is **absent from Message 2, 4a, 4b, 4c and 5a.** §10.1 commits to honoring STOP instantly and permanently, but honoring an instruction the recipient was never shown is a weaker compliance posture than it looks, and carrier filtering treats long marketing threads without a visible opt-out as a spam signal — which degrades deliverability on the confirmations and reminders that carry the show rate (§11: ≥80%).
**Fix:** add `STOP to end` to **Message 2 and 5a** (marketing touches — now fits inside the trimmed M2 at 149). Leave 4a/4b/4c clean: these are transactional messages to someone who just booked an appointment, they carry a different consent basis, and cluttering a "Dave's 20 min out" text degrades the customer experience for no compliance gain. Confirm this split with client counsel at the §9.3 gate.

**Validated clean:** M1 152 ✓ · M1 emergency 121 ✓ · M3 126 ✓ · 4a 134 ✓ · 4b 126 ✓ · 4c 119 ✓ · 5a 125 ✓ · 5b 151 ✓ · 15-min nudge 76 ✓ · AI-disclosure reply ~140 ✓ · routing logic §8 — no orphan branches, every path terminates in book / close / suppress ✓.

**Pre-existing item, not a new defect:** §7 "How much is this going to cost?" is annotated at 163 chars and already flagged for per-client trim. Confirmed still over. Must be resolved during client wiring, not at send time.

## 3. What unblocks this

Pillar 3 activates when **one** client reaches SPEED_TO_LEAD, which requires: a close (`sales-agent`) → ONBOARDING → REACTIVATION (Pillar 1) → REVIEWS_REFERRALS (Pillar 2) → SPEED_TO_LEAD. The binding constraint is at the top: **29 CONTACTED prospects, 0 booked.**

**Standing note for `ads-agent`:** the §Handoffs block bars ad launch until this pillar is live on a client. With zero clients, that bar holds — no paid traffic should be pointed at a form nobody is answering.

**On first client, the §9.7 owner gate is blocking, all four:** (a) free-quote offer honored, (b) real daily capacity in the calendar, (c) named human reachable 24/7 for emergency escalation, (d) diagnostic pricing confirmed in writing. Plus the §0.1 overnight auto-reply ON/OFF toggle routed past client counsel. No sends until green.

**Status: BUILT, QA-PASSED (2 fixes applied), 0 clients to deploy against.**
