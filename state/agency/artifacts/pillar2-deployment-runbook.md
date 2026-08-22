# Pillar 2 — Deployment Runbook & Copy QA (v1.1)
**Agent:** reviews-referrals-agent · **Trigger:** Operations step 5b
**Parent doc:** `pillar2-reviews-referrals-system` (the copy + policy master; unchanged and still authoritative)
**This doc:** the execution layer — preflight gates, corrected variable budgets, the exact tool sequence, and the Day-1 wave plan.

---

## 0. STATUS OF STEP 5b THIS CYCLE — NOT RUN (no eligible clients)

| Check | Value |
|---|---|
| Clients in `REVIEWS_REFERRALS` | **0** |
| Clients total (all stages) | **0** |
| Leads CLOSED | 0 · BOOKED 0 · CONTACTED 29 · NEW 3 |
| Messages sent this step | **0** |
| Clients advanced to `SPEED_TO_LEAD` | **0** |

**Nothing was sent and no client was advanced. That is the correct outcome, not a failure.**

Pillar 2 fulfillment consumes a *real* client's FSM job-completion feed. With no client there are no completed jobs, no consented phone numbers, and no Google Business Profile. Sending anything now would mean inventing recipients; recording response/review counts now would mean inventing KPIs. Both are disqualifying. Held deliberately.

### What actually unblocks step 5b (dependency chain, in order)
1. `sales-agent` closes a lead → client created in `ONBOARDING`.
2. `onboarding` completes → client advances to `REACTIVATION`.
3. `reactivation-agent` gets the Pillar 1 sequence **live and sending** → client advances to `REVIEWS_REFERRALS`.
4. **Then** this runbook executes, start to finish, and the client advances to `SPEED_TO_LEAD`.

Current gap is at step 1: **zero BOOKED leads.** This is an outbound/sales constraint, not a fulfillment constraint. Escalated to `sales-agent` and `client-success-agent` via the metrics log (`clients_in_reviews_referrals=0`). No amount of Pillar 2 work moves this number.

---

## 1. COPY QA PASS — three real defects found and fixed

The master doc states SMS character counts rendered with short sample variables (`FIRST`=Karen, `TECH`=Dave, `SENDER`=Bill, link=24). Every count in the master doc **verified accurate as rendered**. But re-rendering at the *maximum* of each declared variable budget breaks three messages. Fixes below are v1.1 and supersede the master copy for those three lines.

### 1.1 Corrected variable budget table (two budgets were missing entirely)

| Variable | Master doc budget | **v1.1 hard budget** | Note |
|---|---|---|---|
| `[FIRST]` | ≤ 8 | ≤ 8 | unchanged |
| `[TECH]` | ≤ 7 | ≤ 7 | unchanged |
| `[BUSINESS]` | ≤ 16 | ≤ 16 | unchanged |
| any link | ≤ 24 | ≤ 24 **(hard fail, not a guideline)** | branded shortener must be verified on mobile before go-live |
| `[SENDER]` | **MISSING** | **≤ 8** | new — was uncounted |
| `[PRIZE]` | **MISSING** | **≤ 10** | new — was uncounted, and this is the dangerous one |

### 1.2 DEFECT A — RATING REQUEST overflows on the *default* prize · SEVERITY: HIGH

The master doc's §0 names **Option A ("free year on us") as the DEFAULT prize**, but every rendered SMS example uses `"$1,000"` (6 chars). Render the default prize wording instead and the canonical rating request runs **~173 chars** at max variables — it splits into two segments, which the doc explicitly forbids ("anything ≥160 gets rewritten, never split").

- Sample render: 145 chars. Max-variable render with `[PRIZE]`="free year of maintenance" (24): **173. FAIL.**
- **Fix:** `[PRIZE]` in SMS is capped at **10 chars** and is a *short phrase*, not the full prize description. Approved SMS prize strings: `free year` (9) · `$1,000` (6) · `$500 card` (9). The full prize description lives in the email, the landing page and `[RULES_LINK]` — never in the SMS.
- Max-variable render with `free year`: **158. PASS** (tight).

### 1.3 DEFECT B — REFERRAL ASK overflows at max variables · SEVERITY: MEDIUM

- Sample render: 154. Max-variable render (`FIRST`=8, `SENDER`=8): **161. FAIL by 1 char.**
- **v1.1 replacement SMS** (keeps the warm beat, buys 12 chars of headroom):
```
[FIRST], that review made our week. Know a neighbor who needs us? [SHARE_LINK] gets them a free tune-up + you 5 extra entries. -[SENDER]
```
- Sample render: **142.** Max-variable render: **149. PASS.**
- `free tune-up` swaps per trade to match the real `[INTRO_OFFER]`; any swap longer than `free tune-up` (12) must be re-counted before send.

### 1.4 DEFECT C — 1–3 STAR RESPONSE has almost no headroom · SEVERITY: LOW (monitor)

- Sample render: 151. Max-variable render (`SENDER`=8): **155. PASS, 5 chars spare.**
- No rewrite. **But** it only survives if the link is ≤24. A 26-char link puts it at 157 and a 30-char link breaks it. This is the message where a split is most costly — it is the one that goes to an already-unhappy customer.
- **Gate:** link length is verified in preflight (§2, gate 6) and this message is the canary. If the client's shortener can't hit 24, this message gets rewritten before any send.

### 1.5 Verified PASS at max variables (no change)
5-star (rating 5) 145→149 · 4-star 135→142 · 48h reminder 124→132 · referral confirmation ~110→~120 · opt-out confirmation 80 · all Appendix A and B messages ≤ 150.

---

## 2. PREFLIGHT — eight gates, all blocking, zero sends until all green

