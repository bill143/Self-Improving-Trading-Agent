# How JP Middleton Built a $5.4M AI Agency — The Blueprint

> Sources: JP Middleton, *"How I Built an AI Agency Worth $5.4M As A Beginner So You Can
> Just Copy Me"* (YouTube, youtube.com/watch?v=B2ccMEiFOMk) and his companion
> *"AI Agency Golden Nuggets"* 7-day system document. His agency is **Gym Members Now**
> (gym/fitness niche): valued at **$5,448,000**, ~**$5.7M profit 2021–2024**,
> **$17M+ revenue over 4 years**, 1,300+ local-business clients closed from 3,000+
> sales calls, 2,000+ gyms served.

This document is the operating manual for the autonomous agent team in
`.claude/agents/` and `agency_team/`. Every agent's MD file traces back to a section
here.

---

## 1. The business model in one paragraph

Sell **one bundled AI system** to local businesses in **one niche**, delivered as an
identical "conveyor belt" for every client. The system does the only thing local
business owners will pay serious money for: **generate sales appointments that turn
into revenue, without the owner or staff lifting a finger.** Get clients via cold
calling, close them on a Zoom call with a fixed 7-step framework, collect payment on
the spot, deliver results, then farm referrals — especially inside franchises, where
one happy franchisee can refer hundreds of locations.

Core mantra from the video: **"Fancy fails, simple scales."**

## 2. The five services (sold as one bundle)

None of these is very valuable alone; together they are an extremely valuable system.

| # | Service | What it does | Key facts from the video |
|---|---------|--------------|--------------------------|
| 1 | **AI Database Reactivation** | Re-engage the client's old/dormant leads by SMS+email with a compelling offer; drive them into booked appointments | ~$1,500, compressed into one month; thousands of dead leads sit in every local CRM; zero ad spend needed |
| 2 | **AI Reviews & Referrals** | Plug into the active-customer list; ask for feedback with a raffle offer (e.g., "win a free year"); positive → Google review → auto-respond → referral ask with a guest-pass landing page | Only positive reviews get requested; referrals from happy customers are the best leads a business can get; boosts Google ranking for "X near me" searches |
| 3 | **Website Lead Nurturing (Speed-to-Lead)** | Reply to every website form lead within 5 minutes, 24/7, and drive to booking | Harvard study: response after 5 minutes drops conversion by ~400%; search-intent leads are the hottest leads |
| 4 | **AI Missed-Call Voice Agent** | Phone rings 10 seconds; if staff doesn't pick up, the AI receptionist answers, qualifies non-members, and books tours/consults 24/7 | Local businesses miss 60–70% (one client: 91%) of calls from prospective customers; ~$1,200/mo tooling cost (Synthflow + CallTrackingMetrics) — sell this later, not first |
| 5 | **Paid Ads + AI Lead Nurture** | Run the niche's proven offer (for gyms: the "6-week challenge"), nurture every ad lead to show | Every niche has one proven offer + follow-up + sales process; find it in the Facebook Ad Library by studying agencies already winning in the niche; fund the ads with reactivation revenue |

**Start with services 1+2** (cheap to deliver, easy to sell). Add 3 and 5 next.
Sell 4 last (hardest to sell, highest tooling cost).

## 3. The build sequence (the exact order)

From the video's six steps, merged with the 7-day system:

1. **Copy someone who has done it.** Follow a proven operator's playbook exactly
   (that is what this repo encodes). Vet any mentor: real business, real
   testimonials, real reviews.
2. **Pick the niche (Day 1).** Non-negotiable filters:
   - Physical, location-based businesses where customers walk in (gyms, med spas,
     chiropractors, dental, HVAC, roofing, solar, plumbing, pest control, martial
     arts/yoga/pilates studios, auto detailing…).
   - Each customer worth **$500+ per transaction or $100+/mo recurring**.
   - **Proven demand**: other agencies already making $100K–$500K/mo in that niche
     (competition = validation, not deterrent).
   Rank the top 3 given your unfair advantages; pick #1.
3. **Target franchises (Day 2).** "Choose your ship": find the top 10 franchise
   brands in the niche with 30+ locations, an active franchisee community
   (Facebook groups, conferences, advisory boards), and recent growth. One
   well-connected franchisee referred JP to 200+ businesses — this is how he went
   from $2K/mo to $70K/mo in 12 months.
4. **Build the offer pillars (Days 3–5).** Build the complete campaign assets for
   Database Reactivation, Reviews & Referrals, and Website Lead Nurture *before*
   selling, so fulfillment is a conveyor belt from client #1.
