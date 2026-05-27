#!/usr/bin/env python3
"""
Phase K — Unique H1s, hero subtitles, title tags and meta descriptions
for all 20 location pages.

Run from project root:
    python3 scripts/phase_k_unique_heroes.py

What it does for each page
--------------------------
1. Replaces the <title> tag (Tier 1 pages get a richer version with year)
2. Replaces the <meta name="description"> content
3. Replaces the <h1> text (adds postcode hint for Tier 1)
4. Replaces the hero subtitle <p> (50-120 words, locally factual)

No other markup is touched.
"""

import re, pathlib, sys

ROOT = pathlib.Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# Per-area data
# ---------------------------------------------------------------------------
PAGES = [
    # ── TIER 1 ──────────────────────────────────────────────────────────────
    {
        "file": "landscaping-leicester.html",
        "title": "Landscaping Leicester LE1–LE5 | Patios, Artificial Grass & Garden Design 2026 | Premium Landscapes",
        "meta_desc": "Local landscaping contractor covering all Leicester LE postcodes. Patios, artificial grass, composite decking, driveways & full garden makeovers — fixed-price quotes, fully insured, free AI design preview.",
        "h1": "Landscaping in Leicester, LE1–LE5",
        "hero_sub": "Premier Landscapes designs and builds outdoor spaces across every LE postcode — from the Victorian terraces of Clarendon Park and Stoneygate to the 1970s semis of Beaumont Leys and the new-builds of Meridian. We understand Leicester's varied ground conditions: the heavy Mercia Mudstone clay under the south suburbs, the river-valley alluvium near the Soar, and the mixed made-ground beneath inner-city plots. Whether you need a porcelain patio that handles clay movement, a SuDS-compliant permeable driveway, or a full rear-garden transformation, we deliver fixed-price, fully insured work — with a free AI design visualisation included.",
    },
    {
        "file": "landscaping-stoneygate.html",
        "title": "Landscaping Stoneygate Leicester LE2 | Patios, Decking & Garden Design 2026 | Premium Landscapes",
        "meta_desc": "Specialist landscaping in Stoneygate LE2. Victorian and Edwardian rear gardens transformed with porcelain patios, composite decking & artificial grass. Free instant quote & AI design preview.",
        "h1": "Landscaping in Stoneygate, Leicester LE2",
        "hero_sub": "Stoneygate's leafy streets — London Road, Knighton Road, Westleigh Road — are lined with Victorian and Edwardian villas whose rear gardens combine generous proportions with the classic Leicester challenge: heavy Mercia Mudstone clay that shrinks in summer and waterloggs in winter. We specialise in drainage-led designs for exactly this profile — laying robust Type 1 sub-bases, installing French drains where needed, and finishing with materials that won't lift or crack. From porcelain terraces to composite decking and lush artificial lawns, every project is fixed-price and fully insured. Your free AI garden preview is included with every quote.",
    },
    {
        "file": "landscaping-knighton.html",
        "title": "Landscaping Knighton Leicester LE2 | Patios, Artificial Grass & Garden Design 2026 | Premium Landscapes",
        "meta_desc": "Landscaping specialists in Knighton LE2. Porcelain patios, artificial grass, composite decking & full garden makeovers for Knighton's spacious Victorian gardens. Free instant quote.",
        "h1": "Landscaping in Knighton, Leicester LE2",
        "hero_sub": "Knighton's tree-lined avenues — Elmfield Avenue, Welford Road, Knighton Church Road — sit within the LE2 postcode on land underlain by Mercia Mudstone, meaning gardens here are naturally clay-heavy and prone to waterlogging after wet winters. Our team works on these plots week in, week out: installing gravel sub-bases deep enough to accommodate seasonal clay movement, matching porcelain and sandstone tones to the warm ironstone brickwork of period properties, and creating low-maintenance artificial-lawn areas that look immaculate year-round. All work is fixed-price and fully insured, with a complimentary AI design preview to help you visualise your finished garden before we break ground.",
    },
    {
        "file": "landscaping-clarendon-park.html",
        "title": "Landscaping Clarendon Park Leicester LE2 | Patios, Decking & Garden Design 2026 | Premium Landscapes",
        "meta_desc": "Landscaping in Clarendon Park LE2. Compact Victorian rear gardens transformed with porcelain patios, raised decking & artificial grass. Free instant quote & AI garden visualisation.",
        "h1": "Landscaping in Clarendon Park, Leicester LE2",
        "hero_sub": "Clarendon Park sits in the heart of the LE2 postcode, just south of Victoria Park, where tightly terraced Victorian streets give way to some of Leicester's most characterful rear gardens — often no wider than 4–6 metres but surprisingly long. We've honed our approach for this footprint: split-level porcelain patios that maximise usable space, slimline raised composite decking, and smart artificial lawns that bring green colour without demanding a back-breaking mow. The underlying Mercia Mudstone clay means drainage detailing is critical; our sub-bases are always engineered for movement. Fixed-price, fully insured, free AI preview included.",
    },
    {
        "file": "landscaping-kirby-muxloe.html",
        "title": "Landscaping Kirby Muxloe LE9 | Patios, Artificial Grass & Garden Design 2026 | Premium Landscapes",
        "meta_desc": "Premium Landscapes is based in Kirby Muxloe LE9 — your truly local landscaping contractor. Patios, artificial grass, composite decking, driveways & full garden makeovers. Free instant quote.",
        "h1": "Landscaping in Kirby Muxloe, Leicestershire LE9",
        "hero_sub": "Kirby Muxloe is our home — Premium Landscapes is based at 44 Barwell Road, LE9 2AA, which means we know this village's gardens better than any contractor. The area spans a mix of inter-war semis, 1980s estates around Castle Lane, and newer builds on the western fringe, all sitting above Mercia Mudstone with pockets of glacial till near the Rothley Brook corridor. We're typically on-site within days rather than weeks. Whether you're transforming a front driveway with SuDS-compliant block paving, adding composite decking to a south-facing rear, or commissioning a full garden makeover — you get our fastest response, fixed pricing, and a free AI design preview.",
    },
    {
        "file": "landscaping-oadby.html",
        "title": "Landscaping Oadby Leicester LE2 | Patios, Artificial Grass & Garden Design 2026 | Premium Landscapes",
        "meta_desc": "Landscaping in Oadby LE2. Generous suburban gardens transformed with porcelain patios, artificial grass, composite decking & driveways. Cheshire Gate to The Oval — free instant quote.",
        "h1": "Landscaping in Oadby, Leicestershire LE2",
        "hero_sub": "Oadby sits in the LE2 postcode on the southern edge of Leicester, where post-war detached and semi-detached housing offers some of the most generous garden plots in the city — many with 12–18 m rear lawns and wide side accesses. The ground here is predominantly heavy Mercia Mudstone clay with occasional pockets of glacial outwash gravel near the Sence valley, so drainage design is always factored into our sub-base specification. From sandstone patio extensions at The Oval to full garden makeovers along Harborough Road, we deliver beautifully finished outdoor spaces at fixed, transparent prices — with a complimentary AI visualisation of your finished garden.",
    },
    {
        "file": "landscaping-wigston.html",
        "title": "Landscaping Wigston Leicester LE18 | Patios, Artificial Grass & Garden Design 2026 | Premium Landscapes",
        "meta_desc": "Landscaping in Wigston LE18. 1930s and post-war gardens transformed with porcelain patios, artificial grass & composite decking across Wigston Magna, South Wigston & Wigston Fields. Free quote.",
        "h1": "Landscaping in Wigston, Leicestershire LE18",
        "hero_sub": "Wigston — spanning Wigston Magna, South Wigston, and Wigston Fields — falls within the LE18 postcode and is characterised by 1930s and post-war housing stock with established rear gardens, many retaining original concrete-slab paths and tired lawns that are ripe for transformation. The clay-dominant Mercia Mudstone beneath most of the area means gardens can be boggy after wet spells; our drainage-engineered sub-bases solve this before laying any surface. Blaby District Council governs planning here, so we advise on any permitted-development rules relevant to your project upfront. Fixed prices, fully insured, and a free AI design preview — no obligation.",
    },
    # ── TIER 2 / REMAINING ───────────────────────────────────────────────────
    {
        "file": "landscaping-anstey.html",
        "title": "Landscaping Anstey Leicestershire LE7 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Anstey LE7. Patios, artificial grass, composite decking & garden makeovers for Anstey's varied housing stock above Charnian rock. Free instant quote, fully insured.",
        "h1": "Landscaping in Anstey, Leicestershire LE7",
        "hero_sub": "Anstey lies 5 miles north-west of Leicester city centre in the LE7 postcode, governed by Charnwood Borough Council. The village sits on Charnian quartzite and slate — ancient Pre-Cambrian rock that gives gardens here noticeably better drainage than the clay-heavy south suburbs, but can mean shallower topsoil and the occasional encounter with solid rock just below the surface. We account for this in our groundworks spec, ensuring bases are properly prepared whether we hit soft ground or bedrock. Anstey's mix of Victorian stone cottages, inter-war semis, and modern cul-de-sacs all suit our patio, decking, and artificial-lawn services well.",
    },
    {
        "file": "landscaping-birstall.html",
        "title": "Landscaping Birstall Leicestershire LE4 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Birstall LE4. Patios, artificial grass, composite decking & full garden makeovers for Birstall and Wanlip. River Soar floodplain drainage expertise. Free instant quote.",
        "h1": "Landscaping in Birstall, Leicestershire LE4",
        "hero_sub": "Birstall is a substantial north Leicester suburb in the LE4 postcode, sitting on a mix of Mercia Mudstone and the alluvial deposits left by the River Soar floodplain. Gardens on the lower-lying streets near the river need careful drainage detailing — we always assess ground conditions before specifying sub-base depth. Charnwood Borough Council covers this area; most residential garden works fall comfortably within permitted development. Popular with families attracted by good schools and easy ring-road access, Birstall properties often feature generous 1960s and 1970s rear gardens ideal for a porcelain patio, low-maintenance artificial lawn, or composite decking zone.",
    },
    {
        "file": "landscaping-blaby.html",
        "title": "Landscaping Blaby Leicestershire LE8 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Blaby LE8. Patios, artificial grass, driveways & full garden makeovers in Blaby village and the surrounding LE8 area. Blaby District Council planning guidance included. Free quote.",
        "h1": "Landscaping in Blaby, Leicestershire LE8",
        "hero_sub": "Blaby village and the wider LE8 postcode sits in the heart of Blaby District — one of Leicestershire's most active planning authorities for residential garden and driveway applications. We're familiar with local permitted-development limits and SuDS requirements for front driveways in this area, where Mercia Mudstone clay and Soar valley alluvium make drainage detailing essential. From the new-build estates off Lutterworth Road to the older housing stock along the A426 corridor, we cover a broad mix of property types. All projects are fixed-price, fully insured, and include a free AI garden visualisation so you can see the finished result before work begins.",
    },
    {
        "file": "landscaping-cosby.html",
        "title": "Landscaping Cosby Leicestershire LE9 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Cosby LE9. Rural village gardens transformed with patios, artificial grass & garden makeovers. 8 miles from our Kirby Muxloe base — fast local response. Free instant quote.",
        "h1": "Landscaping in Cosby, Leicestershire LE9",
        "hero_sub": "Cosby is a quiet South Leicestershire village in the LE9 postcode, governed by Blaby District Council, approximately 8 miles from our Kirby Muxloe base. The village sits on Mercia Mudstone with river-terrace gravels near Cosby Brook — ground that tends to drain reasonably well compared to pure Mudstone areas but still benefits from a properly engineered sub-base. Cosby's housing is a pleasing mix of older stone and brick cottages, 1960s–1980s semis, and some modern detached properties, most offering good-sized rear plots. We work across all these garden types: from family-sized artificial lawns to elegant sandstone terraces and low-maintenance planted borders.",
    },
    {
        "file": "landscaping-enderby.html",
        "title": "Landscaping Enderby Leicestershire LE19 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Enderby LE19. Patios, artificial grass, composite decking & full garden makeovers near Fosse Park. Blaby District planning expertise. Free instant quote, fully insured.",
        "h1": "Landscaping in Enderby, Leicestershire LE19",
        "hero_sub": "Enderby occupies the LE19 postcode at the south-western edge of Leicester, sandwiched between the A563 ring road and open Leicestershire countryside. The area is overseen by Blaby District Council and has seen significant housing growth near Fosse Park, adding a large stock of 1990s–2010s properties with modest but neatly proportioned rear gardens. The ground here is predominantly Mercia Mudstone clay, so we always specify adequate sub-base depth and perimeter drainage on new patio installations to prevent pooling. We're regularly working in Enderby and can typically schedule a survey within a few days — fixed price, fully insured, with a free AI garden preview included.",
    },
    {
        "file": "landscaping-glenfield.html",
        "title": "Landscaping Glenfield Leicestershire LE3 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Glenfield LE3. Patios, artificial grass, composite decking & driveways for Glenfield's range of bungalows, semis and estates. Hinckley Road corridor and beyond. Free quote.",
        "h1": "Landscaping in Glenfield, Leicestershire LE3",
        "hero_sub": "Glenfield sits in the LE3 postcode on the north-western fringe of Leicester, governed by Hinckley & Bosworth Borough Council for its outer sections and partly by Leicester City for areas nearer Beaumont Leys. The village and surrounding housing estates — stretching along Hinckley Road and Dominion Road — mix 1930s bungalows, post-war semis, and more recent developments. Soils here are a blend of Mercia Mudstone and Charnian-derived material, generally giving workable ground conditions. We regularly install porcelain patios, composite decking, and low-maintenance artificial grass in Glenfield, usually with a fast turnaround given our 4-mile proximity from base.",
    },
    {
        "file": "landscaping-hinckley.html",
        "title": "Landscaping Hinckley Leicestershire LE10 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Hinckley LE10. Patios, artificial grass, composite decking & garden makeovers covering Hinckley, Burbage & Earl Shilton. Hinckley & Bosworth Borough. Free instant quote.",
        "h1": "Landscaping in Hinckley, Leicestershire LE10",
        "hero_sub": "Hinckley is the main town of Hinckley & Bosworth Borough, covered by the LE10 postcode district, approximately 15 miles west of our Kirby Muxloe base via the A47. The town's character ranges from Victorian terraces in the historic centre to large 1980s and 1990s estates in Burbage and Earl Shilton. Ground conditions vary: the town centre and northern areas sit on Coal Measures with loamy soils, while southern suburbs are underlain by Triassic Mercia Mudstone. We cover all Hinckley areas for patios, artificial grass, composite decking, and full garden redesigns — all at fixed prices, fully insured, with our complimentary AI design preview.",
    },
    {
        "file": "landscaping-loughborough.html",
        "title": "Landscaping Loughborough Leicestershire LE11 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Loughborough LE11 & LE12. Patios, artificial grass, composite decking & full garden makeovers. Charnwood Borough, 15 miles north of our base. Free instant quote, fully insured.",
        "h1": "Landscaping in Loughborough, Leicestershire LE11",
        "hero_sub": "Loughborough is the principal town of Charnwood Borough, covered mainly by the LE11 postcode (with LE12 covering surrounding villages), and lies approximately 15 miles north of our Kirby Muxloe base via the A6. The town's housing stock runs from Victorian red-brick terraces near the town centre, through the inter-war semis of Shelthorpe and Woodthorpe, to the modern builds around Nanpantan. The geology transitions here: Charnian volcanic rocks in the west give firmer, better-drained ground, while the lower Soar valley to the east carries alluvial clay. Our fixed-price patios, decking, artificial grass, and full garden redesigns come with a free AI visualisation — no obligation.",
    },
    {
        "file": "landscaping-markfield.html",
        "title": "Landscaping Markfield Leicestershire LE67 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Markfield LE67. Patios, artificial grass, composite decking & garden makeovers on Charnian quartzite geology. NW Leicestershire, fast response from our LE9 base. Free quote.",
        "h1": "Landscaping in Markfield, Leicestershire LE67",
        "hero_sub": "Markfield is a large village in the LE67 postcode on the edge of Charnwood Forest, governed by North West Leicestershire District Council and approximately 8 miles from our Kirby Muxloe base. The village sits prominently on Charnian quartzite and Pre-Cambrian igneous rock — the same hard geology exploited at the nearby Stanton under Bardon quarry. This means gardens here often have shallower topsoil than clay-belt areas, and groundwork can encounter solid rock at shallow depth; our team carries appropriate equipment to deal with this. Housing ranges from older stone terraces in the village centre to newer detached estates off the A50.",
    },
    {
        "file": "landscaping-narborough.html",
        "title": "Landscaping Narborough Leicestershire LE19 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Narborough & Littlethorpe LE19. Patios, artificial grass, composite decking & garden makeovers beside the River Soar. Blaby District — free instant quote, fully insured.",
        "h1": "Landscaping in Narborough, Leicestershire LE19",
        "hero_sub": "Narborough and adjoining Littlethorpe sit in the LE19 postcode in the Soar valley, governed by Blaby District Council, approximately 6 miles south-west of our Kirby Muxloe base. The River Soar runs directly through the village, and much of Narborough's housing is built on alluvial soils and river terrace gravels — ground that generally drains well but can hide pockets of soft fill on older infill plots. We always assess ground conditions during our initial survey, specifying the appropriate sub-base depth and edge restraints before any paving is laid. From low-maintenance artificial lawns to full porcelain patio installations, our work here is fixed-price and fully insured.",
    },
    {
        "file": "landscaping-ratby.html",
        "title": "Landscaping Ratby Leicestershire LE6 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Ratby LE6. Patios, artificial grass, composite decking & garden makeovers in this rural west Leicestershire village. 3 miles from our base — fastest local response. Free quote.",
        "h1": "Landscaping in Ratby, Leicestershire LE6",
        "hero_sub": "Ratby is one of our closest regular work areas — barely 3 miles from our Kirby Muxloe base via Desford Lane — sitting in the LE6 postcode under Hinckley & Bosworth Borough Council. The village stands on Charnian igneous and metamorphic rocks with pockets of glacial till, giving firmer and better-draining ground conditions than the Mercia Mudstone clay found further south. Gardens here range from long stone-walled rear plots in the old village core to larger open-plan lawns on the post-war and modern estates off Forge Road and Stamford Street. We offer very fast scheduling for Ratby clients, with fixed pricing, full insurance, and a complimentary AI design preview.",
    },
    {
        "file": "landscaping-syston.html",
        "title": "Landscaping Syston Leicestershire LE7 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Syston LE7. Patios, artificial grass, composite decking & garden makeovers in this north Leicester town on the River Wreake. Charnwood Borough. Free instant quote, fully insured.",
        "h1": "Landscaping in Syston, Leicestershire LE7",
        "hero_sub": "Syston is a substantial market town in the LE7 postcode, governed by Charnwood Borough Council, 6 miles north of Leicester centre along the A607. The town sits in the Wreake valley where alluvial soils and river terrace gravels dominate — a geology that offers better natural drainage than pure Mercia Mudstone but can produce variable ground conditions on older plots near the River Wreake itself. Syston has grown rapidly in recent decades, with a mix of Victorian terraces in the centre, 1970s–1990s semis, and newer family housing east of Barkby Road. We cover all these property types for patios, artificial lawns, decking, and driveways, with fixed pricing and full insurance throughout.",
    },
    {
        "file": "landscaping-thurmaston.html",
        "title": "Landscaping Thurmaston Leicestershire LE4 | Patios, Artificial Grass & Garden Design | Premium Landscapes",
        "meta_desc": "Landscaping in Thurmaston LE4. Patios, artificial grass, composite decking & garden makeovers on the River Soar floodplain north of Leicester. Free instant quote, fully insured.",
        "h1": "Landscaping in Thurmaston, Leicestershire LE4",
        "hero_sub": "Thurmaston is a large village in the LE4 postcode bordering Birstall to the north and Leicester's Hamilton district to the south, governed by Charnwood Borough Council. The settlement sits on the eastern bank of the River Soar on alluvial soils and river terrace gravels, meaning drainage can be a live consideration on lower-lying plots — we specify appropriate sub-base depths accordingly. The housing mix is typical of a 20th-century Leicester suburb: post-war terraces and semis, 1970s estates along Melton Road, and a growing number of modern homes near Thurmaston Retail Park. We frequently work here given our 7-mile proximity, offering fixed-price patios, artificial grass, decking and full garden redesigns.",
    },
]

