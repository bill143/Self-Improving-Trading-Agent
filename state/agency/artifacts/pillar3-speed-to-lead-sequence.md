# Pillar 3 — Master Speed-to-Lead Nurture Sequence
**Agent:** lead-nurture-agent · **Phase:** 5 (build once, deploy per client)
**Niche (locked Phase 1):** Residential home services — HVAC, plumbing & electrical contractors, US, owner-operated, 5–50 technicians (roofing/solar adjacent)
**Fulfillment trigger:** attaches to the client's website forms **after Pillars 1–2 are live**. Also nurtures 100% of leads produced by `ads-agent` (same sequence, same SLA, same rules) and every `[SHARE_LINK]` referral booking handed over by Pillar 2.

**The thesis, in one line:** a homeowner who types "AC repair near me" and fills out a form is not browsing — they are in pain, and they filled out three other forms on the same trip. Responding inside 5 minutes vs. after 5 minutes moves conversion by roughly **400%** (Harvard Business Review, 2018 lead-response research). The average owner-operated shop answers in ~24 hours, because at 6pm the office is closed and at 3am the owner is asleep. **We answer in under 5 minutes, every hour of every day.** In this niche the first responder doesn't just win the lead — they win a $5,000–$12,500 replacement ticket that the other two contractors never got to quote.

---

## 0. The SLA (this is the entire product — everything else is copy)

| Lead type | Target first touch | Hard ceiling | Channel |
|---|---|---|---|
| **Emergency** (no heat, no cool, leak/flood, no power, sewage) | **60 seconds** | 5 min | **Phone call first**, SMS as backup |
| Standard repair / quote / estimate request | **60 seconds** | 5 min | SMS |
| Maintenance plan / tune-up / general question | 5 min | 15 min | SMS |
| Inbound reply to any of our messages | **5 minutes**, around the clock | 15 min | Same channel they used |

**Median response time under 5 minutes is a non-negotiable, permanently measured KPI.** Pillar 2's handoff note specifies a 60-second SLA on referral bookings; that is the *target* for every lead type above. 5 minutes is the *ceiling*, not the goal. Any client month where median first-touch exceeds 5 minutes is a fulfillment failure and gets escalated to `client-success-agent`, not explained away.

### 0.1 Quiet hours vs. the 3 a.m. promise — the rule that keeps this legal

This is the single most misunderstood part of the pillar, so it is written as a decision table and is not open to improvisation.

| Situation | Action |
|---|---|
| Form submitted 8:00am–8:00pm lead-local time | Fire Message 1 immediately (target 60s). |
| Form submitted 8:00pm–8:00am local, **and the submission is under 15 minutes old** | Fire Message 1 immediately. This is a **direct reply to a request the consumer made moments ago** — they are demonstrably awake, they just typed their number into a box asking to be contacted. A shop that answers a 2am no-heat form at 2:02am is doing exactly what the homeowner asked for. |
| Form submitted overnight but we're processing it **more than 15 minutes late** (integration lag, backfill, batch import) | **Queue for 8:00am local.** A cold-open text at 4am to someone who filled a form at 11pm is not a reply, it's a marketing message. Do not send. |
| **Emergency flag** on the form, any hour | **Call immediately.** No cap, no queue. Someone with a flooded basement at 3am wants a phone to ring. |
| Follow-up Messages 2, 3, and both no-show win-backs | **Strictly 8:00am–8:00pm lead-local time, always.** These are marketing touches. They obey Pillar 1 §6 quiet hours without exception. No Sundays for Message 3. |

> **Standing instruction to `client-success-agent`:** the overnight-instant-reply position is sound and is how every serious lead-response platform operates, but it is our most aggressive interpretation. Route it past the client's counsel during onboarding and give every client an **"overnight auto-reply: ON/OFF"** toggle in their settings. If a client toggles OFF, everything overnight queues to 8:00am and we tell them plainly what that costs them.

---

## 1. Placeholder glossary (swap per client, per lead)

