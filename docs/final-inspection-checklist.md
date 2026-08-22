# Final Inspection Checklist — Everlasting Care Compliance Platform

Two parts: a **technical acceptance** check (the software works), and a **compliance
validation** check (the software is correct for real NDIS use). The second part must be
signed off by a qualified person before the platform is relied on for actual audits or
claims — the platform assists compliance, it does not replace professional judgement.

## Part A — Technical acceptance (verifiable now)
- [ ] `uv run --extra compliance --extra dev python -m pytest` → all tests green.
- [ ] `python -m everlasting_compliance profile` shows the correct provider profile.
- [ ] `python -m everlasting_compliance catalog` lists every encoded obligation rule.
- [ ] Dashboard loads over HTTPS and requires login.
- [ ] Logging a reportable incident opens the 24h + 5-day obligations and a register entry.
- [ ] Reminder sweep dispatches (or queues) reminders for overdue/due-soon items.
- [ ] Bulk claim CSV generates and enforces the 90-day + filename + ABN rules.
- [ ] Backups run and restore; state and backups are onshore (Sydney/AU).
- [ ] Fail2Ban + UFW active; dashboard not exposed on a raw port.
- [ ] Anthropic key rotated (it passed through chat during the build).

## Part B — Compliance validation (qualified reviewer sign-off)
For each item, confirm the encoded rule matches the **current** regulation and the
provider's actual circumstances.
- [ ] **Registration groups / pathway** — Certification vs Verification correct for the
      groups Everlasting Care actually holds.
- [ ] **Deadline rules** — 24h/5-day incident, 60-day final, URP 5-day, 90-day claim,
      5-year screening, 3-year renewal, mid-term audit timing all current.
- [ ] **Renewal date** — registration renewal before 2027-10-24 confirmed against the
      actual certificate.
- [ ] **Policy suite** — the ~43 required policies match the current Practice Standards;
      Module 2A and under-18 scope toggles set correctly.
- [ ] **Registers** — all required registers present and mapped to real workflows.
- [ ] **Retention** — 7-year incident / 5-year payment / 7-year Fair Work timesheet
      periods correct.
- [ ] **Claiming** — support item codes, GST treatment (GST-free defaults), and pricing
      align with the current NDIS Pricing Arrangements and Price Limits.
- [ ] **Privacy** — participant data handling meets the Privacy Act + NDIS rules;
      onshore residency confirmed.
- [ ] **Business rules** — anything the provider does differently from the encoded
      defaults is captured and adjusted.

## Sign-off
| Role | Name | Date | Signature |
|---|---|---|---|
| Technical acceptance | | | |
| Compliance validation (qualified) | | | |
| Provider (Everlasting Care) | | | |
