# Cold-Call Script v2 — Home Services (HVAC / Plumbing Franchisees)
**Agent:** `appointment-setter-agent` · **Status:** SCRIPT OF RECORD, ops cycle 1
**Supersedes:** the generic blueprint opener, for this niche only.

---

## 0. ⚠️ The one line that was removed, and why

The blueprint opener reads: *"we ran some test ads in your area and found a strong demand for your services."*

**That line is prohibited on every call in this cycle.** My standing guardrail permits it only when `ads-agent` has actually done ad-library research for the prospect's area/market. It has not:

- Phase 6 §0: *"I do not have a direct Meta Ad Library integration."* Competitor ad data came from published third-party teardowns, graded MEDIUM-HIGH, none of it local to our prospects.
- Phase 6 §5 step 3: the **local Ad Library pull (5 live competitor ads in the client's metro)** is a per-client fulfillment step that is **blocked and un-run** — gated behind a client clearing REACTIVATION. We have zero clients.
- We have run **no ads at all**, test or otherwise, in Medina OH, Naples FL, Corpus Christi TX or anywhere else on this list.

Saying it would be a fabricated result in the first fifteen seconds of a relationship with a buyer whose defining trait is contempt for marketers who lie. It also directly contradicts Phase 6 §7 ("no fabricated claims") and Phase 7 §8 ("never fabricate a case study, a client name, or a dollar result").

**Reinstatement condition:** the line returns, per-metro only, once `ads-agent` has pulled live Ad Library data for that specific metro and can state what it found.

## 0b. Second removed claim: we have no clients

We have **zero clients** (state: `clients_total: 0`). Therefore: no "we work with several One Hour franchisees," no "shops like yours are seeing," no implied roster. Phase 7 already ruled on this — *"We're newly launched in this vertical"* — and that honesty is a conversion asset in this niche, not a liability.

---

## 1. The opener (structure preserved, claim corrected)

> **"Hey — this is Bill O'Neill's office, O'Neill Contractors. I'm looking for the owner, is he in today?"**

Structure is intact from the proven script: **identify → ask for the owner → reason for call → curiosity hook → two-option close for the appointment.** Only the factual claim inside the hook changed.

### Gatekeeper (expect this — see §5 below)
> "What's this regarding?"

> **"It's about his dormant customer list — the people who called last year, got a number, and never got back on the schedule. I need sixty seconds with whoever owns the P&L. Is that him?"**

Never: "I just wanted to reach out." Never pitch the gatekeeper. Ask for the owner **by role** — we have no owner names on this list and inventing one burns the call in ten seconds (`prospect-list-cycle-1` §2, §5).

### Reason for call — the accurate demand insight
> **"Reason for my call: Bill's a contractor, not a marketer — he runs O'Neill Contractors. We've built an AI system that works the customer list you already own. The people who called six-plus months ago about a specific broken thing, got a quote, and never got invoiced. It goes out in your service manager's name, on your list, with zero ad spend. That's the piece almost every shop your size is sitting on and nobody's touching."**

Everything in that paragraph is true and defensible: it describes our own mechanism (Pillar 1), not a claim about their market, their competitors, or results we've produced.

### The ask — two concrete times, always
> **"Are you available today for a 30-minute Zoom, or would tomorrow work better? … I've got 9:30 a.m. and 11:00 a.m. Eastern Thursday — do either of those work?"**

### Frame the meeting
> **"It's 15 to 30 minutes. Bill walks you through the whole thing himself. He'll ask you some nosy questions about your numbers, and if it can't help you he'll tell you that and give you your time back."**

### Collect, then confirm on the spot
Name · best direct phone · email · confirm the invite while still on the line. Confirmation SMS inside 60 seconds (Phase 7 §0).

---

## 2. Objection handling on the cold call

| They say | We say |
|---|---|
| "Is this lead generation?" | "That's one of the services we have, among the others." *(Do not pitch. The call sells the appointment, nothing else.)* |
| "Is this an AI calling me?" | **"Yes. I'm an AI agent working for O'Neill's agency. Bill's a real contractor and the work is real. Want me to put him on instead?"** Immediately, plainly, every single time. |
| "Corporate handles our marketing." | "Good — that's exactly why I'm not calling about advertising. This is a service reminder to your own customer list. No brand creative, no discount, nothing corporate has to approve." |
| "What's it cost?" | "That's Bill's conversation, not mine — it depends on the size of your list. That's what the 30 minutes is for." |
| "Send me an email." | "Happy to. What's the best address? — and let's hold a time anyway so it doesn't die in your inbox during a no-heat call. Thursday 9:30 or 11?" |
| "Not interested." | One re-ask, then out clean: "Fair enough. Can I check back after the season?" → **DECLINED**, not DNC. |
| **"Take me off your list."** | **"Done — permanently, right now. Sorry to bother you."** → **DNC immediately. No re-ask, no rebuttal, ever.** |

## 3. Do NOT pitch on this call
Per `prospect-list-cycle-1` §5 and Phase 2 §4: **never pitch brand-facing advertising to a franchisee.** Ads are structurally blocked until a client's reactivation cash lands (Phase 6 §5 gate 1). Lead with reactivation of their own database and after-hours answer rate. Nothing else.

## 4. Calling hours (prospect's local time)
Dial window **8:00 a.m.–5:00 p.m. local, Mon–Fri.** No Sundays, no holidays.
- **Eastern:** FL, GA, NC, OH
- **Central:** TX
Franchise dispatch queues are busiest 7–9 a.m. and after the first heat/cold event; mid-morning and early afternoon are the realistic owner windows.

## 5. Known field conditions (from `lead-scraper-agent`)
- **Many of these numbers are call-tracking numbers** routed into the *customer* queue, not the owner's desk. Expect a dispatcher. Budget 2–3 transfers to reach an owner.
- **All 32 leads score exactly 3** — the franchise flag only. Scores are uninformative for prioritisation. Work **brand rank order** (One Hour #1 → Benjamin Franklin #2), not score.
- **Cluster discipline:** Orlando returned 3 Benjamin Franklin numbers, Augusta 2 One Hour numbers. These may be one owner holding multiple territories. **Dial the primary only; hold the siblings until ownership is qualified.** One close may land 2–4 locations.
- **Qualifying question for any owner reached:** *"How many locations do you run, and which brands?"* Authority Brands owners frequently hold Mister Sparky / sibling territories.

## 6. Touch cadence
Max **3 touches over 7 days**, then recycle to a later pass.
1. **Touch 1** — call (+ paired SMS where the line accepts it)
2. **Touch 2** — SMS/email, day 3
3. **Touch 3** — call, different time of day, day 7
Then back to NEW for a later cycle. Never a fourth touch in the window.
