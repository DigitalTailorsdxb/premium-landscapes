#!/usr/bin/env python3
"""Phase E — rewrite thin SEO content on 3 service pages.

For each of natural-stone, sandstone, garden-walls:
  1. Update <title>, meta description, and matching og/twitter tags.
  2. Replace hero subheading paragraph with brief's intro copy (trimmed).
  3. Replace the existing "Options / Materials" section content with brief's
     "Types we install" / "Colour options" H3 list.
  4. INJECT new content sections (cost table + 2-4 educational H2 blocks)
     between the Materials section and the Why-Choose-Us section.
  5. Replace the FAQ section's accordion items with brief's 4-5 new Q&As.
  6. Replace the FAQPage JSON-LD mainEntity array with the new Q&As.
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def faq_accordion_html(items: list[tuple[str, str]]) -> str:
    rows = []
    for q, a in items:
        rows.append(f'''            <div class="faq-item py-5">
                <button class="w-full text-left flex justify-between items-center font-semibold text-gray-900 text-lg" onclick="this.nextElementSibling.classList.toggle('hidden');this.querySelector('i').classList.toggle('fa-chevron-down');this.querySelector('i').classList.toggle('fa-chevron-up')">
                    {q} <i class="fas fa-chevron-down text-blue-600 text-sm ml-4 flex-shrink-0"></i>
                </button>
                <div class="hidden mt-3 text-gray-600 leading-relaxed">{a}</div>
            </div>''')
    return "\n".join(rows)

def faq_jsonld_mainentity(items: list[tuple[str, str]]) -> str:
    arr = []
    for q, a in items:
        arr.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    # Compact one-per-line for readability
    inner = ",\n                ".join(json.dumps(x, ensure_ascii=False) for x in arr)
    return "[\n                " + inner + "\n            ]"

def types_grid_html(cards: list[tuple[str, str, str]]) -> str:
    """Each card: (emoji, h3_title, body_text)."""
    out = []
    for emoji, title, body in cards:
        out.append(f'''                    <div class="bg-white rounded-2xl p-6 shadow-md border border-gray-100 hover:border-blue-300 hover:shadow-lg transition-all">
                        <div class="text-3xl mb-3">{emoji}</div>
                        <h3 class="font-bold text-lg mb-2">{title}</h3>
                        <p class="text-gray-600 text-sm">{body}</p>
                    </div>''')
    return "\n".join(out)

def cost_table_html(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f'<th class="px-4 py-3 text-left font-semibold text-gray-900 border-b border-gray-200">{h}</th>' for h in headers)
    body = ""
    for r in rows:
        cells = "".join(f'<td class="px-4 py-3 border-b border-gray-100 text-gray-700">{c}</td>' for c in r)
        body += f"<tr>{cells}</tr>"
    return f'''                <div class="overflow-x-auto bg-white rounded-2xl shadow-md border border-gray-100 mb-6">
                    <table class="w-full text-sm">
                        <thead class="bg-gray-50"><tr>{head}</tr></thead>
                        <tbody>{body}</tbody>
                    </table>
                </div>'''

def prose_section_html(h2: str, paragraphs: list[str], bg: str = "white") -> str:
    bg_class = "bg-gray-50" if bg == "gray" else "bg-white"
    ps = "\n".join(f'                <p class="text-gray-700 leading-relaxed mb-4">{p}</p>' for p in paragraphs)
    return f'''
    <section class="py-16 px-4 {bg_class}">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold mb-6">{h2}</h2>
{ps}
        </div>
    </section>
'''

def cost_section_html(h2: str, intro: str, headers: list[str], rows: list[list[str]], footer: str, bg: str = "gray") -> str:
    bg_class = "bg-gray-50" if bg == "gray" else "bg-white"
    table = cost_table_html(headers, rows)
    return f'''
    <section class="py-16 px-4 {bg_class}">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold mb-4">{h2}</h2>
            <p class="text-gray-700 mb-6">{intro}</p>
{table}
            <p class="text-gray-600 text-sm italic">{footer}</p>
        </div>
    </section>
'''

# ============================================================================
# Per-page config
# ============================================================================
PAGES = {}

# ---------- /natural-stone-patios-leicester ---------------------------------
PAGES["natural-stone-patios-leicester.html"] = {
    "title": "Natural Stone Patio Installation Leicester | Indian Sandstone & More | Premium Landscapes",
    "meta": "Natural stone patio installation in Leicester. Indian sandstone, slate, limestone and granite laid by experienced installers. Prices from £80/m². Free instant quote.",
    "hero_sub": "The classic patio choice — character, warmth and proven durability. Every slab unique, laid on a properly prepared sub-base by experienced installers across Leicester and Leicestershire.",
    "materials_heading": "Natural Stone Types We Install in Leicester",
    "materials_lead": "Natural stone remains one of the most popular patio choices for Leicester homeowners. Each slab is unique — subtle colour variation, natural texture and a look that improves with age — and the right stone depends on your property style, garden aspect and how much maintenance you want to do.",
    "materials_cards": [
        ("🟤", "Indian Sandstone", "The most popular natural stone patio choice across the UK. Warm buff, raj green, autumn brown and ivory tones that complement Leicester's red-brick housing stock. Workable, affordable and relaxed in feel. Requires sealing every 2–3 years."),
        ("🩶", "Limestone", "Pale grey and cream tones with a clean, contemporary quality. Harder than sandstone, less porous, but still benefits from annual sealing. Popular in Stoneygate, Knighton and Oadby where properties tend towards modern styling."),
        ("🟫", "Slate (Riven)", "Dark grey and charcoal — dramatic, sophisticated, ideal for contemporary gardens with composite decking or powder-coated metalwork. Very hard. We only specify riven (split-face) slate outdoors for slip resistance."),
        ("⬛", "Granite", "The hardest and most durable natural stone available. Almost impervious to staining, frost and wear. Higher cost than sandstone, but a granite patio will outlast the house. Available in grey, black, pink and blue-grey."),
        ("🤍", "Travertine", "A form of limestone with a textured, Mediterranean feel. The natural holes are filled during processing, leaving a surface with good slip resistance. Suits warm-toned, plant-rich gardens and covered outdoor dining areas."),
    ],
    "extra_sections_html": (
        cost_section_html(
            "Natural Stone Patio Costs in Leicester",
            "Typical installed prices across Leicester and Leicestershire. All prices include excavation, compacted sub-base, mortar bed, pointing and waste removal — steps, walls and edging are quoted separately.",
            ["Stone Type", "Typical Installed Cost"],
            [
                ["Indian sandstone (mid-grade)", "£80 – £130/m²"],
                ["Limestone", "£100 – £160/m²"],
                ["Slate (riven)", "£110 – £170/m²"],
                ["Granite", "£130 – £200/m²"],
                ["Travertine", "£120 – £180/m²"],
            ],
            "Prices guide only — your free instant quote gives an exact figure based on your area, access and material choice.",
            bg="gray",
        )
        + prose_section_html(
            "Natural Stone vs Porcelain — Which Is Right for You?",
            [
                "This is the question almost every patio enquiry involves. The honest answer: it depends on what you value most.",
                "<strong>Choose natural stone if</strong> you want genuine character and variation in the material, your property has a traditional, period or cottage aesthetic, budget is a consideration (mid-grade Indian sandstone is notably cheaper than porcelain), or you're comfortable with sealing every 2–3 years.",
                "<strong>Choose porcelain if</strong> zero maintenance is a priority, you want consistent colour across the whole patio, you prefer large-format seamless slabs, or the garden faces north / gets heavy leaf fall where natural stone would stain.",
                "Both materials are excellent. Properly laid and regularly sealed natural stone looks stunning for decades — the maintenance is minimal once you stay on top of it.",
            ],
            bg="white",
        )
        + prose_section_html(
            "Why Sub-base Preparation Is Critical",
            [
                "Natural stone is more variable in thickness than manufactured products — each slab is slightly different, which means the mortar bed beneath it has to compensate rather than being a uniform depth. This requires more skill to lay correctly than porcelain or block paving. Poorly laid natural stone will rock, sink unevenly or crack where the mortar bed is inconsistent.",
                "We lay all natural stone on a full compacted MOT Type 1 sub-base with a semi-dry mortar bed, adjusting for each individual slab. In Leicestershire's clay soil conditions this is especially important — clay moves with moisture changes and a rigid sub-base is essential to prevent long-term settlement.",
            ],
            bg="gray",
        )
        + prose_section_html(
            "Natural Stone Sealing",
            [
                "All natural stone benefits from sealing before first use and resealing every 2–3 years thereafter. Sealing reduces porosity (oil, wine, moss and leaf stain can't penetrate), makes the surface easier to clean, enhances or preserves the natural colour depending on the sealer type, and extends the lifespan of the pointing.",
                "We apply an initial sealer coat to all natural stone installations before handover — colour-enhancing or natural-finish depending on what you prefer.",
            ],
            bg="white",
        )
    ),
    "faq_heading": "Natural Stone Patios Leicester — Frequently Asked Questions",
    "faqs": [
        ("Is natural stone slippery when wet?",
         "Riven (textured) natural stone has good natural slip resistance and is suitable for outdoor use. Polished or honed stone is not appropriate for outdoor patios in the UK climate. We only specify riven finishes for all external installations."),
        ("How do I clean natural stone?",
         "A pH-neutral patio cleaner and a stiff brush or pressure washer on a low setting, once or twice a year, is all that's needed. Avoid acidic cleaners — they etch the surface and break down the sealer."),
        ("Does natural stone crack in frost?",
         "Good quality natural stone laid on a proper sub-base with correct pointing does not crack from frost. Problems occur when water penetrates poorly pointed joints and freezes — which is why pointing and sealing are not optional extras on a natural stone installation."),
        ("How long does a natural stone patio last?",
         "Indefinitely with proper maintenance. Natural stone patios installed decades ago on correctly prepared sub-bases are still in excellent condition. The pointing may need refreshing every 10–15 years."),
        ("Can you match new natural stone to existing features?",
         "We can closely match existing stone colours and types in most cases. For extensions to existing patios, we bring samples to the site survey for comparison."),
    ],
}

# ---------- /sandstone-patios-leicester -------------------------------------
PAGES["sandstone-patios-leicester.html"] = {
    "title": "Sandstone Patio Installation Leicester | Indian Sandstone Specialists | Premium Landscapes",
    "meta": "Indian sandstone patio installation in Leicester and Leicestershire. Warm buff, raj green and autumn brown tones. Properly laid on a compacted sub-base. Free instant quote.",
    "hero_sub": "Leicester's most popular natural stone — warm, versatile and built to last. Properly laid Indian sandstone on a compacted sub-base by skilled, experienced teams.",
    "materials_heading": "Indian Sandstone Colour Options",
    "materials_lead": "Indian sandstone is the most installed natural stone patio surface across Leicester and Leicestershire — and has been for over two decades. Its warm colour palette, natural texture and competitive price make it the go-to for homeowners who want the character of natural stone without the cost of granite or limestone.",
    "materials_cards": [
        ("🟫", "Buff / Natural", "The classic sandstone colour — warm sandy tones with subtle cream and brown variation. Suits virtually every property type across Leicester, from Victorian terraces to modern new builds. The most versatile option and consistently the most popular."),
        ("🩶", "Raj Green", "A distinctive mid-grey to blue-green tone with warm undertones. Works particularly well in contemporary gardens and with grey composite decking, black metalwork and architectural planting. One of the most distinctive natural stone options available."),
        ("🟤", "Autumn Brown", "Rich brown, rust and burgundy tones that complement red and brown brick properties across Leicestershire. Creates an extremely warm, earthy aesthetic and works well in traditional garden schemes with planting borders and timber features."),
        ("🤍", "Ivory / Cream", "Light, almost-white tones that open up shaded gardens and suit south-facing spaces where the pale colour reflects light rather than absorbing it. Requires slightly more regular sealing than darker tones as staining shows more readily."),
        ("⬜", "Kandla Grey", "A cooler grey with subtle blue undertones — more contemporary than buff but more affordable than limestone or slate. Suits modern garden schemes and works well combined with artificial grass or composite decking."),
    ],
    "extra_sections_html": (
        cost_section_html(
            "Sandstone Patio Costs in Leicester",
            "Typical installed prices for Indian sandstone patios across Leicester. Per-m² cost typically £80–£130/m² depending on stone grade, colour and site conditions.",
            ["Patio Size", "Typical Installed Cost"],
            [
                ["Small (up to 20m²)", "£1,600 – £2,800"],
                ["Medium (20–40m²)", "£2,800 – £5,200"],
                ["Large (40m²+)", "£5,200+"],
            ],
            "Prices include full excavation, compacted MOT Type 1 sub-base, semi-dry mortar bed, slab laying, brush-in pointing and waste removal.",
            bg="gray",
        )
        + prose_section_html(
            "Our Sandstone Installation Process",
            [
                "<strong>Excavation and preparation.</strong> We excavate to 200–250mm depth to create the sub-base formation. All topsoil and vegetation are removed and taken off site.",
                "<strong>Sub-base.</strong> 150mm of compacted MOT Type 1 hardcore is laid and compacted in layers. This is the single most important stage of a patio installation — a weak sub-base causes settlement no matter how good the stone is.",
                "<strong>Mortar bed.</strong> A semi-dry mortar bed is laid at approximately 50mm depth, screeded level and adjusted for falls to drain water away from the house. Natural stone requires a full mortar bed — not dot-and-dab, which creates voids that crack the slab over time.",
                "<strong>Stone laying.</strong> Slabs are placed carefully, adjusted for level and consistent joint width, and tapped down firmly. Each row is checked with a spirit level. Edge cuts are made with a disc cutter for clean, precise joints.",
                "<strong>Pointing.</strong> Once the mortar bed has cured (minimum 24 hours), joints are filled with a brush-in pointing compound rated for external use. We choose a pointing colour that complements the stone — not grey mortar on warm-toned sandstone.",
                "<strong>Sealing.</strong> An initial penetrating sealer is applied before handover. This is included in the quote.",
            ],
            bg="white",
        )
        + prose_section_html(
            "Sandstone Maintenance in Leicester",
            [
                "Indian sandstone is a natural, porous material that needs modest ongoing maintenance to look its best.",
                "<strong>Annual cleaning.</strong> A pH-neutral patio cleaner and stiff brush or low-pressure washer removes algae, lichen and general grime. Avoid acid-based cleaners — they strip the sealer and etch the surface.",
                "<strong>Re-sealing.</strong> Every 2–3 years, depending on exposure and use. Re-sealing takes a few hours and a tin of penetrating sealer — a straightforward DIY task.",
                "<strong>Pointing.</strong> May need refreshing after 10–15 years on heavily used patios. A relatively minor job and much less expensive than full replacement.",
                "<strong>What to avoid:</strong> bleach, acidic cleaners, metal tools on the surface, and rust-prone metal furniture or planters in direct contact with the stone without felt feet.",
            ],
            bg="gray",
        )
    ),
    "faq_heading": "Sandstone Patios Leicester — Frequently Asked Questions",
    "faqs": [
        ("Is Indian sandstone good quality for a Leicester patio?",
         "Yes — though quality varies between suppliers and grades. We specify first-quality calibrated Indian sandstone (consistent thickness) from established UK distributors. Avoid uncalibrated or 'budget' sandstone — the thickness variation makes it very difficult to lay correctly."),
        ("Does sandstone stain easily?",
         "Unsealed sandstone stains more readily than porcelain, but a quality penetrating sealer significantly reduces this. Red wine, oil and rust marks can penetrate unsealed stone quickly — but sealed stone resists all of these with normal use."),
        ("Can sandstone be used for a driveway?",
         "Natural sandstone is not suitable for driveways — it's not rated for vehicle loading and will crack under repeated wheel pressure. For driveways we install block paving, resin bound or porcelain (driveway-grade only)."),
        ("What's the difference between calibrated and riven sandstone?",
         "Calibrated sandstone is machined to a consistent thickness — easier to lay and gives more consistent joint lines. Riven sandstone has a naturally split top face — more texture and character, but more variable thickness."),
        ("How often should I reseal Indian sandstone in the UK?",
         "Every 2–3 years for most domestic patios. Shaded, north-facing patios with moss or algae pressure may need slightly more frequent attention; sheltered, south-facing patios can often go the full 3 years."),
    ],
}

# ---------- /garden-walls-leicester -----------------------------------------
PAGES["garden-walls-leicester.html"] = {
    "title": "Garden Wall Construction Leicester | Brick, Block & Stone Walling | Premium Landscapes",
    "meta": "Garden wall construction in Leicester. Retaining walls, boundary walls, raised bed walls and decorative walling. Brickwork, blockwork and natural stone. Free instant quote.",
    "hero_sub": "Retaining walls, boundary walls and raised planters — built properly, built to last. Engineering brick, blockwork, natural stone and sleeper, all on correctly specified footings.",
    "materials_heading": "Types of Garden Wall We Build in Leicester",
    "materials_lead": "A well-built garden wall defines the structure of an outdoor space, provides the bones that planting and hard landscaping hang from, and adds permanent value to a property. We build across Leicester and Leicestershire in brick, block, natural stone and sleeper — from small raised bed borders to substantial retaining walls and full boundary constructions.",
    "materials_cards": [
        ("🧱", "Retaining Walls", "Holding back soil on sloped or tiered gardens — one of the most common requirements in Leicester's varied residential landscape. Engineered correctly: right foundation depth, drainage behind the wall to prevent water build-up, and adequate mass or tie-back. Built in engineering brick, natural stone, concrete block or railway sleeper."),
        ("🪴", "Raised Bed Walls", "Lift planting to a comfortable working height, give excellent drainage for vegetables and ornamental planting, and create defined structure. Built in facing brick to match the house, in natural stone for a more organic feel, or in sleeper for a contemporary look."),
        ("🏡", "Boundary Walls", "Traditional full-height brick or natural stone — replacing fencing on exposed boundaries, completing a front boundary, or creating a permanent garden zone divider. Footings to the depth that wall height and ground conditions require, plus DPC, brickwork and coping in one installation."),
        ("🪑", "Decorative & Seat Walls", "Low walls at 450–600mm double as seating around a patio — one of the most functional design elements we build. Rendered seat walls around porcelain feel contemporary; natural stone around sandstone gives a more organic, traditional look. Can incorporate planters, lighting channels and storage."),
        ("🪜", "Garden Steps", "Brick, natural stone, porcelain or sleeper risers connecting different levels — often built alongside retaining walls or as part of a tiered design. Built to the correct rise and going for comfortable use, with non-slip nosing on all treads."),
    ],
    "extra_sections_html": (
        cost_section_html(
            "Garden Wall Costs in Leicester",
            "Typical installed prices across Leicester. Costs vary with height, material, footing depth and site conditions.",
            ["Wall Type", "Typical Cost"],
            [
                ["Raised bed walls (per linear metre)", "£120 – £250/m"],
                ["Retaining walls (per linear metre)", "£180 – £400/m"],
                ["Boundary walls (per linear metre)", "£200 – £500/m"],
                ["Seat walls (per linear metre)", "£150 – £300/m"],
                ["Garden steps (per step)", "£150 – £350"],
            ],
            "All prices include footings, brickwork/blockwork, coping or capping, and waste removal.",
            bg="gray",
        )
        + prose_section_html(
            "Garden Walls and Retaining Walls — What Makes a Good Build",
            [
                "The failures we're most often called in to repair fall into the same handful of categories.",
                "<strong>Inadequate footings.</strong> A boundary or retaining wall built on a shallow strip footing on Leicestershire clay will lean or crack within a few years as the clay moves with moisture. Footing depth must be sufficient for the wall height and the ground conditions.",
                "<strong>No drainage behind retaining walls.</strong> Water that can't drain through or around a retaining wall builds hydrostatic pressure behind it — the most common cause of retaining wall collapse. Every retaining wall we build includes a drainage aggregate layer plus weep holes or drainage channels.",
                "<strong>Wrong mortar mix.</strong> External brickwork needs a mix rated for the exposure level — too weak and it erodes, too strong and it prevents movement, causing the bricks themselves to crack. We use the appropriate BS mix for the site conditions on every job.",
                "<strong>Missing DPC.</strong> Garden walls need a damp proof course above ground level to prevent rising damp from staining and degrading the brickwork. Boundary and raised bed walls without a DPC show salt efflorescence and deterioration within a few years.",
            ],
            bg="white",
        )
        + prose_section_html(
            "Garden Walls as Part of a Landscaping Project",
            [
                "Garden walls deliver the most impact when they're designed as part of the overall garden scheme — not added afterwards. A retaining wall that also serves as seating, integrated with a porcelain patio and tied into the fencing line, creates a cohesive outdoor space. Raised bed walls that match the house brickwork connect the garden to the architecture of the property.",
                "We regularly build garden walls as part of full garden redesigns and makeovers across Leicester, and every landscaping quote we produce can include walling work.",
            ],
            bg="gray",
        )
    ),
    "faq_heading": "Garden Walls Leicester — Frequently Asked Questions",
    "faqs": [
        ("Do I need planning permission for a garden wall?",
         "In most cases no. Walls under 1 metre adjacent to a highway and under 2 metres elsewhere don't require planning permission under permitted development rights. Conservation area and listed building rules differ — we advise at survey stage."),
        ("How long does a garden wall take to build?",
         "A raised bed or short retaining wall takes 1–3 days. A full boundary wall or more substantial retaining wall takes 3–7 days depending on length and height."),
        ("What's the best material for a retaining wall in Leicester?",
         "For most residential gardens, engineering brick on a concrete footing is the most practical and durable choice. For a more natural look, natural stone (particularly limestone or sandstone) is excellent. Railway sleepers are popular for lower retaining walls and raised beds — quick, good-looking, but a 15–25 year lifespan compared to 50+ years for masonry."),
        ("Can you build a wall to match my house brickwork?",
         "In most cases yes. We source facing bricks to match or closely complement existing house brickwork — important for boundary and raised bed walls that will be seen alongside the property."),
        ("Do garden walls need footings?",
         "Yes — every masonry garden wall needs a concrete strip footing. The footing depth depends on wall height and ground conditions. In Leicestershire's clay soil we typically go to 450–600mm for walls up to 1m high."),
    ],
}

# ============================================================================
# Apply edits
# ============================================================================
def rewrite_page(path: Path, cfg: dict):
    html = path.read_text(encoding="utf-8")
    orig = html

    # ---- 1. Title + meta description + og + twitter ----
    new_title = cfg["title"]
    new_meta = cfg["meta"]
    # Page-card title (shorter) for og/twitter to avoid duplicating long marketing tail
    short_card_title = new_title.split(" | Premium")[0] + " | Premium Landscapes"

    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(r'(<meta name="description" content=")[^"]*(">)', rf'\1{new_meta}\2', html, count=1)
    html = re.sub(r'(<meta property="og:title" content=")[^"]*(">)', rf'\1{short_card_title}\2', html, count=1)
    html = re.sub(r'(<meta property="og:description" content=")[^"]*(">)', rf'\1{new_meta}\2', html, count=1)
    html = re.sub(r'(<meta name="twitter:title" content=")[^"]*(">)', rf'\1{short_card_title}\2', html, count=1)
    html = re.sub(r'(<meta name="twitter:description" content=")[^"]*(">)', rf'\1{new_meta}\2', html, count=1)

    # ---- 2. Hero subheading paragraph (first <p class="text-xl text-blue-100..."> inside hero) ----
    html = re.sub(
        r'(<p class="text-xl text-blue-100 mb-4 max-w-2xl mx-auto">)[^<]*(</p>)',
        rf'\1{cfg["hero_sub"]}\2',
        html, count=1,
    )

    # ---- 3. Replace Options/Materials section body ----
    new_materials = f'''    <!-- Options / Materials -->
    <section class="py-16 px-4 bg-gray-50">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold text-center mb-4">{cfg["materials_heading"]}</h2>
            <p class="text-gray-600 text-center mb-12 max-w-3xl mx-auto">{cfg["materials_lead"]}</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
{types_grid_html(cfg["materials_cards"])}
            </div>
        </div>
    </section>
'''
    html = re.sub(
        r'    <!-- Options / Materials -->.*?</section>\n',
        new_materials,
        html, count=1, flags=re.S,
    )

    # ---- 4. Inject extra educational sections AFTER materials, BEFORE Why-Choose-Us ----
    # Insert the block right before "    <!-- Why Choose Us -->"
    extra = cfg["extra_sections_html"]
    html = html.replace(
        "    <!-- Why Choose Us -->",
        extra.lstrip("\n") + "\n    <!-- Why Choose Us -->",
        1,
    )

    # ---- 5. Replace FAQ section accordion items ----
    new_faq = f'''    <!-- FAQs -->
    <section class="py-16 px-4 bg-white">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold text-center mb-12">{cfg["faq_heading"]}</h2>
{faq_accordion_html(cfg["faqs"])}
        </div>
    </section>
'''
    html = re.sub(
        r'    <!-- FAQs -->.*?</section>\n',
        new_faq,
        html, count=1, flags=re.S,
    )

    # ---- 6. Replace FAQPage mainEntity JSON-LD array ----
    new_main = faq_jsonld_mainentity(cfg["faqs"])
    # Find the FAQPage block and replace its mainEntity array.
    # The mainEntity is an array starting after `"mainEntity": ` and ending
    # before the closing `]` immediately before `}` that ends the FAQPage object.
    def replace_faq_mainentity(m):
        return f'"@type": "FAQPage",\n                "mainEntity": {new_main}'
    html = re.sub(
        r'"@type":\s*"FAQPage",\s*"mainEntity":\s*\[.*?\n\s*\]',
        replace_faq_mainentity,
        html, count=1, flags=re.S,
    )

    if html == orig:
        print(f"  ⚠️  {path.name}: NO changes applied")
    else:
        path.write_text(html, encoding="utf-8")
        print(f"  ✅ {path.name} rewritten")

print("=== Phase E: rewriting 3 thin-content service pages ===\n")
for fname, cfg in PAGES.items():
    rewrite_page(ROOT / fname, cfg)

# ---- Validate JSON-LD on all 3 pages ----
print("\n=== Validate JSON-LD ===")
for fname in PAGES:
    txt = (ROOT / fname).read_text(encoding="utf-8")
    for i, m in enumerate(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S), 1):
        try:
            data = json.loads(m.group(1))
            types = [n.get("@type") for n in data.get("@graph", [])]
            print(f"  ✅ {fname} block#{i}: types = {types}")
        except Exception as e:
            print(f"  ❌ {fname} block#{i}: {e}")
