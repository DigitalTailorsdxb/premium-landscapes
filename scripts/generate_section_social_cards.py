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

    # --- Hubs / general pages (4) ---
    "blog": (
        "images/about-garden.webp",
        "Landscaping & Garden Design Blog",
        "Guides · Tips · Pricing · Leicester",
        "Premium Landscapes blog — landscaping and garden design guides, tips and UK pricing.",
    ),
    "services": (
        "images/services-garden.webp",
        "Landscaping Services in Leicester",
        "Patios · Decking · Driveways · Lighting",
        "Landscaping services in Leicester and Leicestershire by Premium Landscapes.",
    ),
    "garden-design": (
        "images/ai-design-mediterranean.webp",
        "Garden Design in Leicester",
        "AI-powered concepts · Detailed plans",
        "Garden design in Leicester by Premium Landscapes — AI-powered concepts and detailed plans.",
    ),
    "privacy-policy": (
        "images/about-hero.webp",
        "Privacy Policy",
        "Premium Landscapes · Leicester",
        "Privacy policy for Premium Landscapes Leicester.",
    ),

    # --- Patio service-detail pages (5) ---
    "porcelain-patios-leicester": (
        "images/gallery-patio.webp",
        "Porcelain Patios in Leicester",
        "Large-format slabs · Frost-proof · Low-maintenance",
        "Porcelain patio installation in Leicester by Premium Landscapes — large-format, frost-proof slabs.",
    ),
    "sandstone-patios-leicester": (
        "images/natural-stone-patio.webp",
        "Sandstone Patios in Leicester",
        "Indian sandstone · Riven & sawn finishes",
        "Indian sandstone patio installation in Leicester by Premium Landscapes.",
    ),
    "limestone-patios-leicester": (
        "images/natural-stone-patio.webp",
        "Limestone Patios in Leicester",
        "Honed & tumbled finishes · Natural stone",
        "Limestone patio installation in Leicester by Premium Landscapes.",
    ),
    "granite-patios-leicester": (
        "images/natural-stone-patio.webp",
        "Granite Patios in Leicester",
        "Hard-wearing · Flamed & honed finishes",
        "Granite patio installation in Leicester by Premium Landscapes — hard-wearing flamed and honed finishes.",
    ),
    "natural-stone-patios-leicester": (
        "images/natural-stone-patio.webp",
        "Natural Stone Patios in Leicester",
        "Sandstone · Limestone · Granite · Slate",
        "Natural stone patio installation in Leicester by Premium Landscapes — sandstone, limestone, granite and slate.",
    ),

    # --- Driveway service-detail pages (2) ---
    "resin-driveways-leicester": (
        "images/driveway-block-paving.webp",
        "Resin Driveways in Leicester",
        "Resin-bound · SuDS-compliant · UV stable",
        "Resin-bound driveway installation in Leicester by Premium Landscapes — SuDS-compliant and UV-stable.",
    ),
    "block-paving-driveways-leicester": (
        "images/driveway-block-paving.webp",
        "Block Paving Driveways in Leicester",
        "Marshalls · Tobermore · Brett · Real installs",
        "Block paving driveway installation in Leicester by Premium Landscapes — Marshalls, Tobermore and Brett ranges.",
    ),

    # --- Lawn / decking service-detail pages (3) ---
    "turfing-leicester": (
        "images/artificial-turf-family.webp",
        "Turfing in Leicester",
        "Natural lawns · Soil prep · Real turf",
        "Lawn turfing in Leicester by Premium Landscapes — soil preparation and high-quality natural turf.",
    ),
    "raised-decking-leicester": (
        "images/decking-hero.webp",
        "Raised Decking in Leicester",
        "Composite & timber · Built to take levels",
        "Raised decking installation in Leicester by Premium Landscapes — composite and timber, built for sloped gardens.",
    ),
    "timber-decking-leicester": (
        "images/decking-hero.webp",
        "Timber Decking in Leicester",
        "Hardwood & softwood · Bespoke builds",
        "Timber decking installation in Leicester by Premium Landscapes — hardwood and softwood bespoke builds.",
    ),

    # --- Structural / boundary service-detail pages (5) ---
    "fencing-leicester": (
        "images/gallery-garden-pergola.webp",
        "Fencing in Leicester",
        "Closeboard · Featheredge · Slatted · Concrete posts",
        "Garden and boundary fencing installation in Leicester by Premium Landscapes.",
    ),
    "pergolas-leicester": (
        "images/gallery-garden-pergola.webp",
        "Pergolas in Leicester",
        "Timber · Aluminium · Louvered designs",
        "Pergola installation in Leicester by Premium Landscapes — timber, aluminium and louvered designs.",
    ),
    "garden-walls-leicester": (
        "images/projects/birstall/birstall-4.jpg",
        "Garden Walls in Leicester",
        "Brick · Stone · Rendered · Sleeper",
        "Garden wall building in Leicester by Premium Landscapes — brick, stone, rendered and sleeper walls.",
    ),
    "retaining-walls-leicester": (
        "images/projects/peterborough/peterborough-3.jpg",
        "Retaining Walls in Leicester",
        "Engineered · Drainage · Tiered gardens",
        "Retaining wall construction in Leicester by Premium Landscapes — engineered tiered garden solutions.",
    ),
    "garden-makeovers-leicester": (
        "images/after-garden.webp",
        "Garden Makeovers in Leicester",
        "Design · Build · Plant · Finish",
        "Full garden makeovers in Leicester by Premium Landscapes — design, build, plant and finish.",
    ),

    # --- Design / front garden / commercial (3) ---
    "front-garden-landscaping-leicester": (
        "images/projects/wigston/wigston-1.jpg",
        "Front Garden Landscaping Leicester",
        "Driveways · Paths · Planting · Kerb appeal",
        "Front garden landscaping in Leicester by Premium Landscapes — driveways, paths, planting and kerb appeal.",
    ),
    "garden-design-leicester": (
        "images/projects/evington/evington-6.jpg",
        "Garden Design in Leicester",
        "Concept · Detailed plans · Build-ready",
        "Garden design in Leicester by Premium Landscapes — concept, detailed plans and build-ready drawings.",
    ),
    "commercial-astroturf-leicester": (
        "images/artificial-turf-family.webp",
        "Commercial Astroturf Leicester",
        "Schools · Offices · Hospitality · Hard-wearing",
        "Commercial astroturf installation in Leicester by Premium Landscapes — schools, offices and hospitality.",
    ),
}


