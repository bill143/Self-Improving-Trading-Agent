"""Phase 9 — adjacent statutory records (spec §8).

Records outside the two NDIS regulators that auditors and other authorities still
require: insurances, workers compensation, SCHADS timesheets (7-year Fair Work
retention), superannuation, GST treatment, ABN/ASIC, SafeWork WHS notifications, OAIC
breach reports, and Restrictive Practices Authorisation Panel approvals.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from . import service
from .db import DB


@dataclass(frozen=True)
class StatutoryRecordType:
    key: str
    name: str
    authority: str
    retention_class: str = "default"
    has_expiry: bool = False


STATUTORY_TYPES: list[StatutoryRecordType] = [
    StatutoryRecordType("public_liability", "Public liability insurance certificate", "Insurer", has_expiry=True),
    StatutoryRecordType("professional_indemnity", "Professional indemnity insurance certificate", "Insurer", has_expiry=True),
    StatutoryRecordType("workers_compensation", "Workers compensation (icare NSW)", "icare NSW", has_expiry=True),
    StatutoryRecordType("schads_timesheets", "SCHADS Award timesheets and pay records", "Fair Work", "schads_timesheet"),
    StatutoryRecordType("superannuation", "Superannuation records", "ATO"),
    StatutoryRecordType("gst_treatment", "GST treatment documentation (NDIS supports GST-free)", "ATO"),
    StatutoryRecordType("abn_asic", "ABN / ASIC company records", "ASIC"),
    StatutoryRecordType("whs_safework", "WHS incident notifications to SafeWork NSW", "SafeWork NSW", "incident"),
    StatutoryRecordType("oaic_breach", "OAIC notifiable data breach reports", "OAIC", "incident"),
    StatutoryRecordType("rp_authorisation", "Restrictive Practices Authorisation Panel approvals", "NSW RPA Panel"),
]

STATUTORY_BY_KEY: dict[str, StatutoryRecordType] = {t.key: t for t in STATUTORY_TYPES}


class StatutoryService:
    def __init__(self, db: DB):
        self.db = db

    def record(self, type_key: str, data: dict, *, expires_on: date | None = None,
               actor: str = "system") -> int:
        t = STATUTORY_BY_KEY.get(type_key)
        if not t:
            raise KeyError(f"unknown statutory record type '{type_key}'")
        payload = {"type": type_key, "name": t.name, "authority": t.authority, **data}
        if expires_on:
            payload["expires_on"] = expires_on.isoformat()
        rid = self.db.add_record("statutory", payload, ref=type_key,
                                 retention_class=t.retention_class, actor=actor)
        # insurances/workers-comp with an expiry schedule the annual renewal
        if t.has_expiry and expires_on:
            service.schedule_expiry(self.db, "insurance_renewal", expires_on,
                                    subject_type="statutory", subject_id=type_key, actor=actor)
        self.db.audit(actor, f"statutory:{type_key}", str(rid))
        return rid

    def status(self) -> dict:
        held = {r["data"]["type"] for r in self.db.list_records("statutory")}
        missing = [t.key for t in STATUTORY_TYPES if t.key not in held]
        return {"types": len(STATUTORY_TYPES), "held": sorted(held),
                "missing": missing, "complete": not missing}
