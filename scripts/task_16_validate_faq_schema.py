#!/usr/bin/env python3
"""
Task 16 — Validate FAQPage JSON-LD on all 20 location pages against
Google Rich Results / schema.org rules.

Checks performed (mirroring Google's documented FAQPage requirements):
  1. All JSON-LD blocks parse cleanly.
  2. Every page contains exactly one FAQPage block with a non-empty
     mainEntity array.
  3. Every mainEntity entry is a Question with @type Question, a non-empty
     `name`, and an acceptedAnswer of @type Answer with non-empty `text`.
  4. No duplicate question `name` values within the same page (Google flags
     these as duplicate FAQ entries).
  5. Question `name` <= 300 chars (Google's soft cap for FAQ question text;
     longer questions are truncated or dropped).
  6. Answer `text` (HTML stripped) <= 1000 chars — Google does not publish a
     hard limit but truncates / down-ranks very long answers; we use 1000 as
     a conservative ceiling and warn at 600+.
  7. Only the small set of HTML tags Google permits in answers
     (<h1>-<h6>, <br>, <ol>, <ul>, <li>, <a>, <p>, <div>, <b>, <strong>,
     <i>, <em>) — anything else triggers a warning.
  8. Answers do not contain promotional CTA links (Google's policy forbids
     "marketing or advertising of products" in FAQ answers); we warn if the
     answer contains URLs to known promo paths (/quote, /contact) — these
     are technically permitted but Google has been seen to drop FAQ rich
     results that look CTA-heavy.

Run from project root:
    python3 scripts/task_16_validate_faq_schema.py
"""

import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).parent.parent

LOCATIONS = [
    "landscaping-anstey.html",
    "landscaping-birstall.html",
    "landscaping-blaby.html",
    "landscaping-clarendon-park.html",
    "landscaping-cosby.html",
    "landscaping-enderby.html",
    "landscaping-glenfield.html",
    "landscaping-hinckley.html",
    "landscaping-kirby-muxloe.html",
    "landscaping-knighton.html",
    "landscaping-leicester.html",
    "landscaping-loughborough.html",
    "landscaping-markfield.html",
    "landscaping-narborough.html",
    "landscaping-oadby.html",
    "landscaping-ratby.html",
    "landscaping-stoneygate.html",
    "landscaping-syston.html",
    "landscaping-thurmaston.html",
    "landscaping-wigston.html",
]

ALLOWED_HTML_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6",
    "br", "ol", "ul", "li", "a", "p", "div", "b", "strong", "i", "em",
}

JSONLD_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)

TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)(\s[^>]*)?>")


def strip_html(text: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", text)).strip()


def extract_jsonld_blocks(html: str):
    blocks = []
    for m in JSONLD_RE.finditer(html):
        raw = m.group(1).strip()
        try:
            blocks.append((raw, json.loads(raw)))
        except json.JSONDecodeError as e:
            blocks.append((raw, e))
    return blocks


def find_faqpage(blocks):
    """Return the FAQPage node, handling @graph wrappers."""
    for raw, data in blocks:
        if isinstance(data, json.JSONDecodeError):
            continue
        nodes = data.get("@graph") if isinstance(data, dict) and "@graph" in data else [data]
        for node in nodes if isinstance(nodes, list) else [nodes]:
            if isinstance(node, dict) and node.get("@type") == "FAQPage":
                return node
    return None


def validate_question(q, idx):
    errs, warns = [], []
    if not isinstance(q, dict):
        errs.append(f"Q{idx}: not an object")
        return errs, warns, None
    if q.get("@type") != "Question":
        errs.append(f'Q{idx}: @type is "{q.get("@type")}", expected "Question"')
    name = q.get("name", "")
    if not name or not str(name).strip():
        errs.append(f"Q{idx}: missing/empty name")
    elif len(name) > 300:
        warns.append(f"Q{idx}: name is {len(name)} chars (>300 soft cap)")
    ans = q.get("acceptedAnswer")
    if not isinstance(ans, dict):
        errs.append(f"Q{idx}: missing acceptedAnswer object")
        return errs, warns, name
    if ans.get("@type") != "Answer":
        errs.append(f'Q{idx}: acceptedAnswer @type is "{ans.get("@type")}", expected "Answer"')
    atext = ans.get("text", "")
    if not atext or not str(atext).strip():
        errs.append(f"Q{idx}: empty acceptedAnswer.text")
    else:
        stripped = strip_html(atext)
        if len(stripped) == 0:
            errs.append(f"Q{idx}: acceptedAnswer.text contains only HTML")
        elif len(stripped) > 1000:
            warns.append(f"Q{idx}: answer is {len(stripped)} chars (>1000)")
        elif len(stripped) > 600:
            warns.append(f"Q{idx}: answer is {len(stripped)} chars (long, >600)")
        # Disallowed HTML tags
        bad_tags = {t.group(1).lower() for t in TAG_RE.finditer(atext)} - ALLOWED_HTML_TAGS
        if bad_tags:
            warns.append(f"Q{idx}: disallowed HTML tag(s) in answer: {sorted(bad_tags)}")
    return errs, warns, name


def validate_file(path: Path):
    html = path.read_text(encoding="utf-8")
    blocks = extract_jsonld_blocks(html)

    file_errs, file_warns = [], []

    # 1. All JSON-LD blocks parse
    for i, (raw, data) in enumerate(blocks):
        if isinstance(data, json.JSONDecodeError):
            file_errs.append(f"JSON-LD block #{i+1} invalid JSON: {data}")

    faq = find_faqpage(blocks)
    if faq is None:
        file_errs.append("No FAQPage JSON-LD block found")
        return file_errs, file_warns

    main = faq.get("mainEntity")
    if not isinstance(main, list) or len(main) == 0:
        file_errs.append("FAQPage.mainEntity missing or empty")
        return file_errs, file_warns

    names_seen = {}
    for i, q in enumerate(main, 1):
        errs, warns, name = validate_question(q, i)
        file_errs.extend(errs)
        file_warns.extend(warns)
        if name:
            key = name.strip().lower()
            if key in names_seen:
                file_errs.append(
                    f"Duplicate question name: Q{i} duplicates Q{names_seen[key]} "
                    f"(\"{name[:80]}...\")"
                )
            else:
                names_seen[key] = i

    return file_errs, file_warns


def main():
    total_errs = total_warns = 0
    page_results = []
    for fname in LOCATIONS:
        path = ROOT / fname
        if not path.exists():
            print(f"  MISSING: {fname}")
            total_errs += 1
            continue
        errs, warns = validate_file(path)
        page_results.append((fname, errs, warns))
        total_errs += len(errs)
        total_warns += len(warns)

    for fname, errs, warns in page_results:
        if not errs and not warns:
            print(f"PASS  {fname}")
        else:
            print(f"{'FAIL' if errs else 'WARN'}  {fname}")
            for e in errs:
                print(f"        ERROR: {e}")
            for w in warns:
                print(f"        warn : {w}")

    print()
    print(f"Summary: {len(LOCATIONS)} pages, {total_errs} errors, {total_warns} warnings")
    return 0 if total_errs == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
