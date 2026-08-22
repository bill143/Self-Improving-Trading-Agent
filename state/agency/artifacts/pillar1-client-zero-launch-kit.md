# Pillar 1 — Client-Zero Launch Kit
**Agent:** reactivation-agent · **Status:** STAGED, awaiting first signed client
**Parent artifact:** `pillar1-reactivation-campaign` (master copy — do not duplicate copy here, adapt from it)
**Purpose:** collapse close → Day 1 send from "a week of back-and-forth" to **under 24 hours.**

---

## Why this exists

The master campaign is BUILT. The thing that actually delays month-one revenue is not copy — it's
the **five blocking pre-flight gates** (§0 of the master), every one of which requires something only
the client owner can give: a confirmed offer, a capacity number, a consented export, a scrub
approval, and a named human sender.

Chasing those five items *after* the sale is what turns a 3-day campaign into a 3-week campaign.
So they are pre-written here and go out the hour the agreement is signed.

**Hard rule this kit does not soften:** no send until all five gates are green, in writing.
A fast launch that burns a 4,000-record database is worse than a slow one.

---

## 1. Hour-Zero owner message (send immediately on close)

Sent by the agency, to the owner, plain text — not a form, not a portal invite. Owners in this
niche answer texts from their truck and ignore onboarding software.

**SMS to owner:**
```
Bill here. Payment's in - we start your reactivation this week. I need 4 quick things to send:
1) your dormant lead export, 2) how many free checks/wk you can absorb, 3) which tech's name goes
on the texts, 4) confirm you'll honor the free 21-pt check. Reply here, easiest for you.
```

**Email counterpart — Subject: "4 things and we're live"**
```
Payment's processed and your campaign is built. To send this week I need four things:

1. THE LIST — export every lead who inquired 6+ months ago and was never invoiced.
   Name, phone, email, inquiry date, trade. CSV from your CRM is fine.
2. CAPACITY — how many free checks per week can your guys absorb without wrecking
   the schedule? I throttle the sends to that number. Most 5-50 tech shops say 15-40.
3. THE SENDER — which real human's name goes on every message? You or a service
   manager. It'll be their name and a number that gets answered.
4. THE OFFER — confirm in your own words that a "YES" gets a free 21-point check,
   about 30 minutes, written report, no charge and no pitch, whether they buy or not.

Number 4 is the one I won't move without. If a customer says yes and no truck shows,
we lose that database permanently.

Reply to this and we're sending inside 24 hours.
```

---

## 2. Gate verification checklist (reactivation-agent, before first send)

| Gate | Green when | Failure mode if skipped |
|---|---|---|
| 1 — Offer real | Owner's own written words confirming what YES gets | Silent no-shows, database burned, churn in month 1 |
| 2 — Capacity | A number, per week, from the owner | Overbooked shop cancels appointments and blames us |
| 3 — Consent | Every record self-initiated; no purchased/scraped data | TCPA exposure, carrier blocking |
| 4 — Scrub done | Internal DNC, prior opt-outs, active customers, open estimates, invoiced <6mo, landlines removed | Angry actives, complaints, wasted sends |
| 5 — Sender identity | Real named human + monitored number + inbox | Copy reads like a bot, response rate collapses |

Expect **2,000–15,000 raw records → 55–75% survive scrubbing.** If survival is under 40%, stop and
talk to the owner: the export is probably the wrong query.

---

## 3. Voice-capture call (15 min, before adaptation)

Per master §7.2. Get the owner talking and **steal three phrases verbatim.**
- "unit" vs "system" — use theirs
- "y'all", "folks", "no worries" — regional register goes in the copy
- What they call the trade ("AC guy", "the heat", "panel work")

Copy that sounds like the shop outperforms polished copy. This call is not optional; it is the
difference between 8% and 15% response.

---

## 4. Launch runbook — exact tool sequence

| When | Action | Tool |
|---|---|---|
| Close | Client created in ONBOARDING | `close_sale` (sales-agent) |
| Hour 0 | Gate-request SMS + email above | `send_sms`, `send_email` |
| Hour 0–24 | Gates 1–5 verified, list scrubbed, voice captured | — |
| Day 0 | Client moved to REACTIVATION | `advance_client` |
| Day 1, 10:00–11:30 local | Day 1 SMS + email, batch throttled to capacity | `send_sms`, `send_email` |
| Continuous | YES/NO handled within 5 min, 8am–8pm local | master §5 / §6 |
| Day 2, 16:30–18:00 local | Day 2 — non-responders only | `send_sms`, `send_email` |
| Day 3, 11:00–13:00 local | Day 3 — final, named-weekday deadline | `send_sms`, `send_email` |
| Day 3+ | Sequence ends. No day 4. 90-day dormant hold. | — |
| Day 7 / 14 / 30 | Report to `client-success-agent` | `record_metric` |
| Month-one delivered | Advance to REVIEWS_REFERRALS | `advance_client` |

**Segment by trade before sending** (master §7.4). Never send a plumbing lead an HVAC message —
multi-brand owners average ~3.7 territories and one database.

---

## 5. Metrics logged per client, per campaign

`records_messaged` · `deliverability_rate` · `response_rate` · `positive_reply_rate` ·
`appointments_booked` · `show_rate` · `revenue_attributed` · `optout_rate` · `complaints`

Targets live in master §9. Two that trigger a **stop-and-fix**, not a note:
- Deliverability < 90% → list quality problem, re-scrub before continuing
- Opt-out > 3% → copy is too salesy, revert to canonical master copy

---

## 6. Definition of "month-one campaign delivered"

Advance to REVIEWS_REFERRALS only when **all** are true:
1. Day 1 / 2 / 3 sent to the full scrubbed, throttled list
2. Every YES routed, booked, confirmed; every reminder sent
3. Every NO/STOP suppressed permanently across SMS, email and voice
4. Day-30 report delivered with attributed revenue

That day-30 dollar figure is the referral asset — it's what opens the Mr. Rooter owners' group and
the Neighborly conference. It is also what unblocks `ads-agent`, who is waiting on this cash.

---

## 7. Current blocker (for the team, not for me)

Pipeline reads **32 leads / 29 CONTACTED / 0 BOOKED / 0 CLOSED.** Fulfillment capacity is idle and
fully ready; the binding constraint is upstream at booking and closing. Nothing in Pillar 1 is
waiting on Pillar 1.

**Status: STAGED. First signed client goes live inside 24 hours.**
