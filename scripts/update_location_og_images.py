#!/usr/bin/env python3
"""Replace the shared og:image / twitter:image on the 20 location pages with
unique, area-relevant images and add descriptive alt + dimension tags."""
import re
from pathlib import Path

BASE = "https://premium-landscapes.co.uk"

MAPPING = {
    "anstey":         ("/images/about-garden.webp",            1536, 1024, "Mature landscaped garden in Anstey, Leicestershire by Premium Landscapes"),
    "birstall":       ("/images/projects/birstall/birstall-1.jpg", 1200,  900, "Real Premium Landscapes garden transformation completed in Birstall, Leicestershire"),
    "blaby":          ("/images/gallery-patio.webp",            1536, 1024, "Porcelain patio installation in a Blaby family garden by Premium Landscapes"),
    "clarendon-park": ("/images/natural-stone-patio.webp",      1024, 1024, "Natural stone patio behind a Victorian terrace in Clarendon Park, Leicester"),
    "cosby":          ("/images/gallery-garden-pergola.webp",   1536, 1024, "Garden pergola and patio scheme for a Cosby village property by Premium Landscapes"),
    "enderby":        ("/images/artificial-turf-family.webp",   1536, 1024, "Artificial grass family lawn installed in Enderby, Leicestershire"),
    "glenfield":      ("/images/family-garden-lighting.webp",   1536, 1024, "Family garden with outdoor lighting in Glenfield, Leicester by Premium Landscapes"),
    "hinckley":       ("/images/transforming-gardens.webp",     1536, 1024, "Full garden transformation completed in Hinckley, Leicestershire"),
    "kirby-muxloe":   ("/images/projects/kirby-muxloe/kirby-1.jpg", 1440, 1080, "Real Premium Landscapes project completed at our Kirby Muxloe base, Leicestershire"),
    "knighton":       ("/images/ai-design-mediterranean.webp",  1536, 1024, "Mediterranean-style AI garden design preview for a Knighton, Leicester property"),
    "leicester":      ("/images/hero-garden.webp",              1536, 1024, "Premium Landscapes — flagship landscaped garden in Leicester"),
    "loughborough":   ("/images/decking-hero.webp",             1536, 1024, "Composite decking installation in Loughborough, Leicestershire"),
    "markfield":      ("/images/garden-lighting.webp",          1536, 1024, "Garden lighting scheme for a Markfield property in the Charnwood Forest"),
    "narborough":     ("/images/services-garden.webp",          1536, 1024, "Full landscaping service in a Narborough garden by Premium Landscapes"),
    "oadby":          ("/images/after-garden.webp",             1536, 1024, "Finished garden makeover in Oadby, Leicestershire by Premium Landscapes"),
    "ratby":          ("/images/about-hero.webp",               1536, 1024, "Landscaped rear garden in Ratby, Leicestershire by Premium Landscapes"),
    "stoneygate":     ("/images/tropical-paradise-garden.jpg",  1024, 1024, "Lush tropical-style garden design suited to Stoneygate's larger plots, Leicester"),
    "syston":         ("/images/driveway-block-paving.webp",    1024, 1536, "Block-paved driveway installation in Syston, Leicestershire"),
    "thurmaston":     ("/images/project-step5-finished.webp",   1536, 1024, "Finished landscaping project in Thurmaston, Leicestershire"),
    "wigston":        ("/images/projects/wigston/wigston-1.jpg",1024,  768, "Real Premium Landscapes garden project completed in Wigston, Leicestershire"),
}

OG_IMAGE_RE = re.compile(
    r'(    <meta property="og:image" content=")[^"]+(">)\n'
)
TW_IMAGE_RE = re.compile(
    r'(    <meta name="twitter:image" content=")[^"]+(">)\n'
)

for slug, (path, w, h, alt) in MAPPING.items():
    fn = Path(f"landscaping-{slug}.html")
    text = fn.read_text(encoding="utf-8")
    url = f"{BASE}{path}"

    # Build replacement og:image block (image + secure_url + alt + width + height)
    og_block = (
        f'    <meta property="og:image" content="{url}">\n'
        f'    <meta property="og:image:secure_url" content="{url}">\n'
        f'    <meta property="og:image:alt" content="{alt}">\n'
        f'    <meta property="og:image:width" content="{w}">\n'
        f'    <meta property="og:image:height" content="{h}">\n'
    )
    new_text, n1 = OG_IMAGE_RE.subn(og_block, text, count=1)
    assert n1 == 1, f"{fn}: og:image not matched"

    tw_block = (
        f'    <meta name="twitter:image" content="{url}">\n'
        f'    <meta name="twitter:image:alt" content="{alt}">\n'
    )
    new_text, n2 = TW_IMAGE_RE.subn(tw_block, new_text, count=1)
    assert n2 == 1, f"{fn}: twitter:image not matched"

    fn.write_text(new_text, encoding="utf-8")
    print(f"{fn}: og:image -> {path}")

print(f"\nUpdated {len(MAPPING)} location pages.")
