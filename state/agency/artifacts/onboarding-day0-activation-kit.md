# Onboarding — Day-0 Activation Kit (v1)

**Agent:** `onboarding-agent` · **Ops step 4** (CLOSED → REACTIVATION)
**Consumes:** `close_sale` output from `sales-closer-agent`, `pillar1-reactivation-campaign`, `pillar2-reviews-referrals-system`
**Feeds:** `reactivation-agent`, `reviews-referrals-agent`, `client-success-agent`

---

## 0. Cycle 1 status — honest result

| KPI | Target | Actual |
|---|---|---|
| Clients in ONBOARDING | ≥1 | **0** |
| Clients advanced to REACTIVATION | all of them | **0** |
| Close → onboarding complete | <24h | **n/a — no closes exist** |
| Accesses collected | 100% | **n/a** |

`get_state_summary` returns `clients_total: 0` and `clients_by_stage.ONBOARDING: 0`. `list_leads(BOOKED)` and `list_leads(CLOSED)` are both empty. **There is nothing at my station.**

I did not call `close_sale` to create a client to onboard, and I did not call `advance_client` against an invented id. Onboarding is the step where fiction becomes irreversible: `advance_client` to REACTIVATION is the signal that tells `reactivation-agent` a real contractor has handed over a real customer database with a real, confirmed offer. Firing that signal with nothing behind it points a live SMS sequence at a database that does not exist, under a sender identity nobody authorised. `appointment-setter-agent` and `sales-closer-agent` both refused to fabricate one step upstream; I am confirming that call downstream rather than quietly laundering it into a client record.

**Root cause is unchanged and is not mine to fix:** no voice/SMS integration is configured. 37 items sit queued in the outbox, not one phone has rung, so there are no conversations → no appointments → no closes → no clients. Connecting a dialler remains the single highest-value action available to this agency. Secondary: list depth is 32 against a 1,000 floor, zero email addresses on file, owner questionnaire outstanding.

## 1. Where onboarding capacity went instead

The two things most likely to blow the <24h SLA on the *first real close* are (a) not knowing exactly what to ask for, and (b) discovering on day 3 that the offer the client agreed to sell isn't one they'll actually honor. Both are solved before the close, not after. This kit is the fix.

---

## 2. Close-verification gate (before anything else)

Three mechanical acts must have happened **on the sales call**. If any is missing, chase it inside the hour — do not begin access collection, and do not let the clock start on a client who isn't actually a client.

| # | Item | Evidence | If missing |
|---|---|---|---|
| 1 | Payment processed | `process_payment` receipt, month 1 | Call the owner same day. No payment = no onboarding. |
| 2 | Agreement sent | `send_agreement`, 12-mo term, 30-day out in month 1 | Re-send immediately; note the exact terms stated aloud on the call. |
| 3 | Onboarding call booked | Calendar invite, ≤48h from close | Book it by text before end of day. |

Then: `record_metric("close_to_onboarding_start_hours", N)`.

---

## 3. Access checklist — the onboarding call (45 min, one call, one pass)

Least-privilege throughout: **read-only wherever the platform offers it**, a named per-client credential, never a shared agency login, never reused across clients. Access is revoked on churn, same day.

**Blocking for Pillar 1 (cannot send without these):**
- [ ] **CRM / FSM export** — ServiceTitan, Housecall Pro, Jobber or Service Fusion. Dormant records: inquiry date ≥6 months, no invoice, phone present. Plus the active-customer report (needed as a *suppression* input, not a send list).
- [ ] **Internal DNC / prior opt-out list** — must be merged into our permanent shared suppression list before the first send.
- [ ] **Sender identity** — real named human at the business (owner or service manager), plus a reply-monitored number and inbox. Never "the team," never the agency.
- [ ] **Booking link** — tested on mobile, in front of the owner, on the call.
- [ ] **Capacity number** — appointments/week the shop can absorb (typical 5–50 tech: 15–40). The sequence is throttled to this. An overbooked contractor cancels and blames us.
- [ ] **Trade split** — HVAC / plumbing / electrical, so multi-brand owners get the matching variant per record. Never send a plumbing lead an HVAC message.

**Blocking for Pillar 2 (collect now, use next week):**
- [ ] Google Business Profile access + the Place-ID short review link, mobile-tested
- [ ] FSM job-completion webhook + new-customer feed (read-only)
- [ ] Named human who will make the 1-business-hour callback on every 1–3 star
- [ ] Direct phone that actually rings the owner/manager

**Collect now, needed later:**
- [ ] Website form destinations (Pillar 3) · phone system (Pillar 5) · ad account (Pillar 4, blocked until reactivation cash lands) · brand assets, service area, hours, pricing basics

**Voice capture — 15 minutes, on this same call, non-negotiable.** Record how the owner actually talks and steal three phrases for the copy. If he says "unit," we don't write "system." If he says "y'all," we write "y'all." This is the cheapest lift in response rate available and it can only be done live.

---

## 4. Offer confirmation — the hard gate

