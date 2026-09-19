# Prospect List — Ops Cycle 1
**Agent:** `lead-scraper-agent` · **Consumers:** `appointment-setter-agent` (call queue), `sales-closer-agent` (referral upside)

---

## 0. Headline — read this before planning any calling day

| KPI | Target | Actual | Status |
|---|---|---|---|
| Uncontacted `NEW` leads | ≥ 1,000 | **32** | 🔴 **968 short** |
| Leads added this cycle | — | 32 | — |
| % franchise-affiliated | high | **100%** | ✅ |
| Data accuracy (bounce/wrong-number) | low | **unmeasured** — no dials placed yet | ⚠️ |

**I did not hit the 1,000 floor and I did not manufacture rows to look like I did.** Every one of the 32 leads below came out of a live search result with a real phone number attached to a real address. The gap is a capacity problem with a known cause and a known fix, both stated in §4.

---

## 1. What was built

32 franchise locations, all from the **top 2 ranked ships** in `phase2-franchise-targets`:

| Brand | Parent | Rank | Locations added |
|---|---|---|---|
| One Hour Heating & Air Conditioning | Authority Brands | #1 | 20 |
| Benjamin Franklin Plumbing | Authority Brands | #2 | 12 |

**Geography swept:** FL, GA, NC, OH, TX (5 states of 50). Chosen as high-density Sun Belt/Midwest HVAC markets — long cooling seasons, high replacement-ticket volume.

**Franchise-first order was honoured.** 100% of the list is franchise-affiliated, and both brands sit in the Authority Brands **Trades trio** — meaning `sales-closer-agent` should qualify every one of these with the cluster question from §4 of the Phase 2 artifact: *"how many locations and which brands do you run?"* Several of these owners will also hold Mister Sparky and/or sibling territories. One close should land 2–4 locations.

**Multi-territory signal already visible in the data:** Orlando FL returned **three distinct Benjamin Franklin phone numbers** and Augusta GA returned **two distinct One Hour numbers**. That is consistent with the FDD-derived pattern of ~87 owners across ~324 territories. These are flagged as `(loc 2)` / `(loc 3)` — they may be separate territories under one owner. **Do not treat them as separate accounts until qualified.**

---

## 2. Scoring — and why every lead scored exactly 3

Method scoring is: franchise member **+3**, low review count **+2**, visible Meta Ad Library spend **+1**, missing web chat/booking **+1** (max 7).

Every lead scored **3 — the franchise component only.** The other three modifiers require per-location enrichment (Google review counts, Meta Ad Library lookups, website booking-flow checks) that I could not run this cycle. **The scores are therefore uninformative for prioritisation right now — they are all identical.** `appointment-setter-agent` should work this list in the order given (brand rank, then state) rather than by score, until enrichment lands.

**Fields deliberately left empty rather than guessed:** `owner_name`, `email`, `google_reviews`. A fabricated owner name burns the call in the first ten seconds, and a fabricated review count destroys the single best opener we have. Empty is recoverable; wrong is not.

**Website field** is set to the brand root domain, not a location-specific URL — location subpages were not individually verified.

---

## 3. Verification gates from Phase 2 §7 — NOT yet cleared

The Phase 2 handoff instructed me to verify location counts from the official brand locator **before scraping** three brands. I did not reach them this cycle and they remain open:

- **#5 Mister Sparky** — location count UNVERIFIED. Must confirm 30+ US locations before list-building.
- **#9 Zoom Drain** — everything UNVERIFIED. F1 gate unconfirmed.
- **#10 Mighty Dog Roofing** — everything UNVERIFIED. F1 gate unconfirmed.

If any fails the 30+ test, promote a bench brand from Phase 2 §3 (1-800-Plumber + Air, bluefrog Plumbing + Drain, Roof Maxx, Precision Garage Door).

---

## 4. Why the list is 32 and not 1,000 — root cause and fix

**Root cause: research throughput, not intent.** The sweep ran on general web search. Measured yield was **~3 unique verified locations per query**, and the session's search budget capped out at **11 queries**. 11 × ~3 ≈ 32. That is the whole story. At this yield, 1,000 leads needs **~330+ queries** — roughly 30 sessions of the current budget.

**This is a tooling gap the agency should fix rather than grind around:**

1. **Brand locator pages are the high-yield source, not search engines.** `onehourheatandair.com/locations/`, `benjaminfranklinplumbing.com`, and the Neighborly brand locators each enumerate 200–400 locations on a handful of paginated/ZIP-driven pages. One fetch of a locator index is worth ~100 search queries. **Requesting: an HTTP fetch capability for public brand locator pages** (respecting robots.txt and rate limits per guardrails). This single change takes the list from 32 to 1,000+ in one cycle.
2. **Or a Google Places / Maps API key**, which would also close the `google_reviews` gap that currently flattens every score to 3.

**Interim plan if no new tooling arrives — run these in priority order, ~32 leads/cycle:**
- Cycle 2: finish One Hour + Benjamin Franklin across CA, AZ, NV, TN, SC, VA, PA, MI.
- Cycle 3: **Mr. Rooter (#3)** — highest-confidence owners' group in the whole report; best referral conductivity per close.
- Cycle 4: **Aire Serv (#4)**, then **Mr. Electric (#6)**.
- Cycle 5: clear the §3 verification gates on Mister Sparky / Zoom Drain / Mighty Dog Roofing.
- Deprioritise Roto-Rooter (#7, no territory protection) and Rooter-Man (#8, single-truck skew — outside the 5–50 tech ICP).

---

## 5. Honest risk notes for `appointment-setter-agent`

- **Phone numbers are tracking numbers in many cases.** Franchise brands route Yelp/locator numbers through call-tracking. They reach the branch, but they land in the *customer* queue, not the owner's desk. Expect to be gatekept by a dispatcher. Ask for the owner by role, not by name (we have no names yet).
- **Wrong-number/bounce rate is unmeasured.** Report the first 50 dials back to me so I can score source accuracy and drop low-quality sources (Yelp-derived records are the majority of this batch and are the least fresh).
- **Do not pitch brand-facing advertising** to any of these — Phase 2 §4. Lead with reactivation of their own database and speed-to-lead/after-hours answer rate.

---

## 6. Blocking dependency still open (inherited, unresolved)

The **owner questionnaire from Bill is still outstanding.** Phase 2 flags that if his preference is commercial/federal rather than residential, the entire ship list — and therefore this prospect list — is aimed at the wrong market. 32 leads is a cheap thing to throw away; 1,000 is not. **There is an argument for resolving the questionnaire before spending 30 cycles building the full list.** Flagging it rather than burning the budget blind.
