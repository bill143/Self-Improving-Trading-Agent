# Pillar 1 — Master AI Database Reactivation Campaign
**Agent:** reactivation-agent · **Phase:** 3 (build once, deploy per client)
**Niche (locked Phase 1):** Residential home services — HVAC, plumbing & electrical contractors, US, owner-operated, 5–50 technicians (roofing/solar adjacent)
**Database definition:** dormant leads who inquired 6+ months ago and never converted — no job invoiced, no membership sold.
**Purpose:** produce booked appointments in month one at $0 ad spend. This is the first thing `sales-agent` sells (~$1,500, compressed into month one) and the first thing fulfillment delivers. Cash from this pillar funds the client's paid ads; `ads-agent` waits on it.

---

## 0. Pre-flight gate — DO NOT SEND until all five are green

| # | Gate | Who confirms | Blocking? |
|---|---|---|---|
| 1 | **The offer is real and the owner will honor it** — written confirmation, in the owner's own words, of exactly what a "YES" gets. | Client owner, in writing | **YES** |
| 2 | **Capacity exists** — owner confirms how many appointments/week they can absorb (typical 5–50 tech shop: 15–40). Sequence is throttled to that number. | Client owner | **YES** |
| 3 | **Consent** — every record was a self-initiated inquiry (form fill, phone call, quote request) where the customer supplied the number. No purchased lists, no scraped numbers, no third-party data. | reactivation-agent audit of export | **YES** |
| 4 | **Suppression scrub** — remove: internal DNC, prior opt-outs, active customers, open estimates, anyone invoiced in the last 6 months, litigator/known-complainant list, landlines flagged as non-SMS. | reactivation-agent | **YES** |
| 5 | **Sender identity** — a real named human at the business (owner or service manager) whose name goes on every message, plus a reply-monitored number and inbox. | Client owner | **YES** |

**Why gate 1 is absolute:** a contractor who won't send a truck for free will silently no-show the appointment, and we burn a 4,000-record database we can never re-warm. Confirm the offer, then send.

---

## 1. THE REACTIVATION OFFER

> **Primary offer (type c — free consultation/inspection):** A no-charge, no-obligation **21-Point System Health Check** on the exact system they called us about months ago — done in about 30 minutes, with a written report and an honest "here's what I'd do if it were my house," whether or not they ever buy anything.

*One sentence, sender's voice:* "You called us a while back and we never got you taken care of — I'd like to make that right with a free check on your system, no charge and no sales pitch."

**Why this offer for this niche (do not substitute casually):**
- **It re-opens the original conversation instead of starting a new one.** These people already raised their hand about a specific problem. The hook is the unfinished business, not a coupon.
- **It costs the contractor a truck roll, not margin.** No brand discounting — which matters enormously for franchisees (One Hour, Benjamin Franklin, Mr. Rooter, Aire Serv, Mister Sparky, Mr. Electric), whose agreements police discounting and creative but say nothing about a service reminder to their own customer list. **No corporate approval required.** This is the wedge Phase 2 §4 told us to use.
- **It converts at the highest ticket in the niche.** A tech standing in front of a 14-year-old system is the highest-probability path to a $5,000–$12,500 replacement. One recovered job pays the entire retainer, several times over.
- **It's honest.** Nothing here is fake scarcity or a fake prize.

**Alternate offer (type b — limited-time discount).** Use ONLY if the owner refuses free truck rolls: *"$79 diagnostic + tune-up, normally $189 — first 20 homes only, then it goes back up."* Same three-day cadence, swap the noun.

**Never run offer (a) raffle/prize in this niche.** Homeowners with a broken system don't want a raffle, and it cheapens a $10K purchase decision. Rejected on purpose.

**RULE: one offer per client per campaign. Never mix two.** Two offers in one sequence halves response and doubles confusion.

**Seasonal timing (HVAC only):** run the cooling angle Mar–Jun, the heating angle Sep–Nov. Off-peak, pivot the noun to "maintenance plan check" rather than "beat the rush."

---

## 2. DAY 1 — SMS & EMAIL
**Angle:** we dropped the ball. Personal admission, zero marketing gloss.
**Send:** Tue–Thu, 10:00–11:30am local.