# ---------------------------------------------------------------------------
# Patterns to find and replace
# ---------------------------------------------------------------------------

TITLE_PATTERN = re.compile(r'<title>.*?</title>', re.DOTALL)
META_DESC_PATTERN = re.compile(
    r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']*?)(["\']>)',
    re.IGNORECASE
)
H1_PATTERN = re.compile(
    r'(<h1[^>]*>)\s*Landscaping in [^<]+?\s*(</h1>)',
    re.IGNORECASE | re.DOTALL
)
HERO_SUB_PATTERN = re.compile(
    r'(<p class="text-xl md:text-2xl mb-4 text-white/90 max-w-3xl mx-auto leading-relaxed">)'
    r'[^<]*?'
    r'(</p>)',
    re.DOTALL
)


def process_page(data: dict) -> str:
    filepath = ROOT / data["file"]
    if not filepath.exists():
        print(f"  SKIP  {data['file']} — not found")
        return "skip"

    html = filepath.read_text(encoding="utf-8")
    original = html

    # 1. Title
    html = TITLE_PATTERN.sub(f'<title>{data["title"]}</title>', html, count=1)

    # 2. Meta description
    html = META_DESC_PATTERN.sub(
        lambda m: m.group(1) + data["meta_desc"] + m.group(3),
        html, count=1
    )

    # 3. H1
    html = H1_PATTERN.sub(
        lambda m: m.group(1) + "\n                " + data["h1"] + "\n            " + m.group(2),
        html, count=1
    )

    # 4. Hero subtitle paragraph
    html = HERO_SUB_PATTERN.sub(
        lambda m: m.group(1) + "\n                " + data["hero_sub"] + "\n            " + m.group(2),
        html, count=1
    )

    if html == original:
        print(f"  WARN  {data['file']} — no changes made (patterns may not have matched)")
        return "warn"

    filepath.write_text(html, encoding="utf-8")
    print(f"  OK    {data['file']}")
    return "ok"


def main():
    ok = warn = skip = 0
    for page in PAGES:
        result = process_page(page)
        if result == "ok":
            ok += 1
        elif result == "warn":
            warn += 1
        else:
            skip += 1

    print(f"\nDone — {ok} updated, {warn} warnings, {skip} skipped")
    if warn or skip:
        sys.exit(1)


if __name__ == "__main__":
    main()
