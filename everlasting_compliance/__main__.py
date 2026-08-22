"""CLI for the Everlasting Care compliance platform.

  python -m everlasting_compliance profile        Show the provider profile & regulators
  python -m everlasting_compliance catalog         List the encoded obligation rules
  python -m everlasting_compliance status          Audit-readiness snapshot
  python -m everlasting_compliance seed-demo        Load a demo scenario (no real data)
  python -m everlasting_compliance incident --at ISO8601  Log a reportable incident
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone

from . import config, obligations as ob
from .db import DB
from . import service


def _profile() -> dict:
    p = config.PROFILE
    return {
        "provider": p.legal_name,
        "jurisdiction": p.jurisdiction,
        "data_region": p.data_region,
        "audit_pathway": p.audit_pathway,
        "registration_groups": p.registration_groups,
        "registration_renewal_due": p.registration_renewal_due.isoformat(),
        "scope": {
            "module_2a_restrictive_practices": p.scope.module_2a_restrictive_practices,
            "under_18_child_safety": p.scope.under_18_child_safety,
            "multi_tenant_saas": p.scope.multi_tenant_saas,
        },
        "regulators": config.REGULATORS,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="everlasting_compliance")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("profile")
    sub.add_parser("catalog")
    sub.add_parser("status")
    sub.add_parser("seed-demo")
    inc = sub.add_parser("incident")
    inc.add_argument("--at", default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    inc.add_argument("--participant", default="")

    args = parser.parse_args(argv)

    if args.command == "profile":
        print(json.dumps(_profile(), indent=2))
        return 0

    if args.command == "catalog":
        rows = [{
            "key": r.key, "name": r.name, "category": r.category,
            "regulator": r.regulator.value, "trigger": r.trigger.value,
            "conditional": r.conditional,
        } for r in ob.CATALOG]
        print(json.dumps(rows, indent=2))
        return 0

    db = DB()

    if args.command == "seed-demo":
        # Demo scenario only — synthetic ids, no real participant/worker data.
        today = date.today()
        service.schedule_event(db, "incident_24h_notification", datetime.now(timezone.utc).replace(tzinfo=None),
                               subject_type="incident", subject_id="DEMO-INC-1")
        service.schedule_event(db, "incident_5day_report", datetime.now(timezone.utc).replace(tzinfo=None),
                               subject_type="incident", subject_id="DEMO-INC-1")
        service.schedule_expiry(db, "worker_screening_renewal",
                                today.replace(year=today.year + 5),
                                subject_type="worker", subject_id="DEMO-W-1")
        service.schedule_expiry(db, "cpr_renewal", today.replace(year=today.year + 1),
                                subject_type="worker", subject_id="DEMO-W-1")
        service.schedule_expiry(db, "registration_renewal",
                                config.REGISTRATION_RENEWAL_DUE,
                                subject_type="organisation", subject_id="everlasting-care")
        service.schedule_recurring_next(db, "policy_annual_review", today,
                                        subject_type="organisation", subject_id="everlasting-care")
        service.refresh_statuses(db)
        print(json.dumps({"seeded": True, **service.audit_readiness(db)}, indent=2, default=str))
        return 0

    if args.command == "incident":
        event_at = datetime.fromisoformat(args.at.replace("Z", ""))
        ids = {
            "24h": service.schedule_event(db, "incident_24h_notification", event_at,
                                          subject_type="incident", subject_id=args.participant),
            "5day": service.schedule_event(db, "incident_5day_report", event_at,
                                           subject_type="incident", subject_id=args.participant),
        }
        db.audit("cli", "incident:logged", args.participant or "unknown")
        print(json.dumps({"logged_incident_obligations": ids}, indent=2))
        return 0

    if args.command == "status":
        service.refresh_statuses(db)
        print(json.dumps(service.audit_readiness(db), indent=2, default=str))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