`[FIRST]` lead's first name, from the form · `[SENDER]` the real named human at the business — **the same name used in Pillars 1 and 2**, no exceptions · `[BUSINESS]` the shop's *spoken* short name · `[ISSUE]` the service they asked about, **in their own words off the form** · `[TECH]` assigned technician's first name · `[BOOKING_LINK]` · `[REBOOKING_LINK]` · `[DIRECT_PHONE]` a number that actually rings a human · `[DAY]` `[TIME]` `[WINDOW]` from the dispatch board · `[N]` real open slot count.

**Character budget for SMS:** `[FIRST]` ≤ 8 · `[SENDER]` ≤ 5 · `[BUSINESS]` ≤ 16 · `[ISSUE]` ≤ 18 · `[TECH]` ≤ 7 · every link is a **shortened branded link ≤ 24 chars**. All counts below are rendered against a real 24-char link (`go.millerheating.co/bk12`) and the worked example *Karen / Bill / Miller Heating / "your AC not cooling" / Dave*.

**Re-verify every character count after variable swap. Anything ≥160 gets rewritten, never split into two texts.** A split message arrives out of order and instantly reads as a bot.

> **`[ISSUE]` is the highest-leverage variable in this pillar.** Echo the homeowner's own words back at them. If the form says "ac blowing warm," write "your AC blowing warm" — not "your HVAC concern." Generic service categories are what every autoresponder on earth sends; the customer's own phrasing is what proves a person read it.

---

## 2. MESSAGE 1 — THE 5-MINUTE INSTANT RESPONSE

**Trigger:** website form submission or `ads-agent` lead webhook.
**Timing:** target 60 seconds, ceiling 5 minutes, 24/7 per §0.1.
**Angle:** named human + the exact thing they asked about + one frictionless next step. Nothing else. No "thank you for your interest in our company."