5. **Get clients (Day 6).**
   - Scrape a list of **1,000 target businesses** in the niche (AI-scraped, no
     purchased lists).
   - Study the Facebook Ad Library for the niche's winning ad patterns.
   - **Cold call** (the highest-ROI channel — you pick exactly who you call).
     Script angle: *"We're an AI-based [niche] optimization company. After running
     test ads in your area we found strong demand for your services if you leverage
     our new ChatGPT-4 plugin. Are you available today for a 30-minute Zoom call, or
     would tomorrow work better?"* JP's team went **$0 → $260K/mo in ~10 months**
     with one closer and one good cold caller.
6. **Sell with the 7-step framework (Day 7), close on the spot.** Payment first,
   agreement second, onboarding third — in that order, on the call.
7. **Deliver, then compound.** Get results, keep the relationship, ask for
   referrals, expand through the franchise network, become the preferred vendor.

## 4. The 7-step sales framework (verbatim structure)

1. **INTRO** — establish authority and rapport; 1–2 min human moment; then take
   control as "the boss running the meeting."
2. **DISCOVERY** — diagnose with black-and-white numbers: marketing spend, monthly
   leads, booking rate, show rate, close rate, actual profit. Build doubt with
   pillar-based questions ("How do you get reviews? How do you handle missed calls?
   How fast is your lead follow-up?"). End with the killer question: *"Realistically,
   with your current strategy, do you think you'll hit your goals in the next 3–6
   months if you don't change anything?"*
3. **TRANSITION** — *"Is there anything else we haven't covered that would help me
   better understand your situation?"*
4. **AUTHORITY POSITIONING** — *"Based on what we've covered, I've got a good
   understanding of where you're at and where you want to get. My area of expertise
   is helping [niche] owners just like you. Can I walk you through our process?"*
5. **PITCH** — Logical pain → emotional pain → AI solution → benefits, weaving the
   prospect's own words back in ("You know how you told me…"). After each pillar:
   *"What questions do you have on that specifically?"*
6. **TEMPERATURE CHECK** — *"On a scale of 1–10 … where would you say you fall?"*
   Under 9 → re-loop: *"Why aren't you a 1? What would make you a 10?"* (they list
   what they like; isolate the real objection).
7. **CLOSE** — *"First we process payment, second we sign the agreement, third we
   schedule your onboarding."* Say **"investment," never "price."** State the number,
   then **shut up**. Terms: 12-month agreement with a 30-day out in the first month.

## 5. Tooling stack (as used by the presenter)

| Purpose | Tool |
|---------|------|
| CRM + SMS/email automation (services 1–3, 5) | GoHighLevel |
| AI voice receptionist (service 4) | Synthflow |
| Call routing/analytics (service 4) | CallTrackingMetrics |
| Ad research | Facebook (Meta) Ad Library |
| Payments | Cents (pushes fees to customer), Stripe, or Waves |
| Agreements | Dropbox Sign (free) or DocuSign |

## 6. KPIs the team tracks

- Leads scraped → contacted → appointments booked → shows → closes → cash collected
- Per-client: reactivation responses, reviews generated, referrals generated,
  missed calls answered, ad-lead response time (<5 min), appointments booked
- JP's ads benchmark: ~$7,900/mo spend → 20+ sales, $20K+ cash down, $200K+ cash
  collected including recurring

## 7. How this repo turns the method into a 100% AI-run business

- **`.claude/agents/*.md`** — one Markdown file per team member. Each encodes its
  mission, its exact position in the sequence above, its operating prompts (adapted
  from JP's own prompts), its KPIs, and its handoff rules. These files are the
  single source of truth: they work as Claude Code subagents *and* as system prompts
  for the autonomous runner.
- **`agency_team/`** — the autonomous orchestrator. It loads the MD roles, walks the
  foundation phases (niche → franchises → pillars → client acquisition prep) exactly
  once, then runs daily operations (outreach → sales → onboarding → fulfillment →
  referrals) on a loop with no human in the picture. All external sends (SMS, email,
  calls, invoices, agreements) go through connectors; when a connector has no API
  credentials yet, the action is queued to a durable outbox instead of being lost,
  so the pipeline never blocks.
- **Compliance guardrails** are built into every outward-facing agent: honor
  opt-outs (TCPA), never fabricate results or reviews, only solicit reviews from
  genuinely positive customers, and never misrepresent the AI as a human when asked.