# Extra pages that need a dedicated path (e.g. project case-study pages live
# under projects/) and/or special meta-tag handling because they lack some of
# the OG / Twitter tags the simple PAGES path expects.
#   slug -> (
#       page_path_rel,
#       source_image,
#       headline,
#       sub_left,
#       og:image:alt,
#       url_path,        # used if we need to *insert* a new og:url
#       short_title,     # used for og/twitter:title if we have to insert
#       description,     # used for og/twitter:description if we have to insert
#   )
EXTRA_PAGES: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    # Homepage + key conversion pages
    "home": (
        "index.html",
        "images/hero-garden.webp",
        "Landscaping & Garden Design Leicester",
        "Patios · Driveways · Decking · Full Makeovers",
        "Landscaping and garden design in Leicester by Premium Landscapes — patios, driveways, decking and full makeovers.",
        "/",
        "Premium Landscapes Leicester",
        "Leicester landscapers specialising in patios, artificial grass, composite decking and full garden makeovers.",
    ),
    "quote": (
        "quote.html",
        "images/ai-design-mediterranean.webp",
        "Free Quote & AI Garden Design",
        "Photorealistic preview · 90 seconds · No cost",
        "Free instant landscaping quote and AI garden design preview from Premium Landscapes.",
        "/quote",
        "Free AI Garden Quote",
        "Free instant landscaping quote and photorealistic AI garden design preview from Premium Landscapes.",
    ),
    "about": (
        "about.html",
        "images/about-hero.webp",
        "About Premium Landscapes",
        "Leicester landscaping specialists",
        "About Premium Landscapes — Leicester landscaping and garden design specialists.",
        "/about",
        "About Premium Landscapes",
        "Meet Premium Landscapes — Leicester landscaping specialists building patios, driveways, decking and full garden makeovers.",
    ),
    "about-premium-landscapes": (
        "about-premium-landscapes.html",
        "images/about-garden.webp",
        "Premium Landscapes — Company Profile",
        "Who we are · What we do · Where we work",
        "Premium Landscapes company profile — Leicester landscaping and garden design.",
        "/about-premium-landscapes",
        "Premium Landscapes Company Profile",
        "Premium Landscapes — Leicester landscaping company profile: services, areas covered and how our quote process works.",
    ),
    "contact": (
        "contact.html",
        "images/services-garden.webp",
        "Contact Premium Landscapes",
        "Leicester · 07877 934782 · Free quotes",
        "Contact Premium Landscapes Leicester for a free landscaping quote.",
        "/contact",
        "Contact Premium Landscapes",
        "Get in touch with Premium Landscapes Leicester for a free landscaping quote, AI garden design preview or site visit.",
    ),
    "gallery": (
        "gallery.html",
        "images/gallery-garden-pergola.webp",
        "Garden Transformations Gallery",
        "Real Leicester projects · Before & after",
        "Garden transformations gallery — real Leicester projects by Premium Landscapes.",
        "/gallery",
        "Garden Transformations Gallery",
        "Real garden transformation projects by Premium Landscapes in Leicester and Leicestershire — before and after photos.",
    ),
    "case-studies": (
        "case-studies.html",
        "images/after-garden.webp",
        "Project Case Studies",
        "Real Leicestershire transformations",
        "Landscaping project case studies — real Leicestershire transformations by Premium Landscapes.",
        "/case-studies",
        "Project Case Studies",
        "Real landscaping case studies from Premium Landscapes — patios, decking, driveways and full garden makeovers across Leicestershire.",
    ),
    "areas-we-cover": (
        "areas-we-cover.html",
        "images/about-hero.webp",
        "Areas We Cover",
        "Leicester · Leicestershire · 20-mile radius",
        "Areas covered by Premium Landscapes — Leicester, Leicestershire and surrounding villages.",
        "/areas-we-cover",
        "Areas We Cover",
        "Premium Landscapes covers Leicester and surrounding villages including Oadby, Wigston, Narborough, Hinckley and Loughborough.",
    ),

    # Project case-study pages (projects/*.html). Slugs prefixed with
    # "project-" so the generated JPG sits at images/social/project-*.jpg
    # and never clashes with a top-level page slug.
    "project-artificial-grass-narborough": (
        "projects/artificial-grass-narborough.html",
        "images/artificial-turf-family.webp",
        "Artificial Grass, Narborough",
        "Real project · Premium Landscapes",
        "Artificial grass installation in Narborough — real project case study by Premium Landscapes.",
        "/projects/artificial-grass-narborough",
        "Artificial Grass Installation, Narborough",
        "Real artificial grass installation in Narborough by Premium Landscapes — pet- and family-friendly lawn case study.",
    ),
    "project-back-garden-patio-birstall": (
        "projects/back-garden-patio-birstall.html",
        "images/projects/birstall/birstall-4.jpg",
        "Back Garden Patio, Birstall",
        "Porcelain · Sleeper planters · Real project",
        "Back garden porcelain patio transformation in Birstall by Premium Landscapes.",
        "/projects/back-garden-patio-birstall",
        "Back Garden Patio Transformation, Birstall",
        "Back garden patio transformation in Birstall — grey porcelain, sleeper planters and hydrangea planting by Premium Landscapes.",
    ),
    "project-composite-decking-kirby-muxloe": (
        "projects/composite-decking-kirby-muxloe.html",
        "images/projects/kirby-muxloe/kirby-4.jpg",
        "Composite Decking, Kirby Muxloe",
        "Millboard · Real project · Premium Landscapes",
        "Composite decking installation in Kirby Muxloe — real project case study by Premium Landscapes.",
        "/projects/composite-decking-kirby-muxloe",
        "Composite Decking Installation, Kirby Muxloe",
        "Composite decking installation in Kirby Muxloe by Premium Landscapes — full project case study.",
    ),
    "project-composite-decking-wigston": (
        "projects/composite-decking-wigston.html",
        "images/decking-hero.webp",
        "Composite Decking, Wigston",
        "Real project · Premium Landscapes",
        "Composite decking project in Wigston by Premium Landscapes — full case study.",
        "/projects/composite-decking-wigston",
        "Composite Decking Project, Wigston",
        "Composite decking project in Wigston by Premium Landscapes — full case study.",
    ),
    "project-driveway-kirby-muxloe": (
        "projects/driveway-kirby-muxloe.html",
        "images/projects/kirby-muxloe-driveway/driveway-3.jpg",
        "Driveway, Kirby Muxloe",
        "Gravel · Block paving · Real project",
        "Gravel driveway with block paving in Kirby Muxloe — case study by Premium Landscapes.",
        "/projects/driveway-kirby-muxloe",
        "Gravel Driveway with Block Paving, Kirby Muxloe",
        "Gravel driveway with block paving edging in Kirby Muxloe by Premium Landscapes — full project case study.",
    ),
    "project-front-garden-renovation-wigston": (
        "projects/front-garden-renovation-wigston.html",
        "images/projects/wigston/wigston-1.jpg",
        "Front Garden Renovation, Wigston",
        "Real project · Premium Landscapes",
        "Front garden renovation in Wigston — real project case study by Premium Landscapes.",
        "/projects/front-garden-renovation-wigston",
        "Front Garden Renovation, Wigston",
        "Front garden renovation in Wigston by Premium Landscapes — full case study.",
    ),
    "project-full-garden-design-evington": (
        "projects/full-garden-design-evington.html",
        "images/projects/evington/evington-6.jpg",
        "Full Garden Design, Evington",
        "Design · Build · Plant · Real project",
        "Full garden design in Evington, Leicester — real project case study by Premium Landscapes.",
        "/projects/full-garden-design-evington",
        "Full Garden Design, Evington Leicester",
        "Full garden design and build in Evington, Leicester by Premium Landscapes — complete project case study.",
    ),
    "project-full-garden-makeover-oadby": (
        "projects/full-garden-makeover-oadby.html",
        "images/after-garden.webp",
        "Full Garden Makeover, Oadby",
        "Design · Build · Real project",
        "Full garden makeover in Oadby — real project case study by Premium Landscapes.",
        "/projects/full-garden-makeover-oadby",
        "Full Garden Makeover, Oadby",
        "Full garden makeover in Oadby by Premium Landscapes — design, build, plant and finish case study.",
    ),
    "project-porcelain-patio-leicester": (
        "projects/porcelain-patio-leicester.html",
        "images/gallery-patio.webp",
        "Porcelain Patio, Leicester",
        "Real project · Premium Landscapes",
        "Porcelain patio transformation in Leicester — real project case study by Premium Landscapes.",
        "/projects/porcelain-patio-leicester",
        "Porcelain Patio Transformation, Leicester",
        "Porcelain patio transformation in Leicester by Premium Landscapes — full project case study.",
    ),
    "project-tiered-garden-makeover-peterborough": (
        "projects/tiered-garden-makeover-peterborough.html",
        "images/projects/peterborough/peterborough-3.jpg",
        "Tiered Garden Makeover, Peterborough",
        "Levels · Build · Real project",
        "Tiered full garden makeover in Peterborough — real project case study by Premium Landscapes.",
        "/projects/tiered-garden-makeover-peterborough",
        "Tiered Full Garden Makeover, Peterborough",
        "Tiered full garden makeover in Peterborough by Premium Landscapes — multi-level design and build case study.",
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


def update_html_extra(
    page_path: Path,
    slug: str,
    alt: str,
    short_title: str,
    description: str,
    url_path: str,
) -> None:
    """Like update_html() but for pages that may be missing some/all of the
    OG / Twitter meta tags (e.g. areas-we-cover.html has none; case-studies.html
    has og:* but no twitter:*). Inserts whatever's missing in a sensible spot."""
    text = page_path.read_text(encoding="utf-8")

    host_match = re.search(r'<meta property="og:url" content="(https?://[^/"]+)', text)
    if host_match:
        host = host_match.group(1)
    else:
        canon = re.search(r'<link rel="canonical" href="(https?://[^/"]+)', text)
        host = canon.group(1) if canon else BASE_URL

    card_url = f"{host}/images/social/{slug}.jpg"
    page_url = f"{host}{url_path}"
    full_title = f"{short_title} | Premium Landscapes"

    og_image_block = (
        f'    <meta property="og:image" content="{card_url}">\n'
        f'    <meta property="og:image:secure_url" content="{card_url}">\n'
        f'    <meta property="og:image:alt" content="{alt}">\n'
        f'    <meta property="og:image:width" content="{CARD_W}">\n'
        f'    <meta property="og:image:height" content="{CARD_H}">\n'
    )
    new_text, n_og = OG_BLOCK_RE.subn(og_image_block, text, count=1)

    if n_og == 0:
        # No existing og:image — insert a complete OG block after the
        # apple-touch-icon link (a stable anchor present on every page).
        og_full = (
            f'    <meta property="og:type" content="website">\n'
            f'    <meta property="og:url" content="{page_url}">\n'
            f'    <meta property="og:title" content="{full_title}">\n'
            f'    <meta property="og:description" content="{description}">\n'
            + og_image_block
        )
        anchor_re = re.compile(r'(    <link rel="apple-touch-icon"[^>]*>\n)')
        new_text, n_anchor = anchor_re.subn(lambda m: m.group(1) + og_full, text, count=1)
        if n_anchor == 0:
            raise RuntimeError(f"{page_path}: no apple-touch-icon anchor to insert OG block")

    tw_image_block = (
        f'    <meta name="twitter:image" content="{card_url}">\n'
        f'    <meta name="twitter:image:alt" content="{alt}">\n'
    )
    new_text2, n_tw = TW_BLOCK_RE.subn(tw_image_block, new_text, count=1)

    if n_tw == 0:
        if re.search(r'<meta name="twitter:card"', new_text2):
            # twitter:card present but no twitter:image — slot it in after card
            new_text2 = re.sub(
                r'(    <meta name="twitter:card" content="[^"]+">\n)',
                lambda m: m.group(1) + tw_image_block,
                new_text2,
                count=1,
            )
        else:
            tw_full = (
                f'    <meta name="twitter:card" content="summary_large_image">\n'
                f'    <meta name="twitter:url" content="{page_url}">\n'
                f'    <meta name="twitter:title" content="{full_title}">\n'
                f'    <meta name="twitter:description" content="{description}">\n'
                + tw_image_block
            )
            new_text2, n_after = re.subn(
                r'(    <meta property="og:image:height" content="\d+">\n)',
                lambda m: m.group(1) + tw_full,
                new_text2,
                count=1,
            )
            if n_after == 0:
                raise RuntimeError(f"{page_path}: cannot place twitter block")

    page_path.write_text(new_text2, encoding="utf-8")


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

    for slug, (page_rel, src_rel, headline, sub_left, alt, url_path, short_title, description) in EXTRA_PAGES.items():
        src = ROOT / src_rel
        if not src.exists():
            raise FileNotFoundError(f"Source image missing: {src}")
        page = ROOT / page_rel
        if not page.exists():
            raise FileNotFoundError(f"Page missing: {page}")
        out = OUT_DIR / f"{slug}.jpg"
        render_card(src, headline, sub_left, out)
        update_html_extra(page, slug, alt, short_title, description, url_path)
        print(f"{slug:40s} -> {out.relative_to(ROOT)}")

    print(f"\nGenerated {len(PAGES) + len(EXTRA_PAGES)} social cards.")


if __name__ == "__main__":
    main()
