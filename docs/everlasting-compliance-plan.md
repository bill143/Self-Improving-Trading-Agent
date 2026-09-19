# Everlasting Care — NDIS Compliance Platform: Phasing Plan

**Provider:** Everlasting Care (Sydney, NSW) — NDIS registered provider, **Certification
pathway** (holds Assist-Personal Activities + Daily Tasks/Shared Living, so the Core
Module + on-site audit applies).
**Regulators:** NDIS Quality & Safeguards Commission (quality/safety/registration) and
the NDIA (funding/claims/pricing); plus NSW OCG (worker screening/WWCC), ATO/Fair
Work/SafeWork NSW/OAIC.
**Purpose (default, changeable at inspection):** internal compliance operations tool
for Everlasting Care, architected to extend to multi-tenant SaaS later.
**Scope toggles (default):** Module 2A (restrictive practices) — **built, toggleable**;
under-18 / child-safety — **built, toggleable, default off**.

This is the build spec derived directly from the compliance inventory supplied by the
owner. Source of truth for the regulations themselves: the NDIS Practice Standards and
Quality Indicators (to be pinned as the authoritative document at final inspection).

---

## Delivery model
Full-stack, built end-to-end and autonomously, phase by phase, to a **final inspection**
checkpoint. No per-step human approvals. Every phase lands code + tests + a committed,
pushed increment. The only steps that require the owner are physical, not approvals: the
paid **Sydney server** for live deployment, and the real **credentials/tokens** (Telegram
bot, NDIS PRODA/myID). Those are wired at the end through a durable queue so they never
block the build.

**Regulatory-honesty gate:** the platform implements the supplied spec faithfully, but
before it is relied on for real audits or claims it must be validated against current
NDIS regulations by a qualified person. That validation IS the final inspection.

## Architecture
- **Backend:** Python (standard library + FastAPI for the dashboard/API). SQLite now,
  designed to migrate to Postgres for production.
- **Pattern:** the proven orchestrator + specialist-agents + durable auditable state +
  deadline "gates" pattern (same shape as `agency_team`, rebuilt for compliance).
- **AI fleet:** Orchestrator + Scout (regulatory watch), Scribe (policies/reports),
  Reach (reminders + Telegram intake), Dev (builds registers/tools). Roles live in
  `.claude/agents/ec-*.md` — one Markdown file per agent.
- **Interfaces:** Telegram bot for field staff (incident intake, deadline reminders) +
  a live read-only mission-control dashboard for management.
- **Non-negotiables:** Sydney data residency, encryption at rest, role-based access
  (admin/manager/worker/auditor-read-only), immutable audit log, 7-year retention
  (incidents) / 5-year (payments) enforced by the retention engine.

---

## Phases

### Phase 0–1 — Scaffold + Obligations/Deadline Engine  ← highest risk, built first
The single thing that deregisters providers is a missed deadline. So the deadline engine
is the spine of the whole platform.
- Project scaffold, config (regulators, registration groups, retention, scope toggles),
  data model, SQLite persistence, immutable audit log.
- **Deadline engine** encoding the real NDIS cadences and hard deadlines:
  reportable incident 24h notification + 5-business-day report + conditional 60-day final;
  unauthorised restrictive practice 5-business-day; NDIA payment request 90-day; worker
  screening 5-year (90-day renewal window); First Aid 3-year; CPR annual; registration
  renewal 3-year (Everlasting Care due before **2027-10-24**, prep ~Apr 2027); mid-term
  audit ~18 months; monthly restrictive-practice report; annual policy review; participant
  plan (annual) + risk assessment (6-monthly) + consent (annual); quarterly register
  reconciliation; annual insurance renewal.
- Status model: upcoming → due_soon → overdue → submitted → closed, with per-obligation
  lead-time alerting.

