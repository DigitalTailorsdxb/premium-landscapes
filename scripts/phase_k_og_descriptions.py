#!/usr/bin/env python3
"""Sync og:description on the 20 location pages with their <meta name="description">.

Some location pages had a richer, fact-anchored meta description (Phase K work)
but their og:description was still the old short templated string. This script
copies the meta description verbatim into the og:description tag so social
previews on Facebook/LinkedIn/WhatsApp/iMessage match what's in the head."""
import re
import sys
from pathlib import Path
from html import escape, unescape

ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted(
    p for p in ROOT.glob("landscaping-*.html")
    if p.name != "landscaping-cost-uk.html"
)

META_RE = re.compile(
    r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>',
    re.IGNORECASE,
)
OG_RE = re.compile(
    r'(<meta\s+property="og:description"\s+content=")([^"]*)("\s*/?>)',
    re.IGNORECASE,
)


def main() -> int:
    assert len(PAGES) == 20, f"expected 20 location pages, got {len(PAGES)}"
    seen: dict[str, str] = {}
    changed = 0
    for path in PAGES:
        html = path.read_text(encoding="utf-8")
        meta_match = META_RE.search(html)
        og_match = OG_RE.search(html)
        if not meta_match or not og_match:
            print(f"SKIP {path.name}: missing meta/og description tag")
            continue
        meta_content = meta_match.group(1)
        # og:description should mirror meta description. Re-escape just in case
        # the meta description contains unescaped entities (it shouldn't, but
        # we round-trip to be safe).
        new_og = escape(unescape(meta_content), quote=True)
        if og_match.group(2) == new_og:
            continue
        if new_og in seen:
            print(f"WARN {path.name}: og:description duplicates {seen[new_og]}")
        seen[new_og] = path.name
        new_html = html[:og_match.start()] + og_match.group(1) + new_og + og_match.group(3) + html[og_match.end():]
        path.write_text(new_html, encoding="utf-8")
        changed += 1
        print(f"OK   {path.name}")
    print(f"\nUpdated {changed}/{len(PAGES)} pages.")
    # Final duplicate check across all 20.
    descs: dict[str, list[str]] = {}
    for path in PAGES:
        html = path.read_text(encoding="utf-8")
        m = OG_RE.search(html)
        if m:
            descs.setdefault(m.group(2), []).append(path.name)
    dupes = {k: v for k, v in descs.items() if len(v) > 1}
    if dupes:
        print("\nDUPLICATE og:description values found:")
        for v, names in dupes.items():
            print(f"  - {names}: {v[:80]}...")
        return 1
    print("All 20 og:description values are unique.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
