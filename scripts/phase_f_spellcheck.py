#!/usr/bin/env python3
"""Spell-check priority pages. Whitelists landscaping/UK trade vocabulary."""
import re, glob, os, sys
from html.parser import HTMLParser
from spellchecker import SpellChecker

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRIORITY = [
    'index.html','about.html','contact.html','services.html','gallery.html',
    'quote.html','blog.html','about-premium-landscapes.html',
    # 9 new pages
    'ai-garden-design.html','garden-design-leicester.html',
    'porcelain-patios-leicester.html','block-paving-driveways-leicester.html',
    'resin-driveways-leicester.html','fencing-leicester.html',
    'turfing-leicester.html','pergolas-leicester.html',
    'commercial-astroturf-leicester.html',
    # 6 core service pages
    'patios.html','artificial-grass.html','composite-decking.html',
    'driveways.html','garden-lighting.html','full-garden-makeover.html',
    # blog posts
] + [f'blog-{i}.html' for i in range(1, 21)]

# Domain vocabulary — landscaping, UK trade, place names, brands, technical
WHITELIST = set(w.lower() for w in """
leicester leicestershire oadby wigston narborough birstall hinckley loughborough
kirby muxloe anstey blaby clarendon cosby enderby glenfield knighton markfield
ratby stoneygate syston thurmaston barwell
featheredge closeboard porcelain astroturf decking pergola pergolas suds
gravel-set composite hardcore subsoil topsoil seedbed sub-base subbase
mot kerb kerbs kerbing edging haunching jointing pointing slurry mortared
muga mugas dtex iso fifa itf gdpr nap iso ip permitted dfe ofsted hic en1177
charnian charnwood mercia mudstone alluvium drystone drywall
wisteria clematis jasmine hawthorn
millboard trex cladco trustpilot whatsapp dalle midjourney airtable
seo geo aeo localbusiness faqpage gtm ga4 utm cta cta's
homeowners landscapers groundworks landscaping makeover makeovers
britsh ie eg etc whilst behaviour colour favour realise organise centre
fibre litre metre kilometre programme labour licence defence offence practise
analyse minimise maximise customise standardise prioritise modernise utilise
optimisation neighbour neighbours travelled cancelled labelled
20m 30m 40m 50m 60m 100m 150m 200m 600mm 100mm 150mm 200mm 50mm 40mm 30mm 75mm
sqm m2 m² 4m 1m 2m 3m
postcode postcodes le1 le2 le3 le4 le5 le6 le7 le8 le9 le10 le11 le12 le13 le14 le15 le16 le17 le18 le19
premiumlandscapes premium-landscapes co uk
diy 24/7
""".split())

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.buf = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript'):
            self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript') and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)
    def text(self):
        return ' '.join(self.buf)

spell = SpellChecker(language='en')
# Pretend whitelist is known
spell.word_frequency.load_words(WHITELIST)

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]+")

def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    p = TextExtractor()
    p.feed(html)
    text = p.text()
    words = WORD_RE.findall(text)
    # Filter: only check alphabetic >2, exclude proper-noun looking (Title-case)
    candidates = []
    for w in words:
        lw = w.lower()
        if len(lw) < 3:                          continue
        if lw in WHITELIST:                      continue
        if w[0].isupper() and not w.isupper():   continue  # likely proper noun
        candidates.append(lw)
    misspelled = spell.unknown(set(candidates))
    return sorted(misspelled)

if __name__ == '__main__':
    grand = {}
    for fname in PRIORITY:
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            continue
        miss = check_file(path)
        if miss:
            grand[fname] = miss
    if not grand:
        print('CLEAN — no spelling issues flagged on priority pages')
        sys.exit(0)
    total = sum(len(v) for v in grand.values())
    print(f'{total} flagged tokens across {len(grand)} pages\n')
    for fname, miss in grand.items():
        print(f'--- {fname} ({len(miss)}) ---')
        print('  ' + ', '.join(miss))
        print()
