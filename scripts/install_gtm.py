#!/usr/bin/env python3
"""
Install Google Tag Manager (GTM-56L62ZWF) on every HTML page.
  1. Head snippet inserted immediately after <head> (or <head ...>)
  2. Noscript snippet inserted immediately after <body> (or <body ...>)
Idempotent — skips pages that already carry the GTM container ID.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GTM_ID = 'GTM-56L62ZWF'

GTM_HEAD = (
    '<!-- Google Tag Manager -->\n'
    '<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({\'gtm.start\':\n'
    'new Date().getTime(),event:\'gtm.js\'});var f=d.getElementsByTagName(s)[0],\n'
    'j=d.createElement(s),dl=l!=\'dataLayer\'?\'&l=\'+l:\'\';j.async=true;j.src=\n'
    '\'https://www.googletagmanager.com/gtm.js?id=\'+i+dl;f.parentNode.insertBefore(j,f);\n'
    '})(window,document,\'script\',\'dataLayer\',\'' + GTM_ID + '\');</script>\n'
    '<!-- End Google Tag Manager -->\n'
)

GTM_NOSCRIPT = (
    '<!-- Google Tag Manager (noscript) -->\n'
    '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=' + GTM_ID + '"\n'
    'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
    '<!-- End Google Tag Manager (noscript) -->\n'
)

HEAD_RE = re.compile(r'(<head\b[^>]*>)', re.IGNORECASE)
BODY_RE = re.compile(r'(<body\b[^>]*>)', re.IGNORECASE)

def process(path):
    with open(path, 'r', encoding='utf-8') as f:
        orig = f.read()

    if GTM_ID in orig:
        return False  # already installed

    new = orig

    # Insert after <head ...>
    new = HEAD_RE.sub(lambda m: m.group(1) + '\n' + GTM_HEAD, new, count=1)

    # Insert after <body ...>
    new = BODY_RE.sub(lambda m: m.group(1) + '\n' + GTM_NOSCRIPT, new, count=1)

    if new != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        return True
    return False

def main():
    files = sorted(glob.glob(os.path.join(ROOT, '*.html')))
    changed, skipped = [], []
    for p in files:
        if process(p):
            changed.append(os.path.basename(p))
        else:
            skipped.append(os.path.basename(p))
    print(f'GTM installed on {len(changed)} pages, {len(skipped)} skipped (already present or unmodified)')
    for c in changed[:10]:
        print(' +', c)
    if len(changed) > 10:
        print(f'   ...and {len(changed)-10} more')

if __name__ == '__main__':
    main()
