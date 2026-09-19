# Phase 6 — Ad Intelligence & Master Ad Kit
**Agent:** ads-agent · **Phase:** 6 (build once, localize per client)
**Niche (locked Phase 1):** Residential home services — HVAC, plumbing & electrical contractors, US, owner-operated, 5–50 technicians (roofing/solar adjacent)
**Status:** BUILT. Blocked from deployment on any client until that client's month-one reactivation revenue is collected (Pillar 1 §11).

---

## 0. Provenance & confidence ledger (read first)

I do not have a direct Meta Ad Library integration. Every competitor ad below was collected from published 2025–26 ad-teardown sources that screenshot and cite live Ad Library placements. That is a weaker evidence grade than pulling the Library myself, and I am labelling it rather than hiding it.

| Evidence | Grade | Source |
|---|---|---|
| Ad copy lines quoted in §1 | **MEDIUM-HIGH** — quoted verbatim from teardowns; two are explicitly Ad-Library-sourced (Peterman Brothers, Greens Energy Services, via GetHookd) | gethookd.ai, hookagency.com, simprogroup.com, getjobber.com |
| Structural patterns in §1–§2 | **HIGH** — the same pattern recurs across all five independent sources | as above |
| CPL benchmarks in §6 | **MEDIUM** — third-party aggregated benchmarks, ranges not point estimates | webtonic.io (citing PipelineOn/AdAmigo), sparkugc.com, stackmatix.com, plumbingwebmasters.com |
| Meta Special Ad Category rules in §7 | **HIGH** | jonloomer.com, takeflyte.com |
| "Family imagery outperforms equipment photos by ~40%" | **LOW** — single vendor blog, no methodology published. Treat as a hypothesis to A/B test, **not** a fact to quote to a client. | simprogroup.com |
| Any dollar result promised to a client | **NOT ASSERTED.** §6 is a model with stated inputs, never a guarantee. | — |

**Standing duty:** once a client ad account exists, pull 5 live local competitor ads from the Meta Ad Library directly and re-run this analysis for that metro. Ad Library no longer shows likes/comments/shares (per Hook Agency), so the only free proxy for "this ad is winning" is **longevity** — an ad running 60+ days is being paid for because it works. Sort by first-seen date, not by looks.

---

## 0b. THE OFFER — a required correction to my brief

My standing brief names the gym niche's proven offer ("6 weeks free"). **We are not in the gym niche.** Running "free" as a cold-traffic front end in home services is a documented failure mode: generic no-hook "free estimate" offers push CPL above ~$150 with materially worse lead quality (PipelineOn 2026 data via Web Tonic). A free truck roll sold to a stranger on Facebook attracts tire-kickers; a free truck roll offered to *your own dormant database* (Pillar 1) works because the relationship already exists.

**The proven paid-ads offer for this niche is the price-anchored, deadline-dated seasonal tune-up.**

> ### 🎯 MASTER OFFER: "$89 21-Point System Tune-Up — booked before [DATED DEADLINE]"
> HVAC canonical. Plumbing swap: **$89 Whole-Home Plumbing & Water-Heater Inspection**. Electrical swap: **$89 Whole-Home Electrical Safety Inspection**.

Why this and not something else:
1. **It is the pattern that actually recurs in the winning ads** (§1b) — every high-performing example anchors a specific dollar figure to a specific named service with a deadline.
2. **A small paid commitment is a qualification filter.** $89 costs the homeowner enough to screen out browsers, and costs less than the contractor's truck roll — so the front end roughly washes its face and the ad budget is buying *access*, not discounts.
3. **The money is the back end.** A technician standing in front of a 14-year-old system is the highest-probability path to the $5,000–$12,500 replacement that pays for everything (Phase 1 §1). We are buying qualified in-home appointments, not tune-up revenue.
4. **It reuses the "21-point" asset already built in Pillar 1** — one mechanism, two channels, consistent client-side language.
5. **No brand-discount conflict.** A priced service promotion is far easier to get past a One Hour / Benjamin Franklin / Mr. Rooter franchisor than co-branded discount creative.

**Price is a variable, not a doctrine.** $79–$99 is the working band. Set it below the client's standard diagnostic fee (commonly ~$189) so the anchor is visible, and never below their true truck-roll cost. Confirm the number in writing with the owner before launch — same gate discipline as Pillar 1 §0.