### SMS (HVAC — canonical)
```
[TECH] here at [BUSINESS]. You called about your AC back in [MONTH] and we never got it sorted. Free 21-pt check this week? Reply YES or STOP to end
```
*Rendered:* "Dave here at Miller Heating & Air. You called about your AC back in June and we never got it sorted. Free 21-pt check this week? Reply YES or STOP to end" — **153 chars.**
> Character budget: `[TECH]` ≤ 8, `[BUSINESS]` ≤ 22, `[MONTH]` ≤ 9. If the business name is longer, use the shop's spoken short name ("Miller Heating") — that's what a real person would type anyway.

**Plumbing variant** — "Marcus here at [BUSINESS]. You called about that water heater back in [MONTH] and we never got you scheduled. Free check this week? Reply YES or STOP" *(151)*
**Electrical variant** — "Tony here at [BUSINESS]. You reached out about your panel back in [MONTH] and we dropped the ball. Free safety check? Reply YES or STOP to end" *(143)*

### Email
**Subject:** your call about the AC back in June
**Preview:** we never followed up — that's on us

```
You called us about your AC back in June and we never followed up. That's on
me, not you.

I'd like to make it right: one of my techs will do a free 21-point check on
your system — about 30 minutes, written report, and an honest read on how much
life it's got left. No charge, no pitch. If it's fine, we'll tell you it's fine.

Want me to put you down for this week?

Reply YES to this email and I'll send times.

— Dave Miller, Miller Heating & Air
[PHONE] · [ADDRESS] · Unsubscribe: [LINK]
```
*(96 words in body.)*

---

## 3. DAY 2 — SMS & EMAIL (non-responders only)
**Angle change:** off the apology, onto the calendar. Subtle urgency = the schedule filling, not a countdown clock.
**Send:** next business day, 4:30–6:00pm local (catches people home from work).
**Audience:** no reply, no click, no opt-out.

### SMS (HVAC)
```
Dave again, [BUSINESS]. Not chasing you - just filling free check slots before the summer rush. Want one? Reply YES, or STOP to end.
```
*(141 chars rendered.)*

**Plumbing** — "Marcus again at [BUSINESS]. Not chasing you - just booking the free checks before we get slammed. Want a slot? Reply YES, or STOP." *(139)*
**Electrical** — "Tony again, [BUSINESS]. Not pestering you - just filling this week's free safety checks. Want one? Reply YES, or STOP to end." *(132)*

### Email
**Subject:** before the first hot week
**Preview:** the free checks are going quick

```
Quick follow-up, then I'll leave it alone.

Every year the first 90-degree week hits and my phones don't stop. The people
who get taken care of are the ones already on the calendar.

You're on my list from June, so you get first crack at the free 21-point check
before I open the slots up. Half an hour, no charge, and you'll know exactly
where your system stands going into summer.

Reply YES and I'll text you two times to pick from.

— Dave Miller, Miller Heating & Air
[PHONE] · Unsubscribe: [LINK]
```
*(92 words.)*

---

## 4. DAY 3 — SMS & EMAIL (final)
**Angle:** clean deadline, permission to say no. The "NO is fine" line is what makes this convert — it removes the pressure that makes people ignore you.
**Send:** third business day, 11:00am–1:00pm local. Deadline is always a named weekday, never "24 hours."

### SMS (HVAC)
```
Last note from me - Dave at [BUSINESS]. Free check offer ends Friday. Reply YES for a slot, or NO and I'll leave you alone.
```
*(132 chars rendered.)*

**Plumbing** — "Last one from me, Marcus at [BUSINESS]. Free check ends Friday. Reply YES to grab a time, or NO and I'll stop texting." *(126)*
**Electrical** — "Wrapping this up - Tony at [BUSINESS]. Free safety checks end Friday. Reply YES for a slot, or NO and I'm out of your hair." *(131)*

### Email
**Subject:** closing this out Friday
**Preview:** last one, then I'll stop

```
Last email from me on this.

I'm closing out the free 21-point checks Friday so my guys can get back on
regular calls. After that it's the standard $189 diagnostic.

If you want one, reply YES and I'll get you on the books before the cutoff.
If it's not for you, reply NO and I'll take you off my list for good — no
hard feelings, genuinely.

Either way, thanks for thinking of us back in June.

— Dave Miller, Miller Heating & Air
[PHONE] · Unsubscribe: [LINK]
```
*(89 words.)*

**Stop rule:** three touches per channel, then the sequence is over. No day 4, no "just bumping this." Non-responders go to a 90-day dormant hold and may be re-approached once, with a different offer.

