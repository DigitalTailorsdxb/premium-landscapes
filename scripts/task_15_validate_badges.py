#!/usr/bin/env python3
"""
Task 15 — Validator. Confirms every location page's hero trust-badge strip
matches the canonical AREAS table in phase_n_postcode_faq.py (the same
source that feeds the FAQPage JSON-LD). Run this whenever phase_n's data
changes to catch drift early.

Exit code 0 = all match; 1 = at least one mismatch.
"""

import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from phase_n_postcode_faq import AREAS
from task_15_trust_badges import postcode_label, drive_label, NO_CHARGE

STRIP_PATTERN = re.compile(
    r'<div class="hero-trust-badges"[^>]*>(.*?)</div>', re.DOTALL
)


def check(area: dict) -> tuple[bool, str]:
    path = ROOT / area["file"]
    if not path.exists():
        return False, f"FAIL  {area['file']} — file missing"
    html = path.read_text(encoding="utf-8")
    m = STRIP_PATTERN.search(html)
    if not m:
        return False, f"FAIL  {area['file']} — no badge strip found"
    block = m.group(1)
    expected = [postcode_label(area), drive_label(area), NO_CHARGE]
    missing = [e for e in expected if e not in block]
    if missing:
        return False, f"FAIL  {area['file']} — missing: {missing}"
    return True, f"OK    {area['file']}"


def main() -> int:
    failures = 0
    for area in AREAS:
        ok, msg = check(area)
        print(" ", msg)
        if not ok:
            failures += 1
    print(f"\n  {len(AREAS) - failures}/{len(AREAS)} pages match canonical data")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
