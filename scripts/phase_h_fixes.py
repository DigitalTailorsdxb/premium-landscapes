#!/usr/bin/env python3
"""
Phase H — Seven audit fixes:
  1. Copyright 2025 → 2026 on all 20 location pages
  2. "Leicester & the Midlands" wording → "Leicester & Leicestershire" sitewide
  3. Add missing JSON-LD schema to 12 content pages
  4. Add email to contact.html LocalBusiness JSON-LD
  5. (Reviews handled separately in config.js + index.html)
  6. (Canonical: only 404.html missing — 404 pages don't carry canonical; skip)
  7. (Sitemap/robots already correct)
Idempotent — safe to re-run.
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.premium-landscapes.co.uk"

# ---------------------------------------------------------------------------
# 1. Copyright 2025 → 2026
# ---------------------------------------------------------------------------
COPYRIGHT_OLD = '&copy; 2025 Premium Landscapes'
COPYRIGHT_NEW = '&copy; 2026 Premium Landscapes'

# ---------------------------------------------------------------------------
# 2. "Midlands" wording replacements (ordered longest → shortest to avoid
#    partial double-replacements; does NOT touch "East Midlands")
# ---------------------------------------------------------------------------
MIDLANDS_REPLACEMENTS = [
    # Explicit "and Home Counties" combos first
    ("Leicester, the Midlands and Home Counties",      "Leicester and Leicestershire"),
    ("leicester, the midlands and home counties",      "leicester and leicestershire"),
    ("across the Midlands and Home Counties",          "across Leicestershire"),
    ("the Midlands and Home Counties",                 "Leicestershire"),
    # "the wider Midlands" variants
    ("Leicester and the wider Midlands",               "Leicester and Leicestershire"),
    ("leicester and the wider Midlands",               "leicester and Leicestershire"),
    ("the wider Midlands",                             "Leicestershire"),
    ("Leicestershire and the wider Midlands",          "Leicestershire"),
    # "and the Midlands" / "& the Midlands"
    ("Leicester and the Midlands",                     "Leicester and Leicestershire"),
    ("leicester and the Midlands",                     "leicester and Leicestershire"),
    ("Leicester & the Midlands",                       "Leicester & Leicestershire"),
    # "across the Midlands" (where standalone, not East Midlands)
    # Only replace when NOT preceded by "East " — handled by regex below
    # Oadby / town + "the Midlands"
    ("Oadby and the wider East Midlands",              "Oadby and Leicestershire"),
    ("Oadby and across the Midlands",                  "Oadby and across Leicestershire"),
    ("on, Oadby and across the Midlands",              "on, Oadby and across Leicestershire"),
    # "Midlands for over" (if appears)
    ("Midlands for over",                              "Leicestershire for over"),
    # Generic standalone when not East
    ("serving the Midlands and Home Counties",         "serving Leicester and Leicestershire"),
    ("eicester and serving the Midlands and Home Counties",
                                                       "eicester and Leicestershire"),
]

# Regex for remaining "across the Midlands" not preceded by "East "
MIDLANDS_ACROSS_RE = re.compile(r'(?<!East )across the Midlands\b')

# ---------------------------------------------------------------------------
# 3. JSON-LD schemas to inject for each missing page
# ---------------------------------------------------------------------------
def make_schema(page_slug, page_type, name, description=None, breadcrumbs=None,
                extra=None):
    """Build a @graph JSON-LD block for a page."""
    if breadcrumbs is None:
        breadcrumbs = [("Home", "/"), (name.split("|")[0].strip(), f"/{page_slug}")]

    items = []

    # WebPage / ContactPage / CollectionPage etc.
    page_node = {
        "@type": page_type,
        "@id": f"{BASE}/{page_slug}#page",
        "url": f"{BASE}/{page_slug}",
        "name": name,
        "breadcrumb": {"@id": f"{BASE}/{page_slug}#breadcrumb"},
        "inLanguage": "en-GB"
    }
    if description:
        page_node["description"] = description
    if extra:
        page_node.update(extra)
    items.append(page_node)

    # BreadcrumbList
    crumb_node = {
        "@type": "BreadcrumbList",
        "@id": f"{BASE}/{page_slug}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": label,
                "item": f"{BASE}{url}" if url != "/" else BASE + "/"
            }
            for i, (label, url) in enumerate(breadcrumbs)
        ]
    }
    items.append(crumb_node)

    return {
        "@context": "https://schema.org",
        "@graph": items
    }


SCHEMAS = {
    "contact.html": {
        "pre_slug": "contact",
        "schema": {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "ContactPage",
                    "@id": f"{BASE}/contact#page",
                    "url": f"{BASE}/contact",
                    "name": "Contact Premium Landscapes | Landscapers in Leicester",
                    "description": "Get in touch with Premium Landscapes — your local landscaper in Leicester. Call, WhatsApp or email us for a free instant quote.",
                    "breadcrumb": {"@id": f"{BASE}/contact#breadcrumb"},
                    "inLanguage": "en-GB"
                },
                {
                    "@type": "BreadcrumbList",
                    "@id": f"{BASE}/contact#breadcrumb",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                        {"@type": "ListItem", "position": 2, "name": "Contact", "item": f"{BASE}/contact"}
                    ]
                },
                {
                    "@type": "LocalBusiness",
                    "@id": f"{BASE}/#business",
                    "name": "Premium Landscapes",
                    "telephone": "+447877934782",
                    "email": "premiumlandscapesuk@gmail.com",
                    "url": f"{BASE}/",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "44 Barwell Road",
                        "addressLocality": "Kirby Muxloe",
                        "addressRegion": "Leicestershire",
                        "postalCode": "LE9 2AA",
                        "addressCountry": "GB"
                    },
                    "openingHoursSpecification": [
                        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "07:30", "closes": "18:00"},
                        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "16:00"}
                    ]
                }
            ]
        }
    },
    "gallery.html": {
        "pre_slug": "gallery",
        "schema": make_schema(
            "gallery", "CollectionPage",
            "Garden Transformations Gallery | Leicester | Premium Landscapes",
            description="Browse completed garden projects across Leicester and Leicestershire — patios, artificial grass, composite decking and full garden makeovers.",
            breadcrumbs=[("Home", "/"), ("Gallery", "/gallery")]
        )
    },
    "services.html": {
        "pre_slug": "services",
        "schema": {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebPage",
                    "@id": f"{BASE}/services#page",
                    "url": f"{BASE}/services",
                    "name": "Landscaping Services Leicester | Patios, Decking, Driveways & More | Premium Landscapes",
                    "description": "Landscaping services in Leicester and Leicestershire — patios, artificial grass, composite decking, driveways and full garden makeovers. Free instant AI quote.",
                    "breadcrumb": {"@id": f"{BASE}/services#breadcrumb"},
                    "inLanguage": "en-GB"
                },
                {
                    "@type": "BreadcrumbList",
                    "@id": f"{BASE}/services#breadcrumb",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                        {"@type": "ListItem", "position": 2, "name": "Landscaping Services Leicester", "item": f"{BASE}/services"}
                    ]
                },
                {
                    "@type": "ItemList",
                    "name": "Landscaping Services in Leicester",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Patio Installation Leicester", "url": f"{BASE}/patios"},
                        {"@type": "ListItem", "position": 2, "name": "Artificial Grass Leicester", "url": f"{BASE}/artificial-grass"},
                        {"@type": "ListItem", "position": 3, "name": "Composite Decking Leicester", "url": f"{BASE}/composite-decking"},
                        {"@type": "ListItem", "position": 4, "name": "Driveways Leicester", "url": f"{BASE}/driveways"},
                        {"@type": "ListItem", "position": 5, "name": "Garden Lighting Leicester", "url": f"{BASE}/garden-lighting"},
                        {"@type": "ListItem", "position": 6, "name": "Full Garden Makeover Leicester", "url": f"{BASE}/full-garden-makeover"}
                    ]
                }
            ]
        }
    },
    "quote.html": {
        "pre_slug": "quote",
        "schema": make_schema(
            "quote", "WebPage",
            "Free AI Garden Quote & Design Visualisation | Premium Landscapes Leicester",
            description="Get a free instant garden quote and photorealistic AI design visualisation from Premium Landscapes — your local landscaper in Leicester.",
            breadcrumbs=[("Home", "/"), ("Get a Free Quote", "/quote")]
        )
    },
    "areas-we-cover.html": {
        "pre_slug": "areas-we-cover",
        "schema": make_schema(
            "areas-we-cover", "WebPage",
            "Areas We Cover | Landscaping Across Leicester & Leicestershire | Premium Landscapes",
            description="Premium Landscapes covers Leicester, Oadby, Wigston, Narborough, Loughborough, Hinckley and 20+ areas across Leicestershire.",
            breadcrumbs=[("Home", "/"), ("Areas We Cover", "/areas-we-cover")]
        )
    },
    "privacy-policy.html": {
        "pre_slug": "privacy-policy",
        "schema": make_schema(
            "privacy-policy", "WebPage",
            "Privacy Policy | Premium Landscapes Leicester",
            description="Privacy policy for Premium Landscapes — how we collect, use and protect your data.",
            breadcrumbs=[("Home", "/"), ("Privacy Policy", "/privacy-policy")]
        )
    },
}

# 6 calculator pages
CALC_PAGES = {
    "patio-cost-calculator.html":              ("Patio Cost Calculator UK 2026 | Instant Price Estimate | Premium Landscapes", "patio-cost-calculator", "Calculate the cost of a new patio in Leicester and the UK. Enter your area and material choice for an instant price estimate."),
    "artificial-grass-cost-calculator.html":   ("Artificial Grass Cost Calculator UK 2026 | Instant Price Estimate | Premium Landscapes", "artificial-grass-cost-calculator", "Calculate artificial grass installation costs instantly. Enter your lawn area and specification for a free price estimate."),
    "composite-decking-cost-calculator.html":  ("Composite Decking Cost Calculator UK 2026 | Instant Price Estimate | Premium Landscapes", "composite-decking-cost-calculator", "Estimate the cost of composite decking for your garden. Enter dimensions and board grade for an instant Leicester price guide."),
    "garden-design-cost-calculator.html":      ("Garden Design Cost Calculator UK 2026 | Instant Price Estimate | Premium Landscapes", "garden-design-cost-calculator", "Estimate garden design and landscaping costs across Leicester and Leicestershire with our free instant calculator."),
    "garden-landscaping-cost-calculator.html": ("Garden Landscaping Cost Calculator UK 2026 | Instant Estimate | Premium Landscapes", "garden-landscaping-cost-calculator", "Calculate full garden landscaping costs for Leicester and Leicestershire projects. Instant estimate by area and specification."),
    "garden-makeover-cost-calculator.html":    ("Garden Makeover Cost Calculator UK 2026 | Instant Price Estimate | Premium Landscapes", "garden-makeover-cost-calculator", "Estimate the cost of a full garden makeover in Leicester. Enter your garden size for an instant price range."),
}

for fname, (title, slug, desc) in CALC_PAGES.items():
    service_name = slug.replace("-cost-calculator", "").replace("-", " ").title()
    breadcrumbs = [("Home", "/"), ("Cost Guides", "/cost-guide"), (f"{service_name} Calculator", f"/{slug}")]
    SCHEMAS[fname] = {
        "pre_slug": slug,
        "schema": {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebApplication",
                    "@id": f"{BASE}/{slug}#app",
                    "url": f"{BASE}/{slug}",
                    "name": title,
                    "description": desc,
                    "applicationCategory": "UtilityApplication",
                    "operatingSystem": "Web",
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP"},
                    "breadcrumb": {"@id": f"{BASE}/{slug}#breadcrumb"},
                    "inLanguage": "en-GB",
                    "provider": {"@id": f"{BASE}/#business"}
                },
                {
                    "@type": "BreadcrumbList",
                    "@id": f"{BASE}/{slug}#breadcrumb",
                    "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": label, "item": f"{BASE}{url}" if url != "/" else f"{BASE}/"}
                        for i, (label, url) in enumerate(breadcrumbs)
                    ]
                }
            ]
        }
    }

# ---------------------------------------------------------------------------
def process_file(path):
    fname = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        orig = f.read()
    new = orig

    # 1. Copyright 2025 → 2026
    if Copyright_OLD := COPYRIGHT_OLD:
        new = new.replace(COPYRIGHT_OLD, COPYRIGHT_NEW)

    # 2. Midlands wording replacements
    for old, repl in MIDLANDS_REPLACEMENTS:
        new = new.replace(old, repl)
    new = MIDLANDS_ACROSS_RE.sub("across Leicestershire", new)

    # 3. Add JSON-LD if page is in SCHEMAS and not already present
    if fname in SCHEMAS and 'application/ld+json' not in new:
        schema_json = json.dumps(SCHEMAS[fname]["schema"], indent=2, ensure_ascii=False)
        injection = f'\n    <script type="application/ld+json">\n    {schema_json}\n    </script>'
        new = re.sub(r'(</head>)', injection + r'\n\1', new, count=1, flags=re.IGNORECASE)

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
    for c in changed[:20]:
        print(' -', c)
    if len(changed) > 20:
        print(f'   ...and {len(changed)-20} more')


if __name__ == '__main__':
    main()