Inherits the master doc §9.5 four-gate owner sign-off and adds four operational gates. Run this the day a client enters `REVIEWS_REFERRALS`.

| # | Gate | Green means | Owner of the gate |
|---|---|---|---|
| 1 | Pillar 1 live | reactivation sequence is actually sending, not merely built | `reactivation-agent` |
| 2 | Prize is real | owner confirms **in writing** he will honor `[PRIZE]`; option A/B/C chosen | client owner |
| 3 | Intro offer is real | owner confirms **in writing** he will honor `[INTRO_OFFER]` truck-roll cost | client owner |
| 4 | Official rules published | `[RULES_LINK]` live, AMOE included, counsel-reviewed, prize ARV < $5,000 | `client-success-agent` |
| 5 | Human named for callbacks | a real person + `[DIRECT_PHONE]` for the 1-business-hour negative SLA | client owner |
| 6 | Links tested | `[GOOGLE_REVIEW_LINK]` (Place-ID short link) opens the review box **on mobile**; all links ≤ 24 chars | this agent |
| 7 | Suppression list loaded | shared permanent DNC/opt-out list synced from Pillar 1; §8 rules 1–10 encoded as filters | this agent |
| 8 | Sender continuity | `[SENDER]` = the identical named human used in Pillar 1, and ≤ 8 chars | this agent |

**Any red gate = no sends. Log the blocked gate as a metric and escalate; do not partially launch.** A half-wired Pillar 2 texts a furious customer or asks a warranty-callback for a rating — both manufacture the 1-star review we exist to prevent.

---

## 3. EXECUTION SEQUENCE — the exact tool calls, per client

Run in this order. Every step records a metric; the whole run is one auditable trail.

**Day 1 — wire + backfill wave 1**
1. Pull the client's completed-job list (last 30 days) + active-customer report.
2. Apply §8 suppression. `record_metric` → `jobs_eligible_after_suppression`, `jobs_suppressed` (expect 60–80% survival; **outside that band, stop and inspect the filter — do not send**).
3. Sort eligible jobs newest-first (freshest memory converts best).
4. `send_sms` (+ `send_email` counterpart) MESSAGE 1, `on_behalf_of` = client id, **throttled to 25/day**, 8am–8pm recipient local, no Sundays/holidays.
5. `record_metric` → `rating_requests_sent`.

**Days 2–14 — backfill waves 2..N + live feed**
6. Continue 25/day until the 30-day backfill is drained, then switch to rolling live sends at 25–40/day.
7. Inbound replies route per §7:
   - `5` → MESSAGE 2 within 5 min → `record_metric` `positive_responses`
   - `4` → 4-star variant → log the "what would've made it a 5" verbatim as service intelligence
   - `1–3` → MESSAGE 3 within 5 min + **manager alert + `place_call` within 1 business hour** + 90-day review-ask suppression + entry stands → `record_metric` `negative_intercepted`
   - trigger words (leak / no heat / no power / flooded / lawyer / chargeback...) → same-day owner escalation, `place_call` to `[DIRECT_PHONE]`
   - `STOP` → instant permanent suppression, all channels, all clients, one confirmation, push to shared list
8. Monitor Google daily. New 5-star confirmed live → post an Appendix §6 auto-response within 24h, rotation enforced (no template twice in 10 reviews), >70% similarity to last 10 replies = regenerate → `record_metric` `reviews_posted`, `review_replies_posted`.
9. +24h after each posted review → MESSAGE 4 referral ask (**v1.1 copy, §1.3**) → `record_metric` `referral_asks_sent`.
10. Friend books via `[SHARE_LINK]` → hand the lead to `speed-to-lead-agent` **immediately** (60-second SLA; a referral that waits an hour is wasted). On job completion: +5 entries, same-day confirmation SMS → `record_metric` `referral_leads`, `referral_entries_credited`.

**Weekly (Mondays)** — digest to `client-success-agent` per master §9.11: response rate, rating distribution, reviews posted, rating trend, referral revenue, **every intercepted negative verbatim with tech + job number**, and the 4-star service-intelligence themes.

**Live criterion → advance.** A client is *live* on Pillar 2 when: all 8 preflight gates green, backfill wave 1 sent, the 4/5 and 1–3 branches have both fired correctly at least once (verified, not assumed), auto-response rotation is posting, and the referral loop has fired at least one ask. **Then** `advance_client` → `SPEED_TO_LEAD` with a note naming the wave-1 volume and first-week response rate. Pillar 2 keeps running forever after; advancing the stage means the *build* is done, not the service.

---

## 4. METRIC SCHEMA (so every client reports identically)

`jobs_completed` · `jobs_suppressed` · `jobs_eligible_after_suppression` · `rating_requests_sent` · `feedback_responses` · `feedback_response_rate` · `positive_responses` (4–5) · `negative_intercepted` (1–3) · `negative_callback_sla_met` · `reviews_posted` · `review_rating_avg` · `review_replies_posted` · `referral_asks_sent` · `referral_leads` · `referral_entries_credited` · `optout_rate`

Targets and failure signals per master §13. Benchmark at 300 completed jobs/mo: ~88 responses, ~75 positive, ~25 reviews, ~13 intercepted, ~7 referral leads.

---

## 5. CHANGE LOG
- **v1.1** — Added `[SENDER]` and `[PRIZE]` character budgets (both were absent). Fixed rating-request overflow on the default prize (Defect A). Rewrote the referral-ask SMS (Defect B). Flagged the 1–3 star message as the link-length canary (Defect C). Added the 8-gate preflight and the "live" criterion for advancing to `SPEED_TO_LEAD`.

**Status: ARMED.** Zero eligible clients this cycle. Executes end-to-end, same day, on the first client that reaches `REVIEWS_REFERRALS`.
