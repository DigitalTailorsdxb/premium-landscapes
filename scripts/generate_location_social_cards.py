#!/usr/bin/env python3
"""Generate bespoke 1200x630 (1.91:1) Open Graph / Twitter social-share cards
for every landscaping-<slug>.html location page.

Each card takes the existing og:image source photo, scales it to cover the
1200x630 frame, applies a subtle bottom-left dark gradient for legibility, and
overlays a brand chip + "Landscaping in <Town>" headline. Output is written to
images/social/landscaping-<slug>.jpg.

The script then rewrites the og:image / og:image:secure_url / og:image:width /
og:image:height / twitter:image meta tags in each landscaping-<slug>.html to
point at the new card, preserving the existing og:image:alt copy.
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

# slug -> (source image path relative to repo root, Town display name)
LOCATIONS: dict[str, tuple[str, str]] = {
    "anstey":         ("images/about-garden.webp",                 "Anstey"),
    "birstall":       ("images/projects/birstall/birstall-1.jpg",  "Birstall"),
    "blaby":          ("images/gallery-patio.webp",                "Blaby"),
    "clarendon-park": ("images/natural-stone-patio.webp",          "Clarendon Park"),
    "cosby":          ("images/gallery-garden-pergola.webp",       "Cosby"),
    "enderby":        ("images/artificial-turf-family.webp",       "Enderby"),
    "glenfield":      ("images/family-garden-lighting.webp",       "Glenfield"),
    "hinckley":       ("images/transforming-gardens.webp",         "Hinckley"),
    "kirby-muxloe":   ("images/projects/kirby-muxloe/kirby-1.jpg", "Kirby Muxloe"),
    "knighton":       ("images/ai-design-mediterranean.webp",      "Knighton"),
    "leicester":      ("images/hero-garden.webp",                  "Leicester"),
    "loughborough":   ("images/decking-hero.webp",                 "Loughborough"),
    "markfield":      ("images/garden-lighting.webp",              "Markfield"),
    "narborough":     ("images/services-garden.webp",              "Narborough"),
    "oadby":          ("images/after-garden.webp",                 "Oadby"),
    "ratby":          ("images/about-hero.webp",                   "Ratby"),
    "stoneygate":     ("images/tropical-paradise-garden.jpg",      "Stoneygate"),
    "syston":         ("images/driveway-block-paving.webp",        "Syston"),
    "thurmaston":     ("images/project-step5-finished.webp",       "Thurmaston"),
    "wigston":        ("images/projects/wigston/wigston-1.jpg",    "Wigston"),
}


def cover_resize(src: Image.Image, w: int, h: int) -> Image.Image:
    """Scale src to fully cover (w, h), centre-cropped."""
    sw, sh = src.size
    scale = max(w / sw, h / sh)
    nw, nh = int(round(sw * scale)), int(round(sh * scale))
    resized = src.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return resized.crop((left, top, left + w, top + h))


def build_gradient(w: int, h: int) -> Image.Image:
    """Vertical gradient: transparent at top, dark at bottom (for text)."""
    grad = Image.new("L", (1, h), 0)
    for y in range(h):
        # ease-in from 0 (top) to 200 (bottom); strongest in lower 60%
        t = y / (h - 1)
        # bias to bottom half
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


def render_card(src_path: Path, town: str, out_path: Path) -> None:
    with Image.open(src_path) as im:
        im = im.convert("RGB")
        base = cover_resize(im, CARD_W, CARD_H)

    # Slight saturation/contrast boost via a soft dark vignette on left edge
    canvas = base.convert("RGBA")

    # Bottom gradient for headline legibility
    canvas.alpha_composite(build_gradient(CARD_W, CARD_H))

    # Subtle dark left-edge vignette for the brand chip
    left_shade = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    lsd = ImageDraw.Draw(left_shade)
    lsd.rectangle([0, 0, 520, CARD_H], fill=(0, 0, 0, 55))
    left_shade = left_shade.filter(ImageFilter.GaussianBlur(80))
    canvas.alpha_composite(left_shade)

    draw = ImageDraw.Draw(canvas)

    # Brand chip top-left: a pill with "PREMIUM LANDSCAPES"
    chip_text = "PREMIUM LANDSCAPES"
    chip_font = ImageFont.truetype(FONT_BOLD, 22)
    cb = chip_font.getbbox(chip_text)
    cw, ch = cb[2] - cb[0], cb[3] - cb[1]
    pad_x, pad_y = 22, 12
    chip_x, chip_y = 48, 44
    chip_box = [chip_x, chip_y, chip_x + cw + pad_x * 2, chip_y + ch + pad_y * 2]
    # rounded rect background
    draw.rounded_rectangle(chip_box, radius=(ch + pad_y * 2) // 2, fill=(37, 99, 235, 235))
    draw.text(
        (chip_x + pad_x, chip_y + pad_y - cb[1]),
        chip_text,
        font=chip_font,
        fill=(255, 255, 255, 255),
    )

    # Headline bottom-left: "Landscaping in <Town>"
    headline = f"Landscaping in {town}"
    headline_font = fit_font(headline, max_width=CARD_W - 96, max_size=84, min_size=52, font_path=FONT_BOLD)
    hb = headline_font.getbbox(headline)
    hw, hh = hb[2] - hb[0], hb[3] - hb[1]
    hx = 48
    hy = CARD_H - 48 - hh - 56  # leave room for subline

    # text shadow for extra legibility on busy photos
    shadow_offsets = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    for dx, dy in shadow_offsets:
        draw.text((hx + dx, hy + dy - hb[1]), headline, font=headline_font, fill=(0, 0, 0, 160))
    draw.text((hx, hy - hb[1]), headline, font=headline_font, fill=(255, 255, 255, 255))

    # Subline: amber-accented brand line
    sub_left = "Patios · Artificial Grass · Decking · Driveways"
    sub_right = "premium-landscapes.co.uk"
    sub_font = ImageFont.truetype(FONT_REG, 24)
    sb = sub_font.getbbox(sub_left)
    sy = hy + (hb[3] - hb[1]) + 18
    for dx, dy in shadow_offsets:
        draw.text((hx + dx, sy + dy - sb[1]), sub_left, font=sub_font, fill=(0, 0, 0, 150))
    draw.text((hx, sy - sb[1]), sub_left, font=sub_font, fill=(245, 158, 11, 255))  # amber-500

    rb = sub_font.getbbox(sub_right)
    rx = CARD_W - 48 - (rb[2] - rb[0])
    for dx, dy in shadow_offsets:
        draw.text((rx + dx, sy + dy - rb[1]), sub_right, font=sub_font, fill=(0, 0, 0, 150))
    draw.text((rx, sy - rb[1]), sub_right, font=sub_font, fill=(255, 255, 255, 255))

    out = canvas.convert("RGB")
    out.save(out_path, "JPEG", quality=86, optimize=True, progressive=True)


OG_BLOCK_RE = re.compile(
    r'    <meta property="og:image" content="[^"]+">\n'
    r'(?:    <meta property="og:image:secure_url" content="[^"]+">\n)?'
    r'(    <meta property="og:image:alt" content="[^"]+">\n)?'
    r'(?:    <meta property="og:image:width" content="[^"]+">\n)?'
    r'(?:    <meta property="og:image:height" content="[^"]+">\n)?'
)

TW_IMAGE_RE = re.compile(r'    <meta name="twitter:image" content="[^"]+">\n')


def update_html(slug: str) -> None:
    fn = ROOT / f"landscaping-{slug}.html"
    text = fn.read_text(encoding="utf-8")
    card_url = f"{BASE_URL}/images/social/landscaping-{slug}.jpg"

    m = OG_BLOCK_RE.search(text)
    if not m:
        raise RuntimeError(f"{fn}: og:image block not found")
    alt_line = m.group(1) or ""  # preserve existing alt
    if not alt_line:
        raise RuntimeError(f"{fn}: og:image:alt missing — won't synthesise")

    replacement = (
        f'    <meta property="og:image" content="{card_url}">\n'
        f'    <meta property="og:image:secure_url" content="{card_url}">\n'
        f'{alt_line}'
        f'    <meta property="og:image:width" content="{CARD_W}">\n'
        f'    <meta property="og:image:height" content="{CARD_H}">\n'
    )
    text = text[:m.start()] + replacement + text[m.end():]

    n = 0
    def _tw(match: re.Match) -> str:
        nonlocal n
        n += 1
        return f'    <meta name="twitter:image" content="{card_url}">\n'
    text = TW_IMAGE_RE.sub(_tw, text, count=1)
    if n != 1:
        raise RuntimeError(f"{fn}: twitter:image not matched")

    fn.write_text(text, encoding="utf-8")


def main() -> None:
    for slug, (src_rel, town) in LOCATIONS.items():
        src = ROOT / src_rel
        if not src.exists():
            raise FileNotFoundError(src)
        out = OUT_DIR / f"landscaping-{slug}.jpg"
        render_card(src, town, out)
        update_html(slug)
        print(f"{slug:16s} -> {out.relative_to(ROOT)}  ({town})")
    print(f"\nGenerated {len(LOCATIONS)} social cards.")


if __name__ == "__main__":
    main()
