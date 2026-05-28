#!/usr/bin/env python3
"""Generate 5 area-service combo SEO pages.

Pages:
  /artificial-grass-oadby
  /block-paving-wigston
  /patios-narborough
  /composite-decking-birstall
  /driveways-hinckley

Also:
  * adds each to sitemap.xml + _redirects
  * swaps the matching service card on the corresponding area page
    so that one inbound link points to the new page (instead of the
    generic service hub).
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://www.premium-landscapes.co.uk"

# ---------------------------------------------------------------------------
# Per-page config
# ---------------------------------------------------------------------------
PAGES = {
    "artificial-grass-oadby": {
        "service_h1": "Artificial Grass Installation",
        "service_keyword": "Artificial Grass",
        "service_hub_url": "/artificial-grass",
        "service_hub_label": "Artificial Grass Leicester",
        "area": "Oadby",
        "area_full": "Oadby, Leicestershire",
        "postcode": "LE2",
        "council": "Oadby & Wigston Borough Council",
        "council_url": "https://www.owbc.gov.uk/planning",
        "distance_km": "10",
        "distance_min": "20",
        "direction": "south-east of Leicester city centre",
        "area_page": "/landscaping-oadby",
        "streets": "Stoughton Road, Glen Road, Wigston Road, Harborough Road and the residential streets around The Oval",
        "ground": "predominantly heavy Mercia Mudstone clay with occasional pockets of glacial outwash gravel near the Sence valley — drainage and a deep compacted sub-base are essential under any new turf installation",
        "garden_profile": "1960s–70s detached and semi-detached homes with generous 60–100 ft rear gardens — among the largest plots of any Leicester suburb",
        "hero_emoji": "🌿",
        "hero_sub": "Premium synthetic turf installation across LE2 — child-safe, pet-friendly, all-weather usable and virtually maintenance-free. Laid on a properly compacted, free-draining sub-base by our local Oadby team.",
        "service_intro_p1": "Oadby is a strong fit for artificial grass. The combination of generous 60–100ft suburban gardens, mature trees that create heavy shade and leaf-litter (where real lawn struggles to thrive), and a high proportion of family homes with dogs and young children makes synthetic turf one of the most practical garden surfaces for the area. The LE2 postcode runs from the leafy streets around The Oval down to the busy A6 London Road corridor — we install across the full postcode and into the LE2 neighbourhoods of Knighton and Stoneygate.",
        "service_intro_p2": "Most artificial grass installations in Oadby fall in the 30–80m² range, with the larger plots around Brocks Hill, Cheshire Gate and the Manor House Gardens estate occasionally running 100m²+. We supply premium European-made turf rated for 10+ years' UV stability, with pile heights from 30mm to 40mm depending on whether the priority is family-garden softness or a more lawn-like finish.",
        "cost_intro": "Indicative installed costs for artificial grass in Oadby. All prices include excavation, weed membrane, MOT Type 1 sub-base, sharp sand laying course, premium turf, joining tape, perimeter pinning and waste removal.",
        "cost_headers": ["Garden Size", "Typical Installed Cost"],
        "cost_rows": [
            ["Small lawn (up to 25m²)", "£950 – £1,600"],
            ["Medium lawn (25–60m²)", "£1,600 – £3,300"],
            ["Large lawn (60–120m²)", "£3,300 – £6,500"],
            ["Premium grade upgrade (40mm pile, EU-made)", "+£8 – £12/m²"],
        ],
        "cost_footer": "Pricing is per m² installed and varies with access, base depth and turf grade. Use our free instant quote tool to get an exact figure for your Oadby garden.",
        "spec_h2": "How We Install Artificial Grass in Oadby",
        "spec_paragraphs": [
            "<strong>Excavation and edging.</strong> We excavate 60–80mm of topsoil from the lawn area and install treated timber or steel edging around the perimeter, set just below the finished turf level.",
            "<strong>Sub-base.</strong> A 50mm compacted MOT Type 1 sub-base is laid and whacker-plated. Oadby's clay soil expands and contracts significantly with moisture changes — skimping on the sub-base depth is the most common cause of artificial grass settling unevenly within 2–3 years.",
            "<strong>Laying course and membrane.</strong> A 25mm layer of compacted sharp sand provides the final laying surface, with a weed-suppressing membrane underneath the sub-base on lawns where invasive growth is a concern.",
            "<strong>Turf.</strong> Premium-grade artificial grass is rolled out, allowed to relax for several hours, then trimmed to the edges and pinned. Multiple-roll installations are joined with adhesive-backed seam tape — invisible from above when done correctly.",
            "<strong>Finishing.</strong> The turf is brushed with a kiln-dried sand infill (optional) to lift the pile and add ballast for stability. The completed lawn is usable immediately.",
        ],
        "local_h2": "Artificial Grass in Oadby — Local Considerations",
        "local_paragraphs": [
            "<strong>Shade.</strong> Many Oadby gardens have mature trees, particularly on the older 1930s plots near the village and the established 1960s estates. Artificial grass is one of the few surfaces that looks the same under deep shade as it does in full sun — a major advantage where real lawn would thin or moss-over.",
            "<strong>Drainage.</strong> All our artificial grass installations drain through the backing at 40+ litres per m² per minute, with the sub-base sloped 1:80 to maintain surface flow. In the lower-lying streets towards the A6 corridor where clay is heaviest, we may specify a deeper sub-base or French drain edging.",
            "<strong>Conservation area note.</strong> The Oadby Village Conservation Area covers the old village core near Church Road. Artificial grass in rear gardens is permitted development and does not need conservation consent — but front-garden installations in the conservation area can have restrictions. We check before quoting.",
        ],
        "faqs": [
            ("Do I need planning permission for artificial grass in Oadby?",
             "No. Replacing a natural lawn with artificial grass in your rear or front garden is permitted development and needs no planning permission. The only exception is front-garden hard surfacing over 5m² that prevents drainage to ground — but artificial grass drains freely through its backing, so this is not a concern in practice. Oadby Village Conservation Area properties should check before installing in a visible front garden."),
            ("How long does artificial grass installation take in Oadby?",
             "Most lawns in Oadby are installed in 1–2 days. A 50m² garden is typically done in a single day; larger installations of 80m²+ may take two days, particularly if access is restricted (some Oadby properties have narrow side gates that require wheelbarrowing material in)."),
            ("What does artificial grass cost in Oadby?",
             "Typical installed costs in Oadby run from approximately £35/m² for standard-grade turf with a basic sub-base, up to £60/m² for premium European-made 40mm turf with a deeper sub-base specification. A typical 50m² Oadby back lawn costs in the region of £1,800–£3,000 fully installed."),
            ("Will artificial grass cope with Oadby's clay drainage?",
             "Yes — when installed correctly. Our installations use a 50–75mm compacted MOT Type 1 sub-base laid to a fall, with sharp sand as the final laying course. This drains significantly better than the surrounding clay subsoil. On the heaviest clay plots we may specify additional French drain edging at perimeter to handle surface run-off."),
            ("Do you cover all of LE2 / Oadby?",
             "Yes — we cover the entire LE2 postcode area including Oadby village, The Oval, Cheshire Gate, Manor House Gardens, Brocks Hill, and along Stoughton Road, Glen Road, Wigston Road and the A6 London Road corridor. Oadby is 10km from our Kirby Muxloe base — a regular service area with no travel surcharge."),
        ],
        # Used for the cross-link patch on the area page:
        "area_page_card_text": "Artificial Grass Oadby",
    },
    "block-paving-wigston": {
        "service_h1": "Block Paving Driveway Installation",
        "service_keyword": "Block Paving",
        "service_hub_url": "/block-paving-driveways-leicester",
        "service_hub_label": "Block Paving Driveways Leicester",
        "area": "Wigston",
        "area_full": "Wigston, Leicestershire",
        "postcode": "LE18",
        "council": "Oadby & Wigston Borough Council",
        "council_url": "https://www.owbc.gov.uk/planning",
        "distance_km": "9",
        "distance_min": "20",
        "direction": "south of Leicester city centre",
        "area_page": "/landscaping-wigston",
        "streets": "Bull Head Street, Aylestone Lane, Welford Road, Leicester Road, Long Street, Bushloe End and Blaby Road",
        "ground": "Mercia Mudstone clay with pockets of alluvium near the Sence Brook valley — block paving needs a properly engineered sub-base on this ground to avoid sinking, rutting or rocking blocks within a few years",
        "garden_profile": "1930s–1960s semi-detached and post-war detached housing with front driveways typically 25–50m² and side-access service strips",
        "hero_emoji": "🧱",
        "hero_sub": "Block paving driveway installation across LE18 — fully SuDS-compliant where required, laid on a proper engineered sub-base for Wigston's clay ground, by experienced local installers.",
        "service_intro_p1": "Block paving remains the most popular driveway surface across Wigston, and for good reason — it's durable, repairable, visually flexible and (when laid correctly) lasts 20+ years with minimal maintenance. Wigston's LE18 postcode runs from the Sence Brook valley in the west to the boundary with Oadby in the east, and almost every street has at least some block-paved frontages from the past two decades.",
        "service_intro_p2": "Most block paving installations we deliver in Wigston are 25–50m² front driveways replacing aged tarmac or worn-out block paving from the 1990s. Larger combined driveway-and-front-garden projects of 60–80m² are common on the post-war detached properties along Bull Head Street and Welford Road. We also install rear block-paved courtyards, paths and parking aprons.",
        "cost_intro": "Indicative installed costs for block paving driveways in Wigston. All prices include excavation, full SuDS-compliant sub-base, MOT Type 1, sharp sand laying course, premium blocks, edge restraints, kiln-dried sand jointing and waste removal.",
        "cost_headers": ["Driveway Size", "Typical Installed Cost"],
        "cost_rows": [
            ["Small driveway (up to 25m²)", "£2,500 – £4,200"],
            ["Medium driveway (25–50m²)", "£4,200 – £8,000"],
            ["Large driveway (50–80m²)", "£8,000 – £12,000"],
            ["Premium block upgrade (Marshalls Drivesett / Tobermore)", "+£12 – £20/m²"],
        ],
        "cost_footer": "Pricing varies with block grade (standard concrete vs premium textured), edging type and any drainage works. SuDS-compliant permeable installation is included by default where surface area exceeds the 5m² front-garden threshold.",
        "spec_h2": "How We Install Block Paving in Wigston",
        "spec_paragraphs": [
            "<strong>Excavation.</strong> We excavate to a minimum 250mm depth for residential driveways — deeper on the heaviest clay plots towards Aylestone Lane and the Sence Brook side. Existing surfaces and topsoil are removed and disposed of off-site.",
            "<strong>Sub-base.</strong> A 150mm compacted MOT Type 1 sub-base is whacker-plated in 75mm layers. This is the single most important stage of a driveway — a weak sub-base on Wigston's clay subsoil will rut and settle within 2–3 years regardless of how good the blocks are.",
            "<strong>SuDS compliance.</strong> Any front driveway over 5m² that replaces a permeable surface (grass, gravel) must either be permeably constructed or drain to a soakaway under the SuDS regulations (Schedule 3, Flood and Water Management Act). We install with permeable paving sub-base and jointing as standard where this applies.",
            "<strong>Edge restraints.</strong> A 100mm × 150mm concrete haunching is laid against the perimeter edge course. Without proper edge restraint, blocks spread sideways under vehicle loading and the whole driveway becomes loose within a few years.",
            "<strong>Laying course and blocks.</strong> A 50mm sharp sand laying course is screeded level. Blocks are laid to the chosen pattern (90°/45° herringbone or stretcher bond most common), cut with a guillotine or block-saw at edges, then whacker-plated to settle.",
            "<strong>Jointing.</strong> Kiln-dried sand is brushed and vibrated into all joints. The completed driveway is fully usable for vehicles within 24 hours.",
        ],
        "local_h2": "Block Paving in Wigston — Local Considerations",
        "local_paragraphs": [
            "<strong>Clay-soil specification.</strong> Wigston's predominantly clay ground means driveway failure (sinking, rutting, edge spread) is almost always traceable to inadequate sub-base depth or missing edge restraint. We do not cut corners on either — all our block-paving installations carry a 10-year workmanship guarantee on the base.",
            "<strong>SuDS rules in practice.</strong> Wigston's older properties often have shallow front gardens that were originally laid to grass. Replacing this with a hard driveway over 5m² triggers SuDS compliance: we install with permeable jointing and a free-draining sub-base, which discharges run-off into the ground beneath the driveway rather than to the public sewer.",
            "<strong>Dropped kerb and access.</strong> If the driveway requires a new dropped kerb, the work itself is the responsibility of Leicestershire County Council Highways (we can advise on the application). For the driveway construction we work right up to the highway boundary; the kerb modification is then booked separately with the council.",
        ],
        "faqs": [
            ("Do I need planning permission for a block paving driveway in Wigston?",
             "Most front driveways under 5m² of new hard surface, or any size installed with permeable construction draining to ground, do not need planning permission under the SuDS rules (Schedule 3 of the Flood and Water Management Act). Non-permeable driveways over 5m² that drain to the highway do need planning consent. We always install SuDS-compliant by default to avoid this — keeps everything within permitted development."),
            ("How long does a block paving driveway take in Wigston?",
             "A typical 30m² front driveway in Wigston takes 4–6 working days from start to finish: 1 day excavation and disposal, 1 day sub-base, 2–3 days laying and cutting blocks, 1 day jointing and finishing. Larger 60m²+ driveways take 7–10 days."),
            ("What does a block paving driveway cost in Wigston?",
             "Typical installed costs in Wigston run from approximately £80/m² for standard concrete blocks on a SuDS-compliant sub-base, up to £140/m² for premium textured blocks (Marshalls Drivesett, Tobermore or similar). A typical 35m² Wigston driveway costs in the region of £2,800–£4,900 fully installed."),
            ("Will the driveway sink on Wigston's clay ground?",
             "Not when installed with proper sub-base depth and edge restraints. The driveway failures we're called in to repair in Wigston almost always trace back to inadequate sub-base (less than 100mm of compacted MOT Type 1) or missing concrete haunching at the edges. Both stages are non-negotiable on our installations."),
            ("Do you cover all of LE18 / Wigston?",
             "Yes — we cover the entire LE18 postcode area including South Wigston, Wigston Magna, Wigston Fields, Little Hill, Glen Parva and the streets around Bull Head Street, Aylestone Lane, Welford Road and Long Street. Wigston is 9km from our Kirby Muxloe base — a core service area with no travel surcharge."),
        ],
        "area_page_card_text": "Driveways Wigston",
    },
    "patios-narborough": {
        "service_h1": "Patio Installation",
        "service_keyword": "Patios",
        "service_hub_url": "/patios",
        "service_hub_label": "Patio Installation Leicester",
        "area": "Narborough",
        "area_full": "Narborough, Leicestershire",
        "postcode": "LE19",
        "council": "Blaby District Council",
        "council_url": "https://www.blaby.gov.uk/business/planning-and-building-control/",
        "distance_km": "6",
        "distance_min": "15",
        "direction": "south-west of Leicester city centre",
        "area_page": "/landscaping-narborough",
        "streets": "Coventry Road, Leicester Road, Desford Road, Mill Lane, Granville Avenue and the Fosse Park-adjacent estates",
        "ground": "river-valley alluvium near the Soar and Sence with Mercia Mudstone underneath — variable drainage depending on plot, with some lower-lying streets needing additional drainage spec",
        "garden_profile": "a mix of mature village properties along Mill Lane and the church area plus modern 1990s–2000s estates around Fosse Park — garden sizes vary widely from 20m² courtyards to 80ft+ rear lawns",
        "hero_emoji": "🪨",
        "hero_sub": "Porcelain, sandstone and natural stone patio installation across LE19 — properly excavated, laid on a compacted sub-base, by an experienced local Narborough team.",
        "service_intro_p1": "Narborough is one of our most-served areas — close to our Kirby Muxloe base, varied housing stock and an active homeowner population investing in their gardens. The LE19 postcode covers the original village core, the modern Whetstone-bordering estates and the residential streets backing onto Fosse Park. We install patios in every part of LE19.",
        "service_intro_p2": "Patios in Narborough span the full range: porcelain (the most popular new choice — zero maintenance, consistent colour, premium look), Indian sandstone (excellent value, traditional appearance), and natural stone including limestone and slate. Project sizes range from 12m² compact rear courtyards on the village terraces to 60m²+ entertaining patios on the larger estate properties.",
        "cost_intro": "Indicative installed costs for patios in Narborough across the main material types. All prices include full excavation, compacted MOT Type 1 sub-base, mortar bed, slab laying, pointing/jointing and waste removal.",
        "cost_headers": ["Material", "Typical Installed Cost"],
        "cost_rows": [
            ["Indian sandstone (mid-grade)", "£80 – £130/m²"],
            ["Porcelain (20mm exterior)", "£110 – £170/m²"],
            ["Limestone", "£100 – £160/m²"],
            ["Natural slate (riven)", "£110 – £170/m²"],
            ["Block paving (clay or concrete)", "£70 – £120/m²"],
        ],
        "cost_footer": "Steps, walls and integrated edging features are quoted separately. Premium-grade or large-format porcelain attracts a small uplift; we will give you exact pricing in the free instant quote.",
        "spec_h2": "How We Install Patios in Narborough",
        "spec_paragraphs": [
            "<strong>Site survey and design.</strong> We measure on-site, confirm levels, identify any drainage requirements and produce a detailed quote including an optional AI visualisation showing how the finished patio will look in your Narborough garden.",
            "<strong>Excavation.</strong> A standard residential patio is excavated to 200–250mm — sometimes deeper on the lower-lying alluvium plots near the Sence Brook where drainage spec needs to be more substantial.",
            "<strong>Sub-base.</strong> 150mm compacted MOT Type 1 hardcore laid in 75mm layers and whacker-plated. This is non-negotiable on every patio we lay regardless of material.",
            "<strong>Mortar bed and laying.</strong> Slabs are laid on a full semi-dry mortar bed (porcelain back-primed with slurry; natural stone laid direct) at the falls required to drain away from the property. Joint widths and patterns are agreed with you at survey stage.",
            "<strong>Pointing.</strong> Flexible jointing compound for porcelain (BS-rated for UK freeze-thaw); semi-dry mortar pointing for natural stone in a colour that complements the material — not generic grey on every job.",
            "<strong>Sealing.</strong> Natural stone is sealed with a penetrating sealer before handover. Porcelain needs no sealing.",
        ],
        "local_h2": "Patios in Narborough — Local Considerations",
        "local_paragraphs": [
            "<strong>Variable ground conditions.</strong> Narborough sits in a river valley — the older village core near the church is on slightly elevated ground with reasonable drainage, but the streets towards the Sence Brook and the modern estates near Fosse Meadows can sit on heavier alluvium with poor natural drainage. We always factor this into the sub-base spec.",
            "<strong>Compact terraced gardens vs estate gardens.</strong> The old village properties around Mill Lane often have small, enclosed rear gardens where 20m²–30m² 'paved courtyard' designs work best — porcelain is particularly popular here because the consistent slab colour reads as a deliberate design choice rather than a cost compromise. The modern estate properties typically have 40–80m²+ patios with integrated steps, walls and lighting.",
            "<strong>Blaby District Council planning.</strong> Narborough falls under Blaby District Council. Residential patios at ground level are permitted development and need no consent. Anything raised above ground level by more than 300mm, or work in the small conservation areas (around the historic church and millpond), can need consent — we check at survey stage.",
        ],
        "faqs": [
            ("Do I need planning permission for a patio in Narborough?",
             "No, in almost all cases. A residential patio laid at or near ground level is permitted development under planning rules. The exceptions are raised patios above 300mm, work in Narborough's small conservation areas (around the church and historic mill area), or work on listed buildings. Blaby District Council is the planning authority for Narborough — we handle any necessary applications as part of the quote."),
            ("How long does a patio installation take in Narborough?",
             "A typical 25m² patio in Narborough takes 4–6 working days: 1 day excavation, 1 day sub-base, 2 days slab laying and cutting, 1 day pointing and finishing. Larger 50m²+ patios with steps or walls take 8–10 days."),
            ("What does a patio cost in Narborough?",
             "Indicative installed prices in Narborough run from approximately £80/m² for Indian sandstone up to £170/m² for premium porcelain. A typical 30m² Narborough patio in mid-grade Indian sandstone costs £2,400–£3,900; the same size in 20mm exterior porcelain costs £3,300–£5,100."),
            ("What's the best patio material for Narborough?",
             "It depends on the property and what matters to you. Porcelain is the leading choice for new patios in Narborough — zero maintenance, no sealing, frost-proof, consistent colour. Indian sandstone is the value choice and suits the older village properties beautifully. Natural slate suits modern, contemporary gardens. We'll bring samples to the site survey so you can compare in your own garden lighting."),
            ("Do you cover all of LE19 / Narborough?",
             "Yes — we cover the entire LE19 postcode area including Narborough village, the streets around Fosse Park, the Mill Lane and church area, and the modern estates on the Whetstone borders. Narborough is 6km from our Kirby Muxloe base — one of our closest service areas with no travel surcharge and quick site visits."),
        ],
        "area_page_card_text": "Patio Installation Narborough",
    },
    "composite-decking-birstall": {
        "service_h1": "Composite Decking Installation",
        "service_keyword": "Composite Decking",
        "service_hub_url": "/composite-decking",
        "service_hub_label": "Composite Decking Leicester",
        "area": "Birstall",
        "area_full": "Birstall, Leicestershire",
        "postcode": "LE4",
        "council": "Charnwood Borough Council",
        "council_url": "https://www.charnwood.gov.uk/pages/planning",
        "distance_km": "11",
        "distance_min": "20",
        "direction": "north of Leicester city centre",
        "area_page": "/landscaping-birstall",
        "streets": "Sibson Road, Birstall Road, Wanlip Lane, Bradgate Lane, Riverside and the streets backing onto Watermead Country Park",
        "ground": "Mercia Mudstone clay across most of Birstall with River Soar alluvium near Watermead — properties on the western edge can be moisture-prone, so subframe ventilation is important on decking installations here",
        "garden_profile": "a mix of established 1960s–80s detached and semi-detached properties along Sibson Road and the older village core, plus modern executive estates around Riverside and Hallam Way",
        "hero_emoji": "🪵",
        "hero_sub": "Premium composite decking installation across LE4 — Millboard, Trex and other leading composite brands, on a properly ventilated subframe, by our experienced Birstall team.",
        "service_intro_p1": "Birstall is excellent territory for composite decking. The village is full of established 1960s–80s properties with garden patios at slightly elevated levels relative to the lawn (often there's a step or two down) — exactly the situation where composite decking outperforms a paved patio. The modern Riverside estates have the kind of contemporary architecture that pairs naturally with composite's clean lines and the popular grey or stone-effect board colours.",
        "service_intro_p2": "Most composite decking projects we install in Birstall are in the 15–40m² range, often combined with a raised step-down to a lawn, integrated planters or seat-walls, and recessed LED riser lighting. We install only premium composite brands (Millboard, Trex, Cladco and similar) on treated timber or aluminium subframes — never the cheaper end of the composite market, which fades, expands inconsistently and looks dated within a few years.",
        "cost_intro": "Indicative installed costs for composite decking in Birstall. All prices include site preparation, subframe (treated timber or aluminium), composite boards, hidden clips, fascia boards, perimeter trim and waste removal.",
        "cost_headers": ["Deck Size", "Typical Installed Cost"],
        "cost_rows": [
            ["Small deck (up to 15m²)", "£2,700 – £4,500"],
            ["Medium deck (15–30m²)", "£4,500 – £8,500"],
            ["Large deck (30–60m²)", "£8,500 – £16,000"],
            ["Premium board upgrade (Millboard / aluminium subframe)", "+£25 – £60/m²"],
            ["Integrated lighting / planters / balustrade", "Quoted separately"],
        ],
        "cost_footer": "Costs vary significantly with board brand (Millboard is at the premium end, Cladco and Composite Prime mid-range), subframe material and the complexity of integrated features. The free instant quote tool gives you a tailored figure for your Birstall garden.",
        "spec_h2": "How We Install Composite Decking in Birstall",
        "spec_paragraphs": [
            "<strong>Subframe.</strong> We build a fully engineered subframe in treated C24 timber (the standard for residential decking) or aluminium (for premium projects or where ground moisture is a concern, such as near Watermead). Joist centres are 300mm for composite — narrower than timber decking — to support the boards correctly and prevent flex.",
            "<strong>Ventilation.</strong> Composite decking needs free airflow underneath the boards to prevent moisture build-up and warping. We design the subframe with at least 100mm clearance from ground level and ensure ventilation gaps around any perimeter walls or enclosed planters.",
            "<strong>Foundations.</strong> Concrete pads or screw piles at every subframe support point. The Birstall clay ground is moisture-active and a properly founded subframe is essential — surface-laid bearers will move within a couple of seasons.",
            "<strong>Boards and fixings.</strong> Composite boards are fixed with hidden stainless steel clips (no visible screws on the deck surface). Boards are laid to the manufacturer's specified expansion gap with end-cuts sealed against moisture ingress.",
            "<strong>Finishing.</strong> Matching fascia and trim to all visible edges and steps. Optional integrated low-voltage LED lighting in risers and perimeter — supplied and installed by us where required.",
        ],
        "local_h2": "Composite Decking in Birstall — Local Considerations",
        "local_paragraphs": [
            "<strong>Moisture and the River Soar.</strong> Properties on the western side of Birstall — particularly the streets backing onto Watermead Country Park and the river floodplain — sit on alluvium with higher natural ground moisture than the rest of the village. Composite is well suited to this (won't rot like timber), but the subframe needs proper ventilation and ground clearance: surface-laid timber bearers are a no-go on this ground.",
            "<strong>Permitted development.</strong> Decking under 300mm above ground level and covering less than 50% of the rear garden is permitted development across England — no planning permission needed. Anything raised more than 300mm, or covering more than half the garden, needs planning consent from Charnwood Borough Council. We check at survey and handle the application if required.",
            "<strong>Brand choices in Birstall.</strong> The most-installed brands in Birstall are Millboard (premium, moulded from real timber, virtually indistinguishable from oak or weathered timber) and Trex (good mid-range with excellent UV warranty). The cheaper imported composites have a notably shorter realistic lifespan and we don't fit them.",
        ],
        "faqs": [
            ("Do I need planning permission for composite decking in Birstall?",
             "Composite decking is permitted development under planning rules — no planning permission needed — provided it's no more than 300mm above existing ground level and covers no more than 50% of the rear garden. Higher or larger decks need consent from Charnwood Borough Council; we handle the application as part of the project where required."),
            ("How long does composite decking take to install in Birstall?",
             "A typical 20m² composite deck in Birstall takes 4–6 working days: 1 day subframe foundations, 1–2 days subframe build, 2 days board installation, 1 day fascia, steps and finishing. Larger decks with integrated lighting, balustrade or steps take 7–10 days."),
            ("What does composite decking cost in Birstall?",
             "Typical installed costs in Birstall run from approximately £180/m² for good mid-range composite (Cladco, Composite Prime) up to £280/m² or more for premium Millboard. A typical 20m² Birstall composite deck costs in the region of £3,600–£5,600 fully installed."),
            ("How long does composite decking actually last?",
             "Premium composite (Millboard, Trex) carries 25–30 year manufacturer warranties on the boards themselves and is realistically expected to outlast that. Our subframes carry a separate 10-year workmanship guarantee. Mid-range composite typically warrantied 20–25 years. The cheap composites at the bottom of the market often start fading and expanding within 5 years — which is why we don't fit them."),
            ("Do you cover all of LE4 / Birstall?",
             "Yes — we cover the entire LE4 postcode covering Birstall including Sibson Road, Birstall Road, Wanlip Lane, the Riverside estate and the streets backing onto Watermead. Birstall is 11km from our Kirby Muxloe base — a core service area with no travel surcharge."),
        ],
        "area_page_card_text": "Composite Decking Birstall",
    },
    "driveways-hinckley": {
        "service_h1": "Driveway Installation",
        "service_keyword": "Driveways",
        "service_hub_url": "/driveways",
        "service_hub_label": "Driveways Leicester",
        "area": "Hinckley",
        "area_full": "Hinckley, Leicestershire",
        "postcode": "LE10",
        "council": "Hinckley & Bosworth Borough Council",
        "council_url": "https://www.hinckley-bosworth.gov.uk/planning",
        "distance_km": "18",
        "distance_min": "30",
        "direction": "west of Leicester city, just off the M69",
        "area_page": "/landscaping-hinckley",
        "streets": "Coventry Road, Rugby Road, Stoke Road, Leicester Road, Trinity Lane, Hollycroft and the Burbage / Barwell-bordering estates",
        "ground": "predominantly Mercia Mudstone over Triassic sandstone — naturally better-draining than central Leicester but still requires a properly engineered driveway sub-base",
        "garden_profile": "1950s–70s suburban detached and semi-detached housing with front driveways typically 30–60m², plus larger Victorian terraces around the town centre with frontages of 20–30m²",
        "hero_emoji": "🚗",
        "hero_sub": "Block paving, resin bound and tarmac driveway installation across LE10 — fully SuDS-compliant, on properly engineered foundations, by experienced Hinckley installers.",
        "service_intro_p1": "Hinckley is one of our regular service areas — just 30 minutes from our Kirby Muxloe base on the M69. The town has a healthy mix of housing stock: established 1950s–70s suburban estates with generous front driveways, larger Victorian and Edwardian terraces around the town centre with smaller frontages, and modern estates on the Burbage and Barwell sides with new-build standard driveways often due for upgrade. Driveways are one of our most-requested services across the LE10 postcode.",
        "service_intro_p2": "We install all three of the main driveway types in Hinckley: block paving (the most popular — durable, repairable, design flexibility), resin bound (clean lines, modern look, fully permeable so SuDS-compliant by default), and tarmac (the value option, particularly for larger driveways and combined driveway-plus-courtyard projects). Typical project sizes in Hinckley range from 25m² front driveways on the terraced streets up to 80m²+ combined frontages on the suburban estates.",
        "cost_intro": "Indicative installed costs for driveways in Hinckley across the three main surface types. All prices include excavation, full SuDS-compliant sub-base, edging, the chosen surface material and waste removal.",
        "cost_headers": ["Driveway Type", "Typical Installed Cost"],
        "cost_rows": [
            ["Tarmac (binder + wearing course)", "£70 – £100/m²"],
            ["Block paving (standard concrete)", "£80 – £120/m²"],
            ["Block paving (premium textured)", "£110 – £160/m²"],
            ["Resin bound (fully permeable)", "£90 – £140/m²"],
            ["Porcelain driveway (heavy-duty 30mm)", "£140 – £200/m²"],
        ],
        "cost_footer": "Dropped kerbs are handled by Leicestershire County Council Highways and quoted separately. The free instant quote tool gives you exact pricing for your specific Hinckley driveway.",
        "spec_h2": "How We Install Driveways in Hinckley",
        "spec_paragraphs": [
            "<strong>Excavation.</strong> Driveway excavation is taken to a minimum 250–300mm — deeper for heavier-duty installations and at the heaviest clay plots. The dig is taken right to the highway boundary where a dropped kerb is in place.",
            "<strong>Sub-base.</strong> 150–200mm of compacted MOT Type 1 in 75mm layers, whacker-plated between layers. The sub-base is the foundation of every driveway — failures (rutting, sinking, edge collapse) almost always trace back to inadequate sub-base depth or compaction.",
            "<strong>SuDS compliance.</strong> Any new front driveway over 5m² that replaces a permeable surface must be SuDS-compliant under Schedule 3 of the Flood and Water Management Act. Resin bound is permeable by construction. Block paving is installed with permeable jointing and a free-draining sub-base. Tarmac driveways are either drained to a soakaway on the property or installed with a permeable border channel.",
            "<strong>Edging and finishing.</strong> Concrete-haunched edging to all perimeter edges, with smooth transitions to the highway, to any garage threshold and to any planted borders. Final surfaces are laid as per material type: tarmac in 2 layers, blocks in the agreed pattern, resin trowel-finished over the permeable base.",
        ],
        "local_h2": "Driveways in Hinckley — Local Considerations",
        "local_paragraphs": [
            "<strong>Variable ground.</strong> Hinckley's ground conditions vary across the town — the western edges over Triassic sandstone drain reasonably well, while the streets towards Barwell and Earl Shilton sit on heavier clay where deeper sub-bases are essential. We adjust spec by site, not by template.",
            "<strong>Driveway choice by property style.</strong> The Victorian and Edwardian terraces around Castle Street and Regent Street tend to suit traditional block paving or sympathetic resin-bound finishes — tarmac usually looks wrong here. The post-war suburban estates around Hollycroft and Trinity Lane work well with all three surface types depending on aesthetic preference. The newer Burbage-bordering estates often suit large-format porcelain or modern resin.",
            "<strong>Dropped kerbs in Hinckley.</strong> If your driveway needs a new dropped kerb, you must apply to Leicestershire County Council Highways before installation. We can advise on the application and time the driveway construction to follow the highway works. The fee for a residential dropped kerb is typically £200–£300 depending on width.",
        ],
        "faqs": [
            ("Do I need planning permission for a new driveway in Hinckley?",
             "Most residential driveways do not need planning permission provided they are SuDS-compliant (permeable construction, or draining to ground rather than to the public sewer). Non-permeable driveways over 5m² that drain to the highway do need consent — we avoid this by installing SuDS-compliant by default. Hinckley & Bosworth Borough Council is the planning authority for any case that does require consent."),
            ("How long does a driveway take to install in Hinckley?",
             "A typical 40m² front driveway in Hinckley takes 5–8 working days depending on surface type: tarmac is the quickest (3–5 days total once sub-base is in), block paving the longest (6–8 days for laying and jointing), resin bound in between."),
            ("What does a driveway cost in Hinckley?",
             "Indicative installed prices in Hinckley run from approximately £70/m² for tarmac up to £200/m² for heavy-duty porcelain. A typical 40m² Hinckley front driveway in standard block paving costs £3,200–£4,800; in resin bound, £3,600–£5,600; in tarmac, £2,800–£4,000."),
            ("Which driveway surface lasts longest?",
             "Properly installed block paving and porcelain are essentially permanent (40+ years) provided the sub-base is correct and edge restraints are in place. Resin bound has a realistic 15–25 year lifespan before re-resining may be needed. Tarmac typically 12–20 years before resurfacing. All carry our 10-year workmanship guarantee on the base regardless of surface choice."),
            ("Do you cover all of LE10 / Hinckley?",
             "Yes — we cover the entire LE10 postcode area including Hinckley town centre, Hollycroft, Trinity, Burbage, Earl Shilton borders, and the streets around Coventry Road, Rugby Road and Leicester Road. Hinckley is 18km from our Kirby Muxloe base, about 30 minutes via the M69 — a regular service area with no travel surcharge."),
        ],
        "area_page_card_text": "Driveways Hinckley",
    },
}

# ---------------------------------------------------------------------------
# Template helpers
# ---------------------------------------------------------------------------
def faq_jsonld(faqs):
    return json.dumps([
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ], ensure_ascii=False, indent=2)

def faq_accordion(faqs):
    out = []
    for q, a in faqs:
        out.append(f'''            <div class="faq-item border-b border-gray-200 py-5">
                <button class="w-full text-left flex justify-between items-center font-semibold text-gray-900 text-lg" onclick="this.nextElementSibling.classList.toggle('hidden');this.querySelector('i').classList.toggle('fa-chevron-down');this.querySelector('i').classList.toggle('fa-chevron-up')">
                    {q} <i class="fas fa-chevron-down text-blue-600 text-sm ml-4 flex-shrink-0"></i>
                </button>
                <div class="hidden mt-3 text-gray-600 leading-relaxed">{a}</div>
            </div>''')
    return "\n".join(out)

def cost_table(headers, rows):
    head = "".join(f'<th class="px-4 py-3 text-left font-semibold text-gray-900 border-b border-gray-200">{h}</th>' for h in headers)
    body = ""
    for r in rows:
        cells = "".join(f'<td class="px-4 py-3 border-b border-gray-100 text-gray-700">{c}</td>' for c in r)
        body += f"<tr>{cells}</tr>"
    return f'''<div class="overflow-x-auto bg-white rounded-2xl shadow-md border border-gray-100 mb-6">
                <table class="w-full text-sm">
                    <thead class="bg-gray-50"><tr>{head}</tr></thead>
                    <tbody>{body}</tbody>
                </table>
            </div>'''

def prose(paragraphs):
    return "\n".join(f'                <p class="text-gray-700 leading-relaxed mb-4">{p}</p>' for p in paragraphs)

def jsonld_graph(slug, cfg):
    page_url = f"{DOMAIN}/{slug}"
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": f"{page_url}#service",
                "name": f"{cfg['service_h1']} in {cfg['area']}",
                "serviceType": cfg["service_keyword"],
                "provider": {
                    "@type": "LocalBusiness",
                    "name": "Premium Landscapes",
                    "telephone": "+447877934782",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "44 Barwell Road",
                        "addressLocality": "Kirby Muxloe",
                        "addressRegion": "Leicestershire",
                        "postalCode": "LE9 2AA",
                        "addressCountry": "GB"
                    }
                },
                "areaServed": {
                    "@type": "Place",
                    "name": cfg["area"],
                    "containedInPlace": {"@type": "Place", "name": "Leicestershire"}
                },
                "url": page_url
            },
            {
                "@type": "FAQPage",
                "@id": f"{page_url}#faq",
                "mainEntity": [
                    {"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in cfg["faqs"]
                ]
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{page_url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
                    {"@type": "ListItem", "position": 2, "name": cfg["service_hub_label"],
                     "item": f"{DOMAIN}{cfg['service_hub_url']}"},
                    {"@type": "ListItem", "position": 3,
                     "name": f"{cfg['service_keyword']} {cfg['area']}",
                     "item": page_url}
                ]
            }
        ]
    }, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# Master page template
# ---------------------------------------------------------------------------
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-56L62ZWF');</script>
<!-- End Google Tag Manager -->

    <!-- Facebook Pixel Code -->
    <script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');window.__plFireFbPixel=function(){{if(window.__plFbFired)return;window.__plFbFired=true;fbq('init','1480425153686683');fbq('track','PageView');}};try{{if(localStorage.getItem('pl_cookie_consent')==='accepted')window.__plFireFbPixel();}}catch(e){{}}</script>
    <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=1480425153686683&ev=PageView&noscript=1"/></noscript>
    <!-- End Facebook Pixel Code -->
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9PGX32QB99"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{
    ad_storage: 'denied', analytics_storage: 'denied',
    ad_user_data: 'denied', ad_personalization: 'denied',
    wait_for_update: 500
  }});
  gtag('js', new Date());
  gtag('config', 'G-9PGX32QB99');
</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="images/logo.png">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:image" content="https://premium-landscapes.co.uk/images/social/{slug}.jpg">
    <meta property="og:image:secure_url" content="https://premium-landscapes.co.uk/images/social/{slug}.jpg">
    <meta property="og:image:alt" content="{service_h1} in {area} by Premium Landscapes">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{og_title}">
    <meta name="twitter:description" content="{meta_desc}">
    <meta name="twitter:image" content="https://premium-landscapes.co.uk/images/social/{slug}.jpg">
    <meta name="twitter:image:alt" content="{service_h1} in {area} by Premium Landscapes">

    <script type="application/ld+json">
{jsonld}
    </script>

    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>
    <script src="scripts/tailwind.js"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '#2563eb',
                        'primary-dark': '#1d4ed8',
                        accent: '#8b5cf6',
                    }},
                    fontFamily: {{ heading: ['Inter', 'sans-serif'] }}
                }}
            }}
        }}
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Open Sans', sans-serif; }}
        h1, h2, h3, h4 {{ font-family: 'Inter', sans-serif; }}
        .hero-gradient {{
            background: linear-gradient(135deg, rgba(37,99,235,0.92) 0%, rgba(139,92,246,0.85) 100%),
                        url('images/hero-garden.webp') center/cover no-repeat;
        }}
        .mobile-menu {{ transition: transform 0.3s ease; }}
        .mobile-menu.active {{ transform: translateX(0) !important; -webkit-transform: translateX(0) !important; }}
    </style>
    <script src="scripts/config.js"></script>
    <link rel="stylesheet" href="styles/mobile.css">
    <link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml">
</head>
<body class="bg-white text-gray-800">
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-56L62ZWF" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <!-- Navigation -->
    <header class="bg-white shadow-sm fixed w-full top-0 z-50" style="-webkit-transform: translateZ(0); transform: translateZ(0);">
        <nav class="container mx-auto px-4 py-0 flex items-center justify-between">
            <a href="/" class="flex items-center"><img src="images/logo.png" alt="Premium Landscapes" class="h-20 md:h-28"></a>
            <div class="hidden md:flex items-center space-x-8">
                <a href="about" class="text-gray-700 hover:text-primary transition">About</a>
                <a href="services" class="text-gray-700 hover:text-primary transition">Landscaping Services Leicester</a>
                <a href="gallery" class="text-gray-700 hover:text-primary transition">Garden Transformation Gallery</a>
                <a href="blog" class="text-gray-700 hover:text-primary transition">Blog</a>
                <a href="quote" class="text-gray-700 hover:text-primary transition flex items-center">Instant Quote &amp; Design <span class="ml-1.5 bg-green-500 text-white text-xs font-bold px-1.5 py-0.5 rounded-full">FREE</span></a>
                <a href="contact" class="text-white bg-primary px-6 py-2 rounded-full hover:bg-primary-dark transition">Contact</a>
            </div>
            <button id="mobileMenuBtn" class="md:hidden text-primary text-2xl"><i class="fas fa-bars"></i></button>
        </nav>
    </header>

    <!-- Mobile Menu -->
    <div id="mobileMenu" class="mobile-menu fixed inset-0 bg-white md:hidden z-[100]" style="-webkit-transform: translateX(100%); transform: translateX(100%);">
        <div class="flex flex-col h-full">
            <div class="flex items-center justify-between p-4 border-b border-gray-100">
                <a href="/"><img src="images/logo.png" alt="Premium Landscapes" class="h-12"></a>
                <button id="closeMobileMenu" class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-100 text-gray-600"><i class="fas fa-times text-lg"></i></button>
            </div>
            <div class="flex-1 overflow-y-auto p-6">
                <div class="flex flex-col space-y-1">
                    <a href="/" class="text-gray-700 hover:bg-gray-50 transition text-lg py-3 px-4 rounded-xl mobile-menu-link">Home</a>
                    <a href="quote" class="text-gray-700 hover:bg-gray-50 transition text-lg py-3 px-4 rounded-xl mobile-menu-link flex items-center justify-between">Instant Quote & Design <span class="bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full">FREE</span></a>
                    <a href="about" class="text-gray-700 hover:bg-gray-50 transition text-lg py-3 px-4 rounded-xl mobile-menu-link">About</a>
                    <a href="services" class="text-gray-700 hover:bg-gray-50 transition text-lg py-3 px-4 rounded-xl mobile-menu-link">Landscaping Services Leicester</a>
                    <a href="gallery" class="text-gray-700 hover:bg-gray-50 transition text-lg py-3 px-4 rounded-xl mobile-menu-link">Garden Transformation Gallery</a>
                    <a href="blog" class="text-gray-700 hover:bg-gray-50 transition text-lg py-3 px-4 rounded-xl mobile-menu-link">Blog</a>
                    <a href="contact" class="text-gray-700 hover:bg-gray-50 transition text-lg py-3 px-4 rounded-xl mobile-menu-link">Contact</a>
                </div>
            </div>
            <div class="p-4 border-t border-gray-100">
                <a href="quote" class="block w-full py-4 bg-primary text-white text-center rounded-xl font-semibold text-lg">Get Free Quote <i class="fas fa-arrow-right ml-2"></i></a>
            </div>
        </div>
    </div>

    <!-- Breadcrumb -->
    <div class="bg-gray-50 border-b border-gray-200 pt-24 md:pt-28">
        <div class="container mx-auto px-4 py-3">
            <nav aria-label="Breadcrumb" class="text-sm text-gray-500">
                <ol class="flex flex-wrap items-center gap-2">
                    <li><a href="/" class="hover:text-primary transition">Home</a></li>
                    <li>/</li>
                    <li><a href="{service_hub_url}" class="hover:text-primary transition">{service_hub_label}</a></li>
                    <li>/</li>
                    <li class="text-gray-800 font-medium">{service_keyword} {area}</li>
                </ol>
            </nav>
        </div>
    </div>

    <!-- Hero -->
    <section class="hero-gradient text-white py-20 px-4">
        <div class="max-w-4xl mx-auto text-center">
            <div class="inline-flex items-center bg-white/20 backdrop-blur-sm rounded-full px-4 py-2 mb-6">
                <i class="fas fa-map-marker-alt mr-2 text-yellow-300"></i>
                <span class="text-sm font-medium">Serving {area_full}</span>
            </div>
            <div class="text-5xl mb-4">{hero_emoji}</div>
            <h1 class="font-heading font-bold text-4xl md:text-6xl mb-6 leading-tight drop-shadow-lg">{service_h1} in {area}, Leicestershire</h1>
            <p class="text-xl md:text-2xl mb-6 text-white/90 max-w-3xl mx-auto leading-relaxed">{hero_sub}</p>
            <div class="flex flex-wrap justify-center gap-3 mb-8">
                <span class="bg-white/15 backdrop-blur-sm rounded-full px-4 py-1.5 text-sm">📍 {postcode} postcode</span>
                <span class="bg-white/15 backdrop-blur-sm rounded-full px-4 py-1.5 text-sm">🚐 {distance_min} min from base</span>
                <span class="bg-white/15 backdrop-blur-sm rounded-full px-4 py-1.5 text-sm">✅ No travel charge</span>
            </div>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="quote" class="bg-white text-primary font-bold px-8 py-4 rounded-full text-lg hover:bg-blue-50 transition shadow-lg">
                    <i class="fas fa-bolt mr-2 text-yellow-500"></i> Get Free Instant Quote
                </a>
                <a href="tel:+447877934782" class="border-2 border-white text-white font-bold px-8 py-4 rounded-full text-lg hover:bg-white/10 transition">
                    <i class="fas fa-phone mr-2"></i> 07877 934782
                </a>
            </div>
            <span class="inline-block mt-5 bg-green-500 text-white text-sm font-bold px-4 py-1.5 rounded-full">100% FREE quote &amp; AI garden design</span>
        </div>
    </section>

    <!-- Trust signals -->
    <section class="bg-white py-10 border-b border-gray-100">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
                <div><p class="text-3xl font-bold text-primary">15+</p><p class="text-gray-600 text-sm mt-1">Years Experience</p></div>
                <div><p class="text-3xl font-bold text-primary">500+</p><p class="text-gray-600 text-sm mt-1">Projects Completed</p></div>
                <div><p class="text-3xl font-bold text-primary">4.9★</p><p class="text-gray-600 text-sm mt-1">Customer Rated</p></div>
                <div><p class="text-3xl font-bold text-primary">Free</p><p class="text-gray-600 text-sm mt-1">AI Garden Design</p></div>
            </div>
        </div>
    </section>

    <!-- Service intro -->
    <section class="py-16 px-4 bg-white">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold mb-6">{service_h1} Across {area} {postcode}</h2>
            <p class="text-gray-700 leading-relaxed mb-4">{service_intro_p1}</p>
            <p class="text-gray-700 leading-relaxed mb-4">{service_intro_p2}</p>
        </div>
    </section>

    <!-- Cost section -->
    <section class="py-16 px-4 bg-gray-50">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold mb-4">{service_keyword} Costs in {area}</h2>
            <p class="text-gray-700 mb-6">{cost_intro}</p>
            {cost_table_html}
            <p class="text-gray-600 text-sm italic">{cost_footer}</p>
            <div class="mt-8 text-center">
                <a href="quote" class="inline-flex items-center gap-2 bg-primary text-white px-8 py-4 rounded-full font-bold hover:bg-primary-dark transition shadow-md">
                    <i class="fas fa-bolt text-yellow-300"></i> Get My Exact {area} Quote
                </a>
            </div>
        </div>
    </section>

    <!-- Spec / process -->
    <section class="py-16 px-4 bg-white">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold mb-6">{spec_h2}</h2>
{spec_prose}
        </div>
    </section>

    <!-- Local considerations -->
    <section class="py-16 px-4 bg-gray-50">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold mb-6">{local_h2}</h2>
{local_prose}
        </div>
    </section>

    <!-- Why choose us -->
    <section class="py-16 px-4 bg-white">
        <div class="max-w-5xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold text-center mb-12">Why {area} Homeowners Choose Premium Landscapes</h2>
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="p-6 bg-blue-50 rounded-2xl">
                    <div class="w-12 h-12 bg-primary rounded-full flex items-center justify-center mb-3"><i class="fas fa-bolt text-white"></i></div>
                    <h3 class="font-bold text-lg mb-2">Instant Quotes</h3>
                    <p class="text-gray-600 text-sm">Get an accurate, itemised price in minutes — not days.</p>
                </div>
                <div class="p-6 bg-purple-50 rounded-2xl">
                    <div class="w-12 h-12 bg-accent rounded-full flex items-center justify-center mb-3"><i class="fas fa-image text-white"></i></div>
                    <h3 class="font-bold text-lg mb-2">Free AI Design</h3>
                    <p class="text-gray-600 text-sm">See your finished garden before we start.</p>
                </div>
                <div class="p-6 bg-green-50 rounded-2xl">
                    <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mb-3"><i class="fas fa-map-marker-alt text-white"></i></div>
                    <h3 class="font-bold text-lg mb-2">Local to {area}</h3>
                    <p class="text-gray-600 text-sm">{distance_min} minutes from our Kirby Muxloe base — no travel charge.</p>
                </div>
                <div class="p-6 bg-amber-50 rounded-2xl">
                    <div class="w-12 h-12 bg-amber-500 rounded-full flex items-center justify-center mb-3"><i class="fas fa-shield-alt text-white"></i></div>
                    <h3 class="font-bold text-lg mb-2">Fully Insured</h3>
                    <p class="text-gray-600 text-sm">All work fully insured with 10-year workmanship guarantee.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- FAQs -->
    <section class="py-16 px-4 bg-gray-50">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold text-center mb-12">{service_keyword} {area} — Frequently Asked Questions</h2>
{faq_accordion_html}
        </div>
    </section>

    <!-- Related services + areas -->
    <section class="py-12 px-4 bg-white">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-2xl font-bold text-center mb-6">Related Pages</h2>
            <div class="grid md:grid-cols-2 gap-6">
                <div class="p-6 bg-blue-50 rounded-2xl">
                    <h3 class="font-bold text-lg mb-3">More about this service</h3>
                    <div class="flex flex-wrap gap-2">
                        <a href="{service_hub_url}" class="bg-white border border-gray-200 rounded-full px-4 py-2 text-sm font-semibold text-gray-700 hover:border-primary hover:text-primary transition">{service_hub_label}</a>
                        <a href="quote" class="bg-white border border-gray-200 rounded-full px-4 py-2 text-sm font-semibold text-gray-700 hover:border-primary hover:text-primary transition">Get Free Quote</a>
                        <a href="gallery" class="bg-white border border-gray-200 rounded-full px-4 py-2 text-sm font-semibold text-gray-700 hover:border-primary hover:text-primary transition">Project Gallery</a>
                        <a href="case-studies" class="bg-white border border-gray-200 rounded-full px-4 py-2 text-sm font-semibold text-gray-700 hover:border-primary hover:text-primary transition">Case Studies</a>
                    </div>
                </div>
                <div class="p-6 bg-green-50 rounded-2xl">
                    <h3 class="font-bold text-lg mb-3">All services in {area}</h3>
                    <div class="flex flex-wrap gap-2">
                        <a href="{area_page}" class="bg-white border border-gray-200 rounded-full px-4 py-2 text-sm font-semibold text-gray-700 hover:border-primary hover:text-primary transition">Landscaping {area}</a>
                        <a href="areas-we-cover" class="bg-white border border-gray-200 rounded-full px-4 py-2 text-sm font-semibold text-gray-700 hover:border-primary hover:text-primary transition">All Areas We Cover</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="py-20 px-4 bg-gradient-to-br from-primary to-accent text-white text-center">
        <div class="max-w-3xl mx-auto">
            <span class="bg-green-400 text-white text-sm px-3 py-1 rounded-full font-bold mb-4 inline-block">100% FREE</span>
            <h2 class="text-3xl md:text-4xl font-bold mb-4">Ready to Transform Your {area} {service_keyword_singular}?</h2>
            <p class="text-blue-100 text-lg mb-8">Get your free instant quote &amp; AI garden design in under 2 minutes. No obligation.</p>
            <a href="quote" class="bg-white text-primary font-bold px-10 py-5 rounded-full text-lg hover:bg-blue-50 transition inline-block shadow-lg">
                <i class="fas fa-magic mr-2"></i> Get My Free Quote &amp; Design
            </a>
            <p class="mt-4 text-white/70 text-sm">Powered by <strong class="text-white">Trade</strong> <strong class="text-amber-300">Engine</strong> · Delivered by email in minutes</p>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-16 px-4">
        <div class="container mx-auto max-w-6xl">
            <div class="grid md:grid-cols-3 gap-10 mb-10">
                <div>
                    <img src="images/logo.png" alt="Premium Landscapes" class="h-16 mb-4 brightness-0 invert opacity-80">
                    <p class="text-gray-400 text-sm">Premium Landscapes — {service_keyword} specialists in {area}, Leicester &amp; Leicestershire. Free instant quotes and AI garden design — no obligation.</p>
                </div>
                <div>
                    <h4 class="font-bold text-lg mb-4">Services</h4>
                    <ul class="space-y-2 text-gray-400 text-sm">
                        <li><a href="patios" class="hover:text-white transition">Patio Installation Leicester</a></li>
                        <li><a href="artificial-grass" class="hover:text-white transition">Artificial Grass Leicester</a></li>
                        <li><a href="composite-decking" class="hover:text-white transition">Composite Decking Leicester</a></li>
                        <li><a href="driveways" class="hover:text-white transition">Driveways Leicester</a></li>
                        <li><a href="garden-lighting" class="hover:text-white transition">Garden Lighting Leicester</a></li>
                        <li><a href="full-garden-makeover" class="hover:text-white transition">Full Garden Makeover Leicester</a></li>
                        <li><a href="areas-we-cover" class="hover:text-white transition">Areas We Cover</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-bold text-lg mb-4">Contact</h4>
                    <ul class="space-y-2 text-gray-400 text-sm">
                        <li><i class="fas fa-phone mr-2 text-primary"></i> <a href="tel:07877934782" class="hover:text-white transition">07877 934782</a></li>
                        <li><i class="fas fa-envelope mr-2 text-primary"></i> <a href="mailto:premiumlandscapesuk@gmail.com" class="hover:text-white transition">premiumlandscapesuk@gmail.com</a></li>
                        <li><i class="fas fa-map-marker-alt mr-2 text-primary"></i> Serving {area}, Leicestershire</li>
                    </ul>
                    <div class="mt-6"><a href="quote" class="inline-block bg-primary text-white px-6 py-3 rounded-full text-sm font-semibold hover:bg-primary-dark transition">Get Free Quote</a></div>
                </div>
            </div>
            <div class="border-t border-gray-800 pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
                <p class="text-gray-500 text-sm">&copy; 2026 Premium Landscapes. All rights reserved. &nbsp;|&nbsp; <a href="/privacy-policy" class="hover:opacity-100 underline">Privacy Policy</a></p>
                <a href="https://trade-engine.co.uk" target="_blank" class="text-gray-500 text-sm hover:text-gray-300 transition flex items-center gap-1">
                    <i class="fas fa-bolt text-amber-500"></i> Powered by <strong class="text-gray-300">Trade</strong> <strong class="text-amber-500">Engine</strong>
                </a>
            </div>
        </div>
    </footer>

    <script src="scripts/main.js"></script>
    <script src="scripts/cookie-consent.js"></script>
</body>
</html>
'''

# ---------------------------------------------------------------------------
# Build pages
# ---------------------------------------------------------------------------
def build_page(slug, cfg):
    canonical = f"{DOMAIN}/{slug}"
    title = f"{cfg['service_h1']} in {cfg['area']}, Leicester {cfg['postcode']} | Premium Landscapes"
    og_title = f"{cfg['service_keyword']} {cfg['area']} | Premium Landscapes"
    # tailored 150-char meta
    meta_desc = f"{cfg['service_h1']} across {cfg['area']} {cfg['postcode']}. {cfg['service_keyword']} specialists serving {cfg['area_full']}. Free instant quote &amp; AI garden design."
    # singular form for CTA ("Garden" / "Driveway"); fall back to service keyword
    sing_map = {
        "Artificial Grass": "Lawn",
        "Block Paving": "Driveway",
        "Patios": "Patio",
        "Composite Decking": "Deck",
        "Driveways": "Driveway",
    }
    service_keyword_singular = sing_map.get(cfg["service_keyword"], "Garden")

    html = TEMPLATE.format(
        title=title,
        og_title=og_title,
        meta_desc=meta_desc,
        canonical=canonical,
        slug=slug,
        jsonld=jsonld_graph(slug, cfg),
        service_h1=cfg["service_h1"],
        service_keyword=cfg["service_keyword"],
        service_keyword_singular=service_keyword_singular,
        service_hub_url=cfg["service_hub_url"],
        service_hub_label=cfg["service_hub_label"],
        area=cfg["area"],
        area_full=cfg["area_full"],
        postcode=cfg["postcode"],
        distance_min=cfg["distance_min"],
        hero_emoji=cfg["hero_emoji"],
        hero_sub=cfg["hero_sub"],
        service_intro_p1=cfg["service_intro_p1"],
        service_intro_p2=cfg["service_intro_p2"],
        cost_intro=cfg["cost_intro"],
        cost_table_html=cost_table(cfg["cost_headers"], cfg["cost_rows"]),
        cost_footer=cfg["cost_footer"],
        spec_h2=cfg["spec_h2"],
        spec_prose=prose(cfg["spec_paragraphs"]),
        local_h2=cfg["local_h2"],
        local_prose=prose(cfg["local_paragraphs"]),
        faq_accordion_html=faq_accordion(cfg["faqs"]),
        area_page=cfg["area_page"],
    )
    out = ROOT / f"{slug}.html"
    out.write_text(html, encoding="utf-8")
    return out

print("=== Building area×service pages ===")
created = []
for slug, cfg in PAGES.items():
    p = build_page(slug, cfg)
    print(f"  ✅ {p.name} ({p.stat().st_size:,} bytes)")
    created.append(slug)

# ---------------------------------------------------------------------------
# Update sitemap.xml
# ---------------------------------------------------------------------------
print("\n=== Updating sitemap.xml ===")
sitemap_path = ROOT / "sitemap.xml"
sm = sitemap_path.read_text(encoding="utf-8")
new_entries = ""
for slug in created:
    if slug in sm:
        print(f"  · {slug} already in sitemap")
        continue
    new_entries += f'''  <url>
    <loc>{DOMAIN}/{slug}</loc>
    <lastmod>2026-05-28</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
'''
if new_entries:
    sm = sm.replace("</urlset>", new_entries + "</urlset>")
    sitemap_path.write_text(sm, encoding="utf-8")
    print(f"  ✅ added {len(created)} sitemap entries")

# ---------------------------------------------------------------------------
# Update _redirects
# ---------------------------------------------------------------------------
print("\n=== Updating _redirects ===")
red_path = ROOT / "_redirects"
red = red_path.read_text(encoding="utf-8")
new_lines = ""
for slug in created:
    rule = f"/{slug}.html /{slug} 301"
    if rule in red:
        print(f"  · {slug} already has redirect")
        continue
    new_lines += rule + "\n"
if new_lines:
    if not red.endswith("\n"):
        red += "\n"
    red += "\n# Phase F — Area×service combo pages\n" + new_lines
    red_path.write_text(red, encoding="utf-8")
    print(f"  ✅ added {len(created)} redirect rules")

# ---------------------------------------------------------------------------
# Cross-link from matching area page: swap the matching service card href
# ---------------------------------------------------------------------------
print("\n=== Cross-linking from area pages ===")
# Map: area page → (existing card href to swap, new url)
# We swap one specific service-card link on each area page from the generic
# /<service> to the new area-specific /<service>-<area>.
swaps = [
    # (area page, old href pattern, new href, card heading text used to disambiguate)
    ("landscaping-oadby.html",      '/artificial-grass',  '/artificial-grass-oadby',     'Artificial Grass Oadby'),
    ("landscaping-wigston.html",    '/driveways',         '/block-paving-wigston',       'Driveways Wigston'),
    ("landscaping-narborough.html", '/patios',            '/patios-narborough',          'Patio Installation Narborough'),
    ("landscaping-birstall.html",   '/composite-decking', '/composite-decking-birstall', 'Composite Decking Birstall'),
    ("landscaping-hinckley.html",   '/driveways',         '/driveways-hinckley',         'Driveways Hinckley'),
]
for fname, old_href, new_href, card_h3_text in swaps:
    p = ROOT / fname
    if not p.exists():
        print(f"  ⚠️  {fname}: not found, skipping")
        continue
    txt = p.read_text(encoding="utf-8")
    # Find the service card whose H3 link text matches card_h3_text and replace
    # the href in BOTH the image's wrapping link (if any) and the H3 link.
    # Pattern: <a href="OLD" ...>HEADING TEXT</a>
    pattern = re.compile(
        r'(<a href=")' + re.escape(old_href) + r'(" class="hover:text-primary transition">' +
        re.escape(card_h3_text) + r'</a>)'
    )
    new_txt, n = pattern.subn(rf'\g<1>{new_href}\g<2>', txt, count=1)
    if n:
        p.write_text(new_txt, encoding="utf-8")
        print(f"  ✅ {fname}: swapped one card link → {new_href}")
    else:
        print(f"  ⚠️  {fname}: card '{card_h3_text}' not found, no swap")

# ---------------------------------------------------------------------------
# Validate JSON-LD on each new page
# ---------------------------------------------------------------------------
print("\n=== Validate JSON-LD on new pages ===")
for slug in created:
    txt = (ROOT / f"{slug}.html").read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S)
    for i, b in enumerate(blocks, 1):
        try:
            data = json.loads(b)
            types = [n.get("@type") for n in data.get("@graph", [])]
            print(f"  ✅ {slug} block#{i}: {types}")
        except Exception as e:
            print(f"  ❌ {slug} block#{i}: {e}")
