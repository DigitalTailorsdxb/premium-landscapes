#!/usr/bin/env python3
"""
Task 15 — Insert hero trust-badge strip (postcode, drive time, no travel charge)
into all 20 location pages, just below the hero subtitle <p>.

Data source: scripts/phase_n_postcode_faq.py — the SAME `AREAS` table that
populates the machine-readable FAQPage JSON-LD on every location page.
Importing from it (rather than re-typing the values) guarantees the visible
hero badges and the JSON-LD answers never drift apart.

Idempotent: re-running first strips any previously-inserted block, so safe to
run after edits to phase_n's AREAS table.
"""

import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from phase_n_postcode_faq import AREAS  # canonical source of truth

NO_CHARGE = "No travel charge"

HERO_P_PATTERN = re.compile(
    r'(<p class="text-xl md:text-2xl mb-4 text-white/90 max-w-3xl mx-auto leading-relaxed">'
    r'.*?</p>)',
    re.DOTALL,
)

EXISTING_STRIP_PATTERN = re.compile(
    r'\s*<div class="hero-trust-badges"[^>]*>.*?</div>',
    re.DOTALL,
)


def postcode_label(area: dict) -> str:
    """Render '<short> postcode' (or 'postcodes' for ranges)."""
    short = area["postcode_short"]
    plural = any(ch in short for ch in ("–", "-", "/", ","))
    return f"{short} {'postcodes' if plural else 'postcode'}"


def drive_label(area: dict) -> str:
    """Render a short, human badge from the canonical drive_min value."""
    mins = area["drive_min"]
    if mins == 0:
        return "Based here — same day"
    return f"{mins} min from base"


def build_strip(area: dict) -> str:
    pc = postcode_label(area)
    dt = drive_label(area)
    return (
        '\n            <div class="hero-trust-badges" aria-label="Local service trust signals">\n'
        f'                <span class="trust-badge"><span class="trust-badge-icon" aria-hidden="true">📍</span>{pc}</span>\n'
        f'                <span class="trust-badge"><span class="trust-badge-icon" aria-hidden="true">🚐</span>{dt}</span>\n'
        f'                <span class="trust-badge"><span class="trust-badge-icon" aria-hidden="true">✅</span>{NO_CHARGE}</span>\n'
        '            </div>'
    )


def process(area: dict) -> str:
    path = ROOT / area["file"]
    if not path.exists():
        return f"SKIP  {area['file']} — not found"

    html = path.read_text(encoding="utf-8")
    original = html

    html = EXISTING_STRIP_PATTERN.sub("", html)
    strip = build_strip(area)

    new_html, n = HERO_P_PATTERN.subn(lambda m: m.group(1) + strip, html, count=1)
    if n != 1:
        return f"WARN  {area['file']} — hero subtitle <p> not found"

    if new_html == original:
        return f"NOCHG {area['file']}"

    path.write_text(new_html, encoding="utf-8")
    return f"OK    {area['file']}  [{postcode_label(area)} · {drive_label(area)}]"


def main():
    for area in AREAS:
        print(" ", process(area))


if __name__ == "__main__":
    main()
