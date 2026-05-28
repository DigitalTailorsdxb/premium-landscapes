#!/usr/bin/env python3
"""Rename /blog-N URLs to descriptive slugs across the entire site.

Single-pass, idempotent on a clean working tree. Steps:
  1. Rename blog-N.html -> <slug>.html (git mv equivalent — just shutil.move).
  2. Sweep every .html file: replace /blog-N and blog-N.html references with
     /<slug> and <slug>.html (longest-first to avoid /blog-1 swallowing /blog-10).
  3. Rewrite the 20 blog lines in _redirects to point .html -> /<slug>, then
     append 20 new /blog-N -> /<slug> 301 rules.
  4. Rewrite blog <loc> URLs in sitemap.xml to /<slug>.
  5. Print a verification report.
"""
from __future__ import annotations
import os, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

SLUG_MAP = {
    1:  "garden-redesign-cost-uk",
    2:  "modern-garden-design-ideas",
    3:  "artificial-grass-vs-natural-turf",
    4:  "best-patio-materials-uk",
    5:  "composite-vs-timber-decking",
    6:  "outdoor-garden-lighting-ideas",
    7:  "family-garden-design-ideas",
    8:  "seasonal-garden-maintenance",
    9:  "garden-makeover-property-value",
    10: "ai-garden-design-tools",
    11: "suds-driveway-rules-leicester",
    12: "patio-sub-base-guide-uk",
    13: "permitted-development-gardens-uk",
    14: "conservation-areas-leicester-landscaping",
    15: "drainage-leicestershire-clay-gardens",
    16: "composite-decking-brands-compared-uk",
    17: "artificial-grass-specifications-guide",
    18: "resin-bound-vs-block-paving-driveways",
    19: "garden-lighting-regulations-uk",
    20: "patio-materials-leicestershire-clay-soil",
}
# Process longer numbers first so /blog-1 doesn't match the start of /blog-10.
ORDERED = sorted(SLUG_MAP.items(), key=lambda kv: -kv[0])

# ---- Step 1: rename files ------------------------------------------------
print("=== Step 1: rename blog-N.html -> <slug>.html ===")
for n, slug in SLUG_MAP.items():
    src = ROOT / f"blog-{n}.html"
    dst = ROOT / f"{slug}.html"
    if src.exists():
        if dst.exists():
            print(f"  SKIP {src.name} -> {dst.name} (dst already exists)")
            continue
        shutil.move(str(src), str(dst))
        print(f"  mv  {src.name} -> {dst.name}")
    else:
        print(f"  ??  {src.name} not found (already renamed?)")

# ---- Step 2: sweep every .html file --------------------------------------
print("\n=== Step 2: sweep all .html for /blog-N and blog-N.html references ===")
# Build two regex pairs per blog id. Use negative lookahead to require the
# blog number is not followed by another digit (so /blog-1 won't match /blog-10).
# Word boundary alone doesn't work because '-' is non-word and digits are word.
def make_subs():
    subs = []
    for n, slug in ORDERED:
        # /blog-N not followed by a digit  ->  /<slug>
        subs.append((re.compile(rf"/blog-{n}(?!\d)"), f"/{slug}"))
        # blog-N.html (relative)  ->  <slug>.html
        subs.append((re.compile(rf"\bblog-{n}\.html\b"), f"{slug}.html"))
    return subs

SUBS = make_subs()
changed = 0
touched_files = []
for path in sorted(ROOT.glob("*.html")):
    if path.name == "blog.html":
        # process below too — but include here
        pass
    text = path.read_text(encoding="utf-8")
    new_text = text
    for pat, repl in SUBS:
        new_text = pat.sub(repl, new_text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        changed += 1
        touched_files.append(path.name)
print(f"  updated {changed} .html files")
for f in touched_files[:30]:
    print(f"    - {f}")
if len(touched_files) > 30:
    print(f"    ... and {len(touched_files)-30} more")

# ---- Step 3: rewrite _redirects ------------------------------------------
print("\n=== Step 3: rewrite _redirects ===")
redir_path = ROOT / "_redirects"
lines = redir_path.read_text(encoding="utf-8").splitlines()
out_lines = []
removed_old = 0
for line in lines:
    # Drop the 20 existing "/blog-N.html /blog-N 301" rules — we'll regenerate.
    m = re.match(r"^/blog-(\d+)\.html\s+/blog-\d+\s+301\s*$", line)
    if m and int(m.group(1)) in SLUG_MAP:
        removed_old += 1
        continue
    out_lines.append(line)
# Append the two new rule sets at the end, grouped.
out_lines.append("")
out_lines.append("# Blog URL rename (slug migration) — old .html -> new slug")
for n in sorted(SLUG_MAP.keys()):
    out_lines.append(f"/blog-{n}.html /{SLUG_MAP[n]} 301")
out_lines.append("")
out_lines.append("# Blog URL rename — old /blog-N -> new slug (no chains, direct)")
for n in sorted(SLUG_MAP.keys()):
    out_lines.append(f"/blog-{n} /{SLUG_MAP[n]} 301")
out_lines.append("")
out_lines.append("# Clean-URL serving for new blog slugs (.html -> clean URL)")
for n in sorted(SLUG_MAP.keys()):
    slug = SLUG_MAP[n]
    out_lines.append(f"/{slug}.html /{slug} 301")
redir_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
print(f"  removed {removed_old} old blog-N.html rules")
print(f"  appended {len(SLUG_MAP)*3} new rules (.html->slug + /blog-N->slug + slug.html->slug)")

# ---- Step 4: rewrite sitemap.xml -----------------------------------------
print("\n=== Step 4: rewrite sitemap.xml blog URLs ===")
smap = ROOT / "sitemap.xml"
text = smap.read_text(encoding="utf-8")
sm_changes = 0
for n, slug in ORDERED:
    new_text, k = re.subn(
        rf"(https://www\.premium-landscapes\.co\.uk)/blog-{n}(?!\d)",
        rf"\1/{slug}",
        text,
    )
    if k:
        text = new_text
        sm_changes += k
smap.write_text(text, encoding="utf-8")
print(f"  replaced {sm_changes} sitemap blog URLs")

# ---- Step 5: verify ------------------------------------------------------
print("\n=== Step 5: verification ===")
# Any stale /blog-N references anywhere?
stale = []
for path in ROOT.glob("*.html"):
    txt = path.read_text(encoding="utf-8")
    for n in SLUG_MAP:
        if re.search(rf"/blog-{n}(?!\d)", txt) or re.search(rf"\bblog-{n}\.html\b", txt):
            stale.append((path.name, n))
if stale:
    print("  ❌ STALE references found:")
    for f, n in stale[:30]:
        print(f"    - {f}: /blog-{n}")
else:
    print("  ✅ no stale /blog-N references in any HTML file")

# sitemap clean?
sm_stale = re.findall(r"/blog-\d+(?!\d)", smap.read_text(encoding="utf-8"))
if sm_stale:
    print(f"  ❌ sitemap has stale: {sm_stale}")
else:
    print("  ✅ sitemap has no /blog-N references")

# all new files exist?
missing = [s for s in SLUG_MAP.values() if not (ROOT / f"{s}.html").exists()]
if missing:
    print(f"  ❌ missing slug files: {missing}")
else:
    print(f"  ✅ all {len(SLUG_MAP)} slug.html files exist")

print("\nDone.")