---

## 1. PATTERN BREAKDOWN

### 1a. The source set

| # | Advertiser / source ad | Category | Where documented |
|---|---|---|---|
| A | **Peterman Brothers** — seasonal question hook, price-anchored offer | Plumbing/HVAC seasonal promo | Meta Ad Library, via GetHookd |
| B | **Greens Energy Services** — emergency question + reassuring answer, click-to-call | HVAC emergency | Meta Ad Library, via GetHookd |
| C | **Filterbuy** — video/Reel, man holding a filthy air filter, conversational hook | HVAC education→retargeting | GetHookd teardown |
| D | **Unnamed HVAC advertiser** — "Furnace fails to turn on?" + free no-registration guide | HVAC lead magnet | Hook Agency teardown |
| E | **Hook Agency's own recommended plumber script** — "$200 OFF + 0% financing" water-heater ad | Plumbing replacement | hookagency.com |
| F | **Metropolitan Heating and A/C Ltd** — problem callout + solution + contact CTA; **QRC** — humour video, team destroying an old AC unit | HVAC brand/response | Jobber teardown |

### 1b. HOOKS — the first-line pattern

**The dominant pattern is the second-person problem question.** Four of six lead with a question that names the homeowner's exact situation, not the company:

- *"Furnace fails to turn on?"* (D)
- *"AC Not Cooling? Emergency Repair Available Today"* (recommended-pattern headline, GetHookd)
- Greens Energy (B) leads with a direct emergency question and immediately answers it reassuringly.
- Peterman Brothers (A) leads with a **seasonal** question rather than an emergency one, then anchors a price.

The video/Reel variant is the same logic in a human voice: *"Your AC is going to fail this summer, here's how to know before it does"* — a technician talking straight to camera in the first three seconds.

**What loses, explicitly:** company-name-first and service-list openers. GetHookd's stated finding is that problem-specific headlines beat "Professional HVAC Services" because they create a pattern interrupt for someone who is *not searching*. Simpro frames the same rule as service-centric vs customer-centric: **"We fix AC" is about you; "Sleep comfortably tonight" is about your customer.**

**Sub-pattern — the geo-salutation.** Hook Agency's plumber script opens *"Hey [CITY] homeowners!"*. Cheap, ugly, and it works, because it self-qualifies the scroll in three words.

**Not a pattern (do not invent one):** I found **no** consistent use of curiosity/withheld-information hooks, no consistent testimonial-led openers, and no consistent shock-stat openers. Home services hooks are literal. Don't get clever.

### 1c. PROMISES — outcomes, numbers, timeframes

Three promise types, and they are cleanly segregated by buying temperature:

| Temperature | Promise shape | Live examples |
|---|---|---|
| **Hot** (system is down) | **Speed.** "Available Today", same-day, we answer now | B, and the "Emergency Repair Available Today" pattern |
| **Warm** (seasonal, planning) | **A specific dollar price on a specific named service, with a dated deadline** | *"$79 Spring AC Tune-Up, Book Before May 31st"*; Peterman Brothers' price-anchored seasonal offer (A) |
| **Cold** (big-ticket, off-season) | **A monthly payment, to kill the price objection before it forms** | *"$200 OFF + 0% financing for 12 months"* (E); *"as low as $129/month"* (Simpro's off-season replacement pattern) |

Consistent across all of them: **the number is specific and the deadline is a named date.** "Save big" and "limited time" do not appear in the winning set. GetHookd's stated reason is that specificity builds trust and a deadline creates action.

**Trust numbers ride shotgun, never lead:** "Serving [City] for 15+ Years", a local phone number, city-specific reviews. They appear in the body or the overlay, never as the hook.

**Timeframe honesty:** the seasonal promise works because it's tied to a real weather event. Simpro's sharpest observation is that the most common mistake is running seasonal HVAC ads *once it's already hot* — by June every competitor is bidding. The promise "before the first hot week" only lands if you're running in March–May.

### 1d. CTAs

Ranked by how often they appear, and they map to temperature:

1. **Click-to-call** — hot traffic. Removes every step between the problem and the phone ringing. Highest converting for emergency intent.
2. **On-platform lead form (Meta Instant Form)** — warm traffic. GetHookd's explicit recommendation is to pair the priced tune-up with a lead form so the homeowner books without leaving Facebook. Lowest friction, **lowest-quality lead** — this is why §5's 5-minute rule is non-negotiable.
3. **"Book before [date]"** — the deadline *is* the CTA in the seasonal ads.
4. **Zero-friction content CTA** — ad D offers a free guide with **no registration required**, deliberately lowering resistance and feeding a retargeting pool rather than a lead list.

Every CTA in the set is **one action**. No ad asks the reader to call *and* fill a form *and* visit the site.

### 1e. STRUCTURE

- **Length: short.** Primary text runs roughly 25–60 words. The offer is visible above the "See more" fold — assume ~125 characters before truncation and put the price there.
- **Order is fixed:** Hook (problem question) → offer with price/number → 2–4 short lines of body → trust line → CTA. Nobody buries the offer.
- **Bullets vs paragraphs:** short single-line paragraphs and emoji-bulleted lists both appear; the plumber script (E) uses emoji bullets. **Bullets carry the "what you get" list; paragraphs never exceed two lines.** Wall-of-text ads are absent from the winning set.
- **CTA placement:** last line of the primary text, plus the platform CTA button. Never mid-body only.
- **Format split:** static image/carousel for offer ads; vertical Reels for top-of-funnel education. Reels are the fastest-growing Meta placement and win on a raw, phone-shot, conversational feel — polished corporate video underperforms native-looking video.

---

## 2. VISUAL CREATIVE BREAKDOWN

**Image type — three families, in descending frequency:**
1. **The technician as a human being** — a real, named, uniformed tech, often pointing at or holding something. Filterbuy (C) is the archetype: a man holding a visibly filthy air filter. The prop does the persuading.
2. **Outcome/comfort imagery** — a family comfortable at home, kids and pets in comfort situations. Simpro claims this beats equipment photos by ~40% (**LOW confidence, unverified — test it, don't quote it**).
3. **Problem imagery** — the old, rusted, failing unit. Used as a before-state and as the hook for replacement ads.

**Losing visual: the equipment beauty shot and the branded truck alone.** Neither carries a human face or a problem.

**Colour palette:** high-contrast and temperature-coded. Cooling/AC creative runs cool blues and whites; heating/furnace creative runs warm oranges and reds; urgency/emergency creative runs red-and-yellow accent blocks. Backgrounds are bright and residential — daylight interiors, driveways, front yards. Dark or studio-lit creative is essentially absent.

**Text overlay:** present on nearly every static. Rules observed: **≤7 words**, the dollar figure at the largest point size, deadline in a contrasting accent block. Overlay must be readable as a thumbnail and readable **with sound off** — the sources are unanimous that vertical/square, sound-off-legible creative is the baseline for Reels.

**Face presence:** high, and it is the single strongest differentiator. Faces are local, non-stock, and often mid-action. Stock photography reads as an ad; a real tech reads as a neighbour.

**Visual hierarchy (dominant, in order):** face or prop → dollar figure → deadline → logo. **Logo is last and small.** Nobody's winning ad is a logo showcase.

**Which style dominates and why:** the **real-technician-with-a-prop, daylight, one-dollar-figure-overlay static** dominates offer campaigns, with **raw vertical Reels** dominating top-of-funnel. It wins because home services is a *trust-at-the-door* purchase — the homeowner is deciding whether to let a stranger into their house. A recognisable local human face pre-answers that question in a way no equipment photo can.

**⚠️ Risky to copy — flagged per guardrail:**
- **Never** reuse Peterman Brothers', Greens Energy's, Filterbuy's or QRC's creative, layouts, logos, taglines, or mascots. Copy the *pattern*, never the asset.
- **Never** name another company's customers, or reuse their review screenshots.
- **Never** use a stock model and imply they're the client's technician. Shoot the client's actual crew — with written permission on file for every face used.
- **Never** stage a "before" photo. A rusted-unit photo must be a real job the client did.
- The QRC-style humour ad (destroying a customer's old AC) is high-variance brand creative that depends on production quality and a tolerant franchisor. **Do not lead a new account with it.**
- Franchisee clients (One Hour, Benjamin Franklin, Mister Sparky, Mr. Rooter, Aire Serv, Mr. Electric): franchisor creative and co-op rules govern logo use, colour and claims. Get written approval before any branded creative runs. The priced tune-up survives this; discount-heavy creative often doesn't.

---

## 3. THE WINNING FORMULA

> ### THE HOME-SERVICES DIRECT-RESPONSE TEMPLATE
>
> **HOOK** — one line, second person, names the problem or the season, ends in a question mark. Include the city if it fits in the first five words. *No company name in the hook.*
>
> **PROMISE** — one line. A specific dollar figure + a specifically named service + a named-date deadline. (Hot traffic substitutes speed for price: "someone at your door today.") Must clear the 125-character fold.
>
> **BODY** — 2–4 short lines or emoji bullets. What the visit includes → what it costs → one local trust signal (years serving [City] / license # / review count). Nothing else. Under 60 words total.
>
> **CTA** — one action only, on the last line, matched to temperature: click-to-call (hot) / Instant Form (warm) / "Book before [date]" (seasonal). Mirror it on the platform CTA button.
>
> **VISUAL** — daylight photo of the client's real, uniformed technician, ideally holding the diagnostic prop. Text overlay ≤7 words with the dollar figure largest and the deadline in a contrast block. Cool palette for cooling, warm for heating, red accent for emergency. Logo small, bottom corner. Square 1:1 for feed, 9:16 for Reels/Stories, legible with sound off.
>
> **SEASONALITY GOVERNS EVERYTHING.** Cooling offers Mar–Jun. Heating offers Sep–Nov. Off-peak, switch to replacement-planning and maintenance-plan angles. Never launch a cooling promo in July into a fully-bid auction.

---

## 4. THREE AD VARIATIONS FOR OUR OFFER

All three are HVAC-canonical with plumbing/electrical swap-ins. `[BRACKETS]` are per-client variables. All claims are structural — no invented testimonials, no fabricated statistics, no before/afters we don't own.

---

### VARIATION 1 — "The Seasonal Tune-Up" (workhorse — 60% of budget)
**Temperature:** warm · **Objective:** Leads (Instant Form) · **Season:** Mar–Jun (cooling) / Sep–Nov (heating)

**Headline:** $89 21-Point AC Tune-Up — Booked Before [FRIDAY, MAY 30]

**Primary text:**
> [CITY] homeowners — when did your AC last get looked at?
> $89 gets you our full 21-point check before the first hot week hits.
> ✅ 21 points checked, top to bottom
> ✅ Written report before we leave — no verbal "trust me"
> ✅ [NAME], licensed in [STATE], serving [CITY] since [YEAR]
> We take [N] of these a week and the calendar closes [DATE].
> Tap below and pick your time.

**CTA:** Book My $89 Tune-Up *(button: Book Now)*

**Visual direction:** Square 1:1. Daylight, driveway or side-of-house. [CLIENT]'s actual technician in branded uniform, kneeling at a condenser unit, gauges in hand, looking at camera. Cool blue/white palette. Overlay top third: **"$89 · 21-POINT AC CHECK"** — dollar figure largest. Bottom-right accent block, orange on white: **"BOOK BY [DATE]"**. Logo small, bottom-left. Shot on a phone, not a studio.

**Swaps:** *Plumbing* — "$89 Whole-Home Plumbing & Water-Heater Inspection", prop = water heater + inspection clipboard. *Electrical* — "$89 Whole-Home Electrical Safety Inspection", prop = open panel with tech pointing, tester in hand.

---

### VARIATION 2 — "No Cool Air" (hot traffic — 25% of budget)
**Temperature:** hot · **Objective:** Calls (click-to-call) · **Season:** heat waves / cold snaps, always-on at low budget

**Headline:** AC Not Cooling? We Answer the Phone.

**Primary text:**
> AC running but blowing warm?
> Call [CLIENT] — a real person picks up, and we'll tell you straight if we can get someone out today.
> 🔧 [N] trucks on the road in [CITY]
> 🔧 Licensed & insured, [STATE] #[LICENSE]
> 🔧 Upfront price before any work starts — you approve it or we pack up
> No hold music. No callback queue.

**CTA:** Call [PHONE] Now *(button: Call Now)*

**Visual direction:** 9:16 vertical, also cut 1:1. Frame 1: technician stepping out of the branded van, door open, mid-stride — motion, not a pose. Red/white urgency accents on a daylight base. Overlay: **"NO COOL AIR? WE'RE ON IT."** Second line smaller: **"[CITY] · SAME-DAY WHEN WE CAN"**. Alt Reel cut: 12s, tech straight to camera — *"If your AC's blowing warm right now, here's the one thing to check before you call anybody."* Raw, handheld, captions burned in.

**⚠️ Copy discipline:** "same-day **when we can**" and "we'll tell you straight if" — never a flat same-day guarantee unless the owner confirms in writing they will honour it every time. Same rule as Pillar 1 gate 1: a promise the client won't keep burns the account.

**Swaps:** *Plumbing* — "No Hot Water? We Answer the Phone." *Electrical* — "Breaker Keeps Tripping? We Answer the Phone."

---

### VARIATION 3 — "The 15-Year Question" (cold/off-season replacement — 15% of budget)
**Temperature:** cold, high-ticket · **Objective:** Leads (Instant Form, qualified) · **Season:** Jul–Aug and Dec–Feb shoulder months

**Headline:** Is Your System Older Than Your Teenager?

**Primary text:**
> Most systems in [CITY] start failing somewhere past year 15.
> If yours is in that range, get the honest version now — while you can plan it, not at 11pm in August when you have no choice.
> Free replacement assessment: we size it, price it in writing, and tell you if you should wait.
> [NAME] has been doing this in [CITY] since [YEAR].
> No pressure. If it's got years left, we'll say so.

**CTA:** Get My Written Assessment

**Visual direction:** Square 1:1, split-frame. Left: a genuinely aged unit from one of [CLIENT]'s real jobs — rust, weathering, no staging. Right: the new install, same shoot. Neutral warm palette. Overlay across the seam: **"15+ YEARS OLD?"**; below: **"FREE WRITTEN ASSESSMENT · [CITY]"**. Alt creative: technician at a kitchen table with a homeowner, paperwork visible, faces relaxed — sells "planning conversation", not "sales visit".

**🔶 Financing variant (3B) — COMPLIANCE-GATED.** The proven high-performer here leads with a monthly payment ("as low as $129/month", "0% financing for 12 months"). **Adding financing language flips the ad into Meta's Credit / Financial Products Special Ad Category.** That means: advertiser verification (Meta mails a physical postcard — start ≥2 weeks before launch), no targeting by age or gender, no detailed demographic targeting, no ZIP-code targeting, and a **minimum 15-mile radius** — which materially breaks tight service-area targeting for a single-location shop. **Rule: never bolt a monthly payment onto an existing ad set.** Run 3B only in a separately configured, verified campaign, and only when the client's service radius is ≥15 miles. Otherwise run Variation 3 as written, with zero credit language.

---

## 5. FULFILMENT PROCEDURE (per client)

1. **GATE — reactivation revenue collected.** Confirm the day-30 Pillar 1 report shows collected cash before a dollar of ad spend. No exceptions, no "we'll start ads while reactivation runs." Cash from the database funds the ads; that sequencing is the whole reason the model works without the client fronting risk.
2. **Written offer confirmation** — exact tune-up price, exact deadline, weekly appointment capacity, and whether same-day language may be used. Same gate discipline as Pillar 1 §0. Overbooking a contractor is worse than underspending.
3. **Local Ad Library pull** — 5 live competitor ads in the client's metro, sorted by first-seen date. Re-run §1 for that market. Do not clone; find the gap.
4. **Creative shoot** — one hour with the client's real crew produces every asset above. Written permission for each face on file.
5. **Localize** — city, tech names, license number, year established, phone, capacity number, seasonal timing for the client's actual climate zone.
6. **Launch** — Variations 1/2/3 at 60/25/15. Radius: the client's real service area (typically 10–20 miles), homeowners 30–65 (drop age targeting entirely on any Credit-category campaign). Exclude existing active customers via custom audience on cold campaigns; run maintenance-plan offers *to* that audience separately, since a past payer is the easiest convert.
7. **Instant handoff** — every lead goes to `lead-nurture-agent` the moment it lands. The 5-minute rule from Pillar 3 applies identically to ad leads. On-platform form leads are the lowest-intent leads we generate and decay fastest; a four-hour callback turns a $50 lead into a competitor's job.
8. **Emergency routing** — any Variation 2 lead mentioning no heat / no cooling / leak / burning smell / no power goes straight to the client's dispatch, not into a booking funnel. Same escalation rule as Pillar 1 §5.
9. **Weekly review** — kill and scale per §6 rules. Report cost-per-show to `client-success-agent`.

---

## 6. BENCHMARKS, MODEL & KILL RULES

**External CPL benchmarks (MEDIUM confidence, ranges not targets):** home-services Meta CPL averaged ~$34 in 2026, up from ~$30.57 in 2025 (AdAmigo via Web Tonic). By lead type: tune-up/service ~$35–65, maintenance plan ~$40–80, replacement estimate ~$80–150. Generic "free estimate" with no service hook frequently exceeds $150 with worse quality. Home-services CPC runs ~$1.20–2.80. Cross-industry form-fill CPLs near $27 are a **floor to plan above, not a plumbing target**.

**Working model at $3,000/mo client spend** — *inputs stated, outputs are arithmetic, not a promise:*

| Input | Value |
|---|---|
| Spend | $3,000 |
| Blended CPL | $50 → **60 leads** |
| Lead→booked (5-min response) | 35% → **21 booked** |
| Show rate (24h + 2h reminders) | 70% → **~15 shows** |
| **Cost per show** | **~$200** |
| Shows → replacement quote | 30% → ~4–5 quotes |
| Quote close rate × $8,000 avg ticket | 40% → **~$14–16K attributed** |
| Modelled ROAS | **~5×** (plus tune-up fees, repairs, plan enrolments) |

At the blueprint's ~$7,900/mo benchmark the same inputs give ~158 leads → ~55 booked → ~39 shows. **Every figure here is a model. Never state it to a prospect as a result.**

**KPIs logged via `record_metric` per client, per campaign:** cost per lead · cost per booked appointment · **cost per show (the north star)** · time from ad lead to first response (target <5 min, this is the metric that moves all the others) · show rate · client ROAS on attributed jobs.

**Kill / scale rules (weekly):**
- Kill any ad set at **2× target CPL after 50+ leads' worth of spend**. Not before — seasonal volatility is wide.
- Kill any creative whose **cost per show** is 2× the account average, even if its CPL looks great. Cheap leads that never open the door are the most expensive thing we buy.
- Scale winners **≤20% budget increase every 3 days**. Faster resets learning.
- Refresh creative every **4–6 weeks** or when frequency >2.5 in a tight service radius.
- If lead→booked drops below 25%, the problem is almost never the ad. Audit response time first.

---

## 7. GUARDRAILS (standing)

- **No fabricated claims, testimonials, before/afters, or statistics.** Every review quoted must be a real, verifiable review of that client. Every before/after must be that client's real job.
- **No competitor brand assets, logos, taglines, mascots, or client names. Ever.** Copy patterns, not property.
- **No health or safety claims.** "Improves your family's health", "eliminates allergens", "prevents carbon monoxide poisoning" — all out. Air quality is described functionally, never medically.
- **No personal-attribute targeting or copy** that asserts knowledge about the reader (income, health, financial hardship). "Struggling to afford your energy bill?" is a policy risk; "Older system? Here's what to check" is not.
- **Financing / monthly-payment language = Meta Credit Special Ad Category.** Separate verified campaign, 15-mile minimum radius, no demographic targeting. Never retrofit onto a live ad set.
- **Franchise clients:** franchisor written approval on branded creative before launch.
- **The offer must be real and honored** — price, deadline, and any same-day language confirmed in writing by the owner. If the deadline is Friday, it ends Friday.
- **Never launch ads before Pillars 1–3 are live and reactivation cash is collected.** An ad lead landing in a shop with no speed-to-lead process is money set on fire.

---

## 8. HANDOFFS

- **`lead-nurture-agent`:** every ad lead, instantly. 5-minute rule, no distinction between ad leads and reactivation leads. Emergency keywords escalate to dispatch.
- **`client-success-agent`:** weekly cost-per-show and ROAS reporting; the month-3 ad ROAS number is a referral asset alongside the Pillar 1 day-30 figure.
- **`sales-agent`:** do **not** sell ads as a month-one deliverable. Ads are the month-two-plus upsell, funded by month-one reactivation cash. Sell the sequence, not the ad budget.
- **`reactivation-agent`:** the "$89 21-point tune-up" ad offer and the "free 21-point check" reactivation offer share one mechanism and must share one client-side vocabulary. Coordinate wording per client so a homeowner who sees both isn't confused about the price.

**Status: BUILT.** Localization blocked per §5 gate 1 until a client clears REACTIVATION.
