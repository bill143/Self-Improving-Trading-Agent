"""CLI entry point: `python -m agency_team` (or the `agency-team` script).

Commands:
  status              Show pipeline state, phase gates, and outbox.
  run [--cycles N]    Run N autonomous cycles (default 1).
  run --forever       Run continuously (the 100% AI-driven mode).
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from .crm import CRM
from .orchestrator import Orchestrator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agency-team")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="show business state")

    run = sub.add_parser("run", help="run autonomous cycles")
    run.add_argument("--cycles", type=int, default=1)
    run.add_argument("--forever", action="store_true")
    run.add_argument("--sleep", type=int, default=300,
                     help="seconds between cycles with --forever (default 300)")

    args = parser.parse_args(argv)
    crm = CRM()

    if args.command == "status":
        print(json.dumps(crm.summary(), indent=2))
        return 0

    orch = Orchestrator(crm=crm)
    cycle = 0
    while True:
        cycle += 1
        result = orch.run_cycle()
        print(json.dumps({"cycle": cycle, **result}, indent=2))
        if args.forever:
            time.sleep(args.sleep)
            continue
        if cycle >= args.cycles:
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
