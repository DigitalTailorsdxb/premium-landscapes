#!/usr/bin/env python3
"""
Phase G — Spread priority keywords 'landscaper Leicester' + 'landscaping
company Leicester' to every page via natural placements (no stuffing).

Strategy:
  - 3 footer-tagline variants → keyword-rich replacements (~91 pages)
  - Homepage hero: extend subheading with one keyword sentence
  - About page hero <p>: rewrite to include keywords naturally
  - 4 new service pages (fencing/turfing/pergolas/commercial-astroturf):
    append one keyword-anchored sentence to intro paragraph

Idempotent — safe to re-run.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Footer tagline replacements ----
FOOTER_REPLACEMENTS = [
    # Main pages (12)
    (
        '<p class="text-gray-400">Professional landscaping services with instant quotes and designs.</p>',
        '<p class="text-gray-400">Premium Landscapes — your local landscaper in Leicester and trusted landscaping company for Leicestershire. Patios, driveways, artificial grass, decking and full garden transformations.</p>'
    ),
    # AI/admin pages (5)
    (
        '<p class="text-stone opacity-80">Transforming gardens with AI-powered design and expert craftsmanship.</p>',
        '<p class="text-stone opacity-80">Premium Landscapes — your local landscaper in Leicester and trusted landscaping company across Leicestershire. AI-powered design with expert craftsmanship.</p>'
    ),
]

# Location pages use a per-town tagline — regex-replace
LOCATION_FOOTER_RE = re.compile(
    r'<p class="text-gray-400 text-sm">Professional landscaping across ([A-Za-z][A-Za-z ]+?) and Leicestershire\.\s*instant quotes and design — free, instant, no obligation\.</p>'
)
def location_footer_sub(m):
    town = m.group(1)
    return (
        f'<p class="text-gray-400 text-sm">Premium Landscapes — your local {town} landscaper '
        f'and trusted landscaping company in Leicester &amp; Leicestershire. '
        f'Free instant quotes and AI garden design — no obligation.</p>'
    )

# ---- Homepage hero subheading: append a keyword sentence ----
HOMEPAGE_HERO_OLD = (
    '<p class="text-lg md:text-2xl mb-5 md:mb-7 max-w-3xl mx-auto text-shadow-strong">\n'
    '                Premium Landscapes designs and builds <strong>patios, artificial grass, composite decking, driveways</strong> and full garden transformations across Leicester and Leicestershire.\n'
    '            </p>'
)
HOMEPAGE_HERO_NEW = (
    '<p class="text-lg md:text-2xl mb-5 md:mb-7 max-w-3xl mx-auto text-shadow-strong">\n'
    '                Premium Landscapes designs and builds <strong>patios, artificial grass, composite decking, driveways</strong> and full garden transformations across Leicester and Leicestershire. As a trusted landscaping company in Leicester and your local landscaper, we cover every property type from compact courtyards to full estate gardens.\n'
    '            </p>'
)

# ---- About page hero <p> ----
ABOUT_HERO_OLD = (
    '<p class="text-xl md:text-2xl mb-10 text-shadow-strong">Transforming outdoor spaces with expertise, innovation, and a passion for exceptional design.</p>'
)
ABOUT_HERO_NEW = (
    '<p class="text-xl md:text-2xl mb-10 text-shadow-strong">Your trusted landscaping company in Leicester — a local landscaper transforming outdoor spaces with expertise, innovation, and a passion for exceptional design.</p>'
)

# ---- 4 service page intros: append a sentence to first intro paragraph ----
SERVICE_INTRO_APPENDS = {
    'fencing-leicester.html': (
        'No skimped posts, no wobbling panels 12 months later.</p>',
        'No skimped posts, no wobbling panels 12 months later. As your local landscaper in Leicester and a trusted landscaping company across Leicestershire, we install fencing to a standard you can rely on for years.</p>'
    ),
    'turfing-leicester.html': (
        'just a properly prepared seedbed, quality turf, and a lawn that establishes quickly and stays looking good.</p>',
        'just a properly prepared seedbed, quality turf, and a lawn that establishes quickly and stays looking good. As your local landscaper in Leicester and a trusted landscaping company across Leicestershire, we lay lawns built to last.</p>'
    ),
    'pergolas-leicester.html': (
        'Premium Landscapes designs and installs pergolas across Leicester and Leicestershire.</p>',
        'Premium Landscapes designs and installs pergolas across Leicester and Leicestershire. As your local landscaper in Leicester and a trusted landscaping company, we design pergolas that integrate cleanly with the rest of your garden.</p>'
    ),
    'commercial-astroturf-leicester.html': (
        'with specifications tailored to the use case, occupancy requirements and any relevant safety standards.</p>',
        'with specifications tailored to the use case, occupancy requirements and any relevant safety standards. As a trusted landscaping company in Leicester and your local commercial landscaper, we deliver turf systems built for high-use environments.</p>'
    ),
}

# ---- Minimal-footer pages: inject keyword tagline before copyright ----
MINIMAL_FOOTER_ANCHOR = '<p class="text-sm text-gray-500 mb-2">&copy; 2026 Premium Landscapes. All rights reserved.'
MINIMAL_FOOTER_INJECTION = (
    '<p class="text-sm text-gray-600 mb-3 max-w-2xl mx-auto">Premium Landscapes — your local landscaper in Leicester and trusted landscaping company across Leicestershire. Free instant quotes and AI garden design — no obligation.</p>\n'
    '            ' + MINIMAL_FOOTER_ANCHOR
)
# Guard token so idempotent — only inject if our tagline isn't already present
MINIMAL_FOOTER_GUARD = 'your local landscaper in Leicester and trusted landscaping company across Leicestershire. Free instant quotes'

# ----------------------------------------------------------
def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        orig = f.read()
    new = orig

    # Footer tagline — fixed replacements
    for old, repl in FOOTER_REPLACEMENTS:
        if old in new:
            new = new.replace(old, repl)

    # Footer tagline — per-town regex
    new = LOCATION_FOOTER_RE.sub(location_footer_sub, new)

    base = os.path.basename(path)

    # Homepage hero
    if base == 'index.html' and HOMEPAGE_HERO_OLD in new:
        new = new.replace(HOMEPAGE_HERO_OLD, HOMEPAGE_HERO_NEW)

    # About hero
    if base == 'about.html' and ABOUT_HERO_OLD in new:
        new = new.replace(ABOUT_HERO_OLD, ABOUT_HERO_NEW)

    # Service page intro appends
    if base in SERVICE_INTRO_APPENDS:
        old, repl = SERVICE_INTRO_APPENDS[base]
        if old in new:
            new = new.replace(old, repl)

    # Minimal-footer injection (52 pages)
    if MINIMAL_FOOTER_ANCHOR in new and MINIMAL_FOOTER_GUARD not in new:
        new = new.replace(MINIMAL_FOOTER_ANCHOR, MINIMAL_FOOTER_INJECTION, 1)

    if new != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        return True
    return False

def main():
    files = sorted(glob.glob(os.path.join(ROOT, '*.html')))
    changed = []
    for p in files:
        if process_file(p):
            changed.append(os.path.basename(p))
    print(f'Modified {len(changed)} files')
    for c in changed[:15]:
        print(' -', c)
    if len(changed) > 15:
        print(f' ... and {len(changed)-15} more')

if __name__ == '__main__':
    main()