---

## 5. "YES" RESPONSE HANDLER
**SLA: first reply within 5 minutes, 8am–8pm local. After hours, auto-reply immediately and a human follows at 8:05am.**

**Step 1 — instant confirmation + single CTA (SMS):**
```
Perfect. Pick whatever time works here: [BOOKING_LINK] - takes 20 seconds. If nothing fits, text me a day and I'll work around you. - Dave
```
*(137 chars.)*

**Step 2 — if no booking within 15 minutes, one nudge (this is where most bookings are lost):**
```
Easier if I just do it - I've got Wed 2pm or Thu 9am open. Which one? - Dave
```
*(75 chars.)* Two options, never an open question. Booked by text counts the same as booked by link.

**Step 3 — confirmation the moment it's on the calendar:**
```
You're set: [DAY] [TIME] at [ADDRESS]. Tech is [NAME], he'll text when he's 20 min out. Nothing to prep. - Dave, [BUSINESS]
```
*(122 chars.)*

**Step 4 — reminders (this is the entire show rate):**
- **24 hours before:** "Reminder - [NAME] is coming by tomorrow [TIME] for the free check. Still good? Reply Y or tell me a better day. - Dave" *(118)*
- **2 hours before:** "[NAME] is on the way for your 2pm - see you shortly. - [BUSINESS]" *(65)*

**Email counterpart (if the YES came by email):**
**Subject:** got you — pick a time
```
Great — here's my calendar: [BOOKING_LINK]

Grab any slot that works. It's about 30 minutes and you'll get a written
report before we leave. Nothing to prepare, just need access to the unit.

If none of those times work, reply with a day that does and I'll fit you in.

— Dave
```

**Escalation:** any YES that mentions no heat / no cooling / a leak / a burning smell / no power is **not** a health-check booking. Flag as urgent, route to the client's dispatch immediately, and notify `speed-to-lead-agent`. That's a same-day paying job — do not put it in a booking funnel.

---

## 6. "NO / STOP" RESPONSE HANDLER
**Honor instantly and permanently. TCPA is not a judgment call.**

**Triggers (case-insensitive, whole-word or leading token):** STOP, STOPALL, UNSUBSCRIBE, CANCEL, END, QUIT, OPTOUT, OPT OUT, REMOVE, "take me off", "don't text", "no thanks", "not interested", "leave me alone", NO.

**On trigger — automatic, in this order:**
1. Suppress the record across **SMS, email and voice**, for **all** campaigns, permanently. Never per-campaign.
2. Push to the client's CRM as DNC and to our internal permanent suppression list, so no future client campaign can ever re-add them.
3. Send exactly ONE confirmation, then never contact again.

**Soft NO / "not interested" (SMS):**
```
Got it - I'll take you off the list, no more texts from us. If your AC ever gives you trouble, we're around. - Dave, [BUSINESS]
```
*(126 chars.)*

**Hard STOP / unsubscribe:** send **only** the carrier-standard confirmation, nothing else — no pitch, no "sorry to see you go," no re-engagement line:
```
You're unsubscribed from [BUSINESS] messages. You will not receive further texts.
```
*(80 chars.)*

**Email unsubscribe:** one-click, no login, no preference-center maze, processed immediately. Confirmation page reads: *"Done — you're off the list. Sorry for the interruption."*

**Angry/complaint replies:** do not auto-respond. Suppress, flag to the client owner within the hour, and log it. One complaint handled personally beats ten automated apologies.

**Hard rules:** never re-import a suppressed number, even from a fresh client export. Never text a suppressed record "one last time." Quiet hours enforced 8am–8pm **recipient local time**, no Sundays, no federal holidays.

---

## 7. Per-client adaptation checklist (fulfillment SOP)

