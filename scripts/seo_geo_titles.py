#!/usr/bin/env python3
"""Task 2.2 — Rewrite geo-page <title> and meta description to compliant lengths.

Idempotent: re-running produces the same result. For each landscaping-[town] page it
sets the <title>, og:title and twitter:title to the short town title, and rewrites the
meta description to <=155 chars (town name twice, one service, one CTA).
"""
import re
import sys

# town slug -> (new title, new meta description)
PAGES = {
    "leicester": (
        "Landscaping in Leicester | Premium Landscapes",
        "Landscaping in Leicester by a local, fully insured team. Patios, "
        "driveways &amp; artificial grass across Leicester. Free instant quote today.",
    ),
    "oadby": (
        "Landscaping in Oadby | Premium Landscapes",
        "Landscaping in Oadby for suburban gardens \u2014 patios, artificial grass "
        "&amp; driveways across Oadby LE2. Local, insured team. Free instant quote.",
    ),
    "wigston": (
        "Landscaping in Wigston | Premium Landscapes",
        "Landscaping in Wigston LE18 \u2014 patios, artificial grass &amp; composite "
        "decking for Wigston gardens. Local, insured team. Free instant quote.",
    ),
    "narborough": (
        "Landscaping in Narborough | Premium Landscapes",
        "Landscaping in Narborough LE19 \u2014 patios, artificial grass &amp; garden "
        "makeovers across Narborough &amp; Littlethorpe. Insured. Free instant quote.",
    ),
    "loughborough": (
        "Landscaping in Loughborough | Premium Landscapes",
        "Landscaping in Loughborough LE11 \u2014 patios, artificial grass &amp; "
        "driveways across Loughborough. Local, insured team. Free instant quote.",
    ),
    "hinckley": (
        "Landscaping in Hinckley | Premium Landscapes",
        "Landscaping in Hinckley LE10 \u2014 patios, artificial grass &amp; garden "
        "makeovers across Hinckley, Burbage &amp; Earl Shilton. Free instant quote.",
    ),
    "birstall": (
        "Landscaping in Birstall | Premium Landscapes",
        "Landscaping in Birstall LE4 \u2014 patios, artificial grass &amp; driveways "
        "for Birstall &amp; Wanlip gardens. Local, insured. Free instant quote.",
    ),
    "syston": (
        "Landscaping in Syston | Premium Landscapes",
        "Landscaping in Syston LE7 \u2014 patios, artificial grass &amp; garden "
        "makeovers across Syston &amp; the River Wreake area. Free instant quote.",
    ),
}


def strip_len(meta: str) -> int:
    """Approx visible length (treat &amp; as one char)."""
    return len(meta.replace("&amp;", "&"))


def apply(slug: str, title: str, meta: str) -> None:
    path = f"landscaping-{slug}.html"
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    orig = html

    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{meta}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{title}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{title}">',
        html,
        count=1,
    )

    if html != orig:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        status = "updated"
    else:
        status = "unchanged"
    print(f"{path}: {status} | title {len(title)} chars | meta {strip_len(meta)} chars")


def main() -> int:
    for slug, (title, meta) in PAGES.items():
        if strip_len(meta) > 155:
            print(f"WARNING: {slug} meta is {strip_len(meta)} chars (>155)")
        apply(slug, title, meta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
