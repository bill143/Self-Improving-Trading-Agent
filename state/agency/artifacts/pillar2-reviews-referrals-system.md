# Pillar 2 — Master Reviews & Referrals System
**Agent:** reviews-referrals-agent · **Phase:** 4 (build once, deploy per client)
**Niche (locked Phase 1):** Residential home services — HVAC, plumbing & electrical contractors, US, owner-operated, 5–50 technicians (roofing/solar adjacent)
**Sold as:** the second half of the Pillars 1+2 starter bundle (`sales-agent`).
**Fulfillment trigger:** starts the moment the Pillar 1 reactivation sequence is live and sending. Never before — Pillar 1 pays for the retainer, Pillar 2 compounds it.

**What this pillar produces:** a permanent, self-feeding stream of Google reviews (so the client wins "HVAC near me" / "plumber near me") and free referral jobs, at **$0 ad spend**. It runs off customers the client already has.

---

## 0. The mechanic — and why it's built this way

> **Quarterly drawing.** Every customer who answers the post-job feedback text is entered. Each friend they refer who actually books adds **5 extra entries**. Framed as *"here's how to improve your odds,"* never as *"do us a favor."*

**Three structural rules that make this legal and honest — none are optional:**

1. **The entry is for the FEEDBACK, not the review.** A 1-star response earns the identical entry as a 5-star response. We reward the customer for telling us the truth. Google's policy prohibits incentivising reviews; this design never does. **The drawing is never mentioned in the review ask, and never mentioned in a public review reply.** (See §11.)
2. **We never gate reviews.** Unhappy customers are not punished, not suppressed, not talked out of posting. We simply do not *ask* them to post publicly — we ask them for detail and put a manager on the phone. If they post publicly anyway, we answer publicly and well (Appendix C).
3. **No purchase necessary.** A prize + chance + consideration is an illegal lottery in most US states. Official rules must carry a free alternate method of entry (AMOE) so the promotion is a sweepstakes, not a lottery. Details in §12.

### Prize selection (pick ONE per client, per quarter)

| Option | Real cost to contractor | Perceived value | Use when |
|---|---|---|---|
| **A — "Free year on us": 12 months of the maintenance plan + priority scheduling + waived diagnostic fee** | ~$180–$400 (mostly labor already scheduled) | High | **DEFAULT.** Cheapest real cost, and it puts the winner on a recurring plan — the prize *creates* an annuity customer. |
| **B — $1,000 credit toward any service or install** | Up to $1,000, only if redeemed on real work | Highest pull | Client wants maximum response rate and has margin headroom. |
| **C — $500 Visa/home-improvement gift card** | $500 hard cash | Medium-high | Client insists on a no-strings prize. Least preferred — pure expense, no customer created. |

