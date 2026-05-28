#!/usr/bin/env python3
"""
Task 21 — Validate FAQPage JSON-LD on the 7 service pages.
Reuses the same checks as scripts/task_16_validate_faq_schema.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from task_16_validate_faq_schema import validate_file  # noqa: E402

ROOT = Path(__file__).parent.parent

SERVICE_PAGES = [
    "patios.html",
    "artificial-grass.html",
    "composite-decking.html",
    "driveways.html",
    "garden-lighting.html",
    "full-garden-makeover.html",
    "garden-design.html",
]


def main():
    total_errs = total_warns = 0
    results = []
    for fname in SERVICE_PAGES:
        path = ROOT / fname
        if not path.exists():
            print(f"  MISSING: {fname}")
            total_errs += 1
            continue
        errs, warns = validate_file(path)
        results.append((fname, errs, warns))
        total_errs += len(errs)
        total_warns += len(warns)

    for fname, errs, warns in results:
        if not errs and not warns:
            print(f"PASS  {fname}")
        else:
            print(f"{'FAIL' if errs else 'WARN'}  {fname}")
            for e in errs:
                print(f"        ERROR: {e}")
            for w in warns:
                print(f"        warn : {w}")

    print()
    print(f"Summary: {len(SERVICE_PAGES)} pages, {total_errs} errors, {total_warns} warnings")
    return 0 if total_errs == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