### SMS — standard repair/quote (canonical)
```
[FIRST] - [SENDER] at [BUSINESS]. Got your request about [ISSUE]. Grab a time and I'll send a tech: [BOOKING_LINK] Reply STOP to end
```
*Rendered:* "Karen - Bill at Miller Heating. Got your request about your AC not cooling. Grab a time and I'll send a tech: go.millerheating.co/bk12 Reply STOP to end" — **152 chars.** (At maximum variable lengths: 157. If a client's variables run longer, shorten the tail to "STOP to end" — saves 6 — before touching anything else.)

**Plumbing variant** — "Karen - Bill at Ace Plumbing. Got your request about the water heater. Grab a time and I'll send a tech: go.aceplumbing.co/bk12 STOP to end" *(140)*
**Electrical variant** — "Karen - Bill at Ace Electric. Got your note about the panel upgrade. Pick a time and I'll get a tech out: go.aceelectric.co/bk12 STOP to end" *(140)*
**Ad-lead variant** (`ads-agent` source — reference the *offer* they clicked, not a form field) — "Karen - Bill at Miller Heating. You asked about the $89 tune-up. Grab a time here and I'll send a tech: go.millerheating.co/bk12 STOP to end" *(139)*

### SMS — EMERGENCY branch (no heat / no cool / leak / no power / sewage / "urgent")
Do **not** send a booking link to someone standing in two inches of water. Call, then text.
```
[FIRST] - [SENDER] at [BUSINESS]. Saw you've got [ISSUE]. Calling you in 2 min. If I miss you, call me direct: [DIRECT_PHONE]
```
*Rendered:* "Karen - Bill at Miller Heating. Saw you've got no heat. Calling you in 2 min. If I miss you, call me direct: 555-123-4567" — **121 chars.**

**The call must actually be placed within 2 minutes of that text.** Promising a call and not making it is worse than never texting. Emergency leads route straight to the client's dispatch line per Pillar 1 §5 escalation — same rule, both directions.

### Email counterpart (fires simultaneously — some people never text back but always read email)
**Subject:** got your message about [ISSUE]
**Preview:** we can get someone out

```
[FIRST] — got your request about [ISSUE] just now.

I can have a tech out to you. Easiest way is to grab whatever time works
here: [BOOKING_LINK] — takes about 20 seconds and you'll get a confirmation
right away.

If none of those work, just reply to this with a day that does and I'll fit
you in around it.

— [SENDER], [BUSINESS]
[DIRECT_PHONE] · Unsubscribe: [LINK]
```
*(68 words in body.)*

### The 15-minute two-option nudge (this is where most bookings are actually won)
If Message 1 is delivered and there's no click and no reply after 15 minutes, send **one** nudge with two concrete times — never an open question. Lifted from Pillar 1 §5 because it works:
```
Easier if I just do it - I've got [DAY] [TIME] or [DAY] [TIME] open. Which works? -[SENDER]
```
*Rendered:* "Easier if I just do it - I've got Thu 2pm or Fri 9am open. Which works? -Bill" — **76 chars.** Booked by text counts exactly the same as booked by link.

---

## 3. MESSAGE 2 — THE 24-HOUR FOLLOW-UP

**Trigger:** no reply, no booking, no click, 24 hours after Message 1.
**Timing:** 8:00am–8:00pm lead-local. Prefer 4:30–6:00pm — catches homeowners back from work, same window that outperforms in Pillar 1 §3.
**Angle change:** off "I got your request," onto **"did somebody else already handle this?"** In home services the honest truth is that they filled out three forms. Naming that out loud is disarming, and it surfaces the real objection instead of letting the lead rot. Friendly, mildly urgent, zero pressure.

### SMS (HVAC canonical)
```
[FIRST] - [SENDER] again at [BUSINESS]. Did you get [ISSUE] sorted? If you're still collecting quotes, mine's free and takes 20 min: [BOOKING_LINK]
```
*Rendered:* "Karen - Bill again at Miller Heating. Did you get the AC sorted? If you're still collecting quotes, mine's free and takes 20 min: go.millerheating.co/bk12" — **152 chars.**

**Plumbing** — "Karen - Bill again at Ace Plumbing. Did you get the water heater handled? If you're still deciding, my quote's free: go.aceplumbing.co/bk12" *(138)*
**Electrical** — "Karen - Bill again at Ace Electric. Did you get the panel sorted? If you're still getting bids, mine's free and quick: go.aceelectric.co/bk12" *(140)*

### Email
**Subject:** did you get the AC handled?
**Preview:** if it's sorted I'll leave you be

```
[FIRST] — following up on your note about [ISSUE].

If you already got it handled, tell me and I'll leave you alone, genuinely.

If you're still deciding, here's the honest pitch: my quote is free, it takes
about 20 minutes, and you'll get a written number before we leave — not a
"we'll call you next week." Most people we see are comparing two or three
shops, and that's fine. I'd just like to be one of them.

[BOOKING_LINK]

— [SENDER], [BUSINESS]
[DIRECT_PHONE] · Unsubscribe: [LINK]
```
*(93 words.)*

---

## 4. MESSAGE 3 — THE 48-HOUR NUDGE (final)

**Trigger:** still no response, 48 hours after Message 1.
**Timing:** 8:00am–8:00pm lead-local, 11:00am–1:00pm preferred. **Never a Sunday.**
**Angle:** direct, no fluff, real scarcity, and explicit permission to say no. The "tell me no and I'm out of your hair" line is what makes this convert — it removes the pressure that makes people ignore texts.

### SMS (HVAC canonical)
```
[FIRST] - last one from me. I've got [N] spots left this week for [ISSUE]: [DAY] am or [DAY] pm: [BOOKING_LINK] STOP to end
```
*Rendered:* "Karen - last one from me. I've got 2 spots left this week for AC quotes: Thu am or Fri pm: go.millerheating.co/bk12 STOP to end" — **126 chars.**

**Seasonal-urgency variant, HVAC only** (Mar–Jun cooling, Sep–Nov heating — mirrors Pillar 1 §1) — "Karen - last one from me. First hot week hits and I'm booked solid for 10 days. 2 quote slots left this week: go.millerheating.co/bk12 STOP to end" *(145)*
**Plumbing** — "Karen - last note from me. 2 slots left this week for the water heater, Thu or Fri. Want one? go.aceplumbing.co/bk12 Or reply NO and I'm done." *(141)*
**Electrical** — "Karen - wrapping this up. I've got 2 openings left this week for panel quotes: go.aceelectric.co/bk12 Reply NO and I'll leave you alone." *(135)*

> ### The scarcity rule — read this before you deploy
> **`[N]` and the named days are pulled live from the client's dispatch board and must be literally true at send time.** If the board has eleven open slots, the message says eleven or the scarcity line gets dropped entirely and we fall back to the plain close. Pillar 1 §10 guardrail — *no fake scarcity* — is inherited here word for word. Manufactured urgency in a trade where the customer will meet your technician face-to-face on Thursday is a fast way to torch a client's reputation, and it is the exact behavior that makes homeowners distrust contractors in the first place.
>
> **Plain fallback when slots are plentiful:** "Karen - last one from me. Still happy to look at the AC and quote it free, no pressure: go.millerheating.co/bk12 Or reply NO and I'm out of your hair." *(150)*

### Email
**Subject:** closing this out
**Preview:** last one, then I'll stop

```
Last email from me on this, [FIRST].

I've got [N] quote slots left this week — [DAY] morning and [DAY] afternoon —
and after that I'm into next week's schedule.

If you want one: [BOOKING_LINK]

If it's handled, or you went another direction, just reply NO and I'll take
you off my list. No hard feelings at all — I'd rather know than keep
bothering you.

Either way, thanks for reaching out to us.

— [SENDER], [BUSINESS]
[DIRECT_PHONE] · Unsubscribe: [LINK]
```
*(85 words.)*

**Stop rule: three touches per channel and the sequence is over.** No Message 4 nudge, no "just bumping this to the top of your inbox." Non-responders drop into a **90-day hold**, then become eligible for Pillar 1's dormant reactivation database — which is where they belong and where they'll convert better anyway.

---

## 5. MESSAGE 4 — BOOKING CONFIRMATION SEQUENCE

Show rate in home services is not luck. It is these three messages. A homeowner has to be home, has to move a car, has to put the dog away — reminders are respect, not nagging.

### 4a — Immediate confirmation (fires within 60 seconds of the booking)
```
You're on the books, [FIRST]: [DAY] [WINDOW]. [TECH] will text when he's 20 min out. Nothing to prep, just need access to the unit. -[SENDER]
```
*Rendered:* "You're on the books, Karen: Thu 10/17, 2-4pm. Dave will text when he's 20 min out. Nothing to prep, just need access to the unit. -Bill" — **134 chars.**

**Plumbing tail** — "...just need a path to the water heater. -Bill" · **Electrical tail** — "...just need access to the panel. -Bill" · **Emergency same-day** — "You're set, Karen. Dave's headed your way now, ETA about 40 min. Shut the water off at the main if you haven't - I'll walk you through it if you call. -Bill" *(155)*

**Email confirmation** carries what SMS can't: the tech's name, the window, the address on file, what it costs (or that it's free), and a one-click reschedule link. **A reschedule link in the confirmation email raises show rate — it converts silent no-shows into moved appointments.**

### 4b — 24 hours before
```
[FIRST] - [TECH]'s coming tomorrow between [WINDOW] for [ISSUE]. Still good? Reply Y, or tell me a better day and I'll move it. -[SENDER]
```
*Rendered:* "Karen - Dave's coming tomorrow between 2 and 4 for the AC. Still good? Reply Y, or tell me a better day and I'll move it. -Bill" — **126 chars.**

The "tell me a better day" offer is deliberate. **We would much rather move an appointment than burn a truck roll on an empty driveway.** A reschedule at this stage costs the client nothing; a no-show costs them two hours of a technician's day.

### 4c — 2 hours before
```
[TECH]'s headed your way for the [TIME] - he'll text when he's 20 out. Anything I should tell him before he gets there? -[SENDER]
```
*Rendered:* "Dave's headed your way for the 2pm - he'll text when he's 20 out. Anything I should tell him before he gets there? -Bill" — **119 chars.**

That closing question is doing real work: it surfaces "the gate code is 4412," "the dog bites," "actually can he look at the upstairs unit too" — and every one of those is either a saved trip or an upsell.

**No reply to 4b?** One call attempt at the 2-hour mark before the truck rolls. In this trade a confirmed-by-voice appointment shows at a materially higher rate than a silent one, and the client is about to spend real money on fuel and labor.

---

## 6. MESSAGE 5 — NO-SHOW WIN-BACK

**Trigger:** technician marks "no access" / "customer not home" / appointment marked no-show in the FSM.
**Timing:** **within 30 minutes** of the failed visit — while they're feeling the "oh no, I forgot" — then one more at 48 hours. Both inside 8am–8pm local.
**Angle:** completely non-judgmental. No "you missed your appointment," no "our technician's time is valuable." People no-show because life happened, and they are already slightly embarrassed. The only job here is to make rebooking feel free of consequence.

### 5a — Same day (within 30 min)
```
[FIRST] - looks like we missed each other today. No big deal, happens. Want to grab another time? [REBOOKING_LINK] -[SENDER]
```
*Rendered:* "Karen - looks like we missed each other today. No big deal, happens. Want to grab another time? go.millerheating.co/rb12 -Bill" — **125 chars.**

### 5b — 48 hours later (one final touch, then stop)
```
[FIRST] - still want someone to look at [ISSUE]? Happy to come back out, no charge for the trip. [REBOOKING_LINK] Or reply NO and I'll close it out.
```
*Rendered:* "Karen - still want someone to look at the AC? Happy to come back out, no charge for the trip. go.millerheating.co/rb12 Or reply NO and I'll close it out." — **151 chars.**

**"No charge for the trip" must be cleared with the owner in writing** (§9 gate). Most 5–50 tech shops will happily eat one repeat trip on a quote; almost none will eat two. If the owner says no, cut that clause — the rest of the message still works.

### Email — same-day
**Subject:** we missed you today

```
[FIRST] — [TECH] swung by this afternoon and couldn't get anyone at the door.
No problem at all, it happens more than you'd think.

If you still want eyes on [ISSUE], pick whatever time is easiest here:
[REBOOKING_LINK]

And if the timing just isn't right, reply NO and I'll close it out — no
hard feelings.

— [SENDER], [BUSINESS]
[DIRECT_PHONE] · Unsubscribe: [LINK]
```
*(70 words.)*

**Hard stop: two win-back touches, then the lead is closed and moved to the 90-day hold.** Chasing a two-time no-show is how a client's phone number ends up flagged as spam by carriers.

---

## 7. Conversational reply handling (the part that isn't a sequence)

Most real bookings in this pillar come from a **back-and-forth**, not from a link click. Every inbound reply gets a human-sounding answer **within 5 minutes, 24/7**, and every answer ends by moving toward a time on the calendar.

**Three rules for every reply:** (1) answer the actual question first, (2) never quote a price by text, (3) close with a concrete next step — ideally two specific times.

| They say | Reply |
|---|---|
| "My unit's 18 years old, is it even worth fixing?" | "Honestly, sometimes yes and sometimes no - depends what failed. Dave can tell you in 20 min and I'll give you both numbers, repair and replace. Thu 2pm? -Bill" *(157)* |
| "How much is this going to cost?" | "Diagnostic's [X] and it comes off the repair if you go ahead. I won't guess at the repair number sight unseen - that's how people get surprised. Want a slot? -Bill" *(163 → trim `[X]` phrasing per client; **never quote a replacement by text**, route to owner per Pillar 1 §8)* |
| "Do you work on Trane / Rheem / Carrier?" | "Yep, we work on all of them - parts are the only thing that ever slows us down and we stock the common ones. Want me to get Dave out Thu? -Bill" *(142)* |
| "Are you licensed and insured?" | "We are - license [#] and I can send the insurance cert over if you want it for your file. Happy to bring a copy Thursday. -Bill" *(126)* |
| "Do you do financing?" | "We do, and approval takes about 5 min online - but let's find out what you actually need first before we talk money. Thu 2pm or Fri 9? -Bill" *(139)* |
| "Can you come today?" | "Let me check the board - what's your zip? If Dave's already out that way I can probably squeeze you in this afternoon. -Bill" *(123)* |
| "Just send me a price by email." | "I can send our diagnostic pricing, but an honest install number needs eyes on the equipment and the ductwork. 20 min visit, free, no pressure. Fair? -Bill" *(153)* |
| **"Am I talking to a real person?"** | **"Honest answer - I'm an AI assistant that answers for [BUSINESS] so nobody waits. Real techs do the work. Want me to have [SENDER] call you?"** *(~140)* |
| Anything about mold/asthma/health, injury, an insurance claim, a lawyer, a permit dispute, or a warranty coverage argument | **Do not answer. Route to the owner.** "That's a [SENDER] question, not mine - I'll have him call you today. What's a good time?" *(89)* |
| **"I smell gas" / "something's burning" / "sparking" / CO alarm** | **STOP. Do not troubleshoot, do not book.** "Get everyone out of the house now and call 911 and the gas company from outside. Once you're safe, call us at [DIRECT_PHONE]." *(148)* — then alert the client's dispatch immediately. |

**Escalate to the owner's phone, never to a form,** on: "flooded," "water damage," "no heat" with an elderly or infant household, "carbon monoxide," "lawyer," "BBB," "chargeback," or any mention of a competitor already having started work. Same trigger-word discipline as Pillar 2 §4.

---

## 8. Routing logic (one page — this is the whole engine)

```
Website form submit  ──┐
ads-agent lead webhook ─┼─→  suppression + consent check (§10)
Pillar 2 [SHARE_LINK]  ─┘         │
                                  ├─ prior STOP on this number ─→ NO TEXT. Call + email only (§10.2)
                                  │
                          emergency flag?
                             │           │
                            YES          NO
                             │           │
                    CALL in 60s     MSG 1 SMS + email in 60s (24/7 per §0.1)
                    + SMS backup         │
                    + dispatch alert     ├─ no reply/click 15 min ─→ two-option nudge
                             │           │
                             └───────────┤
                                         ├─ REPLY ──→ conversational handling (§7), 5-min SLA
                                         │              └─→ book by text
                                         ├─ BOOKED ─→ 4a confirm (60s) ─→ 4b (24h) ─→ 4c (2h)
                                         │                                      │
                                         │                          ┌───────────┴──────────┐
                                         │                       SHOWED                NO-SHOW
                                         │                          │                     │
                                         │            → hand to Pillar 2         5a (30 min)
                                         │              (rating request              │
                                         │               2-3h post-job)         no reply 48h
                                         │                                            │
                                         │                                        5b final
                                         │                                            │
                                         │                                     rebook or close
                                         ├─ no response 24h ─→ MSG 2 (8am-8pm local)
                                         ├─ no response 48h ─→ MSG 3 (8am-8pm, no Sunday)
                                         └─ still nothing ──→ CLOSE. 90-day hold ─→ Pillar 1 database
                                         
   STOP / opt-out at any point ─→ suppress permanently, all channels, all clients (§10)
```

**The Pillar 2 handoff is the compounding loop:** every lead this pillar books and shows becomes a completed job, which triggers Pillar 2's rating request 2–3 hours later, which produces a review and a referral, which arrives back here as a new inbound lead. Pillars 2 and 3 feed each other indefinitely at zero ad cost.

---

## 9. Fulfillment SOP (per client — starts only after Pillars 1–2 are live)

**Week 1 — wiring**
1. **Instrument every entry point.** Website contact form, "request service" form, quote/estimate form, footer form, chat widget, Google Local Services Ads leads, Facebook/Google lead-form ads from `ads-agent`, and the Pillar 2 referral flow. **A form we don't know about is a lead that waits 24 hours.** Audit the site page by page; owners routinely forget two or three forms.
2. **Fix the form before touching the copy.** Required fields: name, mobile, email, service needed (free text — this becomes `[ISSUE]`), address or zip, and **"Is this an emergency?"** as a visible checkbox. Remove every other field. Each additional field costs conversions, and we are being paid to produce booked jobs, not complete records.
3. **Consent language under the submit button** (plain, visible, unchecked-by-default where the client's counsel prefers it):
   > *"By submitting, you agree that [BUSINESS] may contact you by phone, text and email about your request, including with an automated system. Message and data rates may apply. Reply STOP to opt out. Consent isn't a condition of purchase."*
   Log the timestamp, IP, page URL and exact consent text with every submission. **That record is the client's defense if a TCPA complaint ever lands, and it is worth more than the retainer.** `client-success-agent` routes the final wording past client counsel — TCPA consent standards have moved repeatedly in recent years and we do not freelance on this.
4. **Sender identity:** the **same named human as Pillars 1 and 2.** A new name appearing in the customer's thread is the single clearest bot tell.
5. **Capture voice:** 15 minutes with the owner, steal three real phrases, put them in the copy. If he says "unit," don't write "system." Inherited from Pillar 1 §7.2.
6. **Build and test:** `[BOOKING_LINK]` and `[REBOOKING_LINK]` **tested on a phone, on cellular data, not on desktop wifi.** Booking calendar synced live to the dispatch board with real capacity and real drive-time buffers. Test-submit every form at 2am and confirm the text lands.
7. **Owner sign-off gate — blocking, all four:** (a) the free/flat-rate quote offer in Messages 2, 3 and 5b is real and will be honored; (b) capacity per day is confirmed and the calendar reflects it; (c) a named human is reachable for emergency escalations 24/7; (d) diagnostic pricing is confirmed in writing so §7 never improvises a number. **No sends until all four are green.** Same discipline as Pillar 1 §0 and Pillar 2 §9.5.

**Week 2+ — steady state**
8. Run the sequence. Monitor the reply queue continuously — **the 5-minute SLA applies to replies, not just first touches**, and that is where it most often slips.
9. **Log every single lead:** source, submit timestamp, first-touch timestamp, **response time in seconds**, replies, booked y/n, showed y/n, no-show recovered y/n, job value if it closed.
10. **Weekly report to `client-success-agent`** every Monday: median and 90th-percentile response time, leads by source, lead→booking rate, show rate, no-show recovery rate, revenue attributed, plus **any lead that waited longer than 5 minutes and why**. Misses get reported, not buried.
11. **Monthly:** hand `ads-agent` the conversion data by source and by ad. Speed-to-lead data is what makes paid traffic profitable — an ad set that produces leads that never book gets killed on our numbers, not on click metrics.

---

## 10. Consent, opt-outs and suppression

### 10.1 Inherited verbatim from Pillar 1 §6
STOP / STOPALL / UNSUBSCRIBE / CANCEL / END / QUIT / OPTOUT / REMOVE / "take me off" / "don't text" / "leave me alone" → **suppress instantly and permanently across SMS, email and voice, for every campaign and every client**, push to the shared permanent suppression list, send exactly one carrier-standard confirmation, never contact again.
```
You're unsubscribed from [BUSINESS] messages. You will not receive further texts.
```
*(80 chars.)*

### 10.2 The conflict case — a prior opt-out submits a new form
This will happen, and getting it wrong is how a client gets sued.

A previous STOP is a **revocation of consent to text that number.** A new form submission is a new request for contact — but it arrives through a channel that cannot prove the person understood they were re-subscribing. **Our rule: do not resume texting on the strength of a form fill alone.** Instead:
- **Call** them (they just asked to be contacted) and **email** them.
- Resume SMS **only** if they text us first, or explicitly re-opt-in by replying START/YES to a single one-time confirmation the client's counsel has approved.
- Never silently re-add a suppressed number to any list, from any import, ever. Pillar 1 §6 and Pillar 2 §10, same list, one list, forever.

### 10.3 Additional suppression for this pillar
Do not run the nurture sequence on: existing customers with an open job (route to dispatch, not to a nurture sequence); spam/bot submissions (honeypot + rate-limit); vendor and job-application submissions; commercial/property-manager inquiries unless the client sells commercial; leads outside the service area (send one honest "we don't cover your area, try [X]" and close — **do not** nurture someone the client can't serve).

---

## 11. KPI targets and the volume model

A 5–50 tech shop with a functioning website and Pillar 2 running produces roughly **40–150 inbound web/ad leads per month.** Model at 100:

| Stage | Rate | Result |
|---|---|---|
| Inbound leads | — | 100 |
| Contacted inside 5 min | **100%** | 100 |
| Engage (reply or click) | 45–60% | ~50 |
| **Booked** | **35–50%** | **~42 appointments** |
| Show | 80–88% | ~35 completed visits |
| No-shows recovered | 30–40% of the ~7 | ~2 rebooked and shown |
| → handed to Pillar 2 for review/referral | — | ~37 completed jobs |

**The comparison that sells this pillar:** the same 100 leads answered the next morning book at roughly 10–15%. We are not adding leads — we are recovering 25–35 appointments a month the client was already paying to generate and then losing to whoever picked up the phone first.

| Metric | Target | Failure signal |
|---|---|---|
| **Median first response time** | **< 5 min, 24/7 (target <60s)** | any month above 5 min = fulfillment failure, escalate |
| 90th-percentile response time | < 5 min | a long tail means the overnight or webhook path is broken |
| Emergency call-back time | < 2 min | any miss = same-day escalation to the owner |
| Reply SLA adherence | 100% within 5 min | slipping here quietly kills booking rate |
| Lead → booking | 35–50% | <25% → offer is weak or the booking link is broken on mobile |
| Show rate | ≥ 80% | <70% → reminders aren't firing or windows are too wide |
| No-show recovery | 30–40% | <20% → 5a is going out too late, tighten to 30 min |
| Opt-out rate | < 1% | >2% → cadence too heavy, cut Message 3 |
| Leads with no touch at all | **0** | any non-zero = an un-instrumented form, audit the site |

All logged per client, per lead, via `record_metric`.

---

## 12. Guardrails — standing, non-negotiable

- **Honor STOP instantly and permanently, across every channel and every client.** No re-imports, no "one last text," no per-campaign suppression.
- **Follow-up messages (2, 3, 5a, 5b) obey 8am–8pm recipient local time, no Sundays for Message 3.** Only the immediate reply to a just-submitted form runs around the clock, per §0.1.
- **If asked directly whether they're talking to an AI, answer honestly** — first time, every time, no deflection, no "I'm here to help!" The honest answer converts better than the dodge anyway, and one caught lie ends the client relationship.
- **Medical, legal, insurance-claim, permit and warranty-dispute questions are never answered.** Routed to the business, same hour.
- **Gas smell, burning smell, sparking, CO alarm: safety instruction and 911 first, dispatch second, booking never.** Do not troubleshoot a hazard by text.
- **Never quote a replacement or install price by text.** Diagnostic/trip pricing only, exactly as the owner confirmed it in writing. This is a $5K–$12.5K conversation and it belongs to the owner.
- **No fake scarcity.** `[N]` slots and named days come off the live dispatch board or the line gets dropped. Inherited from Pillar 1 §10.
- **Sender is always a real named human at the business** — never "the team," never the agency, never a bot persona. Same name across Pillars 1, 2 and 3.
- **Three touches, then stop.** Two win-backs, then stop. Non-responders go to the 90-day hold, not into another sequence.
- **Never promise a call we don't place.** The 2-minute emergency callback is a hard commitment.

---

## Handoffs

- **`sales-agent`:** this is the first upsell after the Pillars 1+2 starter bundle. Sell §11's comparison — *"you're already buying these leads; you're losing 25 of them a month to a 24-hour response time"* — never a promised booking count.
- **`ads-agent`:** **blocked from launching until this pillar is live on the client.** Paying for clicks that land in a form nobody answers for a day is setting money on fire. Every ad lead enters this sequence via webhook; conversion-by-source data flows back monthly.
- **`reactivation-agent`:** shares the permanent suppression list and inherits our 90-day-hold non-responders into the dormant database. Sends us every emergency-flagged YES per Pillar 1 §5.
- **`reviews-referrals-agent`:** every showed-and-completed appointment we book is handed over for the 2–3h post-job rating request. Their `[SHARE_LINK]` referral bookings come back to us at the 60-second SLA.
- **`client-success-agent`:** Monday report per §9.10, including every SLA miss. Median response time is the headline number on the client's dashboard — it is the most visible, most defensible proof of value we produce, and it is the one metric an owner can verify himself by filling out his own form at midnight.
- **`voice-ai-agent` (Pillar 5):** inbound *calls* that go unanswered are the mirror image of this problem. Missed-call-text-back fires this same Message 1 within 60 seconds of a dropped call.

**Status: BUILT.** Ready to deploy on the first client the day Pillars 1–2 are live and the §9.7 owner gate is green.
