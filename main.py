#!/usr/bin/env python3
"""
DevOps Alert Processor Agent — entrypoint.
Reads mock alerts, runs the full pipeline, prints a JSON summary.
"""
import json
import sys
from pathlib import Path

from agent.processor import process_all, results_to_dict

ALERTS_FILE = Path(__file__).parent / "mock_data" / "alerts.json"


def main():
    print("=" * 60)
    print("  DevOps Alert Processor Agent")
    print("=" * 60)

    alerts = json.loads(ALERTS_FILE.read_text())
    print(f"\nLoaded {len(alerts)} alerts from {ALERTS_FILE.name}\n")

    results = process_all(alerts)

    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    for r in results:
        remediation_icon = "✓" if r.remediation["status"] == "executed" else "—"
        print(
            f"  [{r.severity.upper():8}] {r.alert_id} | {r.title[:40]:40}"
            f" → {', '.join(r.routed_to) or 'silent':30} [{remediation_icon} {r.remediation.get('runbook_id') or 'no runbook'}]"
        )

    output_path = Path("/tmp/alert_results.json")
    output_path.write_text(json.dumps(results_to_dict(results), indent=2))
    print(f"\nFull results written to {output_path}")


if __name__ == "__main__":
    main()
