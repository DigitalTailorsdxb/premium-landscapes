#!/usr/bin/env python3
"""
Phase F — GDPR consent gating + footer/service label keyword optimisation +
title/meta length fixes. Run from repo root: python3 scripts/phase_f_compliance.py

Idempotent: safe to re-run.
"""
import os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- A. GDPR — replace FB Pixel init+track and add Consent Mode default ----------
# OLD: fbq init+track fires on page load
OLD_FB = re.compile(
    r"<script>!function\(f,b,e,v,n,t,s\)\{[^<]*?\}\(window,document,'script','https://connect\.facebook\.net/en_US/fbevents\.js'\);\s*fbq\('init',\s*'1480425153686683'\);\s*fbq\('track',\s*'PageView'\);\s*</script>",
    re.DOTALL
)
# NEW: loader still runs (queue exists), but init+track deferred via consent flag.
# cookie-consent.js calls window.__plFireFbPixel() on accept.
NEW_FB = (
    "<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){"
    "n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};"
    "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];"
    "t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];"
    "s.parentNode.insertBefore(t,s)}(window,document,'script',"
    "'https://connect.facebook.net/en_US/fbevents.js');"
    "window.__plFireFbPixel=function(){if(window.__plFbFired)return;"
    "window.__plFbFired=true;fbq('init','1480425153686683');"
    "fbq('track','PageView');};"
    "try{if(localStorage.getItem('pl_cookie_consent')==='accepted')"
    "window.__plFireFbPixel();}catch(e){}</script>"
)

# OLD GA: gtag('config') without prior consent default
OLD_GA = re.compile(
    r"<script>\s*window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];\s*"
    r"function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*"
    r"gtag\('js',\s*new Date\(\)\);\s*"
    r"gtag\('config',\s*'G-9PGX32QB99'\);\s*</script>",
    re.DOTALL
)
NEW_GA = (
    "<script>\n"
    "  window.dataLayer = window.dataLayer || [];\n"
    "  function gtag(){dataLayer.push(arguments);}\n"
    "  // GDPR — default-deny until cookie-consent.js updates on accept (Consent Mode v2)\n"
    "  gtag('consent', 'default', {\n"
    "    ad_storage: 'denied',\n"
    "    analytics_storage: 'denied',\n"
    "    ad_user_data: 'denied',\n"
    "    ad_personalization: 'denied',\n"
    "    wait_for_update: 500\n"
    "  });\n"
    "  gtag('js', new Date());\n"
    "  gtag('config', 'G-9PGX32QB99');\n"
    "</script>"
)

# ---------- B. Body service-card / footer labels: add "Leicester" suffix ----------
# Carefully replace ONLY closing-anchor labels (>Label</a>) to avoid clobbering
# breadcrumbs, headings or surrounding prose.
LABEL_MAP = {
    ">Patio Installation</a>":   ">Patio Installation Leicester</a>",
    ">Artificial Grass</a>":     ">Artificial Grass Leicester</a>",
    ">Composite Decking</a>":    ">Composite Decking Leicester</a>",
    ">Garden Lighting</a>":      ">Garden Lighting Leicester</a>",
    ">Full Garden Makeover</a>": ">Full Garden Makeover Leicester</a>",
    ">Driveways</a>":            ">Driveways Leicester</a>",
    ">Patios</a>":               ">Patios Leicester</a>",
}

# ---------- C. Trim fencing meta description (164 -> <=155 chars) ----------
FENCING_META_OLD = ('Professional fencing installation in Leicester. Timber, composite, '
                    'closeboard and decorative fencing. Free instant quote online. '
                    'Fully installed, all waste removed.')
FENCING_META_NEW = ('Professional fencing installation in Leicester. Timber, composite, '
                    'closeboard and decorative fencing. Free quote — all waste removed.')

# ---------- D. Trim titles >60 chars on the 9 new pages ----------
TITLE_MAP = {
    'ai-garden-design.html':
        ('AI Garden Design Leicester | Free Instant Design in 90 Seconds | Premium Landscapes',
         'AI Garden Design Leicester | Free Design in 90 Seconds'),
    'garden-design-leicester.html':
        ('Garden Design Leicester | AI-Powered & Traditional Garden Design | Premium Landscapes',
         'Garden Design Leicester | AI-Powered & Traditional Design'),
    'porcelain-patios-leicester.html':
        ('Porcelain Patio Installation Leicester | Large Format Porcelain Slabs | Premium Landscapes',
         'Porcelain Patio Installation Leicester | Large Format Slabs'),
    'block-paving-driveways-leicester.html':
        ('Block Paving Driveways Leicester | Expert Installation | Premium Landscapes',
         'Block Paving Driveways Leicester | Expert Installation'),
    'resin-driveways-leicester.html':
        ('Resin Bound Driveways Leicester | SUDS Compliant | Premium Landscapes',
         'Resin Bound Driveways Leicester | SUDS Compliant'),
    'fencing-leicester.html':
        ('Fencing Installation Leicester | Garden & Boundary Fencing | Premium Landscapes',
         'Fencing Installation Leicester | Garden & Boundary Fencing'),
    'turfing-leicester.html':
        ('Turfing & Lawn Installation Leicester | New Lawn in a Day | Premium Landscapes',
         'Turfing & Lawn Installation Leicester | New Lawn in a Day'),
    'pergolas-leicester.html':
        ('Pergolas & Garden Structures Leicester | Installed by Premium Landscapes',
         'Pergolas & Garden Structures Leicester | Installation'),
    'commercial-astroturf-leicester.html':
        ('Commercial Astroturf Leicester | Schools, Gyms & Sports Facilities | Premium Landscapes',
         'Commercial Astroturf Leicester | Schools & Sports Facilities'),
}

# =========================================================
def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        orig = f.read()
    new = orig

    # A.1 FB Pixel rewrite
    if "fbq('init', '1480425153686683')" in new:
        new2, n = OLD_FB.subn(NEW_FB, new)
        if n:
            new = new2

    # A.2 GA4 Consent Mode default
    if "gtag('config', 'G-9PGX32QB99')" in new and "gtag('consent', 'default'" not in new:
        new = OLD_GA.sub(NEW_GA, new)

    # B. Label keyword swap
    for old_lbl, new_lbl in LABEL_MAP.items():
        if old_lbl in new:
            new = new.replace(old_lbl, new_lbl)

    # C. Fencing meta description
    if path.endswith('fencing-leicester.html') and FENCING_META_OLD in new:
        new = new.replace(FENCING_META_OLD, FENCING_META_NEW)

    # D. Title trim
    base = os.path.basename(path)
    if base in TITLE_MAP:
        old_t, new_t = TITLE_MAP[base]
        # Page title
        new = new.replace(f'<title>{old_t}</title>', f'<title>{new_t}</title>')
        # og:title / twitter:title (keep matching site signal)
        new = new.replace(f'content="{old_t}"', f'content="{new_t}"')

    if new != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        return True
    return False

def main():
    html_files = sorted(glob.glob(os.path.join(ROOT, '*.html')))
    changed = []
    for p in html_files:
        if process_file(p):
            changed.append(os.path.basename(p))
    print(f'Modified {len(changed)} files')
    if changed:
        # show first 20
        for c in changed[:20]:
            print(' -', c)
        if len(changed) > 20:
            print(f' ... and {len(changed)-20} more')

if __name__ == '__main__':
    main()