### Phase 2 — Registers (evidence of live practice)
The 15+ organisation-wide registers auditors check to prove policy is actually happening:
incident, reportable-incident tracker, complaints/feedback, continuous improvement, risk,
training (with expiry alerts), worker screening, restrictive practice, medication error,
hazard/WHS, policy (version control), asset/vehicle, conflict of interest, consent, key
personnel. Each entry versioned and audit-logged.

### Phase 3–4 — Participant files + Worker files
- **Participant file** per participant: intake/eligibility, consents (annual refresh),
  service agreement, plan copy + budget, service booking, needs + risk assessment,
  individual support plan (annual review), progress notes (per shift), medication records,
  restrictive-practice entries, money/property log, incidents, complaints, transition/exit.
- **Worker file** per worker: identity/right-to-work, NDIS Worker Screening (5yr, portable),
  WWCC, orientation module certificate (per employer), First Aid (3yr)/CPR (annual),
  qualifications, Code of Conduct, induction, infection control/PPE, role-dependent
  competencies, supervision/CPD, secondary-employment declaration. Employer-side:
  risk-assessed roles register, portal verify/link/unlink, expiry notifications.

### Phase 5 — Governance + Policy Suite (Core Module)
The ~40–50 core policies across Governance / Rights / Service Delivery / Workforce /
Risk & Safeguarding, each with version number, owner, approval date, review date, and an
annual review cycle. Scribe agent drafts and maintains them; policy register enforces
version control.

### Phase 6–7 — NDIA claiming + Regulator submissions
- **Claiming:** service bookings, "my provider" relationships, payment requests (single +
  bulk CSV up to 5,000 rows, filename <20 chars incl. .CSV), 90-day window enforcement,
  pricing compliance against NDIS Pricing Arrangements & Price Limits, invoice validation
  (valid ABN, item codes, dates, units, rates, GST-free treatment), retention (7yr
  incidents / 5yr payments).
- **Commission submissions workflow:** reportable incident 24h/5-day/60-day, unauthorised
  restrictive practice, monthly restrictive-practice reporting, change notifications,
  worker screening verify/link, mid-term audit, renewal + self-assessment, conditional
  audit, responses to compliance notices/information requests.

### Phase 8 — 5-agent AI fleet + Telegram + dashboard
Orchestrator + Scout/Scribe/Reach/Dev wired across every module; Telegram interface
(outbox-queued until the bot token is provided); the live read-only mission-control
dashboard (FastAPI) showing audit-readiness, upcoming deadlines, overdue items, and
register health.

### Phase 9–10 — Hardening, deployment package, final inspection
Adjacent statutory records (insurance, workers comp/icare, SCHADS timesheets 7yr, super,
GST docs, ABN/ASIC, SafeWork WHS, OAIC breach reporting, Restrictive Practices
Authorisation). Security hardening scripts for the Sydney droplet (Fail2Ban + UFW +
backups + TLS), encryption/retention verification, end-to-end tests, a deployment runbook,
and the compliance-validation checklist for the qualified reviewer.

---

## Compliance calendar encoded (cadence → obligations)
| Cadence | Obligations |
|---|---|
| Per shift | Progress notes, medication records, timesheet |
| Per event | Incident report, complaint log, reportable notification (24h / 5-day) |
| Weekly | Bulk claim upload, claim rejection reconciliation |
| Monthly | Restrictive-practice report, training-expiry sweep, claims reconciliation |
| Quarterly | Reconcile internal incident register vs Commission portal; internal audit; risk review |
| 6–12 monthly | Participant plan + risk-assessment reviews, consent refresh, emergency-plan test |
| Annually | Policy review, CPR renewals, WHS audit, insurance renewals, worker performance reviews |
| 18 months | Mid-term audit |
| 3 years | First Aid renewals, registration renewal audit |
| 5 years | Worker screening renewals |

## Key fixed dates
- **Registration renewal due before 2027-10-24**; renewal prep begins ~2027-04.
- Mid-term audit ~18 months into the 3-year cycle.
