#!/usr/bin/env python3
"""
Task 20 — Insert hero trust-badge strip on the 7 service pages, mirroring the
location-page pattern added by scripts/task_15_trust_badges.py.

Reuses the existing `.hero-trust-badges` / `.trust-badge` styles in
styles/liquid-glass.css (no CSS changes required).

Badges here are service-appropriate (not location-specific): they reinforce
the local/insured/fixed-price story for service-intent visitors.

Idempotent: strips any previously-inserted block before re-inserting.
"""

import re
import pathlib

ROOT = pathlib.Path(__file__).parent.parent

SERVICES = [
    {
        "file": "patios.html",
        "subtitle_class": "text-blue-200 text-lg mb-8 max-w-2xl mx-auto",
        "badges": [
            ("💷", "Fixed-price quote"),
            ("🛡️", "Fully insured"),
            ("✨", "Free AI design preview"),
        ],
    },
    {
        "file": "artificial-grass.html",
        "subtitle_class": "text-blue-200 text-lg mb-8 max-w-2xl mx-auto",
        "badges": [
            ("💷", "Fixed-price quote"),
            ("🛡️", "Fully insured"),
            ("✨", "Free AI design preview"),
        ],
    },
    {
        "file": "composite-decking.html",
        "subtitle_class": "text-blue-200 text-lg mb-8 max-w-2xl mx-auto",
        "badges": [
            ("💷", "Fixed-price quote"),
            ("🛡️", "Fully insured"),
            ("✨", "Free AI design preview"),
        ],
    },
    {
        "file": "driveways.html",
        "subtitle_class": "text-blue-200 text-lg mb-8 max-w-2xl mx-auto",
        "badges": [
            ("💷", "Fixed-price quote"),
            ("🛡️", "Fully insured"),
            ("✨", "Free AI design preview"),
        ],
    },
    {
        "file": "garden-lighting.html",
        "subtitle_class": "text-blue-200 text-lg mb-8 max-w-2xl mx-auto",
        "badges": [
            ("💷", "Fixed-price quote"),
            ("🛡️", "Fully insured"),
            ("✨", "Free AI design preview"),
        ],
    },
    {
        "file": "full-garden-makeover.html",
        "subtitle_class": "text-blue-200 text-lg mb-8 max-w-2xl mx-auto",
        "badges": [
            ("💷", "Fixed-price quote"),
            ("🛡️", "Fully insured"),
            ("✨", "Free AI design preview"),
        ],
    },
    {
        "file": "ai-garden-design.html",
        "subtitle_class": "text-xl text-blue-100 mb-4 max-w-2xl mx-auto",
        "badges": [
            ("✨", "100% free"),
            ("⚡", "90-second delivery"),
            ("✅", "No obligation"),
        ],
    },
]

EXISTING_STRIP_PATTERN = re.compile(
    r'\s*<div class="hero-trust-badges"[^>]*>.*?</div>',
    re.DOTALL,
)


def build_strip(badges):
    lines = [
        '\n            <div class="hero-trust-badges" aria-label="Service trust signals">'
    ]
    for icon, label in badges:
        lines.append(
            f'                <span class="trust-badge"><span class="trust-badge-icon" aria-hidden="true">{icon}</span>{label}</span>'
        )
    lines.append('            </div>')
    return "\n".join(lines)


def process(service):
    path = ROOT / service["file"]
    if not path.exists():
        return f"SKIP  {service['file']} — not found"

    html = path.read_text(encoding="utf-8")
    original = html

    html = EXISTING_STRIP_PATTERN.sub("", html)

    pattern = re.compile(
        r'(<p class="' + re.escape(service["subtitle_class"]) + r'">.*?</p>)',
        re.DOTALL,
    )
    strip = build_strip(service["badges"])
    new_html, n = pattern.subn(lambda m: m.group(1) + strip, html, count=1)
    if n != 1:
        return f"WARN  {service['file']} — hero subtitle <p> not found"

    if new_html == original:
        return f"NOCHG {service['file']}"

    path.write_text(new_html, encoding="utf-8")
    return f"OK    {service['file']}"


def main():
    for service in SERVICES:
        print(" ", process(service))


if __name__ == "__main__":
    main()