**Hard ceiling: total prize value stays under $5,000.** Florida and New York require registration and bonding for promotions above that threshold — we stay well under it and avoid the whole regime. *(Confidence: HIGH on the existence of those thresholds; `client-success-agent` still routes official rules past the client's counsel before quarter 1 launch.)*

**Word choice:** say **"quarterly drawing"** in all customer-facing copy. Never "raffle" — in several states "raffle" is a regulated charitable-gaming term. Never "sweepstakes" in the SMS either; it reads corporate.

---

## 1. Placeholder glossary (swap per client, per send)

`[FIRST]` customer first name · `[TECH]` technician's first name · `[BUSINESS]` shop's *spoken* short name · `[SENDER]` real named human, usually the owner (matches Pillar 1 sender) · `[PRIZE]` short prize phrase · `[JOB]` the thing we fixed, in the customer's words · `[GOOGLE_REVIEW_LINK]` · `[FEEDBACK_FORM_LINK]` · `[SHARE_LINK]` · `[RULES_LINK]` · `[INTRO_OFFER]` what the referred friend gets · `[DIRECT_PHONE]` a number that actually rings the owner/manager.

**Character budget for SMS:** `[TECH]` ≤ 7 · `[BUSINESS]` ≤ 16 · `[FIRST]` ≤ 8 · every link is a **shortened branded link ≤ 24 chars**. All counts below are rendered with a 24-char link. **Re-verify every SMS after variable swap; anything ≥160 gets rewritten, never split.**

---

## 2. MESSAGE 1 — RATING REQUEST

**Trigger:** job marked complete + invoice closed in the FSM (ServiceTitan / Housecall Pro / Jobber).
**Timing:** 2–3 hours after the tech clears the property. Not instantly (customer is still cleaning up), not next day (memory of the tech's face is the whole asset). **Quiet hours 8am–8pm recipient local time.** A 1am no-heat call gets its request at 10am, not at 1:15am.
**Angle:** the tech's name in the first six words. In home services people don't rate "the company," they rate *Dave*.

### SMS — HVAC (canonical)
```
Hey [FIRST] - [TECH] just finished up at your place. How'd he do, 1 to 5? Reply with a number, it enters you in our [PRIZE] drawing. -[SENDER] STOP to end
```
*Rendered:* "Hey Karen - Dave just finished up at your place. How'd he do, 1 to 5? Reply with a number, it enters you in our $1,000 drawing. -Bill STOP to end" — **145 chars.**

**Plumbing variant** — "Hey Karen - Marcus just finished the water heater. How'd he do, 1 to 5? Reply with a number, it enters you in our $1,000 drawing. -Bill STOP to end" *(146)*
**Electrical variant** — "Hey Karen - Tony just wrapped up the panel work. How'd he do, 1 to 5? Reply with a number, it enters you in our $1,000 drawing. -Bill STOP to end" *(144)*
**Maintenance-plan / tune-up visit** — "Hey Karen - Dave finished your tune-up today. How'd he do, 1 to 5? Just reply with a number and you're in our $1,000 drawing. -Bill STOP to end" *(142)*

### SMS — single reminder (48h later, non-responders only, then STOP)
```
Just checking - did [TECH] do right by you? Reply 1-5 (one number is all I need) and you're in the drawing. -[SENDER]. STOP to end
```
*(124 chars.)* **One reminder. Ever. There is no third ask.**

### Email
**Subject:** how'd [TECH] do?
**Preview:** one number, that's all I need

```
[TECH] just wrapped up at your place today.

Quick one: on a scale of 1 to 5, how did he do? Reply to this email with a
number — that's it.

Every response goes into our quarterly drawing for [PRIZE]. Your entry counts
the same whether you rate us a 5 or a 1. I'd honestly rather know the truth.

Thanks for having us out.

— [SENDER], [BUSINESS]
[PHONE] · No purchase necessary, official rules: [RULES_LINK] · Unsubscribe: [LINK]
```
*(77 words in body.)*

---

## 3. MESSAGE 2 — 5-STAR RESPONSE (rating 4–5)

**Trigger:** inbound reply parsed as 4 or 5.
**Timing:** inside 5 minutes, automated. The moment of goodwill is measured in minutes.

### SMS — rating 5
```
Love hearing that - I'll tell [TECH]. Your entry's locked in. If you've got 30 secs, a Google review helps us a lot: [GOOGLE_REVIEW_LINK] -[SENDER]
```
*(145 chars with a 24-char link.)*

### SMS — rating 4 (different message on purpose)
A 4 in this trade almost always means one small thing went sideways. We collect that intelligence *and* still ask.
```
Glad [TECH] took care of you. What would've made it a 5? Genuinely want to know. And if you're up for it: [GOOGLE_REVIEW_LINK] -[SENDER]
```
*(135 chars.)* Any reply to "what would've made it a 5" is logged as service intelligence and included in the weekly digest (§9).

### Email
**Subject:** passing this along to [TECH]

```
Thanks [FIRST] — that's exactly what we're going for, and I'll make sure
[TECH] hears it.

Your entry in the quarterly drawing is locked in either way.

One favor, if you've got half a minute: would you put that in a Google review?
It's the single biggest thing that helps a local shop like ours get found by
our own neighbors.

[GOOGLE_REVIEW_LINK]

Either way — thanks for having us out.

— [SENDER]
```
*(72 words.)*

> **Note what is absent:** no mention of the drawing *inside* the review ask paragraph, no "leave a review and you'll be entered." The entry was already confirmed, unconditionally, one sentence earlier. That separation is deliberate and is what keeps us compliant with Google's incentive policy.

---

## 4. MESSAGE 3 — 1–3 STAR RESPONSE

**Trigger:** inbound reply parsed as 1, 2 or 3.
**Timing:** inside 5 minutes, automated — then a **human call within 1 business hour**, no exceptions.
**Angle:** acknowledge, don't grovel. Contractors' customers smell insincerity instantly. One clean line of ownership, then a question.

### SMS
```
Thanks for being straight with me - that's not the job we want to do. What went wrong? [FEEDBACK_FORM_LINK] I'll call you myself. Entry's in. -[SENDER]
```
*(151 chars with a 24-char link.)*

### Email
**Subject:** that's not the job we want to do

```
Thanks for telling me straight — I'd rather hear it than not.

Can you give me the details here? [FEEDBACK_FORM_LINK] It takes a minute and
it comes to me directly, not to a queue.

I'll call you personally within one business day either way.

And your drawing entry stands. You told me the truth — that's exactly what
the entry is for.

— [SENDER], owner
[DIRECT_PHONE]
```
*(69 words.)*

### Hard rules on this branch
- **A 1–3 star response NEVER receives a review ask.** Not that day, not later, not in a newsletter. Permanent flag on the record for 90 days.
- **The entry stands and is visible in the entry count.** No quiet removal. That's the difference between a raffle and a bribe.
- **Manager alert fires immediately** to `[DIRECT_PHONE]` and the client's ops inbox with: customer, address, job number, tech, invoice amount, rating, verbatim text.
- **Escalate to same-day if the reply contains:** "still not working", "leak", "no heat", "no cool", "no power", "burning", "flooded", "damage", "charged me", "lawyer", "BBB", "chargeback". These are warranty/callback events with real revenue and liability at stake, not sentiment. Route to the owner's phone, not to a form.
- If the customer *does* post a public 1–3 star review anyway, respond using **Appendix C** — owner-approved, posted by a human, never auto-posted.

---

## 5. MESSAGE 4 — REFERRAL ASK

**Trigger:** a public 5-star review is confirmed live on Google (verified by monitor, not by the customer's promise).
**Timing:** 24 hours after the review posts. Same-day feels transactional; a week later the warmth is gone.
**Angle:** their odds, not our pipeline.

### SMS
```
[FIRST], thanks for the review - made our week. Know a neighbor who needs us? [SHARE_LINK] gets them a free tune-up + you 5 extra entries. -[SENDER]
```
*(154 chars with a 24-char link.)*

**Trade-specific `[INTRO_OFFER]` for the friend** (must mirror a real offer the owner will honor — same gate as Pillar 1 §0.1):
- HVAC → free 21-point system health check (identical to the Pillar 1 offer; one operational SOP, one truck-roll cost)
- Plumbing → free whole-home plumbing inspection + water-heater flush
- Electrical → free panel & safety inspection
- Fallback if the owner refuses free truck rolls → "$50 off their first visit"

### Email
**Subject:** your review + a favor for a neighbor

```
[FIRST], I saw your review this morning — thank you, genuinely.

Here's how to make it worth something to you: send this to anyone you know
who needs [TRADE] work. [SHARE_LINK]

They get [INTRO_OFFER] on their first visit. And every one who actually books
puts 5 more entries in your name for the quarterly drawing — so your odds go
up for doing a neighbor a favor.

No pressure at all. Forward it or don't.

— [SENDER]
```
*(78 words.)*

### Referral loop mechanics
- `[SHARE_LINK]` is per-customer and attributed. Friend lands on a one-field booking flow (name + address + phone). No account creation, no form maze.
- **Entries credit on booked-and-completed job**, not on click, not on form fill. Stated plainly in the official rules so nobody feels cheated.
- **Confirmation SMS to the referrer, same day the friend's job completes:**
  ```
  [FRIEND] just had us out - that's 5 more entries for you. You're at [N] now. Thanks for the intro. -[SENDER]
  ```
  *(~110 chars.)* This message is the flywheel: it is the single highest-yield trigger for a *second* referral.
- **Quarterly re-ask** to every past 5-star reviewer, 10 days before the draw: "Drawing's [DATE]. You're at [N] entries — [SHARE_LINK] is worth 5 more each if you know anyone. -[SENDER]" *(~118 chars.)*
- **Cap:** 10 referral credits per customer per quarter. Prevents the one guy who spams a Facebook group and turns the promotion into a lead-broker scheme.

---

## 6. MESSAGE 5 — GOOGLE REVIEW AUTO-RESPONSES (five 5-star replies)

Public replies posted to the client's Google Business Profile. **Not SMS/email** — these are published replies, so no channel split applies.
**Timing:** within 24 hours, always inside 48.
**Rules:** 2–3 sentences. Thank `[FIRST]` by name. Reference something specific — the tech, the actual job, the weather, the neighborhood. One natural mention of city or service (Google reads these; keyword-stuffing reads as spam to humans, which is worse). **Never mention the drawing, the referral link, or any promotion in a public reply.** Rotate so the same template never appears twice within 10 reviews or twice in the same week.

**1 — Tech-credit open**
> Thanks [FIRST] — I'll make sure [TECH] sees this. That [JOB] is a miserable one to track down and he stayed after it until it was right. Holler if it gives you any trouble at all.

**2 — Specific-detail open**
> [FIRST], [TECH] told us about [DETAIL] — glad we caught it before it turned into a real problem. Appreciate you trusting us with the [JOB], and enjoy not thinking about it for a while.

**3 — Emotional open**
> This one made [TECH]'s whole day, [FIRST]. Getting you back up and running the same day was the goal, and I'm glad we hit it. Thanks for the kind words.

**4 — Neighborhood/local open**
> Appreciate this, [FIRST]. We've been doing [TRADE] work in [CITY] a long time and reviews from folks right here in [NEIGHBORHOOD] still mean the most. Give us a call whenever you need us.

**5 — Plain and short**
> Thank you, [FIRST]. Straightforward job, done right, no surprises on the bill — that's what we're aiming for every time. Glad [TECH] took care of you.

**Variable bank so the rotation doesn't go stale:** `[JOB]` = capacitor / condenser fan motor / evaporator coil / water heater / main line clog / sump pump / panel upgrade / GFCI circuit / ductwork. `[DETAIL]` = the corroded fitting, the cracked heat exchanger, the roots in the line, the double-tapped breaker. `[NEIGHBORHOOD]` pulled from the service address.

**Quality gate:** before posting, run a similarity check against the client's last 10 published replies. >70% overlap = regenerate. A profile full of "Thank you for your business!" is worse than no replies at all.

---

## 7. Routing logic (one page, this is the whole engine)

```
Job complete + invoice closed
        │
        ├─ suppression check (§8) ── fail ─→ do not send
        │
   RATING REQUEST (2-3h post-job, 8am-8pm local)
        │
        ├─ no reply 48h ─→ ONE reminder ─→ no reply ─→ close, no further contact
        │
        ├─ reply = 5 ──→ 5-STAR SMS/EMAIL ──→ review posted? ──yes─→ AUTO-RESPONSE (24h)
        │                                          │                        │
        │                                          no ─→ close              └─→ REFERRAL ASK (+24h)
        │                                                                            │
        │                                                              friend books & job completes
        │                                                                            │
        │                                                              +5 entries + confirmation SMS
        │
        ├─ reply = 4 ──→ 4-STAR SMS/EMAIL (what would've made it a 5?) ─→ log intel ─→ review path
        │
        ├─ reply = 1-3 → 1-3 STAR SMS/EMAIL + feedback form
        │                + MANAGER ALERT (call within 1 business hour)
        │                + 90-day review-ask suppression
        │                + entry stands
        │                + escalate to owner same-day on trigger words
        │
        └─ reply = STOP/opt-out ─→ suppress permanently, all channels, all clients (§10)
```

---

## 8. Suppression list — do not send a rating request if…

1. The record is on the permanent DNC/opt-out list (shared with Pillar 1 — one list across every client, forever).
2. The job was a **warranty callback or a re-visit on a job we already botched**. Asking "how'd we do?" after fixing our own mistake is how you manufacture a 1-star.
3. The customer already left a review for this client in the last **6 months**.
4. The customer rated 1–3 within the last **90 days**.
5. The job is **unpaid, disputed, or in collections**.
6. The invoice is a **quote/estimate only** — no work performed, nothing to rate.
7. The customer is a **landlord/property manager** who wasn't on site. Route to the tenant only with the owner's written OK; otherwise skip.
8. **Commercial/warranty-company dispatch** (home warranty jobs). The customer didn't choose the client and their rating reflects the warranty company, not the shop.
9. Same household already received a rating request in the last **30 days**.
10. **Insurance-claim roofing work** (adjacent segment) — see §12 legal note. No referral incentive attaches to these jobs at all.

Expect **60–80% of completed jobs to survive suppression.** That is the correct number; a system that texts 100% of jobs is a system that will eventually text a furious customer.

---

## 9. Fulfillment SOP (per client, after Pillar 1 is live)

**Week 1 — wiring**
1. Connect the FSM (ServiceTitan / Housecall Pro / Jobber / Service Fusion) job-completion webhook + the new-customer feed. Read-only where possible.
2. Confirm the sender identity — **the same named human as Pillar 1.** Continuity matters; a new name in the customer's thread reads as a bot.
3. Capture voice: 15 minutes with the owner, steal three real phrases, put them in the copy. If he says "unit," don't write "system."
4. Get `[GOOGLE_REVIEW_LINK]` (the Place-ID short link, tested on mobile), build the feedback form, build the per-customer `[SHARE_LINK]` domain.
5. **Owner sign-off gate — blocking, all four:** (a) the prize is real and he'll honor it; (b) `[INTRO_OFFER]` is real and he'll honor it; (c) official rules with AMOE are published at `[RULES_LINK]`; (d) a human is named and available to make the 1-hour callback on every 1–3 star. **No sends until all four are green.** Same discipline as Pillar 1 §0.
6. Backfill: run the rating request against the last **30 days** of completed jobs, throttled to 25/day. This produces reviews in week 1 and is the demo that sells month 2.

**Week 2+ — steady state**
7. Rolling sends, capped at **25–40 rating requests/day** so the 1-hour callback SLA on negatives is always honorable.
8. Monitor Google daily; auto-respond to new 5-stars within 24h; queue 1–3 star public reviews for owner-approved human reply (Appendix C).
9. Fire the referral ask 24h after each posted review. Track entries. Send the friend-booked confirmation same day.
10. Quarterly: run the draw, publish the winner (with written consent), reset entries, launch the next quarter's prize.
11. **Weekly digest to `client-success-agent`** every Monday:
    - responses / response rate · rating distribution · reviews posted · rating average & trend
    - referral links shared, friends booked, referral revenue
    - **negative feedback intercepted** — verbatim, with tech name and job number
    - **service intelligence:** recurring themes from 4-star "what would've made it a 5" replies (this is often the most valuable line on the page — it's free ops consulting from their own customers, and it's a retention weapon)

---

## 10. Opt-outs (inherited verbatim from Pillar 1 §6)

STOP / UNSUBSCRIBE / CANCEL / END / QUIT / REMOVE / "take me off" / "don't text" → **suppress instantly and permanently across SMS, email and voice, for every campaign and every client**, push to the shared permanent suppression list, send exactly one carrier-standard confirmation, never contact again.

```
You're unsubscribed from [BUSINESS] messages. You will not receive further texts.
```
*(80 chars.)*

**Their existing drawing entries remain valid.** Opting out of messages is not a forfeiture. If they win, the client contacts them once, by phone, to deliver the prize. This is written into the official rules.

---

## 11. Guardrails — standing, non-negotiable

- **No fake reviews. Ever.** Not written by us, not written by staff, not "seeded," not incentivised beyond the feedback drawing. One fake review can get a client's profile suspended and would end this agency.
- **No review gating.** We never suppress, delay, or discourage a negative public review. We route unhappy customers to a human faster than we route happy ones to Google.
- **The entry is for feedback, never for the review.** The drawing is never mentioned in the same breath as the review ask, and never appears in a public reply.
- **1–3 star = zero review asks.** Absolute.
- **The prize and the intro offer must be real and honored**, confirmed by the owner in writing before a single send.
- **Quiet hours 8am–8pm recipient local time.** No Sundays, no federal holidays. Emergency-call customers get their request during business hours.
- **Sender is always a real named human at the business.** Never "the team," never the agency, never a bot persona.
- **Never ask the customer to mention a keyword, a city, or a product in their review.** Coached reviews are detectable and dishonest.
- **Photos, names and reviews are not reused in ads** without written permission (hands off to `ads-agent`).

---

## 12. Legal notes for this niche (route past client counsel before quarter 1)

| Issue | Position |
|---|---|
| **Lottery vs sweepstakes** | Prize + chance + consideration = illegal lottery. We eliminate consideration with a published **AMOE**: anyone may enter free via a web form or mailed card, no purchase and no service required. Rules must state it in plain English. |
| **Official rules** | Published at `[RULES_LINK]`, linked in every email footer and the SMS-landing page. Must state: sponsor, eligibility (18+, service area, no employees/family), entry methods incl. AMOE, entry period, draw date and method, odds statement, prize description and ARV, winner notification, "void where prohibited." |
| **Prize value** | Kept under $5,000 to stay clear of FL/NY registration-and-bonding thresholds. *(HIGH confidence the thresholds exist; counsel confirms.)* |
| **Google policy** | Incentivising reviews is prohibited. Our entry is granted for responding to a private feedback request, identically across all ratings, and is never referenced in the review ask or the public reply. |
| **TCPA** | Post-service messages to a customer who supplied their number for the job. Still treated as marketing: STOP honored instantly and permanently, quiet hours enforced, sender identified in message 1. |
| **Referral rewards & licensing** | Sweepstakes entries (not cash) are the default reward specifically because a handful of states restrict cash referral fees paid to unlicensed persons. If an owner insists on cash, `client-success-agent` gets a written state-law check first. |
| **Insurance / roofing work** | **No referral incentive, no prize entry, and no deductible-adjacent offer ever attaches to an insurance-claim job.** Rebating on insurance work is illegal in many states. Adjacent-segment roofing/solar clients get the reviews half of this pillar only, with the referral half restricted to retail (non-claim) jobs. |

---

## 13. KPI targets & the volume model

A 5–50 tech shop completes roughly **150–600 jobs/month.** Model at 300 completed jobs:

| Stage | Rate | Result |
|---|---|---|
| Completed jobs | — | 300 |
| Survive suppression (§8) | ~70% | 210 eligible |
| Feedback responses | 35–45% | **~88 responses** |
| Rated 4–5 | ~85% | **~75 positive** |
| Rated 1–3 | ~15% | **~13 intercepted before they go public** |
| 4–5 → posted Google review | 30–35% | **~25 reviews** |
| Reviewers who share `[SHARE_LINK]` | ~25% | ~6 shares |
| Friends who book & complete | — | **~7 free referral leads** |

That lands squarely on the blueprint benchmark (76 positive responses, 24 reviews, 7 referral leads, 8 negatives intercepted) — **in a niche where 7 referral leads at a $5,000–$12,500 replacement ticket is a five-figure month from zero ad spend.** That number, not the review count, is what `sales-agent` sells.

| Metric | Target | Failure signal |
|---|---|---|
| Feedback response rate | 35–45% | <25% → timing is wrong, move closer to the truck leaving |
| Reviews / month | 20–30 (at 300 jobs) | <10 → the review link is broken on mobile; test it |
| Rating average trend | rising, ≥ 4.7 | falling → this is an ops problem, escalate to owner, not a copy problem |
| Negative intercepted | 100% of 1–3 star responses get a human call within 1 business hour | any miss → throttle sends until staffed |
| Public 1–3 star reviews | falling quarter over quarter | rising while private negatives fall → we're routing, not fixing |
| Referral leads / month | 5–10 | <3 → the intro offer is too weak, or entry confirmation isn't firing |
| Opt-out rate | <1% | >2% → cadence too heavy, cut the 48h reminder |
| Review-reply coverage | 100% within 48h | — |

All logged per client via `record_metric`.

---

## Appendix A — Draw-cycle messages

**T-10 days, all entrants:** "Drawing's [DATE] and you're in it - [N] entries. [SHARE_LINK] is worth 5 more each if you know anyone who needs us. -[SENDER] STOP to end" *(~140)*
**Winner:** "[FIRST] - you won the [PRIZE] drawing. Not a scam, I promise. Call me at [DIRECT_PHONE] and I'll set it up. -[SENDER], [BUSINESS]" *(~128)*
**Everyone else:** "Drawing's done - [WINNER_FIRST] in [CITY] took it. Next one starts today, and you're already entered from your last visit. -[SENDER] STOP to end" *(~144)*

The "you're already entered" line is the retention hook: it makes the next service call feel like a lottery ticket.

## Appendix B — Objection micro-handlers

| They say | Reply |
|---|---|
| "Is this a real drawing?" | "Real one - rules and past winners are here: [RULES_LINK]. Last quarter's went to a customer over in [CITY]. -[SENDER]" *(~118)* |
| "I don't do Google." | "No worries at all, your entry's already in. Thanks for the rating. -[SENDER]" *(~76)* |
| "Are you paying me for a review?" | "Nope - the entry's for answering my text, good rating or bad. The review's just a favor if you feel like it. -[SENDER]" *(~119)* |
| "Take me off this." | Opt-out flow, §10. No pitch, no retention line. |

## Appendix C — Public replies to 1–3 star reviews (owner-approved, human-posted, NEVER auto-posted)

> [FIRST], this isn't how we do things and I'd like to make it right. I'm [SENDER], the owner — my direct line is [DIRECT_PHONE]. Call me and I'll get it sorted personally.

> Appreciate you telling us, [FIRST]. I've pulled the job file and I'm reviewing it with [TECH] today. Reach me directly at [DIRECT_PHONE] — I'd rather fix this than argue about it here.

**Rules:** never dispute facts publicly, never mention the drawing, never name the customer's address or job details, never blame the tech in public, always a direct human phone number, always posted by a person. Two templates only — anything more starts looking scripted on a profile where the negatives are the most-read replies.

---

## Handoffs

- **`sales-agent`:** sold with Pillar 1 as the starter bundle. Sell §13 — *"7 free referral leads a month at your ticket"* — never a promised review count.
- **`client-success-agent`:** Monday digest per §9.11. The negative-feedback log is the retention weapon; the referral revenue figure is the upsell trigger into Pillars 3–5.
- **`speed-to-lead-agent`:** every referral `[SHARE_LINK]` booking is a live inbound lead and inherits the 60-second response SLA. A referral that waits an hour is a referral wasted.
- **`ads-agent`:** rising review count and rating are prerequisites for profitable local ads. Do not launch paid traffic into a 3.9-star profile.
- **`reactivation-agent`:** shares the permanent suppression list. One list, both pillars, forever.

**Status: BUILT.** Ready to deploy on the first signed client the day the Pillar 1 sequence goes live.