1. **Pull the list:** export dormant records, inquiry date ≥ 6 months old, no invoice, phone present. Run the §0 gate-4 scrub. Expect 2,000–15,000 raw → typically 55–75% survive scrubbing.
2. **Capture the voice.** 15-minute call with the sender. Record how they actually talk. Steal three phrases and put them in the copy. If they say "unit," don't write "system." If they say "y'all," write "y'all."
3. **Swap the variables:** `[TECH]` `[BUSINESS]` `[MONTH]` `[PHONE]` `[ADDRESS]` `[BOOKING_LINK]` `[NAME]` `[DAY]` `[TIME]`. `[MONTH]` is per-record — the real month they inquired. **This single personalization is the highest-leverage variable in the sequence; never fall back to "a while back" if the date exists.**
4. **Multi-brand owners** (One Hour + Benjamin Franklin + Mister Sparky in one building; Benjamin Franklin owners average ~3.7 territories): one database, one dispatch board, but **segment by trade** and send the matching trade variant. Never send a plumbing lead an HVAC message.
5. **Throttle to capacity** from gate 2. Send in daily batches sized so positive replies never exceed what the shop can dispatch. An overbooked contractor cancels appointments and blames us.
6. **Re-verify character counts after every swap.** Any SMS ≥ 160 gets rewritten, not split.
7. **Send Day 1 → Day 2 → Day 3** on consecutive business days. Reply SLA 5 minutes. Book, confirm, remind.
8. **Report** responses, bookings, shows and attributed revenue to `client-success-agent` at day 7, day 14 and day 30. The day-30 dollar figure is the referral asset — it's what opens the Mr. Rooter owners' group and the Neighborly conference.

---

## 8. Objection micro-handlers (all under 160, all sound like a person)

| They say | Reply |
|---|---|
| "How much?" | "The check itself is free - nothing due at the door. If you want work done after, I'll quote it and you decide. Want a slot? - Dave" *(129)* |
| "Already got it fixed." | "Good, glad it's handled. Want me to note your system's age so we can flag it before it quits on you? - Dave" *(107)* |
| "Who is this?" | "Dave Miller, I own [BUSINESS] here in [CITY]. You called us in [MONTH] about your AC and I'm circling back. Sorry it took me this long." *(134)* |
| "Went with someone else." | "No problem at all - hope they did right by you. I'll take you off the list. We're here if you ever need a second opinion. - Dave" *(127)* |
| "Is this a real person?" | "Real person, sitting in the shop on [STREET]. Call me at [PHONE] if it's easier. - Dave" *(87)* |
| Price shopping a replacement | Route to owner immediately. Do not quote by text. This is a $5K–$12.5K conversation. |

---

## 9. KPIs — targets and reporting

| Metric | Target (3-day sequence, scrubbed list) | Notes |
|---|---|---|
| Deliverability | ≥ 95% | Below 90% = list quality problem, stop and re-scrub |
| Total response rate | 8–15% | Across all three days |
| Positive-reply rate | 3–6% | Of records messaged |
| Reply-to-booking | ≥ 60% | Driven almost entirely by the 5-min SLA and the two-option nudge |
| Show rate | ≥ 70% | Driven by the 24h + 2h reminders |
| Appointments booked, month 1 | 25–60 on a 3,000-record database | Blueprint benchmark: dozens of opportunities at $0 ad cost |
| Attributed revenue, month 1 | ≥ 3× the retainer | One HVAC replacement ($5K–$12.5K) usually clears it alone |
| Opt-out rate | < 2% | Above 3% = the copy is too salesy, revert to canonical |
| Complaints | 0 tolerated | Any complaint escalates to the owner same day |

Every one of these is logged via `record_metric` per client, per campaign.

---

## 10. Guardrails (standing, non-negotiable)
- **STOP is instant and permanent, across every channel and every client.** No exceptions, no re-imports.
- **Only message records the client legitimately holds contact consent for** — self-initiated inquiries only.
- **The offer must be real and honored.** Written owner confirmation before a single send.
- **Sender identity is always a real named human at the business.** Never "the team," never an agency name, never a bot persona.
- **Quiet hours 8am–8pm recipient local time.** No Sundays, no holidays.
- **No fake scarcity.** If the deadline is Friday, the offer actually ends Friday.
- **No medical/safety claims, no invented savings percentages, no "you've been selected."**

---

## 11. Handoffs
- **`sales-agent`:** this is the month-one deliverable you're selling (~$1,500, compressed). Sell the mechanism in §1 and the benchmark in §9 — never promise a specific dollar figure.
- **`client-success-agent`:** day 7 / 14 / 30 reports come from §7.8. The day-30 number is the referral trigger.
- **`speed-to-lead-agent`:** inherits every emergency-flagged YES per §5.
- **`ads-agent`:** blocked until month-one reactivation revenue lands. That's the funding source.

**Status: BUILT. Ready to deploy on the first signed client immediately after ONBOARDING.**
