"""
Phase E — Premium Landscapes
============================
1. Rewrites four thin service pages with the full content provided in the
   May 2026 owner brief (fencing, turfing, pergolas, commercial astroturf).
2. Adds the missing "Blog" link to the main desktop navigation across every
   site page that has the standard nav block but is missing Blog.
3. Updates each rewritten page's <head>: title, meta description, OG/Twitter
   tags and the Service + FAQPage + BreadcrumbList JSON-LD so the schema
   matches the new visible FAQs.

Re-runnable. Idempotent for nav insertion (only adds Blog if missing).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# CONTENT DATA — every word taken directly from the owner-supplied brief
# (attached_assets/Pasted-Still-outstanding-Blog-missing-from-main-nav-this-is-th_...)
# ---------------------------------------------------------------------------

PAGES = {
    "fencing-leicester": {
        "title": "Fencing Installation Leicester | Garden & Boundary Fencing | Premium Landscapes",
        "meta_desc": "Professional fencing installation in Leicester. Timber, composite, closeboard and decorative fencing. Free instant quote online. Fully installed, all waste removed.",
        "service_type": "Fencing Installation",
        "h1": "Fencing Installation in Leicester",
        "subheading": "Boundary, Garden and Decorative Fencing — Supplied and Installed",
        "intro_paragraphs": [
            "Whether you need new boundary fencing after a storm, a complete garden enclosure for privacy and security, or decorative fencing to finish a landscaping project, Premium Landscapes installs fencing across Leicester and Leicestershire. We supply and fit all common fencing types — from traditional closeboard and featheredge to contemporary composite panels and decorative metal railings.",
            "Every installation uses properly set concrete posts, the correct post depth for the panel height, and waste removal on the day. No skimped posts, no wobbling panels 12 months later."
        ],
        "sections": [
            {
                "h2": "Fencing Types We Install in Leicester",
                "blocks": [
                    {"h3": "Closeboard / Featheredge Fencing", "p": "The most common timber fencing choice across the UK — overlapping vertical featheredge boards fixed to arris rails, with concrete or timber posts. Fully solid, excellent privacy, and available in standard heights from 900mm to 1.8m. Suitable for all boundary conditions, including exposed gardens where panel fencing would flex and fail."},
                    {"h3": "Timber Panel Fencing", "p": "Standard and decorative timber panels (overlap, waney lap, lattice-top, trellis-top) are widely used across Leicester for garden boundaries and internal dividers. Panel fencing installs quickly and is cost-effective for straightforward straight runs. We set all posts in concrete and include gravel boards as standard to prevent base rot."},
                    {"h3": "Composite Fencing", "p": "Composite fencing panels use a wood-plastic composite material that looks like timber but requires zero maintenance — no painting, no treating, no warping. Colour-stable for 20+ years, resistant to rot, insects and UV. Ideal for homeowners who want the look of wood without the annual upkeep."},
                    {"h3": "Trellis and Decorative Fencing", "p": "Trellis panels on post extensions, painted metal railings, picket fencing and slatted screens for contemporary gardens. Decorative fencing works as a design feature as well as a boundary — particularly for front gardens where you want to define the space without blocking light or views."},
                    {"h3": "Acoustic Fencing", "p": "Heavy-duty close-boarded acoustic fencing is available for properties on busy roads where noise reduction is a priority. These panels use thicker, denser boards and are installed with acoustic-grade posts and rails to provide meaningful noise attenuation."},
                ],
            },
            {
                "h2": "Fencing Costs in Leicester",
                "table": {
                    "headers": ["Fence Type", "Typical Cost Per Metre (Installed)"],
                    "rows": [
                        ["Closeboard / featheredge", "£85 – £130/m"],
                        ["Timber panel", "£75 – £110/m"],
                        ["Composite panel", "£130 – £200/m"],
                        ["Trellis / decorative", "£70 – £120/m"],
                        ["Acoustic fencing", "£150 – £250/m"],
                    ],
                },
                "after_table_paragraphs": [
                    "Prices include posts, concrete, gravel boards (where applicable), full installation and waste removal. Gate fitting is quoted separately.",
                    'Use our <a href="/quote" class="text-primary font-semibold hover:underline">free quote tool</a> for a tailored price based on your specific run length, height and material.'
                ],
            },
            {
                "h2": "What's Included in Our Fencing Installation",
                "intro": "Every fencing job we quote includes:",
                "bullets": [
                    "Post holes dug to the correct depth (minimum 600mm for 1.8m fence)",
                    "Concrete-set posts — no post spikes",
                    "Gravel boards as standard on timber panel and closeboard installations",
                    "Full panel or board fitting",
                    "Capping rails and post caps where specified",
                    "All waste and old fencing removed from site on the day",
                    "Site left clean and tidy",
                ],
                "after_bullets": "We do not subcontract fencing work — the same team that installs your patio or lawn installs your fencing.",
            },
            {
                "h2": "Fencing Replacement in Leicester",
                "paragraphs": [
                    "Storm damage is one of the most common reasons for emergency fencing calls across Leicestershire. We handle full fence replacements — stripping out damaged posts and panels, disposing of all old materials, and installing a full new run with properly set concrete posts.",
                    "If only sections of your fence are damaged, we can match existing materials where possible for a seamless repair. However, for fences over 10 years old, a full replacement is typically better value than a patchwork repair that leaves old posts in weakened ground.",
                    'We cover emergency fencing replacement across <a href="/landscaping-leicester" class="text-primary font-semibold hover:underline">Leicester</a>, <a href="/landscaping-oadby" class="text-primary font-semibold hover:underline">Oadby</a>, <a href="/landscaping-wigston" class="text-primary font-semibold hover:underline">Wigston</a>, <a href="/landscaping-narborough" class="text-primary font-semibold hover:underline">Narborough</a>, <a href="/landscaping-birstall" class="text-primary font-semibold hover:underline">Birstall</a>, <a href="/landscaping-hinckley" class="text-primary font-semibold hover:underline">Hinckley</a>, <a href="/landscaping-loughborough" class="text-primary font-semibold hover:underline">Loughborough</a> and surrounding Leicestershire areas.',
                ],
            },
            {
                "h2": "Fencing and Your Boundaries",
                "paragraphs": [
                    "In England, you're generally responsible for the boundaries marked on your title deeds — these are usually indicated by a \"T\" mark on the boundary. Before installing new fencing, we recommend checking your title plan and confirming boundary ownership with your neighbour where relevant. We install fencing on your side of the agreed boundary line.",
                    "We do not handle boundary disputes, but we're happy to advise on typical arrangements for semi-detached and terraced Leicester properties where boundary responsibility is often shared or unclear.",
                ],
            },
            {
                "h2": "Fencing for New Landscaping Projects",
                "paragraphs": [
                    "If you're having a patio, artificial lawn or full garden redesign installed, new fencing is often part of the same project. Including fencing in the same quote simplifies the job significantly — ground preparation happens once, access is coordinated, and the finished result is cohesive rather than piecemeal.",
                    'We regularly install fencing as part of <a href="/full-garden-makeover" class="text-primary font-semibold hover:underline">full garden transformations</a> across Leicester, and all our landscaping quotes can include a fencing element.',
                ],
            },
        ],
        "faqs": [
            ("How long does fencing installation take?", "A standard residential fence run (10–20 metres) takes 1–2 days. Longer runs or projects including gate posts may take 2–3 days. We remove all old materials the same day."),
            ("Do I need planning permission for a fence?", "In most cases, no. Fences up to 2 metres high on boundaries that don't face a highway do not require planning permission. Fences over 1 metre adjacent to a highway or in a conservation area may need permission. We can advise at survey stage."),
            ("How long does timber fencing last?", "Pressure-treated timber fencing typically lasts 15–25 years depending on the wood grade, treatment specification, and conditions. All our timber is pressure-treated as standard. Composite fencing carries a 20–25 year manufacturer warranty."),
            ("Can you install a gate at the same time?", "Yes. We can fit timber, composite or metal gates as part of the same installation — including gate posts, hinges and latches. Automated gate systems are outside our scope but we can install the posts and framework for a gate opener system."),
            ("Do you install fencing on slopes?", "Yes. Sloped ground is accommodated either by stepping the fence in level sections (step-down method) or by raking the panels to follow the slope (gravel-board method). We discuss the best approach at survey stage."),
            ("What's the difference between closeboard and panel fencing?", "Closeboard uses individual featheredge boards fixed to rails — more wind-resistant and longer-lasting than panels. Panel fencing uses prefabricated panels slotted between posts — faster to install and often slightly cheaper, but more vulnerable to wind damage if a panel warps or cracks."),
        ],
        "related_services": [
            ("Full Garden Makeover Leicester", "/full-garden-makeover"),
            ("Artificial Grass Leicester", "/artificial-grass"),
            ("Composite Decking Leicester", "/composite-decking"),
            ("Block Paving Driveways Leicester", "/block-paving-driveways-leicester"),
        ],
        "cta_h2": "Get a Free Fencing Quote",
        "cta_p": "Tell us the run length, height and fence type you have in mind — get an itemised quote in under 90 seconds.",
        "breadcrumb_label": "Fencing Leicester",
    },

    "turfing-leicester": {
        "title": "Turfing & Lawn Installation Leicester | New Lawn in a Day | Premium Landscapes",
        "meta_desc": "Professional turfing in Leicester. Premium lawn turf supplied and laid — new lawn ready in a day. Includes ground preparation. Free instant quote online.",
        "service_type": "Turfing and Lawn Installation",
        "h1": "Turfing & Lawn Installation in Leicester",
        "subheading": "A Perfect New Lawn Supplied, Laid and Ready to Use",
        "intro_paragraphs": [
            "A well-laid lawn transforms a garden instantly — and a properly installed new turf lawn looks and feels like it's been there for years. Premium Landscapes supplies and lays premium turf across Leicester and Leicestershire, with full ground preparation included as standard. No turf laid on top of existing weeds, no skimped topsoil depth — just a properly prepared seedbed, quality turf, and a lawn that establishes quickly and stays looking good."
        ],
        "sections": [
            {
                "h2": "Our Turfing Service in Leicester",
                "intro": "We offer a complete turfing service — not just turf delivery and drop-off. Every job includes:",
                "bullets": [
                    "Removal of existing lawn, weeds or surface material (where required)",
                    "Ground cultivation to a minimum 100mm depth",
                    "Application of topsoil where required to reach a suitable grade",
                    "Ground levelling and firming to create an even seedbed",
                    "Premium turf supply and laying",
                    "Turf edges cut clean and straight",
                    "Initial watering on the day of installation",
                    "Aftercare guidance for the first 6 weeks",
                ],
                "after_bullets": "We use premium-grade turf from established UK turf growers — not bargain-grade roll-up that yellows within a season.",
            },
            {
                "h2": "Turfing vs Seeding — Which Is Right for You?",
                "paragraphs": ["Both create a lawn, but they suit different situations."],
                "subgroups": [
                    {"label": "Turfing is the right choice when:", "bullets": [
                        "You want a usable lawn quickly (turf can be lightly used within 4–6 weeks)",
                        "Your garden needs a tidy, finished appearance fast — before a sale, event or project sign-off",
                        "You have children or pets who need access sooner rather than later",
                        "The existing ground has significant weed pressure that would undermine seed germination",
                        "You're installing turfing as part of a wider landscaping project",
                    ]},
                    {"label": "Seeding is the right choice when:", "bullets": [
                        "You have a large area to cover and cost is the primary driver",
                        "You're happy to wait 3–6 months for a usable lawn",
                        "The area is too irregular or steep for turf rolls to be laid effectively",
                    ]},
                ],
                "after_paragraphs": ["For most residential Leicester gardens, turfing is the practical choice — the cost difference versus seeding is modest, and the result is immediate and reliable."],
            },
            {
                "h2": "Turfing Costs in Leicester",
                "table": {
                    "headers": ["Area Size", "Typical Cost (Supplied & Laid)"],
                    "rows": [
                        ["Small (up to 25m²)", "£450 – £800"],
                        ["Medium (25–60m²)", "£800 – £1,600"],
                        ["Large (60m²+)", "£1,600+"],
                    ],
                },
                "after_table_paragraphs": ["Prices include ground preparation, topsoil where required, premium turf supply, laying and initial watering. Removal of old lawn or hard landscaping is quoted separately where significant volume is involved."],
            },
            {
                "h2": "Lawn Preparation — Why It Matters More Than the Turf",
                "paragraphs": ["Most lawn failures in Leicester come from inadequate ground preparation, not poor turf quality. The most common mistakes are:"],
                "subgroups": [
                    {"label": "Laying turf on top of existing weeds.", "p": "Perennial weeds — especially couch grass, creeping buttercup and dandelions — will push straight through new turf within 6–8 weeks. The existing lawn or surface must be killed off and cultivated before new turf goes down."},
                    {"label": "Insufficient topsoil depth.", "p": "Turf needs a minimum of 100mm of good quality topsoil to establish a proper root system. Laying turf on 30–40mm of topsoil over compacted subsoil produces a lawn that turns yellow in dry periods and doesn't recover from wear."},
                    {"label": "Poor drainage.", "p": "Leicestershire's clay-heavy soil compacts easily and holds water. Where drainage is poor, a layer of sharp sand worked into the topsoil — or a more substantial drainage solution — prevents waterlogging that kills grass roots from below."},
                ],
                "after_paragraphs": ["We address all three of these at the preparation stage. Our turf installations include proper cultivation, topdressing where needed, and a drainage assessment on every job."],
            },
            {
                "h2": "Turfing for Garden Makeovers in Leicester",
                "paragraphs": [
                    "New turfing is one of the most common elements of a full garden makeover. Once the hard landscaping is complete — patio, decking, fencing, raised beds — a fresh lawn ties the space together and gives it a finished, professional appearance.",
                    'We regularly install new lawns as part of <a href="/full-garden-makeover" class="text-primary font-semibold hover:underline">full garden redesigns</a> across <a href="/landscaping-leicester" class="text-primary font-semibold hover:underline">Leicester</a>, <a href="/landscaping-oadby" class="text-primary font-semibold hover:underline">Oadby</a>, <a href="/landscaping-wigston" class="text-primary font-semibold hover:underline">Wigston</a>, <a href="/landscaping-narborough" class="text-primary font-semibold hover:underline">Narborough</a> and the wider Leicestershire area. If you\'re planning a garden transformation, include the lawn in the same quote — it\'s more cost-effective than returning to do it separately, and the ground preparation works in sequence with the rest of the project.',
                ],
            },
            {
                "h2": "Turfing Aftercare — The First 6 Weeks",
                "paragraphs": ["New turf needs consistent moisture for the first 3–4 weeks while it roots into the prepared ground. This is especially important in the first two weeks."],
                "subgroups": [
                    {"label": "Week 1–2:", "p": "Water daily in dry weather — early morning is best. The turf should feel cool and damp when you press it. Don't walk on it."},
                    {"label": "Week 3–4:", "p": "Continue watering every 2–3 days. You can check rooting by gently lifting a corner — if it resists, roots are establishing."},
                    {"label": "Week 5–6:", "p": "First mow. Set the mower blade high (at least 40mm) for the first cut. Never remove more than one-third of the grass height in a single cut."},
                    {"label": "Week 6 onwards:", "p": "Normal maintenance begins — mowing fortnightly in growing season, feeding in spring and autumn, aerating annually."},
                ],
                "after_paragraphs": ["We provide a full written aftercare guide with every turfing installation."],
            },
        ],
        "faqs": [
            ("How long after turfing can I use the lawn?", "Light foot traffic from 3–4 weeks. Normal use from 6–8 weeks. Children and pets ideally from 6 weeks to allow full rooting."),
            ("What time of year is best for turfing?", "Autumn (September–November) is ideal — ground is still warm for rooting but cooler temperatures reduce water stress. Spring (March–May) is the second best window. Summer turfing is possible but requires consistent watering in dry spells. We turf year-round in Leicester — avoiding only frozen or waterlogged ground conditions."),
            ("Do I need to water a new lawn every day?", "In the first two weeks, yes — daily watering in dry conditions is essential. After week 3, every 2–3 days is sufficient. After the first mow, water as needed based on conditions."),
            ("Can you turf a sloped garden?", "Yes. Gentle slopes turf well and establish without issues. Steep slopes may require turf staples to prevent rolls from sliding during establishment. Very steep banks are sometimes better suited to ground cover planting than turf."),
            ("Will you remove my old lawn?", "Yes — old lawn stripping and disposal is included in most quotes. For larger volumes we may need to allow for skip costs, which we'll include in the quote."),
            ("Can you match new turf to an existing lawn area?", "We can come close using similar grass mixes, but exact matching to an existing lawn is difficult — turf varieties vary and established lawns develop their own character. For small repairs, seeding an overseeding mix to blend is often better than turf."),
        ],
        "related_services": [
            ("Artificial Grass Leicester", "/artificial-grass"),
            ("Full Garden Makeover Leicester", "/full-garden-makeover"),
            ("Fencing Leicester", "/fencing-leicester"),
            ("Garden Design Leicester", "/garden-design-leicester"),
        ],
        "cta_h2": "Get a Free Turfing Quote",
        "cta_p": "Send us the rough size of the area and any access notes — we'll come back with an itemised price including ground preparation.",
        "breadcrumb_label": "Turfing Leicester",
    },

    "pergolas-leicester": {
        "title": "Pergolas & Garden Structures Leicester | Installed by Premium Landscapes",
        "meta_desc": "Pergola installation in Leicester. Timber, aluminium and composite pergolas — designed and installed for your garden. Free instant quote online.",
        "service_type": "Pergola and Garden Structure Installation",
        "h1": "Pergolas & Garden Structures in Leicester",
        "subheading": "Shade, Structure and Style — Year-Round Outdoor Living",
        "intro_paragraphs": [
            "A well-positioned pergola transforms a patio from a summer-only space to a year-round outdoor room. Whether you want a simple timber overhead structure for climbing plants, a fully louvred aluminium pergola with adjustable roof slats and integrated lighting, or a bespoke garden structure to define a seating or dining area, Premium Landscapes designs and installs pergolas across Leicester and Leicestershire.",
            "We supply and install pergola structures from leading UK manufacturers, alongside bespoke timber-framed designs built to your specific measurements — including built-in seating, raised planting sections and integrated lighting as part of the same installation.",
        ],
        "sections": [
            {
                "h2": "Types of Pergola We Install in Leicester",
                "blocks": [
                    {"h3": "Timber Pergolas", "p": "Traditional timber pergolas — typically pressure-treated softwood or naturally durable hardwood — provide a classic garden structure that ages well and supports climbing plants such as wisteria, roses, clematis and jasmine. Timber pergolas are available in a wide range of sizes and profiles, from simple post-and-beam structures to detailed decorative designs with chamfered posts and shaped rafter ends. Timber pergolas can be painted or stained to match fencing, decking or garden furniture, and are typically the most cost-effective option for straightforward garden overhead structures."},
                    {"h3": "Aluminium Louvred Pergolas", "p": "Aluminium louvred pergolas use adjustable roof slats that open and close to control sun and rain — creating a genuinely weatherproof outdoor living space that works year-round. The best systems include motorised slats, integrated guttering that channels rain through the posts, built-in LED lighting in the rafters, and optional side screens or glass walls. For homeowners who want to maximise outdoor living time regardless of the British weather, a louvred aluminium pergola is the most practical solution. They require zero maintenance — no painting, no sealing, no rot."},
                    {"h3": "Composite Pergolas", "p": "Composite pergolas use the same wood-plastic composite material used in quality decking — giving the warmth and texture of timber with none of the maintenance requirements. Composite pergola components are available in a range of colours and profiles and are typically used where low maintenance is a priority but the client prefers the appearance of wood over aluminium."},
                    {"h3": "Bespoke Timber Garden Structures", "p": "Beyond standard pergola frames, we build bespoke garden structures including: garden arches, arbours, raised seating platforms with overhead canopies, garden bars with overhead shelter, and covered outdoor dining areas. These are designed and built to the specific dimensions and requirements of your outdoor space."},
                ],
            },
            {
                "h2": "Pergola Installation Costs in Leicester",
                "table": {
                    "headers": ["Pergola Type", "Typical Installed Cost"],
                    "rows": [
                        ["Timber pergola (standard)", "£1,800 – £4,500"],
                        ["Timber pergola (bespoke)", "£4,500 – £12,000+"],
                        ["Composite pergola", "£3,500 – £8,000"],
                        ["Aluminium louvred pergola", "£6,000 – £18,000+"],
                    ],
                },
                "after_table_paragraphs": ["Costs depend on size, specification, post depth requirements, and any integrated features (lighting, screens, planting sections). Foundations are included — we do not quote structure costs separately from the groundwork."],
            },
            {
                "h2": "Pergola Positioning and Planning",
                "paragraphs": [
                    "The right position for a pergola depends on sun orientation, views, how you plan to use the space, and what you want to screen or frame. We assess all of these at the site survey stage — most Leicester gardens have at least one or two positions where a pergola adds significantly more value than others.",
                ],
                "intro2": "Key considerations:",
                "bullets": [
                    "Sun orientation — south or west-facing aspects maximise usable time. A pergola on a north-facing patio primarily provides rain shelter rather than shade.",
                    "Proximity to the house — a pergola adjacent to the house extends the indoor/outdoor flow. A freestanding pergola further into the garden creates a destination space.",
                    "Planting integration — if you want climbing plants, the pergola needs to be positioned away from areas that receive very limited sunlight.",
                    'Planning permission — most domestic pergolas don\'t require planning permission under <a href="/blog-13" class="text-primary font-semibold hover:underline">permitted development</a> rules, provided they don\'t exceed 2.5m high on structures within 2m of a boundary, or 3m high elsewhere. We advise on this at survey stage.',
                ],
            },
            {
                "h2": "Combining a Pergola with Your Garden Project",
                "paragraphs": [
                    "A pergola adds the most value when it's designed and installed as part of the wider garden scheme — rather than added to an existing patio as an afterthought. When the pergola posts can be positioned during patio installation, the foundations integrate cleanly with the slab layout. Integrated lighting can be run underground in conduit during the same groundwork phase. The result is a seamlessly finished space rather than a structure that was clearly added later.",
                    'If you\'re planning a new <a href="/patios" class="text-primary font-semibold hover:underline">patio</a>, <a href="/composite-decking" class="text-primary font-semibold hover:underline">decking area</a> or <a href="/full-garden-makeover" class="text-primary font-semibold hover:underline">full garden redesign</a>, include the pergola in the initial design. We produce AI-generated visualisations that show the pergola in context — so you can see exactly how the finished space will look before any work begins.',
                ],
            },
        ],
        "faqs": [
            ("Do I need planning permission for a pergola in Leicester?", "Most pergolas installed under permitted development rights don't require planning permission. The main rules: structures within 2m of a boundary must not exceed 2.5m in height; structures further from a boundary can be up to 3m (or 4m with a ridged roof). Conservation area and listed building rules differ. We advise at survey stage."),
            ("How long does a timber pergola last?", "A properly treated softwood pergola lasts 15–20 years. Hardwood pergolas last 25–40 years depending on species. Aluminium and composite pergolas come with 20–25 year manufacturer warranties and effectively last indefinitely."),
            ("Can a pergola support heavy climbing plants like wisteria?", "Yes — provided the structure is designed with this in mind. Wisteria is particularly heavy and vigorous; timber pergolas for wisteria should use heavy-section posts and beams (minimum 100×100mm posts) with substantial fixings. We factor this in at design stage if climbing plants are part of the brief."),
            ("Can you add lighting to a pergola?", "Yes. Integrated LED lighting in the rafters, post-mounted uplights and festoon lighting run on concealed fixings are all standard additions. Power supply is run underground during installation and connected to an external socket or fusebox by your electrician."),
            ("Will a louvred pergola keep rain out completely?", "Premium louvred aluminium systems are effectively weatherproof — the slats close to create a watertight roof and water drains through internal channels in the posts. Standard timber and composite pergolas provide shade and partial rain protection but are not fully weatherproof."),
        ],
        "related_services": [
            ("Composite Decking Leicester", "/composite-decking"),
            ("Patio Installation Leicester", "/patios"),
            ("Garden Design Leicester", "/garden-design-leicester"),
            ("Garden Lighting Leicester", "/garden-lighting"),
        ],
        "cta_h2": "Get a Free Pergola Quote",
        "cta_p": "Tell us roughly where the pergola will go and what you want from it — we'll come back with options and an itemised price.",
        "breadcrumb_label": "Pergolas Leicester",
    },

    "commercial-astroturf-leicester": {
        "title": "Commercial Astroturf Leicester | Schools, Gyms & Sports Facilities | Premium Landscapes",
        "meta_desc": "Commercial astroturf installation in Leicester for schools, nurseries, gyms and sports facilities. Heavy-duty artificial grass to spec. Get a quote today.",
        "service_type": "Commercial Artificial Grass Installation",
        "h1": "Commercial Astroturf for Schools & Commercial Properties in Leicester",
        "subheading": "Heavy-Duty Artificial Grass Built for High-Use Commercial Environments",
        "intro_paragraphs": [
            "Commercial astroturf — artificial grass specified and installed for constant, heavy-use environments — serves a very different purpose to residential garden artificial grass. Schools, nurseries, leisure centres, sports facilities, corporate landscaping and HMO communal gardens all have specific requirements around durability grade, drainage capacity, pile height, infill specification and groundworks depth that residential-grade products won't meet.",
            "Premium Landscapes installs commercial-grade artificial grass across Leicester and Leicestershire for schools, nurseries, sports facilities, care homes, leisure facilities and commercial property grounds — with specifications tailored to the use case, occupancy requirements and any relevant safety standards.",
        ],
        "sections": [
            {
                "h2": "Commercial Astroturf Applications in Leicester",
                "blocks": [
                    {"h3": "Schools and Nurseries", "p": "Primary and secondary schools and nurseries in Leicester use commercial astroturf on playgrounds, MUGA surrounds, play areas and courtyard spaces. School-specification artificial grass must meet specific safety standards — particularly EN 1177 impact attenuation requirements for play areas where falling from equipment is a risk. We specify and install artificial grass with the correct HIC (Head Injury Criterion) rating, appropriate underlay and pad specification for the relevant fall height. We've installed artificial grass in school playgrounds and nursery outdoor learning areas across Leicestershire — understanding the procurement process, site access requirements during term time, and the DfE guidance on outdoor surface specifications."},
                    {"h3": "Sports Facilities and MUGA Surfaces", "p": "Multi-Use Games Areas (MUGAs), five-a-side football pitches, tennis court surrounds and general sports surfaces require artificial grass specified for lateral movement, ball roll and multi-sport use. We install sand-filled and rubber-crumb-infilled artificial grass to FIFA Quality Programme and ITF standards where required, on properly engineered shockpad base systems. For smaller five-a-side facilities and MUGA installations, we work with clients on specifications that meet performance requirements within the project budget — including appropriate shock absorption layers, line marking and perimeter edging."},
                    {"h3": "HMO and Residential Development Communal Spaces", "p": "Houses in Multiple Occupation (HMOs) and residential development communal gardens represent a significant commercial application of artificial grass in Leicester. Commercial-grade turf in these environments needs to withstand constant foot traffic from multiple occupants without matting, flattening or visibly wearing — residential-grade grass installed by individual occupants typically fails within 18 months in communal HMO settings. We install commercial-grade artificial grass in HMO communal gardens and residential development shared spaces across Leicester city centre and inner-city areas — properly specified for multi-occupancy use with a latex-backed, high-density pile product on a compacted sub-base."},
                    {"h3": "Corporate and Commercial Landscaping", "p": "Office courtyard spaces, hotel grounds, care home gardens and leisure facility outdoor areas all use artificial grass as part of their commercial landscaping. These installations typically need to look consistently well-maintained year-round without any management input — low-maintenance is the primary driver in commercial contexts. Commercial artificial grass on properly engineered groundworks requires almost zero ongoing maintenance: occasional brushing and leaf blowing, and a rinse down as needed. No watering, no mowing, no seasonal treatments."},
                ],
            },
            {
                "h2": "Commercial vs Residential Artificial Grass — Key Differences",
                "paragraphs": ["Commercial-specification artificial grass differs from residential products across several critical parameters:"],
                "table": {
                    "headers": ["Specification", "Residential", "Commercial"],
                    "rows": [
                        ["Pile density", "15,000–20,000 dtex", "22,000–28,000 dtex"],
                        ["Backing", "Standard single-layer", "Heavy-duty dual-layer"],
                        ["Drainage capacity", "15–25 litres/m²/hour", "40–80 litres/m²/hour"],
                        ["UV stability", "8–10 year warranty", "12–15 year warranty"],
                        ["Infill", "Sand or none", "Sand + rubber crumb"],
                        ["Sub-base depth", "75–100mm", "150–200mm"],
                        ["Typical lifespan", "10–15 years", "15–25 years"],
                    ],
                },
                "after_table_paragraphs": ["Installing residential-grade grass in a commercial environment is the most common reason commercial artificial grass fails prematurely. We specify the correct product for the intended use before quoting — not after."],
            },
            {
                "h2": "Commercial Astroturf Costs in Leicester",
                "paragraphs": ["Commercial astroturf costs more than residential installations because of the higher-grade materials, deeper sub-base specification and longer installation time. As a guide:"],
                "table": {
                    "headers": ["Application", "Typical Cost per m² (Installed)"],
                    "rows": [
                        ["School playground / nursery", "£55 – £85/m²"],
                        ["MUGA / sports surface", "£65 – £120/m²"],
                        ["HMO / communal garden", "£45 – £70/m²"],
                        ["Corporate / care home grounds", "£50 – £80/m²"],
                    ],
                },
                "after_table_paragraphs": [
                    "All costs include groundworks, sub-base, commercial-grade turf supply and installation. Play-area safety surfacing, shock pads and EN 1177 certification are additional and quoted separately.",
                    "<strong>Minimum project size for commercial installations: 50m².</strong>",
                ],
            },
            {
                "h2": "Our Commercial Installation Process",
                "subgroups": [
                    {"label": "Site Survey and Specification:", "p": "We visit the site to assess the area, existing ground conditions, drainage, access constraints and use-case requirements. We produce a written specification including product details, sub-base depth, drainage scheme and any relevant safety standard compliance."},
                    {"label": "Groundworks:", "p": "Commercial installations use a deeper, more heavily compacted sub-base than residential — typically 150–200mm of MOT Type 1 hardcore compacted in 75mm lifts. Where the existing surface is tarmac or concrete in good condition, we assess whether direct overlay is feasible (this can reduce cost significantly on large commercial areas)."},
                    {"label": "Drainage:", "p": "Where drainage capacity requirements exceed what standard perforated sub-base provides — particularly on intensively used school playgrounds — we install additional drainage channels or a perforated drainage pipe network beneath the sub-base."},
                    {"label": "Installation:", "p": "Commercial-grade turf is installed in full-width rolls to minimise seam count. All seams are glued on a joining tape rated for commercial use. Infill is machine-applied to the specified density."},
                    {"label": "Sign-Off:", "p": "We provide a completion report including specification summary, maintenance requirements and product warranties on completion."},
                ],
            },
        ],
        "faqs": [
            ("Do you install artificial grass for schools in Leicester?", "Yes. We have experience with school and nursery playground installations across Leicestershire, including EN 1177-compliant play area surfacing. We understand site access requirements during term time and procurement timescales for educational settings."),
            ("Can commercial astroturf meet BS EN 1177 safety requirements?", "Yes — with the correct shock pad underlay and pile height specification. Play areas from which children can fall require impact-attenuating surfacing that meets EN 1177. We specify the appropriate shock pad for the critical fall height of the equipment in the area."),
            ("How long does commercial astroturf last?", "Commercial-grade artificial grass installed on correct groundworks typically lasts 15–25 years. The backing material is the component that usually determines lifespan — dual-layer commercial backings outlast single-layer residential backings by a significant margin in high-footfall environments."),
            ("Can commercial astroturf be installed on existing concrete or tarmac?", "Yes — if the existing surface is structurally sound, level and drains adequately. Installing over a good existing base can reduce the project cost substantially on large commercial areas. We assess the existing surface at survey stage and advise honestly on whether direct overlay is appropriate."),
            ("Do you provide a maintenance service for commercial astroturf?", "We don't currently offer ongoing maintenance contracts, but we provide a comprehensive written maintenance guide and can advise on periodic deep-clean and brushing requirements. For school and sports facility installations, we can recommend specialist artificial grass maintenance contractors in the East Midlands."),
            ("Is a planning application required for commercial artificial grass installation?", "Typically not for like-for-like replacement of existing hard landscaping or grass areas. Changes to school grounds may require consent from the LA or governing body. We advise on planning considerations at survey stage."),
        ],
        "related_services": [
            ("Artificial Grass Leicester", "/artificial-grass"),
            ("Garden Design Leicester", "/garden-design-leicester"),
            ("Fencing Leicester", "/fencing-leicester"),
            ("Full Garden Makeover Leicester", "/full-garden-makeover"),
        ],
        "cta_h2": "Get a Commercial Astroturf Quote",
        "cta_p": "Send us the site address, approximate area and intended use — we'll produce a written specification and quote.",
        "breadcrumb_label": "Commercial Astroturf Leicester",
    },
}

# ---------------------------------------------------------------------------
# HTML RENDERING HELPERS
# ---------------------------------------------------------------------------

def _bullets(items):
    lis = "\n".join(f"                    <li>{i}</li>" for i in items)
    return f'                <ul class="list-disc pl-6 space-y-2 text-gray-700 mb-4 leading-relaxed">\n{lis}\n                </ul>'

def _table(t):
    head = "".join(f'<th class="px-4 py-3 text-left text-sm font-semibold text-gray-900 bg-gray-50 border border-gray-200">{h}</th>' for h in t["headers"])
    body = "".join(
        "<tr>" + "".join(f'<td class="px-4 py-3 text-sm text-gray-700 border border-gray-200">{c}</td>' for c in row) + "</tr>"
        for row in t["rows"]
    )
    return f'''                <div class="overflow-x-auto my-6">
                    <table class="min-w-full border border-gray-200 rounded-lg overflow-hidden">
                        <thead><tr>{head}</tr></thead>
                        <tbody>{body}</tbody>
                    </table>
                </div>'''

def _render_section(s, idx):
    bg = "bg-white" if idx % 2 == 0 else "bg-gray-50"
    out = [f'    <section class="py-12 md:py-16 px-4 {bg}">',
           '        <div class="max-w-4xl mx-auto">',
           f'            <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-6">{s["h2"]}</h2>',
           '            <div class="prose-body">']
    # paragraphs (before)
    for p in s.get("paragraphs", []):
        out.append(f'                <p class="text-gray-700 leading-relaxed mb-4">{p}</p>')
    # intro line then bullets
    if s.get("intro"):
        out.append(f'                <p class="text-gray-700 leading-relaxed mb-3">{s["intro"]}</p>')
    if s.get("bullets") and not s.get("intro2"):
        out.append(_bullets(s["bullets"]))
    if s.get("after_bullets"):
        out.append(f'                <p class="text-gray-700 leading-relaxed mb-4">{s["after_bullets"]}</p>')
    # H3 blocks (types of fencing / pergolas)
    for b in s.get("blocks", []):
        out.append(f'                <h3 class="text-xl font-bold text-gray-900 mt-6 mb-2">{b["h3"]}</h3>')
        out.append(f'                <p class="text-gray-700 leading-relaxed mb-4">{b["p"]}</p>')
    # subgroups (label + bullets) or (label + paragraph)
    for sg in s.get("subgroups", []):
        if "bullets" in sg:
            out.append(f'                <p class="text-gray-700 font-semibold mt-4 mb-2">{sg["label"]}</p>')
            out.append(_bullets(sg["bullets"]))
        else:
            out.append(f'                <p class="text-gray-700 leading-relaxed mb-3"><strong>{sg["label"]}</strong> {sg["p"]}</p>')
    # second intro/bullets (e.g. pergola "Key considerations")
    if s.get("intro2"):
        out.append(f'                <p class="text-gray-700 leading-relaxed mt-4 mb-3">{s["intro2"]}</p>')
        if s.get("bullets"):
            out.append(_bullets(s["bullets"]))
    # table
    if s.get("table"):
        out.append(_table(s["table"]))
    for p in s.get("after_table_paragraphs", []):
        out.append(f'                <p class="text-gray-700 leading-relaxed mb-3">{p}</p>')
    # after_paragraphs
    for p in s.get("after_paragraphs", []):
        out.append(f'                <p class="text-gray-700 leading-relaxed mb-3">{p}</p>')
    out.append('            </div>')
    out.append('        </div>')
    out.append('    </section>')
    return "\n".join(out)

def _render_hero(p):
    intro = "".join(f'\n                    <p class="text-blue-100 text-lg leading-relaxed mb-3">{para}</p>' for para in p["intro_paragraphs"])
    return f'''    <section class="hero-gradient text-white py-16 md:py-20 px-4">
        <div class="max-w-4xl mx-auto">
            <p class="text-blue-200 text-sm uppercase tracking-wider mb-3 font-semibold">{p["subheading"]}</p>
            <h1 class="text-3xl md:text-5xl font-extrabold mb-6 leading-tight">{p["h1"]}</h1>
            <div>{intro}
            </div>
            <div class="mt-8 flex flex-wrap gap-3">
                <a href="/quote" class="inline-block bg-white text-primary font-bold px-6 py-3 rounded-full hover:bg-blue-50 transition shadow-lg">Get a Free Instant Quote</a>
                <a href="/contact" class="inline-block bg-white/10 backdrop-blur text-white border border-white/30 font-semibold px-6 py-3 rounded-full hover:bg-white/20 transition">Talk to Us</a>
            </div>
        </div>
    </section>'''

def _render_faqs(p):
    items = "\n".join(
        f'''                <details class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
                    <summary class="font-semibold text-gray-900 cursor-pointer">{q}</summary>
                    <p class="text-gray-700 mt-3 leading-relaxed">{a}</p>
                </details>'''
        for q, a in p["faqs"]
    )
    return f'''    <section class="py-12 md:py-16 px-4 bg-gray-50">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-8 text-center">Frequently Asked Questions</h2>
            <div class="space-y-4">
{items}
            </div>
        </div>
    </section>'''

def _render_related(p):
    cards = "\n".join(
        f'                <a href="{href}" class="block bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md hover:border-primary transition text-center"><span class="font-semibold text-primary">{label} →</span></a>'
        for label, href in p["related_services"]
    )
    return f'''    <section class="py-12 md:py-16 px-4 bg-white">
        <div class="max-w-5xl mx-auto">
            <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-8 text-center">Related Services</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
{cards}
            </div>
        </div>
    </section>'''

def _render_cta(p):
    return f'''    <section class="py-16 px-4 hero-gradient text-white text-center">
        <div class="max-w-3xl mx-auto">
            <span class="bg-green-400 text-white text-sm px-3 py-1 rounded-full font-bold mb-4 inline-block">100% FREE</span>
            <h2 class="text-3xl md:text-4xl font-bold mb-4">{p["cta_h2"]}</h2>
            <p class="text-blue-100 text-lg mb-8">{p["cta_p"]}</p>
            <a href="/quote" class="inline-block bg-white text-primary font-bold px-10 py-4 rounded-full text-lg hover:bg-blue-50 transition shadow-lg">
                <i class="fas fa-magic mr-2"></i> Get My Free Quote &amp; Design
            </a>
        </div>
    </section>'''

def _render_breadcrumb(p):
    return f'''    <div class="bg-gray-50 border-b border-gray-100">
        <div class="max-w-7xl mx-auto px-4 py-3 text-sm text-gray-500">
            <nav aria-label="Breadcrumb"><ol class="flex items-center gap-2">
                <li><a href="/" class="hover:text-primary">Home</a></li>
                <li><span class="mx-1">/</span></li>
                <li><a href="/services" class="hover:text-primary">Services</a></li>
                <li><span class="mx-1">/</span></li>
                <li><span class="text-gray-800 font-medium">{p["breadcrumb_label"]}</span></li>
            </ol></nav>
        </div>
    </div>'''

def render_body(p):
    parts = [_render_breadcrumb(p), _render_hero(p)]
    for idx, s in enumerate(p["sections"], start=1):
        parts.append(_render_section(s, idx))
    parts.append(_render_faqs(p))
    parts.append(_render_related(p))
    parts.append(_render_cta(p))
    return "\n".join(parts)

# ---------------------------------------------------------------------------
# HEAD / SCHEMA UPDATES
# ---------------------------------------------------------------------------

def build_schema(slug, p):
    canonical = f"https://www.premium-landscapes.co.uk/{slug}"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "serviceType": p["service_type"],
                "provider": {"@type": "LocalBusiness", "name": "Premium Landscapes", "url": "https://www.premium-landscapes.co.uk"},
                "areaServed": {"@type": "City", "name": "Leicester"},
                "url": canonical,
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in p["faqs"]
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.premium-landscapes.co.uk/"},
                    {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://www.premium-landscapes.co.uk/services"},
                    {"@type": "ListItem", "position": 3, "name": p["breadcrumb_label"], "item": canonical},
                ],
            },
        ],
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)

def update_head(html, slug, p):
    # Title
    html = re.sub(r"<title>.*?</title>", f"<title>{p['title']}</title>", html, count=1, flags=re.DOTALL)
    # Meta description
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{p["meta_desc"]}">', html, count=1)
    # OG title / description
    html = re.sub(r'<meta property="og:title" content="[^"]*">',
                  f'<meta property="og:title" content="{p["title"]}">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">',
                  f'<meta property="og:description" content="{p["meta_desc"]}">', html, count=1)
    # Twitter
    html = re.sub(r'<meta name="twitter:title" content="[^"]*">',
                  f'<meta name="twitter:title" content="{p["title"]}">', html, count=1)
    html = re.sub(r'<meta name="twitter:description" content="[^"]*">',
                  f'<meta name="twitter:description" content="{p["meta_desc"]}">', html, count=1)
    # Replace the first JSON-LD block (the service/FAQ/breadcrumb graph)
    schema_json = build_schema(slug, p)
    new_block = f'<script type="application/ld+json">\n{schema_json}\n    </script>'
    html = re.sub(r'<script type="application/ld\+json">\s*\{[^<]*?"@graph".*?</script>',
                  new_block, html, count=1, flags=re.DOTALL)
    return html

# ---------------------------------------------------------------------------
# REWRITE THIN PAGES
# ---------------------------------------------------------------------------

HEADER_END_RE = re.compile(r"</header>\s*", re.IGNORECASE)
FOOTER_START_RE = re.compile(r"<footer\b", re.IGNORECASE)

def rewrite_page(slug, p):
    fp = ROOT / f"{slug}.html"
    html = fp.read_text(encoding="utf-8")
    html = update_head(html, slug, p)

    m1 = HEADER_END_RE.search(html)
    m2 = FOOTER_START_RE.search(html, m1.end() if m1 else 0)
    if not (m1 and m2):
        raise RuntimeError(f"{slug}: cannot locate header/footer boundaries")

    new_body = render_body(p)
    # find the line start of the <footer to keep its indent
    footer_line_start = html.rfind("\n", 0, m2.start()) + 1
    new_html = html[:m1.end()] + "\n" + new_body + "\n" + html[footer_line_start:]
    fp.write_text(new_html, encoding="utf-8")
    return fp

# ---------------------------------------------------------------------------
# UNIVERSAL "BLOG" NAV INSERTION
# ---------------------------------------------------------------------------

# Match the entire <a href="gallery" ...>...</a> tag (single line), and insert
# a Blog link with the same anchor classes right after it if Blog is absent.
GALLERY_TAG_RE = re.compile(
    r'(<a\s+href="gallery"([^>]*class="([^"]*)"[^>]*)>([^<]*)</a>)',
    re.IGNORECASE,
)

def insert_blog_nav(html):
    """Insert <a href="blog">Blog</a> directly after the Gallery anchor.

    Safer inline insertion — never copies surrounding content as "indent".
    Works equally well on pretty-printed multi-line navs and minified
    single-line navs. Idempotent: skips if a Blog link already exists in
    the short window immediately after Gallery.
    """
    changes = 0

    def repl(match):
        nonlocal changes
        full_tag = match.group(1)
        classes = match.group(3)
        # Look forward 300 chars only — if Blog already follows Gallery, skip.
        end = min(len(html), match.end() + 300)
        window_after = html[match.end():end]
        if re.search(r'<a\s+href="/?blog"[^>]*>\s*Blog\s*<', window_after):
            return full_tag
        # Detect indent style of the gallery line — only whitespace chars,
        # never arbitrary content. If gallery sits on a multi-line block,
        # mirror the indent on a new line; otherwise stay inline.
        line_start = html.rfind("\n", 0, match.start()) + 1
        prefix = html[line_start:match.start()]
        blog_link = f'<a href="blog" class="{classes}">Blog</a>'
        changes += 1
        if prefix and re.fullmatch(r"[ \t]+", prefix):
            return f"{full_tag}\n{prefix}{blog_link}"
        return f"{full_tag}{blog_link}"

    new_html = GALLERY_TAG_RE.sub(repl, html)
    return new_html, changes


def update_all_navs():
    summary = []
    for fp in sorted(ROOT.glob("*.html")):
        try:
            html = fp.read_text(encoding="utf-8")
        except Exception:
            continue
        new_html, n = insert_blog_nav(html)
        if n > 0 and new_html != html:
            fp.write_text(new_html, encoding="utf-8")
            summary.append((fp.name, n))
    return summary

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print("== Phase E rewrite ==")
    for slug, p in PAGES.items():
        fp = rewrite_page(slug, p)
        print(f"  rewrote: {fp.name}")
    print()
    print("== Phase E nav update ==")
    nav_changes = update_all_navs()
    for name, n in nav_changes:
        print(f"  + Blog added in {name} ({n} place{'s' if n > 1 else ''})")
    print(f"Total nav files updated: {len(nav_changes)}")
    print()
    # Validate
    import json as _json
    errs = 0
    for slug in PAGES:
        h = (ROOT / f"{slug}.html").read_text(encoding="utf-8")
        for b in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', h, re.DOTALL):
            try:
                _json.loads(b)
            except Exception as e:
                print(f"  X {slug}: JSON-LD error: {e}")
                errs += 1
    print(f"JSON-LD validation: {'OK' if errs == 0 else f'{errs} errors'}")


if __name__ == "__main__":
    main()
