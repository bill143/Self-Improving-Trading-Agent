"""Provider profile, regulatory constants, retention rules, and scope toggles.

These are the facts the whole platform is built around. Everything the owner might
change at final inspection lives here so it is edited in exactly one place.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def state_dir() -> Path:
    env = os.environ.get("EC_STATE_DIR")
    d = Path(env) if env else REPO_ROOT / "state" / "everlasting_compliance"
    d.mkdir(parents=True, exist_ok=True)
    return d


# --- Regulators ------------------------------------------------------------
REGULATORS = {
    "NDIS_COMMISSION": {
        "name": "NDIS Quality and Safeguards Commission",
        "scope": "Registration, Practice Standards, Code of Conduct, incidents, "
                 "complaints, worker screening, restrictive practices",
        "portal": "NDIS Commission Provider Portal",
    },
    "NDIA": {
        "name": "National Disability Insurance Agency",
        "scope": "Plans, budgets, service bookings, claims, pricing",
        "portal": "myplace + my NDIS provider portal (PRODA / myID + RAM)",
    },
    "OCG_NSW": {
        "name": "NSW Office of the Children's Guardian",
        "scope": "NDIS Worker Check (NSW screening), Working With Children Check",
        "portal": "Service NSW",
    },
    "STATUTORY": {
        "name": "ATO / Fair Work / SafeWork NSW / OAIC",
        "scope": "GST-free supply rules, SCHADS Award, WHS, Privacy Act",
        "portal": "Standard federal/state channels",
    },
}

# Registration groups Everlasting Care holds → these trigger the Certification pathway.
REGISTRATION_GROUPS = [
    "Assist-Personal Activities",
    "Daily Tasks / Shared Living (Supported Independent Living)",
]
AUDIT_PATHWAY = "Certification"  # document review + on-site assessment + interviews

# Retention (years). Enforced by the retention engine; nothing is hard-deleted early.
RETENTION_YEARS = {
    "incident": 7,
    "payment": 5,
    "invoice": 5,
    "schads_timesheet": 7,  # Fair Work
    "participant_record": 7,
    "worker_record": 7,
    "default": 7,
}

# Fixed dates specific to Everlasting Care.
REGISTRATION_RENEWAL_DUE = date(2027, 10, 24)   # renewal must be lodged before this
REGISTRATION_RENEWAL_PREP = date(2027, 4, 24)   # ~6 months prior


@dataclass
class Scope:
    """Feature toggles the owner confirms at inspection."""
    module_2a_restrictive_practices: bool = True   # built; on because personal care/SIL
    under_18_child_safety: bool = False            # built; off until confirmed in scope
    multi_tenant_saas: bool = False                # single-tenant internal tool for now


@dataclass
class ProviderProfile:
    legal_name: str = "Everlasting Care"
    jurisdiction: str = "NSW, Australia"
    data_region: str = "Sydney (AU) — onshore residency required"
    registration_groups: list[str] = field(default_factory=lambda: list(REGISTRATION_GROUPS))
    audit_pathway: str = AUDIT_PATHWAY
    registration_renewal_due: date = REGISTRATION_RENEWAL_DUE
    scope: Scope = field(default_factory=Scope)


PROFILE = ProviderProfile()
