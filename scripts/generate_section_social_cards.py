#!/usr/bin/env python3
"""Generate bespoke 1200x630 Open Graph / Twitter social-share cards for every
service page, blog post, cost-guide page and cost-calculator page, then rewrite
the og:image / twitter:image meta tags on each page to point at its new card.

Follows the same visual template as scripts/generate_location_social_cards.py
(brand chip top-left, headline + amber subline bottom-left, site URL bottom-
right). Output: images/social/<slug>.jpg.
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_URL = "https://premium-landscapes.co.uk"
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "images" / "social"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CARD_W, CARD_H = 1200, 630

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# page filename (without .html) -> (source image rel path, headline, sub_left, og:image:alt)
PAGES: dict[str, tuple[str, str, str, str]] = {
    # --- Service pages (7) ---
    "patios": (
        "images/gallery-patio.webp",
        "Patio Installation in Leicester",
        "Porcelain · Sandstone · Limestone · Granite",
        "Patio installation in Leicester by Premium Landscapes — porcelain, sandstone, limestone and granite.",
    ),
    "artificial-grass": (
        "images/artificial-turf-family.webp",
        "Artificial Grass in Leicester",
        "Premium lawns · Family-friendly · Pet-safe",
        "Artificial grass installation in Leicester by Premium Landscapes — premium pet- and family-friendly lawns.",
    ),
    "composite-decking": (
        "images/decking-hero.webp",
        "Composite Decking in Leicester",
        "Millboard · Trex · Cladco installations",
        "Composite decking installation in Leicester by Premium Landscapes — Millboard, Trex and Cladco specialists.",
    ),
    "driveways": (
        "images/driveway-block-paving.webp",
        "Driveways in Leicester",
        "Block paving · Resin · SuDS-compliant",
        "Driveway installation in Leicester by Premium Landscapes — block paving, resin and SuDS-compliant drives.",
    ),
    "garden-lighting": (
        "images/family-garden-lighting.webp",
        "Garden Lighting in Leicester",
        "LED · Low-voltage · Part P certified",
        "Garden lighting installation in Leicester by Premium Landscapes — Part P certified, low-voltage LED schemes.",
    ),
    "full-garden-makeover": (
        "images/transforming-gardens.webp",
        "Full Garden Makeovers in Leicester",
        "Design · Build · Plant · Finish",
        "Full garden makeovers in Leicester by Premium Landscapes — design, build, plant and finish in one project.",
    ),
    "ai-garden-design": (
        "images/ai-design-mediterranean.webp",
        "Free AI Garden Design",
        "Photorealistic preview · 90 seconds · No cost",
        "Free AI garden design from Premium Landscapes — photorealistic preview of your garden in 90 seconds.",
    ),

    # --- Blog posts (20) ---
    "blog-1": (
        "images/about-garden.webp",
        "Garden Redesign Costs 2026",
        "UK pricing · Premium Landscapes · Insights",
        "Garden redesign costs in the UK for 2026 — guide by Premium Landscapes.",
    ),
    "blog-2": (
        "images/gallery-garden-pergola.webp",
        "Modern Small Garden Ideas",
        "Design inspiration · Premium Landscapes",
        "Modern garden design ideas for small UK spaces by Premium Landscapes.",
    ),
    "blog-3": (
        "images/artificial-turf-family.webp",
        "Artificial Grass vs Natural Turf",
        "UK 2026 comparison · Premium Landscapes",
        "Artificial grass vs natural turf comparison for UK gardens in 2026 by Premium Landscapes.",
    ),
    "blog-4": (
        "images/natural-stone-patio.webp",
        "Best Patio Materials for UK Weather",
        "Materials guide · Premium Landscapes",
        "Choosing the best patio materials for UK weather — guide by Premium Landscapes.",
    ),
    "blog-5": (
        "images/decking-hero.webp",
        "Composite vs Timber Decking",
        "UK 2026 buyer's guide · Premium Landscapes",
        "Composite vs timber decking — 2026 UK buyer's guide by Premium Landscapes.",
    ),
    "blog-6": (
        "images/garden-lighting.webp",
        "Outdoor Garden Lighting Ideas",
        "Design inspiration · Premium Landscapes",
        "Outdoor garden lighting ideas to transform evenings — Premium Landscapes guide.",
    ),
    "blog-7": (
        "images/after-garden.webp",
        "The Perfect Family Garden",
        "Safe · Fun · Low-maintenance",
        "Creating the perfect family garden — safe, fun and low-maintenance ideas from Premium Landscapes.",
    ),
    "blog-8": (
        "images/services-garden.webp",
        "Year-Round Garden Maintenance",
        "UK seasonal calendar · Premium Landscapes",
        "Seasonal garden maintenance calendar for UK gardens by Premium Landscapes.",
    ),
    "blog-9": (
        "images/about-hero.webp",
        "Garden Makeovers & Home Value",
        "UK 2026 ROI guide · Premium Landscapes",
        "How much value a garden makeover adds to your home — UK 2026 guide by Premium Landscapes.",
    ),
    "blog-10": (
        "images/ai-design-mediterranean.webp",
        "AI Garden Design in 2026",
        "Tools & trends · Premium Landscapes",
        "How AI garden design tools are revolutionising UK landscaping — Premium Landscapes 2026 insights.",
    ),
    "blog-11": (
        "images/projects/kirby-muxloe-driveway/driveway-1.jpg",
        "SuDS Driveway Rules 2026",
        "Planning & Regulations · Premium Landscapes",
        "SuDS driveway rules in 2026 explained for Leicester homeowners by Premium Landscapes.",
    ),
    "blog-12": (
        "images/project-step3-construction.webp",
        "Patio Sub-Bases Explained",
        "BS 7533 · MOT Type 1 · Engineering",
        "Patio sub-bases explained — BS 7533, MOT Type 1 and Leicestershire ground conditions by Premium Landscapes.",
    ),
    "blog-13": (
        "images/about-hero.webp",
        "Permitted Development 2026",
        "Planning & Regulations · Premium Landscapes",
        "Permitted development for gardens — when planning permission is needed in 2026 by Premium Landscapes.",
    ),
    "blog-14": (
        "images/tropical-paradise-garden.jpg",
        "Leicester Conservation Areas",
        "Planning & Regulations · Premium Landscapes",
        "Landscaping in Leicester conservation areas — homeowner's guide by Premium Landscapes.",
    ),
    "blog-15": (
        "images/project-step2-cleared.webp",
        "Drainage for Clay Gardens",
        "French drains · Soakaways · SuDS",
        "Drainage for Leicestershire clay gardens — French drains, soakaways and SuDS compliance by Premium Landscapes.",
    ),
    "blog-16": (
        "images/decking-hero.webp",
        "Millboard vs Trex vs Cladco",
        "Composite decking brands · UK 2026",
        "Composite decking brand comparison — Millboard vs Trex vs Cladco UK 2026 by Premium Landscapes.",
    ),
    "blog-17": (
        "images/artificial-turf-family.webp",
        "Artificial Grass Specs Decoded",
        "Pile · Density · Backing · Drainage",
        "Artificial grass specifications decoded — pile height, density, backings and drainage by Premium Landscapes.",
    ),
    "blog-18": (
        "images/driveway-block-paving.webp",
        "Resin vs Block Paving Driveways",
        "UK 2026 comparison · Premium Landscapes",
        "Resin-bound vs resin-bonded vs block paving — UK driveway comparison 2026 by Premium Landscapes.",
    ),
    "blog-19": (
        "images/family-garden-lighting.webp",
        "Garden Lighting Regulations",
        "Part P · IP ratings · Voltage",
        "Garden lighting regulations explained — Part P, IP ratings and voltage by Premium Landscapes.",
    ),
    "blog-20": (
        "images/gallery-patio.webp",
        "Patios for Clay Soil",
        "Porcelain · Sandstone · Limestone · Granite",
        "Choosing patio materials for Leicestershire clay soil by Premium Landscapes.",
    ),

    # --- Cost guide hub + 5 deep-dives (6) ---
    "cost-guide": (
        "images/services-garden.webp",
        "UK Landscaping Cost Guide 2026",
        "Real prices · All services · No guesswork",
        "UK landscaping cost guide 2026 — real prices for patios, lawns, decking, driveways and more by Premium Landscapes.",
    ),
    "patio-cost-per-m2": (
        "images/gallery-patio.webp",
        "Patio Cost Per m² — UK 2026",
        "Porcelain · Sandstone · Block paving",
        "Patio cost per square metre in the UK for 2026 — price guide by Premium Landscapes.",
    ),
    "artificial-grass-cost": (
        "images/artificial-turf-family.webp",
        "Artificial Grass Cost — UK 2026",
        "Per m² pricing · Installation included",
        "Artificial grass installation cost in the UK for 2026 — price guide by Premium Landscapes.",
    ),
    "composite-decking-cost": (
        "images/decking-hero.webp",
        "Composite Decking Cost — UK 2026",
        "Per m² pricing · Brands compared",
        "Composite decking cost in the UK for 2026 — price guide per m² by Premium Landscapes.",
    ),
    "garden-design-cost": (
        "images/about-garden.webp",
        "Garden Design Cost — UK 2026",
        "Concept · Detailed plans · Build pricing",
        "Garden design cost in the UK for 2026 — price guide by Premium Landscapes.",
    ),
    "landscaping-cost-uk": (
        "images/hero-garden.webp",
        "Landscaping Cost — UK 2026",
        "Full project ranges · Real examples",
        "Landscaping cost in the UK for 2026 — full project pricing by Premium Landscapes.",
    ),

    # --- Cost calculators (6) ---
    "patio-cost-calculator": (
        "images/natural-stone-patio.webp",
        "Patio Cost Calculator 2026",
        "Instant estimate · UK pricing · Free",
        "Patio cost calculator — instant UK 2026 price estimate by Premium Landscapes.",
    ),
    "artificial-grass-cost-calculator": (
        "images/artificial-turf-family.webp",
        "Artificial Grass Cost Calculator",
        "Instant estimate · UK pricing · Free",
        "Artificial grass cost calculator — instant UK 2026 price estimate by Premium Landscapes.",
    ),
    "composite-decking-cost-calculator": (
        "images/decking-hero.webp",
        "Composite Decking Cost Calculator",
        "Instant estimate · UK pricing · Free",
        "Composite decking cost calculator — instant UK 2026 price estimate by Premium Landscapes.",
    ),
    "garden-design-cost-calculator": (
        "images/tropical-paradise-garden.jpg",
        "Garden Design Cost Calculator",
        "Instant estimate · UK pricing · Free",
        "Garden design cost calculator — instant UK 2026 price estimate by Premium Landscapes.",
    ),
    "garden-makeover-cost-calculator": (
        "images/after-garden.webp",
        "Garden Makeover Cost Calculator",
        "Instant estimate · UK pricing · Free",
        "Garden makeover cost calculator — instant UK 2026 price estimate by Premium Landscapes.",
    ),
    "garden-landscaping-cost-calculator": (
        "images/about-hero.webp",
        "Landscaping Cost Calculator",
        "Instant estimate · UK pricing · Free",
        "Garden landscaping cost calculator — instant UK 2026 price estimate by Premium Landscapes.",
    ),
}


def cover_resize(src: Image.Image, w: int, h: int) -> Image.Image:
    sw, sh = src.size
    scale = max(w / sw, h / sh)
    nw, nh = int(round(sw * scale)), int(round(sh * scale))
    resized = src.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return resized.crop((left, top, left + w, top + h))


def build_gradient(w: int, h: int) -> Image.Image:
    grad = Image.new("L", (1, h), 0)
    for y in range(h):
        t = y / (h - 1)
        v = int(220 * max(0.0, (t - 0.25) / 0.75) ** 1.4)
        grad.putpixel((0, y), min(v, 220))
    grad = grad.resize((w, h))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    overlay.putalpha(grad)
    return overlay


def fit_font(text: str, max_width: int, max_size: int, min_size: int, font_path: str) -> ImageFont.FreeTypeFont:
    size = max_size
    while size > min_size:
        f = ImageFont.truetype(font_path, size)
        bbox = f.getbbox(text)
        if (bbox[2] - bbox[0]) <= max_width:
            return f
        size -= 2
    return ImageFont.truetype(font_path, min_size)


def render_card(src_path: Path, headline: str, sub_left: str, out_path: Path) -> None:
    with Image.open(src_path) as im:
        im = im.convert("RGB")
        base = cover_resize(im, CARD_W, CARD_H)

    canvas = base.convert("RGBA")
    canvas.alpha_composite(build_gradient(CARD_W, CARD_H))

    left_shade = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    lsd = ImageDraw.Draw(left_shade)
    lsd.rectangle([0, 0, 520, CARD_H], fill=(0, 0, 0, 55))
    left_shade = left_shade.filter(ImageFilter.GaussianBlur(80))
    canvas.alpha_composite(left_shade)

    draw = ImageDraw.Draw(canvas)

    chip_text = "PREMIUM LANDSCAPES"
    chip_font = ImageFont.truetype(FONT_BOLD, 22)
    cb = chip_font.getbbox(chip_text)
    cw, ch = cb[2] - cb[0], cb[3] - cb[1]
    pad_x, pad_y = 22, 12
    chip_x, chip_y = 48, 44
    chip_box = [chip_x, chip_y, chip_x + cw + pad_x * 2, chip_y + ch + pad_y * 2]
    draw.rounded_rectangle(chip_box, radius=(ch + pad_y * 2) // 2, fill=(37, 99, 235, 235))
    draw.text(
        (chip_x + pad_x, chip_y + pad_y - cb[1]),
        chip_text,
        font=chip_font,
        fill=(255, 255, 255, 255),
    )

    headline_font = fit_font(headline, max_width=CARD_W - 96, max_size=78, min_size=40, font_path=FONT_BOLD)
    hb = headline_font.getbbox(headline)
    hw, hh = hb[2] - hb[0], hb[3] - hb[1]
    hx = 48
    hy = CARD_H - 48 - hh - 56

    shadow_offsets = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    for dx, dy in shadow_offsets:
        draw.text((hx + dx, hy + dy - hb[1]), headline, font=headline_font, fill=(0, 0, 0, 160))
    draw.text((hx, hy - hb[1]), headline, font=headline_font, fill=(255, 255, 255, 255))

    sub_right = "premium-landscapes.co.uk"
    sub_font = ImageFont.truetype(FONT_REG, 24)
    sub_left_fitted = sub_left
    # shrink sub_left if it would collide with right URL
    max_sub_w = CARD_W - 96 - sub_font.getbbox(sub_right)[2] - 40
    sf = sub_font
    if sf.getbbox(sub_left_fitted)[2] > max_sub_w:
        sf = fit_font(sub_left_fitted, max_width=max_sub_w, max_size=24, min_size=16, font_path=FONT_REG)
    sb = sf.getbbox(sub_left_fitted)
    sy = hy + (hb[3] - hb[1]) + 18
    for dx, dy in shadow_offsets:
        draw.text((hx + dx, sy + dy - sb[1]), sub_left_fitted, font=sf, fill=(0, 0, 0, 150))
    draw.text((hx, sy - sb[1]), sub_left_fitted, font=sf, fill=(245, 158, 11, 255))

    rb = sub_font.getbbox(sub_right)
    rx = CARD_W - 48 - (rb[2] - rb[0])
    for dx, dy in shadow_offsets:
        draw.text((rx + dx, sy + dy - rb[1]), sub_right, font=sub_font, fill=(0, 0, 0, 150))
    draw.text((rx, sy - rb[1]), sub_right, font=sub_font, fill=(255, 255, 255, 255))

    out = canvas.convert("RGB")
    out.save(out_path, "JPEG", quality=86, optimize=True, progressive=True)


# Replaces the existing single-line og:image tag (and any adjacent
# og:image:secure_url / alt / width / height lines) with our full block.
OG_BLOCK_RE = re.compile(
    r'(    )<meta property="og:image" content="[^"]+">\n'
    r'(?:    <meta property="og:image:secure_url" content="[^"]+">\n)?'
    r'(?:    <meta property="og:image:alt" content="[^"]+">\n)?'
    r'(?:    <meta property="og:image:width" content="[^"]+">\n)?'
    r'(?:    <meta property="og:image:height" content="[^"]+">\n)?'
)

TW_BLOCK_RE = re.compile(
    r'(    )<meta name="twitter:image" content="[^"]+">\n'
    r'(?:    <meta name="twitter:image:alt" content="[^"]+">\n)?'
)


def update_html(slug: str, alt: str) -> None:
    fn = ROOT / f"{slug}.html"
    text = fn.read_text(encoding="utf-8")

    # detect whether page uses www. host so we don't change the URL host
    m_existing = re.search(r'<meta property="og:image" content="(https?://[^/]+)/', text)
    host = m_existing.group(1) if m_existing else BASE_URL

    card_url = f"{host}/images/social/{slug}.jpg"

    og_replacement = (
        f'    <meta property="og:image" content="{card_url}">\n'
        f'    <meta property="og:image:secure_url" content="{card_url}">\n'
        f'    <meta property="og:image:alt" content="{alt}">\n'
        f'    <meta property="og:image:width" content="{CARD_W}">\n'
        f'    <meta property="og:image:height" content="{CARD_H}">\n'
    )
    new_text, n_og = OG_BLOCK_RE.subn(og_replacement, text, count=1)
    if n_og != 1:
        raise RuntimeError(f"{fn}: og:image block not matched")

    tw_replacement = (
        f'    <meta name="twitter:image" content="{card_url}">\n'
        f'    <meta name="twitter:image:alt" content="{alt}">\n'
    )
    new_text2, n_tw = TW_BLOCK_RE.subn(tw_replacement, new_text, count=1)
    if n_tw == 0:
        # No existing twitter:image — insert right after the og:image block.
        # Find the position immediately after our newly-written og block.
        idx = new_text.find(og_replacement) + len(og_replacement)
        new_text2 = new_text[:idx] + tw_replacement + new_text[idx:]

    fn.write_text(new_text2, encoding="utf-8")


def main() -> None:
    for slug, (src_rel, headline, sub_left, alt) in PAGES.items():
        src = ROOT / src_rel
        if not src.exists():
            raise FileNotFoundError(f"Source image missing: {src}")
        page = ROOT / f"{slug}.html"
        if not page.exists():
            raise FileNotFoundError(f"Page missing: {page}")
        out = OUT_DIR / f"{slug}.jpg"
        render_card(src, headline, sub_left, out)
        update_html(slug, alt)
        print(f"{slug:40s} -> {out.relative_to(ROOT)}")
    print(f"\nGenerated {len(PAGES)} social cards.")


if __name__ == "__main__":
    main()