> **Nothing goes live without the client's offer confirmed as real, in the owner's own words, in writing.**

Get an email or signed one-pager back before any send. A contractor who won't roll a truck for free will silently no-show the appointment, and we burn a database we can never re-warm.

**Pillar 1 default (HVAC):** free 21-Point System Health Check — ~30 min, written report, honest read, no charge, no pitch. Plumbing → free whole-home inspection + water-heater flush. Electrical → free panel & safety inspection. If the owner refuses free truck rolls → fall back to the $79 diagnostic (normally $189), first 20 homes. **One offer per campaign. Never mix two.**

**Pillar 2 (confirm in the same email, four items):** (a) the quarterly drawing prize is real and he'll honor it — default is 12 months of the maintenance plan, ~$180–$400 real cost, keeps total prize value well under $5,000; (b) the referral intro-offer is real; (c) official rules with a free alternate method of entry will be published; (d) the named human for the 1-hour negative callback.

**Confirmation email to send, day 0:**

> Subject: confirming exactly what we're offering your customers
>
> [NAME] — before we text a single one of your customers I need you to confirm, in your own words, what a "yes" gets them. Two things:
>
> 1. The reactivation offer: *[offer]*. Anyone who says yes gets this, at no charge, no pitch. Roughly [N] a week, which is the number you gave me.
> 2. The quarterly drawing prize: *[prize]*.
>
> Reply "confirmed" and the name you want on the messages, and we start. If either one doesn't sit right, tell me now and we'll change it — the one thing we can't do is offer something you won't honor.

---

## 5. Kickoff order — fixed, never reordered

1. **`reactivation-agent`** — month 1, funds everything. Target: **first message sent within 72h of close.**
2. **`reviews-referrals-agent`** — the moment Pillar 1 is live and sending. Starts with the 30-day backfill at 25/day, which produces reviews in week 1.
3. **`lead-nurture-agent`** — attach to website forms.
4. **`ads-agent`** — **blocked** until reactivation cash is collected. Also blocked below a 4.7 rating; do not buy traffic into a 3.9-star profile.
5. **`voice-receptionist-agent`** — once stable and upsold.

`advance_client` to REACTIVATION only after §2, §3-blocking and §4 are all green. The note records what was collected and what was kicked off.

---

## 6. Expectation-setting script (say this aloud on the onboarding call)

> "Here's your week one. Today I pull your dormant list — people who called you six-plus months ago and never got taken care of — and scrub it against your do-not-contact list, your active customers, and anyone you've invoiced recently. What's left gets three texts over three business days, from *[sender name]*, from a number that rings back to you. Not from us, not from a robot — your name is on it, because that's the only version that works.
>
> When someone says yes, they get an answer in five minutes and a time slot. You'll see the bookings land on your calendar. Your only job is to send the truck and honor the free check.
>
> You'll get a report at day 7, day 14 and day 30 — responses, bookings, shows, and the revenue we can attribute. The day-30 number is the one that matters.
>
> Two things I need from you: tell me the truth about how many appointments a week you can actually absorb, and if anything in the message doesn't sound like you, say so now. We'd rather rewrite it than send something your customers won't recognise."

**Also state plainly:** STOP is honored instantly and permanently; quiet hours are 8am–8pm local, no Sundays or holidays; any "no heat / no cool / leak / burning smell / no power" reply is routed to their dispatch immediately as a same-day paying job, not into a booking funnel.

---

## 7. Handoff to `client-success-agent`

Register at the moment of `advance_client`: client id, package, monthly investment, cash collected, close date, **30-day review date** (the date the 30-day out expires — book it now, not on day 29), sender identity, confirmed offer, confirmed prize, capacity cap, day 7/14/30 report dates.

---

## 8. Trigger conditions for the next onboarding cycle

| Trigger | My action |
|---|---|
| Any client appears in ONBOARDING | Run §2 within the hour; onboarding call booked ≤48h; §3–§4 complete; `advance_client` to REACTIVATION with the collected-and-kicked-off note |
| Close verification fails (§2) | Chase the missing act same day; escalate to `sales-closer-agent`; clock does not start |
| Owner won't confirm the offer in writing | **Hold the send.** Fall back to the $79 diagnostic. Escalate to `client-success-agent` if he refuses both — a client who won't honor an offer is a 30-day-out risk on day 1 |
| Multi-territory owner closes | One database, one dispatch board, **segment by trade and by location**; confirm capacity per location, not in aggregate |
| Accesses incomplete at 24h | Advance nothing. Log which access is missing and why; daily chase until green |

## 9. KPIs I will report

`close_to_onboarding_complete_hours` (<24) · `pct_accesses_collected` (100) · `hours_to_first_reactivation_message` (<72) · `week1_activity_delivered` (bookings on the client's calendar in the first 7 days) · `offer_confirmed_in_writing` (binary, blocking).

---

**Status: READY. Zero clients onboarded in cycle 1 because zero clients exist. The kit above turns the first close into a live reactivation sequence inside 72 hours without a single day lost to "what do we need from you again?"**
