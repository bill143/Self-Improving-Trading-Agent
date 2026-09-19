"""Phase 6 — NDIA claiming.

The NDIA portals give providers no API key; claiming is a bulk-CSV upload against the
myplace portal. So this module GENERATES a valid bulk-claim CSV, enforces the rules
that get claims rejected (90-day window, valid ABN, support-item code, dates within
plan, GST treatment), and opens the 90-day payment obligation from each service
booking's end so a claim window can never lapse.

Rules encoded from the compliance inventory (spec §7):
- Payment request within 90 days from the end of a service booking.
- Bulk upload: up to 5,000 rows; filename under 20 characters including ".CSV".
- Claims must align with NDIS Pricing Arrangements; dates within the correct plan.
- Plan-managed invoices need a valid ABN. Most NDIS supports are GST-free.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from datetime import date, timedelta

from . import service
from .db import DB

BULK_MAX_ROWS = 5000
FILENAME_MAX_LEN = 20  # including ".CSV"
CLAIM_WINDOW_DAYS = 90
GST_CODES = {"P1": "GST-free", "P2": "GST applicable"}  # NDIS supports default GST-free (P1)


def validate_abn(abn: str) -> bool:
    """Australian Business Number checksum (mod-89 weighted)."""
    digits = [c for c in str(abn) if c.isdigit()]
    if len(digits) != 11:
        return False
    nums = [int(c) for c in digits]
    nums[0] -= 1
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    return sum(n * w for n, w in zip(nums, weights)) % 89 == 0


@dataclass
class ClaimLine:
    participant_id: str            # NDIS number
    support_item_number: str       # e.g. 01_011_0107_1_1
    service_date: date
    quantity: float
    unit_price: float
    gst_code: str = "P1"
    claim_reference: str = ""
    abn: str = ""                  # required for plan-managed invoices

    @property
    def total(self) -> float:
        return round(self.quantity * self.unit_price, 2)


def validate_line(line: ClaimLine, *, today: date, plan_start: date | None = None,
                  plan_end: date | None = None, plan_managed: bool = False) -> list[str]:
    """Return a list of rejection reasons (empty == valid)."""
    errors: list[str] = []
    if not line.participant_id:
        errors.append("missing participant NDIS number")
    if not line.support_item_number:
        errors.append("missing support item number")
    if line.quantity <= 0 or line.unit_price <= 0:
        errors.append("quantity and unit price must be positive")
    if line.gst_code not in GST_CODES:
        errors.append(f"invalid GST code {line.gst_code!r}")
    # 90-day claim window
    if line.service_date > today:
        errors.append("service date is in the future")
    elif (today - line.service_date).days > CLAIM_WINDOW_DAYS:
        errors.append(f"outside the {CLAIM_WINDOW_DAYS}-day claim window")
    # plan dates
    if plan_start and line.service_date < plan_start:
        errors.append("service date before plan start")
    if plan_end and line.service_date > plan_end:
        errors.append("service date after plan end")
    # plan-managed invoices require a valid ABN
    if plan_managed and not validate_abn(line.abn):
        errors.append("invalid or missing ABN for a plan-managed invoice")
    return errors


def build_bulk_csv(lines: list[ClaimLine], filename: str) -> tuple[str, list[str]]:
    """Build the bulk-upload CSV text. Returns (csv_text, problems).
    Enforces the row cap and the filename length rule."""
    problems: list[str] = []
    if len(lines) > BULK_MAX_ROWS:
        problems.append(f"{len(lines)} rows exceeds the {BULK_MAX_ROWS}-row bulk limit")
    if len(filename) >= FILENAME_MAX_LEN:
        problems.append(f"filename '{filename}' must be under {FILENAME_MAX_LEN} chars (incl .CSV)")
    if not filename.upper().endswith(".CSV"):
        problems.append("filename must end with .CSV")

    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["RegistrationNumber", "NDISNumber", "SupportsDeliveredFrom",
                "SupportsDeliveredTo", "SupportNumber", "ClaimReference",
                "Quantity", "Hours", "UnitPrice", "GSTCode"])
    for ln in lines[:BULK_MAX_ROWS]:
        w.writerow(["", ln.participant_id, ln.service_date.isoformat(),
                    ln.service_date.isoformat(), ln.support_item_number,
                    ln.claim_reference, ln.quantity, "", f"{ln.unit_price:.2f}", ln.gst_code])
    return buf.getvalue(), problems


class ClaimingService:
    def __init__(self, db: DB):
        self.db = db

    def create_booking(self, participant_id: str, support_item: str,
                       start: date, end: date, budget: float, *, actor: str = "system") -> int:
        """Create a service booking and open its 90-day payment obligation."""
        rid = self.db.add_record("service_booking", {
            "participant_id": participant_id, "support_item": support_item,
            "start": start.isoformat(), "end": end.isoformat(), "budget": budget,
        }, ref=f"{participant_id}:{support_item}", retention_class="payment", actor=actor)
        service.schedule_event(self.db, "ndia_payment_request", end,
                               subject_type="claim", subject_id=participant_id, actor=actor)
        self.db.audit(actor, "booking:created", participant_id, support_item)
        return rid

    def record_claim(self, line: ClaimLine, *, today: date, plan_managed: bool = False,
                     actor: str = "system") -> dict:
        """Validate and store a claim line. Rejected lines are stored with their errors
        so nothing is silently dropped."""
        errors = validate_line(line, today=today, plan_managed=plan_managed)
        rid = self.db.add_record("claim_line", {
            "participant_id": line.participant_id, "support_item": line.support_item_number,
            "service_date": line.service_date.isoformat(), "quantity": line.quantity,
            "unit_price": line.unit_price, "gst_code": line.gst_code, "total": line.total,
            "valid": not errors, "errors": errors,
        }, ref=line.claim_reference, retention_class="payment", actor=actor)
        self.db.audit(actor, "claim:recorded", str(rid), "valid" if not errors else "rejected")
        return {"record_id": rid, "valid": not errors, "errors": errors}
