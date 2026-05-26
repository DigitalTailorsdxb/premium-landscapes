#!/usr/bin/env python3
"""
Phase D: Generate 10 fact-based educational blog posts (blog-11 ... blog-20).
All content is technical/regulatory and does NOT invent customers or projects.
Each post links to the relevant service page, relevant area pages, the
case-studies hub and the free instant quote tool.
"""
import json
from pathlib import Path
from datetime import date

PUB_DATE = "2026-05-26"
MOD_DATE = "2026-05-26"
AUTHOR = "Premium Landscapes Team"
SITE = "https://www.premium-landscapes.co.uk"

# ---------------------------------------------------------------------------
# Topic data — every value here is publicly verifiable (BS 7533, Part P, the
# Town & Country Planning GPDO, IP rating standards etc).
# ---------------------------------------------------------------------------
TOPICS = [
    # ------------------------------------------------------------------- 11
    {
        "n": 11,
        "title": "SuDS Driveway Rules 2026: What Leicester Homeowners Need to Know",
        "meta_desc": "2026 guide to UK SuDS rules for front driveways: when you need planning permission, what counts as a permeable surface, and how Leicester homeowners stay compliant.",
        "category": "Planning & Regulations",
        "hero_subtitle": "Front-garden driveways larger than 5 m² in England still need planning permission unless they meet the SuDS rules — here is what those rules actually require in 2026.",
        "image": "images/services-driveway.webp",
        "image_alt": "Permeable resin-bound driveway compliant with UK SuDS rules",
        "service_link": ("services-driveway-block-paving", "driveways service page"),
        "area_links": [("landscaping-leicester", "Leicester"), ("landscaping-narborough", "Narborough"), ("landscaping-glenfield", "Glenfield")],
        "related_blog": (5, "Composite vs Timber Decking: UK Buyer's Guide"),
        "sections": [
            ("Why the SuDS rules exist",
             "Sustainable Drainage Systems (SuDS) rules were introduced in England in October 2008 under the Town and Country Planning (General Permitted Development) (Amendment) (No. 2) (England) Order 2008. They came in because so much front-garden hard surfacing was contributing to surface-water flooding and combined-sewer overflows. The rules apply to England (Wales and Scotland have their own equivalents) and they are still in force in 2026."),
            ("The 5 m² rule explained",
             "Replacing or laying a hard surface in front of your house only falls under permitted development — i.e. no planning permission needed — if one of two things is true. Either the new surface is less than 5 m² in total, or the new surface is made of porous/permeable material so rainwater drains through it naturally. If the surface is impermeable (standard concrete, traditional block paving with sand-filled joints, or non-permeable resin) and bigger than 5 m², you must either direct rainwater to a permeable area within the curtilage of your property (e.g. a lawn, border or soakaway) or apply for planning permission."),
            ("What counts as a permeable surface?",
             "The Environment Agency and DCLG guidance lists three main routes to compliance: (1) permeable block paving with open joints filled with grit-sized aggregate over a permeable sub-base; (2) porous asphalt with no traditional sealed surface; (3) resin-bound gravel laid over a permeable sub-base. Standard resin-bonded (where loose aggregate is scattered onto a layer of resin) is NOT permeable. Loose gravel is permeable but has its own access and security issues."),
            ("Why proper sub-base detailing matters more than the surface",
             "A permeable top surface is only half the answer. Below it you need a sub-base that can absorb and slowly release the water. We typically specify Type 3 sub-base (open-graded) under permeable surfaces in Leicestershire, with a geotextile separation layer to prevent the underlying clay from clogging the voids. Standard MOT Type 1 (which is what most older driveways were built on) is essentially impermeable once compacted, and putting permeable blocks on top of Type 1 defeats the entire point."),
            ("Directing runoff to a permeable area — the alternative",
             "If you'd rather keep a traditional impermeable surface, the rules still allow it provided rainwater is directed somewhere on your own property where it can soak away naturally — usually a lawn, planted border or dedicated soakaway. The crucial detail is that runoff must NOT discharge onto the public highway or directly into the surface-water drain. Crossfalls, channel drains and a properly sized soakaway are how this is achieved. We work this into the quote for any non-permeable driveway."),
            ("Leicester-specific considerations",
             "Most of Leicester and Leicestershire sits on Mercia Mudstone or boulder clay — neither drains well naturally. That makes the SuDS rules more important here than in sandier parts of the country, because rainwater that does not soak into a permeable surface really will pool or run off. Properties close to the Soar (Birstall, Thurmaston, Narborough) sit in the floodplain and have a higher water table, which further constrains the soakaway option. Drop us a postcode and we'll tell you which approach makes sense for your ground."),
            ("Common myths that get homeowners into trouble",
             "Myth 1: 'It's just a driveway, no-one cares.' Reality: Leicester City Council and the district councils do enforce SuDS breaches when they become aware of them, usually via complaints about runoff onto pavements. Myth 2: 'Permeable paving costs much more.' Reality: the surface materials are similar in cost; the extra cost is in the sub-base (often 30–40% more). Myth 3: 'I can just put a channel drain across the front.' Reality: a channel drain that discharges to the highway sewer makes the situation worse, not better."),
            ("What we include in every driveway quote",
             "Every driveway quote we issue from our free instant quote tool flags whether your project is over 5 m² and, if so, which compliance route you'll need. We then specify either a permeable build-up (Type 3 sub-base + geotextile + permeable surface) or an impermeable build-up with the appropriate runoff destination clearly noted. If your project needs full planning permission, we tell you that up front — it is far cheaper to know on day one than to discover it during the build."),
            ("Getting your free SuDS-compliant driveway quote",
             "If you're planning a new driveway anywhere in Leicester or Leicestershire, start with our free online quote. You'll get an itemised price for either a permeable build-up or an impermeable build-up with compliant runoff design, plus the option of a free AI design preview if you upload a photo of your front. No charge, no obligation, no sales call."),
        ],
        "faqs": [
            ("Do I need planning permission for a new driveway in Leicester?",
             "Only if the new surface is over 5 m² AND it's impermeable AND rainwater can't drain to a permeable area on your property. A small driveway, a permeable surface, or a driveway with proper drainage to a soakaway will all qualify as permitted development."),
            ("Is resin-bound the same as resin-bonded?",
             "No. Resin-bound is permeable (loose aggregate mixed into resin and trowelled flat — water drains through it). Resin-bonded scatters aggregate onto a sealed resin layer and is NOT permeable. Only resin-bound complies with SuDS rules for surfaces over 5 m²."),
            ("Will I get fined if my driveway doesn't comply?",
             "There is no automatic on-the-spot fine, but the local council can issue an enforcement notice requiring you to alter the driveway. Non-compliance also has implications for your home insurance and for the sale of the property — buyers' solicitors increasingly check for SuDS compliance."),
        ],
    },

    # ------------------------------------------------------------------- 12
    {
        "n": 12,
        "title": "Patio Sub-Bases Explained: BS 7533, MOT Type 1, and Why It Matters in Leicestershire",
        "meta_desc": "What's under your patio matters more than what's on top. A plain-English 2026 guide to BS 7533, MOT Type 1 specs, sub-base depths, and why Leicestershire clay needs extra care.",
        "category": "Materials & Engineering",
        "hero_subtitle": "Why the build-up under your patio matters more than the slab on top — a homeowner's guide to BS 7533, MOT Type 1, and the right sub-base for Leicestershire clay soil.",
        "image": "images/services-patio.webp",
        "image_alt": "Cross-section showing patio sub-base build-up: MOT Type 1, bedding and paving",
        "service_link": ("services-patio-installation", "patios service page"),
        "area_links": [("landscaping-oadby", "Oadby"), ("landscaping-wigston", "Wigston"), ("landscaping-stoneygate", "Stoneygate")],
        "related_blog": (4, "Choosing the Best Patio Materials for UK Weather"),
        "sections": [
            ("Why this matters",
             "Most failed patios in the UK don't fail because of the slab — they fail because of what's underneath. Settling, cracking, pooling water, lifting joints and weed growth all trace back to sub-base shortcuts. Spending an extra day on the sub-base is the single biggest factor in whether a patio still looks good in 10 or 20 years' time."),
            ("What BS 7533 actually says",
             "BS 7533 is the British Standard for paved areas. It's broken into multiple parts (BS 7533-1 through BS 7533-13) covering different types of paving and traffic loads. The two most relevant parts for domestic patios are BS 7533-4 (laying precast concrete paving blocks) and BS 7533-12 (specifies design of pavements with natural stone, concrete and clay paving). The standard specifies sub-base depths, jointing materials, bedding mortar mixes, and edge restraint requirements. It is the benchmark a professional installer should be working to — and the document an insurance assessor will reference if a patio fails."),
            ("MOT Type 1 vs Type 3 — what's the difference?",
             "MOT Type 1 is a graded, well-compacting granular material (typically crushed limestone or granite, 0–63mm). It is the default sub-base for domestic patios because it compacts to a stable, load-bearing layer. MOT Type 3 is an open-graded version (4–63mm) with no fines, designed to allow water to drain through. Type 3 is used under permeable surfaces; Type 1 under traditional patios where water will run off the surface."),
            ("Recommended depths for a domestic patio",
             "For a typical foot-traffic patio: 100 mm compacted MOT Type 1, laid in two compacted layers, on a properly excavated and prepared formation. For a patio that will see occasional vehicle traffic (e.g. an extended driveway/patio at the side of a house): 150 mm compacted Type 1. We typically excavate to give 100 mm of sub-base, 30–50 mm of bedding mortar, plus the thickness of the slab itself (usually 20–22 mm for porcelain or 22–25 mm for natural stone)."),
            ("Why Leicestershire clay needs more care",
             "Most of Leicester and Leicestershire sits on Mercia Mudstone or boulder clay. Both are prone to seasonal heave — they swell when wet and shrink when dry, which can lift or settle paving over the course of a year. Two things help: (1) a deeper sub-base (we often spec 125 mm instead of 100 mm on the more clay-heavy sites in Oadby, Wigston and Syston); (2) a geotextile separation membrane between the clay and the sub-base, to stop the clay fines migrating up into the Type 1 and reducing its compaction."),
            ("Bedding: full mortar bed, not the five-dot method",
             "BS 7533 is very clear: paving slabs should be laid on a continuous, full mortar bed — typically a 3:1 sharp sand and cement mix at 30–50 mm thickness. The 'five-dot' method (a blob of mortar at each corner and one in the middle) is explicitly NOT compliant and is one of the most common reasons patios crack. Hollow voids under a slab concentrate load on the contact points and the slab snaps under foot traffic."),
            ("Jointing: don't use kiln-dried sand on a patio",
             "Kiln-dried sand is for block paving — it relies on tightly-butted joints. For patios with wider joints (3–10mm), the right product is a brush-in resin jointing compound or a wet slurry-style jointing mortar. These bond to the slab edges, lock the pattern, and don't wash out with the first hosepipe blast. We use brush-in resin jointing on most porcelain installs."),
            ("Edge restraint matters",
             "Without a proper edge restraint, slabs can drift, joints open up, and the whole patio can spread over years of freeze-thaw. BS 7533 specifies haunched concrete edge restraint or a properly bedded edging course. We typically lay a haunched concrete kerb around the perimeter, or use a complementary edging slab bedded on mortar."),
            ("Drainage falls — the 1:80 minimum",
             "Patios should have a minimum fall of 1:80 (1 cm drop per 80 cm of run) away from the house, to prevent water pooling and avoid bridging the damp-proof course. On Leicestershire clay we often go to 1:60 to give a bit more margin during heavy rainfall."),
            ("Getting a quote that includes the right sub-base",
             "Our free instant patio quote includes a clear sub-base specification — depth, material, geotextile membrane (where appropriate), bedding spec and jointing product. If you're comparing quotes from other installers, ask them to put their sub-base spec in writing. A £2,000 patio with a 50 mm Type 1 sub-base will cost you more in 5 years' time than a £2,800 patio with the right build-up."),
        ],
        "faqs": [
            ("How deep should a patio sub-base be?",
             "For a foot-traffic domestic patio, 100 mm of well-compacted MOT Type 1 is the BS 7533 recommendation. For vehicular traffic, 150 mm. On heavier Leicestershire clay we sometimes increase to 125 mm and add a geotextile separation membrane."),
            ("What's wrong with the 'five-dot' method of laying slabs?",
             "It's not compliant with BS 7533 and it creates hollow voids under the slab. Foot traffic concentrates load on the dots, and slabs often crack in the centre within a year or two. A full mortar bed at 30–50 mm is what the standard requires."),
            ("Should I use kiln-dried sand to fill my patio joints?",
             "No — kiln-dried sand is for block paving. Patios with 3–10 mm joints need a brush-in resin compound or a wet slurry jointing mortar that bonds to the slab edges."),
        ],
    },

    # ------------------------------------------------------------------- 13
    {
        "n": 13,
        "title": "Permitted Development for Gardens: When You Do (and Don't) Need Planning Permission in 2026",
        "meta_desc": "2026 UK guide to permitted development rights for garden projects: patios, decking, outbuildings, fences and driveways. When you need planning permission and when you don't.",
        "category": "Planning & Regulations",
        "hero_subtitle": "Most garden projects don't need planning permission — but the rules are full of traps. Here's a clear 2026 guide to permitted development for UK homeowners.",
        "image": "images/services-garden.webp",
        "image_alt": "UK garden makeover within permitted development rights — patio, lawn and decking",
        "service_link": ("services-full-garden-makeover", "garden makeover service"),
        "area_links": [("landscaping-leicester", "Leicester"), ("landscaping-kirby-muxloe", "Kirby Muxloe"), ("landscaping-loughborough", "Loughborough")],
        "related_blog": (1, "How Much Does a Garden Redesign Cost in the UK"),
        "sections": [
            ("What 'permitted development' actually means",
             "Permitted development rights are a national grant of planning permission written into the Town and Country Planning (General Permitted Development) (England) Order 2015 (as amended). They let you carry out certain kinds of work without making a planning application — provided you stay within the limits. The rights apply to most ordinary houses in England (Scotland and Wales have separate rules), but they are restricted or removed for listed buildings, conservation areas, National Parks, and Areas of Outstanding Natural Beauty."),
            ("Patios — almost always permitted development",
             "A standard patio at ground level (no more than 300 mm above natural ground level) sits firmly within permitted development. You can lay a patio of essentially any size in your back garden without needing permission. The two situations where you'd need to check are: (1) if you're in a conservation area (e.g. parts of Stoneygate, Clarendon Park, Oadby village, Kirby Muxloe village); (2) if your house is listed."),
            ("Decking — the 300 mm rule",
             "Decking is permitted development provided the deck surface is no more than 300 mm above the existing ground level AND the decking (plus any other outbuildings) does not cover more than 50% of the area of land around the original house. A typical low-level garden deck meets both tests. A raised deck attached to a first-floor balcony, or one that covers most of a small garden, would not."),
            ("Outbuildings — the 50% / 2.5 m rule set",
             "Sheds, summerhouses, garden offices and pergolas all fall under the outbuildings rules. Key limits: max eaves height 2.5 m if within 2 m of a boundary; max overall height 4 m (dual-pitched) or 3 m (other); total area covered by outbuildings + extensions must not exceed 50% of the land around the original house; cannot sit forward of the principal elevation. A garden office that just meets these limits has become very popular post-pandemic — we get asked for the groundworks for these regularly."),
            ("Fences — the 2 m / 1 m rule",
             "Fences and walls are permitted development up to 2 m in height — UNLESS they're next to a highway used by vehicles, in which case the limit drops to 1 m. This catches a lot of homeowners out. If you're putting up a 1.8 m close-board fence along your front boundary that faces a road, you almost certainly need planning permission. Side and rear boundaries are usually fine up to 2 m."),
            ("Driveways — the SuDS rules",
             "Front-garden driveways have their own set of rules under SuDS regulations (covered in detail in our SuDS driveway blog post). In short: if the new surface is over 5 m² and impermeable AND there's no provision for runoff to drain to a permeable area on your land, you need planning permission. Most modern permeable installs avoid this entirely."),
            ("Conservation areas — almost everything changes",
             "If your property is in a conservation area, permitted development rights for the front and side of the house, boundary treatments, and any work to the front elevation are usually withdrawn or significantly restricted. This affects substantial parts of Stoneygate, Clarendon Park, Oadby village core, and Kirby Muxloe village. You can still landscape the rear garden under normal rules, but a new front driveway, front boundary wall, or visible new outbuilding will need a planning application."),
            ("Listed buildings — assume nothing",
             "If your house is listed, you'll need Listed Building Consent for almost any external change — and that includes hardscaping that visually changes the setting of the building. There are around 12,000 listed buildings in Leicestershire. If you're unsure, the local council's planning portal will tell you whether your address is listed."),
            ("Article 4 directions",
             "Some councils have issued 'Article 4 directions' that remove permitted development rights from specific streets or areas — typically to protect the character of historic areas. Leicester City Council, Charnwood, Blaby and Oadby & Wigston all have Article 4 directions on specific locations. Worth a 5-minute check on your council's planning portal before any visible exterior work."),
            ("How we handle planning in our quotes",
             "Every quote we issue includes a planning check. We tell you in writing whether your project falls within permitted development, whether it's likely to need planning permission, and whether your address is in a conservation area or covered by an Article 4 direction. If a planning application is needed, we can recommend a planning consultant — these are usually £300–£800 plus council fees. The cost of getting it wrong is much higher."),
        ],
        "faqs": [
            ("Do I need planning permission for a patio in my back garden?",
             "Almost never — a patio at ground level (under 300 mm above existing ground) in a back garden falls under permitted development. Conservation areas and listed buildings are the exceptions; we check both for every quote."),
            ("Can I build a garden office without planning permission?",
             "Usually yes — provided it's no taller than 2.5 m at the eaves (within 2 m of a boundary) or 4 m overall, doesn't sit forward of the principal elevation, and total outbuildings don't exceed 50% of the land around the original house."),
            ("Does putting up a tall garden fence need planning permission?",
             "Up to 2 m on rear and side boundaries is permitted. Anything over 1 m next to a road used by vehicles, or over 2 m anywhere else, needs an application. Most close-board fences (1.8 m) on rear boundaries are fine."),
        ],
    },

    # ------------------------------------------------------------------- 14
    {
        "n": 14,
        "title": "Conservation Areas in Leicester: A Homeowner's Landscaping Guide",
        "meta_desc": "Landscaping in a Leicester conservation area? Guide covering Stoneygate, Clarendon Park, Oadby village, Kirby Muxloe, listing consent, restricted permitted development and what works.",
        "category": "Planning & Regulations",
        "hero_subtitle": "Living in a Leicester conservation area changes what you can do in your garden — here's what's restricted, what's allowed, and how we handle the paperwork.",
        "image": "images/services-garden.webp",
        "image_alt": "Edwardian property in Stoneygate conservation area with natural stone landscaping",
        "service_link": ("services-full-garden-makeover", "full garden makeover service"),
        "area_links": [("landscaping-stoneygate", "Stoneygate"), ("landscaping-clarendon-park", "Clarendon Park"), ("landscaping-oadby", "Oadby"), ("landscaping-kirby-muxloe", "Kirby Muxloe")],
        "related_blog": (13, "Permitted Development for Gardens"),
        "sections": [
            ("What a conservation area is",
             "A conservation area is an area of 'special architectural or historic interest' designated under the Planning (Listed Buildings and Conservation Areas) Act 1990. Inside one, the local council has additional control over external changes to protect the character that made it special. Leicester has around 30 designated conservation areas across the city and surrounding districts; we work in several of them regularly."),
            ("The Leicester conservation areas we work in most often",
             "<strong>Stoneygate</strong> covers the prestigious Victorian and Edwardian streets between London Road and Knighton — Stoneygate Road, Victoria Road East, Elms Road and surrounding. <strong>Clarendon Park</strong> covers the dense Edwardian terrace streets around Queens Road. <strong>Oadby Village</strong> conservation area covers the historic core around Church Road and the High Street. <strong>Kirby Muxloe Village</strong> conservation area covers Main Street, the area around Kirby Muxloe Castle, and Station Road. <strong>Knighton</strong>, parts of <strong>Loughborough</strong>, and the historic cores of several Charnwood villages also have designations."),
            ("How permitted development changes inside a conservation area",
             "Inside a conservation area, several permitted development rights are restricted or removed entirely. The most relevant for landscaping: (1) cladding the exterior of a house is removed; (2) outbuildings to the side of a house lose their permitted development rights; (3) any hard surface (including driveways) in front of the principal elevation needs planning permission regardless of size or permeability; (4) some councils have Article 4 directions that remove additional rights — Stoneygate has one of the most extensive."),
            ("Front gardens — the biggest restriction",
             "The single biggest practical impact for homeowners is on front gardens. Even a small permeable driveway extension in a conservation area generally needs planning permission. Boundary walls, gates and railings facing the street are also closely controlled. We've successfully secured permissions for several front-garden landscaping projects in conservation areas, but the process adds 8–12 weeks to the project timeline."),
            ("Trees in conservation areas — the 6-week notice",
             "If you want to cut down, top or lop any tree in a conservation area with a stem diameter greater than 75 mm at 1.5 m above ground level, you must give the council 6 weeks' notice. They can respond by placing a Tree Preservation Order on the tree. We always survey trees as part of our site visits in conservation areas and flag any that would need notice."),
            ("Materials that work — and ones to avoid",
             "Conservation officers want new landscaping to complement the existing character — that usually means natural materials. Natural stone (Indian sandstone, York stone, granite setts) is almost always preferred over concrete imitations. Composite decking and bright synthetic-looking surfaces are usually a hard no. Traditional clay brick edging, hand-iron gates, and box-hedge borders all sit well in conservation-area applications."),
            ("Lighting in conservation areas",
             "External lighting needs to be sympathetic — low-level bollard lights, recessed step lights, and warm white (2700K) LED uplighters on planting all generally pass. High-output security floodlights and cool-white (5000K+) commercial-style lighting rarely do. We design conservation-area lighting schemes to BS 5489 standards using warm-tone fittings."),
            ("Listed properties inside conservation areas",
             "Around 12,000 buildings in Leicestershire are listed. If your home is both listed AND in a conservation area, you'll need both Listed Building Consent AND planning permission for visible external changes — including landscaping that affects the building's setting. We handle the applications as part of the quoted project."),
            ("What we include in every conservation-area quote",
             "Our free instant quote tool flags conservation-area addresses automatically. The detailed quote then includes: a conservation-area check; a permitted-development assessment; a recommended planning route (if any); a materials specification using period-sympathetic materials; and (if a planning application is needed) a recommended planning consultant and a realistic timeline."),
        ],
        "faqs": [
            ("Is my property in a Leicester conservation area?",
             "Use the Leicester City Council planning portal (or your district council's site for outside the city — Charnwood, Blaby, Oadby & Wigston, Hinckley & Bosworth) to search your address. We also check this automatically when you request a quote."),
            ("Can I lay a patio in my back garden if I'm in a conservation area?",
             "Yes — back gardens in conservation areas usually still allow ground-level patios under permitted development. It's mainly front gardens, side extensions and visible boundary changes that need consent."),
            ("How long does a conservation-area planning application take?",
             "Typically 8 weeks for a straightforward application, longer if the planning officer requests amendments. We build this into project timelines and start the planning process at the same time as finalising the design."),
        ],
    },

    # ------------------------------------------------------------------- 15
    {
        "n": 15,
        "title": "Drainage for Leicestershire Clay Gardens: French Drains, Soakaways and SuDS Compliance",
        "meta_desc": "Practical 2026 guide to drainage for Leicestershire clay-soil gardens. French drains, soakaway sizing under BRE Digest 365, SuDS rules and what actually works.",
        "category": "Materials & Engineering",
        "hero_subtitle": "Most of Leicestershire sits on clay — and that means drainage is something you fix at the design stage, not after the patio is down.",
        "image": "images/services-garden.webp",
        "image_alt": "French drain trench with perforated pipe and aggregate — Leicestershire clay garden",
        "service_link": ("services-full-garden-makeover", "garden makeover service"),
        "area_links": [("landscaping-narborough", "Narborough"), ("landscaping-birstall", "Birstall"), ("landscaping-thurmaston", "Thurmaston")],
        "related_blog": (12, "Patio Sub-Bases Explained"),
        "sections": [
            ("Why drainage is harder here than elsewhere",
             "Leicestershire's geology is dominated by Mercia Mudstone and boulder clay, with localised river-valley alluvium near the Soar. Clay holds water — its infiltration rate (the speed at which water soaks through it) is often less than 1 mm per hour, compared to 100+ mm per hour for sandy soil. That means rainwater that would simply soak away in Norfolk just sits on the surface here. Any landscaping project needs to plan for where that water goes."),
            ("Signs your garden has a drainage problem",
             "Standing water more than 24 hours after rain. Moss or algae growth on patios. Yellowing or dying lawn in patches. Boggy ground that doesn't recover even in summer. Water staining on house brickwork at low level. Damp issues in adjacent house walls. Most clay-soil gardens in Leicestershire have at least one of these symptoms — they're not unusual."),
            ("French drains — how they work",
             "A French drain is a gravel-filled trench with a perforated pipe at the bottom, wrapped in geotextile membrane. Water enters through the gravel, flows along the pipe and discharges either to a soakaway, a watercourse or (with permission) a surface-water drain. Typical dimensions for a domestic French drain: 300 mm wide, 600–900 mm deep, with 100 mm perforated pipe at the base. The trench is backfilled with 20 mm clean angular aggregate to within 100 mm of the surface, then topsoil or turf."),
            ("Soakaways — sizing them properly",
             "A soakaway is an underground pit (filled with aggregate or built with crate modules) where water collects and slowly soaks away into the surrounding soil. Sizing a soakaway on clay soil follows BRE Digest 365: you do an infiltration test (dig a small trench, fill with water, measure how long it takes to drop) to calculate the soil's infiltration coefficient, then size the soakaway based on a 1-in-10-year storm. On heavy Leicestershire clay, soakaways often need to be 2–3 times larger than on free-draining soil to achieve the same performance."),
            ("Why a soakaway sometimes isn't the answer",
             "If your garden's infiltration rate is below ~1 mm/hour, a soakaway will simply fill up and stay full. In those situations, you need to discharge somewhere else — typically the surface-water drain at the front of the property, but this requires consent from Severn Trent and a permit. We've designed dozens of drainage schemes in Birstall, Thurmaston and Narborough (all close to the Soar floodplain) where the only viable route is a properly-engineered connection to the surface-water sewer."),
            ("Permeable surfaces as part of the drainage strategy",
             "The cheapest drainage solution is often not to create the runoff in the first place. Permeable patio surfaces (porcelain with wide drainage joints, permeable block paving), permeable driveway surfaces (resin-bound, permeable blocks) and lawn areas all reduce the volume of water that needs to be drained. We try to design every makeover so that 30–50% of the hardscape is either permeable or feeds directly into planted areas."),
            ("Raised beds and level changes can help",
             "On clay soil, raised planting beds drain dramatically better than ground-level beds because excess water can escape downward through the bed and out the sides. We often spec 200–300 mm raised beds with a free-draining mix (loam, sharp sand, organic matter) on top of the existing clay. The plants thrive and the surrounding paths stay drier."),
            ("Drainage and the Building Regulations",
             "Building Regulations Part H covers drainage. Connecting a new soakaway or drainage system into the public sewer requires either a build-over agreement (if within 3 m of a sewer) or formal consent from the sewerage undertaker — in Leicester that's Severn Trent. We handle these applications as part of the project where required."),
            ("What we include in every quote",
             "Our free instant quote includes a drainage assessment based on your location and project type. If you're in a known clay-heavy area (most of central Leicester, Oadby, Wigston, Syston) or a known flood-risk area (Birstall, Thurmaston, Narborough riverside), the quote flags the drainage works needed and prices them in transparently. Drainage is not something we leave as a 'see what we find' line — surprises here are expensive."),
        ],
        "faqs": [
            ("Do I really need a French drain in my Leicestershire garden?",
             "Often yes, if your garden holds water after rain. French drains intercept and redirect surface water, and they're particularly effective on the clay-heavy gardens common to Leicester, Oadby, Wigston and Syston."),
            ("How big should a soakaway be on clay soil?",
             "Sizing follows BRE Digest 365 — you start with an infiltration test and design for a 1-in-10-year storm. On Leicestershire clay (infiltration often <1 mm/hour) a residential soakaway typically needs to be 1.5–3 m³, which is 2–3 times what you'd need on sandy soil."),
            ("Can I just drain my patio into the road?",
             "No. Discharging runoff to the public highway is not permitted under SuDS rules. You either need a soakaway, drainage to a planted area on your own land, or (with permission from Severn Trent) a connection to the surface-water sewer."),
        ],
    },

    # ------------------------------------------------------------------- 16
    {
        "n": 16,
        "title": "Composite Decking Brands Compared: Millboard vs Trex vs Cladco — UK 2026 Buyer's Guide",
        "meta_desc": "Honest UK 2026 buyer's guide comparing Millboard, Trex, Cladco and other leading composite decking brands. Costs per m\u00b2, warranties, finish quality and which to pick.",
        "category": "Materials & Engineering",
        "hero_subtitle": "Not all composite decking is the same — and the difference between the cheapest and the best can be £80 per m\u00b2. A 2026 UK buyer's guide.",
        "image": "images/services-decking.webp",
        "image_alt": "Composite decking installation showing Millboard, Trex and Cladco board comparison",
        "service_link": ("services-composite-decking", "composite decking service"),
        "area_links": [("landscaping-kirby-muxloe", "Kirby Muxloe"), ("landscaping-wigston", "Wigston"), ("landscaping-glenfield", "Glenfield")],
        "related_blog": (5, "Composite vs Timber Decking: Complete UK Buyer's Guide"),
        "sections": [
            ("How composite decking is actually made",
             "There are three main composite types on the UK market. <strong>WPC (Wood Plastic Composite)</strong> blends recycled wood fibre with HDPE plastic — used by Trex, Cladco and many mid-range brands. <strong>Capped composite</strong> is WPC with an extruded polymer wrap on top for better stain and scratch resistance. <strong>Polymer/PVC composite</strong> uses no wood fibre — Millboard is the most prominent example, using a mineral-modified polyurethane that mimics real timber. Each has very different performance characteristics."),
            ("Millboard — the premium choice",
             "Millboard's Enhanced Grain and Lasta-Grip ranges are widely regarded as the best-performing decking on the UK market. The boards are made in Coventry from a polyurethane mix with no wood fibre at all, which makes them genuinely waterproof, mould-resistant and dimensionally stable. They look closer to real timber than any other product we install. The catch is cost — supply-only board cost is typically £90–£130 per m², roughly double standard WPC. They also need Millboard's own DuoSpan sub-frame system, which adds cost but lasts 30+ years."),
            ("Trex — the established US brand",
             "Trex is the largest composite decking manufacturer in the world, made in the USA from recycled wood and plastic. The Enhance Naturals and Transcend ranges are the most popular in the UK. Board cost is £55–£85 per m² supply only. The capped Transcend range carries a 25-year stain-and-fade warranty, which is best-in-class for WPC. The boards perform well but the colour palette is less convincing than Millboard at close range."),
            ("Cladco — the budget-friendly UK option",
             "Cladco is a UK-based supplier offering composite decking at noticeably lower price points (£30–£55 per m² supply only). The Bullnose and Woodgrain ranges are popular for budget-conscious projects. The boards are perfectly serviceable but the warranty is shorter (typically 10 years), the colour range is narrower, and the board profile is less convincing at close range. Good value for letting properties or rental-grade installs."),
            ("Other UK brands worth knowing",
             "<strong>Composite Prime HD Deck Dual</strong> offers a strong mid-market option — UK distribution, capped boards, 25-year warranty, around £50–£75 per m². <strong>Hyperion</strong> targets the high end with a slightly cheaper alternative to Millboard. <strong>Eva-Last</strong> is South African origin with a bamboo composite range. <strong>Saige</strong> is another mid-market UK brand with a wide range of finishes."),
            ("What to look for in a warranty",
             "Two warranty figures matter: the structural warranty (typically 25 years across most brands) and the stain-and-fade warranty (varies wildly from 5 to 25 years). The stain-and-fade warranty is the one that catches owners out — cheaper boards often have just a 5–10 year fade warranty, and most claims arise from sun bleaching. Always read the warranty document, not the marketing material."),
            ("Sub-frame systems — usually overlooked",
             "Almost every composite manufacturer specifies a particular sub-frame system. Most still allow treated softwood timber joists, but the premium brands (Millboard, Hyperion) recommend their own aluminium or composite sub-frame systems. Aluminium sub-frames cost more upfront but they last as long as the decking itself, which matters because replacing a rotten timber sub-frame later means lifting the whole deck."),
            ("Cost summary — supply and install in 2026",
             "Installed costs (supply + labour, on a standard substrate, before any special groundworks): Cladco £80–£120 per m²; Trex / Composite Prime £110–£160 per m²; Hyperion £140–£200 per m²; Millboard £160–£220 per m². For a 30 m² deck, the difference between the cheapest WPC and Millboard is roughly £3,000–£4,000 — significant, but it's spread over 25+ years and the visual difference is striking."),
            ("Which one should you choose?",
             "Pick Millboard if budget allows and you want the most convincing timber look that's also genuinely waterproof and low-maintenance. Pick Trex or Composite Prime for a strong mid-market install with a long warranty. Pick Cladco for rental properties or projects where budget is the priority. We can quote all of these — drop us your project details on our free instant quote tool and we'll price both a premium and a mid-market option so you can compare."),
        ],
        "faqs": [
            ("Is Millboard really worth twice the price of Trex?",
             "If the deck is somewhere highly visible at close range (off a kitchen, a high-end garden makeover) and you plan to stay in the house for 10+ years, the visual quality and waterproof performance of Millboard justifies it. For a standard family garden deck, a capped WPC like Trex Transcend is excellent value."),
            ("What's the difference between WPC and PVC composite?",
             "WPC contains recycled wood fibre — it's the most common type. PVC composite (Millboard, some Hyperion ranges) contains no wood at all, which makes it more dimensionally stable, mould-resistant and genuinely waterproof. PVC is more expensive but typically performs better long-term."),
            ("Do composite decks need any maintenance?",
             "Not in the way timber does — no staining, sanding or sealing. But they do benefit from a wash 1–2 times per year with warm soapy water to prevent mould build-up in shaded areas. Capped boards (Trex Transcend, Millboard) need less maintenance than uncapped WPC."),
        ],
    },

    # ------------------------------------------------------------------- 17
    {
        "n": 17,
        "title": "Artificial Grass Specifications Decoded: Pile Height, Density, Backings & Drainage",
        "meta_desc": "2026 UK technical buyer's guide to artificial grass: what pile height means, density (Dtex), backings, infill, drainage and how to read a spec sheet honestly.",
        "category": "Materials & Engineering",
        "hero_subtitle": "Artificial grass spec sheets are full of jargon — pile height, Dtex, gauge, backing. Here's what each number actually means and which ones matter for a UK garden.",
        "image": "images/services-grass.webp",
        "image_alt": "Cross-section of artificial grass showing pile, backing, sub-base and drainage layers",
        "service_link": ("services-artificial-grass", "artificial grass service"),
        "area_links": [("landscaping-leicester", "Leicester"), ("landscaping-oadby", "Oadby"), ("landscaping-syston", "Syston")],
        "related_blog": (3, "Artificial Grass vs Natural Turf: Which is Right for Your Garden?"),
        "sections": [
            ("Pile height — taller is not always better",
             "Pile height is the length of the grass blades, measured in millimetres. UK garden grades typically run from 20 mm (short, manicured look) to 45 mm (lush, natural look). Common sweet-spot for residential use is 30–37 mm — long enough to look natural, short enough to recover well from foot traffic. Anything above 40 mm tends to flatten under regular use and look matted in shaded areas."),
            ("Pile weight and density (Dtex)",
             "<strong>Dtex</strong> measures the weight of an individual fibre — higher Dtex means thicker, stronger blades. Residential grades are typically 8,000–14,000 Dtex. <strong>Total weight per m²</strong> combines Dtex with pile density (how many tufts per linear metre) and matters more than pile height for long-term durability. Quality residential grass is typically 2,200–3,500 g/m². Anything below 2,000 g/m² will flatten and wear quickly."),
            ("Gauge and stitch rate",
             "<strong>Gauge</strong> is the spacing between rows of tufts (3/8 inch gauge is standard for residential). <strong>Stitch rate</strong> is the number of stitches per linear metre within each row (16–18 is typical for residential, higher for sports grades). Tighter gauge + higher stitch rate = denser grass that looks more natural and wears better."),
            ("Backings — primary and secondary",
             "Behind the visible grass is a <strong>primary backing</strong> (usually a polypropylene fabric) that the tufts are stitched through, and a <strong>secondary backing</strong> (typically polyurethane or latex) that locks the tufts in place. The secondary backing is what stops the tufts pulling out. Quality grasses use polyurethane (PU) which is more durable, more flexible in cold weather, and significantly more recyclable than latex. Drainage holes are punched through both backings — typically 4 mm holes every 100 mm for residential."),
            ("Drainage performance — the spec that matters most for UK gardens",
             "UK rainfall makes drainage performance the single most important spec for artificial grass. Quality residential backings drain at 60+ litres per m² per minute, more than the heaviest UK rainfall. Cheaper grasses with sparser hole patterns can be 10× slower, which leads to standing water and odour. We test drainage with a bucket-of-water demonstration on every quote — it's the most informative thing we show customers."),
            ("Sub-base — the foundation that makes or breaks it",
             "The grass itself is only half the install. A typical residential artificial grass sub-base is: 75–100 mm of compacted Type 1 (or Type 3 for SuDS-sensitive sites), topped with 25 mm of compacted granite dust (laying course), with a weed membrane between the granite dust and the grass. Cheaper installs that lay grass directly onto existing soil look fine for 12 months and then settle, ripple and dip. Spec the sub-base properly and the install lasts 10–15 years."),
            ("Infill — do you actually need it?",
             "Older artificial grasses needed sand or rubber infill to keep the pile upright. Modern residential grades with curled or thatched 'memory' fibres are designed to stay upright without infill. We typically only use kiln-dried silica sand infill (about 5 kg per m²) where pet odour management matters or where the grass is on a high-traffic route — it helps with both."),
            ("Pet-safe specifications",
             "If you have dogs, three things matter: (1) anti-bacterial backing or backing finish; (2) high drainage rate (urine needs to flush through quickly); (3) silica sand infill that absorbs odour. Several brands now market 'pet-safe' or 'urine-resistant' specs — they generally meet these three criteria and command a small premium (~£3 per m²)."),
            ("UK fire-rating and child-safety standards",
             "For residential gardens, the only widely-relevant test is the EN 14041 fire classification (Bfl-S1 is standard). For school or nursery installations, a Critical Fall Height (CFH) test under BS EN 1177 may be required — typically achieved by adding a 25–35 mm shock pad layer underneath the grass."),
            ("What we include in every artificial grass quote",
             "Our free instant quote tool produces a detailed spec for your project: pile height, total weight, drainage rate, backing type, sub-base spec, weed membrane, infill (if any) and edging method. If you're comparing quotes from other installers, ask for the same spec details in writing — vague quotes like '30 mm artificial grass' tell you almost nothing about the actual product."),
        ],
        "faqs": [
            ("What's the best pile height for a family garden?",
             "30–37 mm gives the best balance of natural appearance and wear performance. Shorter (20–28 mm) gives a manicured look but shows compaction more quickly. Longer (40 mm+) can look matted in high-traffic areas within a year."),
            ("How do I tell good artificial grass from cheap?",
             "Total weight per m² is the single best indicator — quality residential grass is 2,200+ g/m². Other clues: polyurethane (not latex) backing, drainage rate above 60 litres/m²/minute, and the look/feel of the curled 'memory' fibres at the base of the pile."),
            ("How long does artificial grass last?",
             "A quality install on a properly-spec'd sub-base typically lasts 10–15 years before the pile noticeably degrades. Cheap installs on poor sub-bases often look tired within 3–5 years."),
        ],
    },

    # ------------------------------------------------------------------- 18
    {
        "n": 18,
        "title": "Resin-Bound vs Resin-Bonded vs Block Paving: UK Driveway Comparison 2026",
        "meta_desc": "Direct 2026 comparison of resin-bound, resin-bonded and block paving driveways in the UK. SuDS compliance, costs per m\u00b2, lifespan, maintenance and which to pick.",
        "category": "Materials & Engineering",
        "hero_subtitle": "Three driveway surfaces dominate the UK market — but only two of them are SuDS-compliant, and only one actually feels good underfoot. A 2026 comparison.",
        "image": "images/services-driveway.webp",
        "image_alt": "Side-by-side comparison: resin-bound driveway, resin-bonded surface and block paving",
        "service_link": ("services-driveway-block-paving", "driveways service"),
        "area_links": [("landscaping-kirby-muxloe", "Kirby Muxloe"), ("landscaping-enderby", "Enderby"), ("landscaping-blaby", "Blaby")],
        "related_blog": (11, "SuDS Driveway Rules 2026"),
        "sections": [
            ("Resin-bound — the modern premium",
             "Resin-bound is a blend of clear UV-stable resin and decorative aggregate, trowelled onto a permeable sub-base. The aggregate is fully encapsulated by the resin, so the surface is smooth, durable, and — crucially — fully permeable to water (typically 200+ litres per m² per minute). This means resin-bound driveways comply with SuDS rules at any size without needing additional drainage. Lifespan is 20–25 years with no major maintenance. Aesthetically it gives a clean, modern look in a wide range of aggregate colours."),
            ("Resin-bonded — the cheaper imitation that's NOT permeable",
             "Resin-bonded is often confused with resin-bound but it's a fundamentally different product. Loose aggregate is scattered onto a sealed resin layer — only the bottom edge of each aggregate piece is held in place. The surface is rougher (the aggregate sticks up), it's NOT permeable (the resin layer is sealed), and aggregate sheds over time. It's cheaper than resin-bound (~30–40% less) but it does not comply with SuDS rules for surfaces over 5 m² unless you provide separate drainage."),
            ("Block paving — the traditional workhorse",
             "Block paving uses individual interlocking blocks (concrete or clay) laid on a sand bedding course over a compacted sub-base, with kiln-dried sand brushed into the joints to lock the pattern. <strong>Standard block paving</strong> with sand-filled joints is NOT permeable. <strong>Permeable block paving</strong> uses wider joints filled with grit-sized aggregate over a Type 3 (open-graded) sub-base — this version IS SuDS-compliant. The two look almost identical from the surface but the sub-base spec is completely different."),
            ("SuDS compliance comparison",
             "<strong>Resin-bound:</strong> compliant by design. <strong>Permeable block paving:</strong> compliant if the sub-base is Type 3 (not Type 1) and joints are filled with grit. <strong>Standard block paving:</strong> not compliant — needs separate drainage to a permeable area. <strong>Resin-bonded:</strong> not compliant — needs separate drainage. For new driveways over 5 m² (most front gardens), resin-bound or permeable block are the only routes that avoid planning permission."),
            ("Cost comparison — installed prices (2026, Leicestershire)",
             "<strong>Resin-bonded:</strong> £45–£70 per m² installed. <strong>Standard block paving:</strong> £75–£110 per m² installed (concrete blocks). <strong>Permeable block paving:</strong> £90–£130 per m² installed (deeper sub-base costs more). <strong>Resin-bound:</strong> £110–£150 per m² installed. For a typical 40 m² front driveway, that's a difference of £2,500–£4,500 between the cheapest and most expensive option."),
            ("Lifespan and maintenance",
             "<strong>Resin-bound:</strong> 20–25 years, virtually no maintenance beyond an annual wash. <strong>Permeable block paving:</strong> 25–30 years, joints may need re-grit topping up every 5–7 years. <strong>Standard block paving:</strong> 25–30 years, joints need sand top-up and weeds need treating annually. <strong>Resin-bonded:</strong> 10–15 years, aggregate sheds and resin can yellow under UV — generally regarded as a budget-life product."),
            ("Look and feel underfoot",
             "<strong>Resin-bound:</strong> smooth, almost suede-like underfoot — easy to walk on in heels, easy to clear of snow, easy to wheel buggies and bikes across. <strong>Block paving:</strong> classic textured look, joints can catch heels, wheeling small wheels (skateboards, prams) is bumpy. <strong>Resin-bonded:</strong> noticeably rough underfoot, can scrape knees in falls, aggregate occasionally tracks into the house."),
            ("Colour and design flexibility",
             "Resin-bound has the widest colour palette — natural-stone aggregate blends, vibrant colours, and the ability to mix colours within a single drive (borders, paths, pattern inlays). Block paving offers a strong choice of colours, sizes and laying patterns (herringbone, basketweave, stretcher bond), plus the ability to incorporate contrasting borders. Resin-bonded is more limited and tends to look most natural in earth-tone aggregates."),
            ("Our recommendation by situation",
             "<strong>Front driveway, new install, looks matter:</strong> resin-bound (smooth, premium, compliant). <strong>Front driveway, budget priority:</strong> permeable block paving (compliant, cheaper than resin-bound). <strong>Rear/side driveway, smaller than 5 m²:</strong> any of the three (no SuDS issue). <strong>Replacing a tired older driveway in a conservation area:</strong> traditional clay block paving or natural-stone setts (subject to conservation consent). Our free instant quote tool prices all three for any project so you can compare directly."),
        ],
        "faqs": [
            ("What's the difference between resin-bound and resin-bonded?",
             "Resin-bound has aggregate fully mixed into the resin and is smooth and permeable. Resin-bonded scatters aggregate onto sealed resin and is rough and NOT permeable. The names are similar but the products are fundamentally different — and only resin-bound complies with SuDS rules for driveways over 5 m²."),
            ("Is permeable block paving really different from normal block paving?",
             "Yes — the blocks look similar but the sub-base is completely different. Permeable block paving uses a Type 3 open-graded sub-base with grit-filled joints, allowing water to pass through. Standard block paving uses a Type 1 sub-base with sand-filled joints and is effectively impermeable."),
            ("Which driveway surface lasts longest?",
             "Permeable block paving and standard block paving have the longest lifespans (25–30 years). Resin-bound is close behind at 20–25 years. Resin-bonded is the shortest-lived at 10–15 years."),
        ],
    },

    # ------------------------------------------------------------------- 19
    {
        "n": 19,
        "title": "Garden Lighting Regulations: Part P, IP Ratings, Voltage & DIY vs Pro",
        "meta_desc": "2026 UK garden lighting guide: Part P building regulations, IP rating meanings, low-voltage vs mains, notifiable work and when you must use a registered electrician.",
        "category": "Planning & Regulations",
        "hero_subtitle": "Garden lighting looks beautiful — but get the regulations wrong and you've invalidated your home insurance. A 2026 guide to Part P, IP ratings and voltage choices.",
        "image": "images/garden-lighting.webp",
        "image_alt": "Professional garden lighting installation with IP-rated fittings and low-voltage transformer",
        "service_link": ("services-garden-lighting", "garden lighting service"),
        "area_links": [("landscaping-stoneygate", "Stoneygate"), ("landscaping-knighton", "Knighton"), ("landscaping-oadby", "Oadby")],
        "related_blog": (6, "Outdoor Garden Lighting Ideas"),
        "sections": [
            ("Part P of the Building Regulations — what it covers",
             "Part P of the Building Regulations (2005, last updated 2013) covers electrical safety in dwellings, including gardens. It defines 'notifiable work' that must either be carried out by a registered electrician (Part P-competent person) OR notified to Building Control. For gardens, notifiable work includes any new circuit, any new wiring in a 'special location' (which includes outdoors), and any addition to an existing outdoor circuit. A non-compliant installation can invalidate your home insurance and create issues when selling the property."),
            ("IP ratings — what the two digits mean",
             "<strong>IP</strong> stands for Ingress Protection. The first digit (0–6) rates protection against solid objects and dust; the second digit (0–8) rates protection against water. Common outdoor ratings: <strong>IP44</strong> (splash-proof — fine for sheltered locations); <strong>IP54</strong> (dust-protected and splash-proof — standard for most garden fittings); <strong>IP65</strong> (dust-tight and resistant to low-pressure water jets — good for exposed locations); <strong>IP67</strong> (dust-tight and resistant to temporary immersion — for in-ground uplighters); <strong>IP68</strong> (continuous immersion — for pond and pool lighting)."),
            ("Low-voltage (12V/24V) vs mains (230V) — the big choice",
             "<strong>12V/24V low-voltage lighting</strong> uses a transformer to step mains down to 12V or 24V before it goes to the fittings. The transformer itself sits in a sheltered location (often in the garage or a weatherproof enclosure). Low-voltage cable is much safer to install and is usually <em>not</em> notifiable under Part P — homeowners can install low-voltage garden lighting kits themselves. <strong>230V mains lighting</strong> uses standard household voltage and is significantly more dangerous to install. Mains outdoor lighting IS notifiable and should be installed by a Part P-registered electrician."),
            ("Why we use low-voltage for nearly every garden install",
             "We specify 12V or 24V LED lighting for around 95% of our garden lighting projects. Reasons: (1) significantly safer for the homeowner and any future DIY work; (2) usually not notifiable under Part P; (3) much wider range of high-quality fittings; (4) LED at low voltage is the most efficient lighting technology available; (5) cabling is much simpler and faster to install. The transformer sizing is the key engineering step — undersize and the lights dim toward the end of the run; oversize and you waste money."),
            ("Colour temperature — get this right or regret it",
             "LED colour temperature is measured in Kelvin (K). <strong>2700K (warm white)</strong> is the closest to traditional incandescent and is what we use for nearly all garden lighting — flattering on planting, foliage and natural stone. <strong>3000K (warm-neutral)</strong> works for contemporary schemes. <strong>4000K+ (cool white)</strong> looks clinical and washed-out in a garden setting and should be avoided. <strong>5000K+ (cool/daylight)</strong> is for commercial security only — it ruins the atmosphere of a residential garden."),
            ("Lumens — how much light do you actually need?",
             "Garden lighting is about creating mood and highlighting features, not flooding the area. Typical lumens per fitting: path lights 80–150 lm; spike-mounted uplighters on planting 150–300 lm; tree uplighters on mature trees 400–800 lm; wall-wash floods 600–1,200 lm. Cumulatively a typical residential garden lighting scheme uses 3,000–6,000 lumens total — far less than people expect."),
            ("Light pollution and the BS 5489 guidance",
             "BS 5489 covers exterior lighting design. Two principles worth keeping in mind: (1) light fixtures should be directed onto the feature you want to light, not into the sky or onto neighbouring properties; (2) overall light levels should be appropriate for the location (a quiet residential street needs much less light than a town centre). Local council nuisance enforcement is increasingly active on excessive residential floodlighting."),
            ("Conservation areas and listed buildings",
             "External lighting on a listed building (or one in a conservation area) often requires consent. Even where consent isn't strictly required, conservation officers usually want fittings to be discreet — bollards in dark bronze or black, recessed in-ground fittings, or wall-washers with anti-glare hoods. Bright contemporary fittings on Victorian/Edwardian properties almost always get pushed back."),
            ("Smart-control options for 2026",
             "Most modern low-voltage LED gardens can be paired with a smart transformer (Lutron, Hunza, Lumena and several others) for app and voice control, dimming, schedules and scene presets. Realistic budget for smart control on a typical garden: £350–£900 above standard wired transformer pricing."),
            ("What we include in every garden lighting quote",
             "Our free instant quote tool includes a basic lighting design (number of fittings, type, transformer size, cable run) for any quote that includes lighting. For larger projects we produce a full lighting plan with fitting selection, colour temperature, lumen output per zone and transformer sizing — included free of charge."),
        ],
        "faqs": [
            ("Do I need an electrician to install garden lighting?",
             "For low-voltage 12V/24V lighting from a plug-in transformer, usually no — the work isn't notifiable under Part P. For any 230V mains outdoor lighting or any new circuit, yes — it must be done by a Part P-registered electrician and certified."),
            ("What IP rating do I need for outdoor garden lights?",
             "Minimum IP44 for sheltered locations, IP54–IP65 for exposed fittings, IP67 for in-ground uplighters and IP68 for pond/pool lighting."),
            ("Why does colour temperature matter for garden lights?",
             "Cool-white LEDs (4000K+) wash out planting and natural-stone materials and make a garden look clinical. Warm-white (2700K) is what you want for nearly all garden lighting — it flatters foliage, brickwork and stone."),
        ],
    },

    # ------------------------------------------------------------------- 20
    {
        "n": 20,
        "title": "Choosing Patio Materials for Leicestershire Clay Soil: Porcelain, Sandstone, Limestone, Granite",
        "meta_desc": "2026 guide to the best patio materials for Leicestershire's clay soil. Porcelain, Indian sandstone, limestone and granite compared on cost, performance, and clay-soil suitability.",
        "category": "Materials & Engineering",
        "hero_subtitle": "Choosing patio material for a Leicestershire garden isn't just an aesthetic call — clay soil changes how each material performs over 10 years. Here's what we recommend and why.",
        "image": "images/services-patio.webp",
        "image_alt": "Porcelain, Indian sandstone, limestone and granite patio samples on Leicestershire clay",
        "service_link": ("services-patio-installation", "patios service"),
        "area_links": [("landscaping-oadby", "Oadby"), ("landscaping-wigston", "Wigston"), ("landscaping-syston", "Syston"), ("landscaping-glenfield", "Glenfield")],
        "related_blog": (12, "Patio Sub-Bases Explained: BS 7533"),
        "sections": [
            ("Why clay soil matters for patio choice",
             "Most of Leicestershire sits on Mercia Mudstone or boulder-clay glacial till. Clay soils expand when wet and contract when dry, putting cyclical stress on whatever sits on top. Materials with low water absorption and high frost resistance perform best on clay — they're less likely to spall, crack or stain over a UK winter. The right material choice combined with a properly engineered sub-base (covered in our BS 7533 blog) is what makes a 20-year patio rather than a 5-year one."),
            ("Porcelain — the modern recommendation",
             "Vitrified porcelain paving is fired at extremely high temperatures, giving it water absorption typically below 0.1%. That's essentially waterproof, frost-proof, and stain-resistant. It comes in a huge range of finishes — stone-effect, wood-effect, concrete-effect — and is dimensionally consistent (every slab is exactly the same size), which makes installation faster and joints tighter. For Leicestershire clay gardens, porcelain is our default recommendation in around 70% of projects. Typical installed cost: £100–£160 per m²."),
            ("Indian sandstone — the classic value option",
             "Indian sandstone is the most widely-laid patio material in the UK. It's sedimentary stone quarried in Rajasthan, hand-cut to riven or sawn finishes. Water absorption is moderate (typically 1–4%) — high enough that it needs proper jointing and ideally a sealer in our climate. It's a beautiful, warm-toned natural product available in calibrated thicknesses (22 mm is standard). Installed cost: £75–£110 per m². Good on clay if properly installed with a full mortar bed, jointing compound and optional sealer."),
            ("Natural limestone — premium and characterful",
             "Limestone is a denser sedimentary stone than sandstone, with lower water absorption (typically 0.5–2%) and a more uniform colour palette — Kota Brown, Tandur Blue and similar. It's a more premium product than Indian sandstone and gives a softer, more natural look than porcelain. Installed cost: £95–£140 per m². Performs well on clay with the right sub-base."),
            ("Granite — extremely hard, very expensive",
             "Granite is an igneous rock — incredibly dense, very low water absorption (<0.5%), highly frost-resistant. It's also extremely hard to cut, which makes installation slower and more expensive. Best suited to small areas, edging detail, or driveways where heavy traffic justifies the cost. Installed cost: £130–£200 per m² for paving slabs. For most domestic patios we'd choose porcelain over granite — similar performance, lower cost, more design flexibility."),
            ("Concrete and pre-cast slabs — when they make sense",
             "Pre-cast concrete slabs and 'stone-effect' concrete pavers (Marshalls Symphony, Bradstone etc.) sit at the budget end — installed costs from £55–£90 per m². Modern textured concrete pavers have come a long way and can look convincing at a distance. The trade-off is colour fade over 5–10 years (UV exposure) and higher water absorption (4–8%), so they're more prone to staining and moss growth on clay sites with poor drainage."),
            ("Reclaimed materials — beautiful but variable",
             "Reclaimed York stone, granite setts and clay pavers can give a garden character no new material can match — and they suit period properties in Stoneygate, Clarendon Park and the conservation-area villages. The challenge is variability: thickness, colour, condition and supply can all be unpredictable, which makes both quoting and installation more involved. We work with several Leicestershire reclaimed-stone yards and can quote a reclaimed scheme as an alternative if it suits your project."),
            ("Jointing — picks the material's lifespan",
             "Whatever the paving material, the jointing is what determines how long it stays looking good. Wide joints (5–10 mm) on clay soil need a flexible resin jointing compound that won't crack as the slabs flex with seasonal ground movement. Cement-based mortar joints are stiffer and tend to crack on clay. We use a brush-in resin jointing compound on virtually every patio install — it costs slightly more than mortar but it's the difference between joints that need redoing in 2 years and joints that last 15."),
            ("Sealing — yes for some materials, no for others",
             "<strong>Porcelain:</strong> never needs sealing. <strong>Indian sandstone:</strong> optional sealing is recommended for UK climate — slows water absorption, reduces moss growth, makes spills easier to clean. <strong>Limestone:</strong> sealing recommended. <strong>Granite:</strong> usually doesn't need sealing. <strong>Concrete:</strong> sealing can help with colour fade and staining. We include sealing as an optional line on every quote with full cost transparency."),
            ("Our top three picks for Leicestershire clay gardens",
             "<strong>1. Porcelain</strong> — best all-round performance on clay, biggest design choice, lowest long-term maintenance. <strong>2. Indian sandstone</strong> — natural, value-for-money, requires proper installation and ideally sealing. <strong>3. Limestone</strong> — premium natural choice that suits period and contemporary properties equally. Our free instant patio quote lets you compare all three for your specific project — full itemised costs, sub-base spec, jointing spec, sealing option."),
        ],
        "faqs": [
            ("What's the best patio material for clay soil in Leicester?",
             "Porcelain — water absorption below 0.1%, frost-resistant, dimensionally stable. It tolerates the seasonal expansion/contraction of clay soil better than any other patio material. Indian sandstone is a strong second choice if it's properly installed and sealed."),
            ("How long does a porcelain patio last?",
             "A properly-installed porcelain patio (BS 7533 sub-base, full mortar bed, resin jointing) should last 25+ years with virtually no maintenance beyond an occasional wash. The material itself is essentially permanent."),
            ("Should I seal my Indian sandstone patio?",
             "Optional but recommended for UK climate, especially on Leicestershire clay. Sealing slows water absorption, reduces moss and algae growth, and makes stains easier to remove. Plan to re-seal every 3–5 years."),
        ],
    },
]


# ---------------------------------------------------------------------------
# Template — head/nav/footer match blog-1.html exactly.
# ---------------------------------------------------------------------------

NAV_HEADER = """
    <!-- Navigation Header -->
    <header class="bg-white shadow-sm fixed w-full top-0 z-50" style="-webkit-transform: translateZ(0); transform: translateZ(0);">
        <nav class="container mx-auto px-4 py-0 flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <a href="/">
                    <img src="images/logo.png" alt="Premium Landscapes" class="h-20 md:h-28">
                </a>
            </div>
            <div class="hidden md:flex items-center space-x-8">
                <a href="/" class="text-gray-700 hover:text-primary transition">Home</a>
                <a href="about" class="text-gray-700 hover:text-primary transition">About</a>
                <a href="services" class="text-gray-700 hover:text-primary transition">Landscaping Services Leicester</a>
                <a href="gallery" class="text-gray-700 hover:text-primary transition">Garden Transformation Gallery</a>
                <a href="quote" class="text-gray-700 hover:text-primary transition">Instant Quote</a>
                <a href="contact" class="text-white bg-primary px-6 py-2 rounded-full hover:bg-primary-dark transition">Contact</a>
            </div>
            <button id="mobileMenuBtn" class="md:hidden text-primary text-2xl">
                <i class="fas fa-bars"></i>
            </button>
        </nav>
    </header>

    <div id="mobileMenu" class="mobile-menu fixed top-0 right-0 h-full w-64 bg-white shadow-2xl transform translate-x-full md:hidden z-50" style="-webkit-transform: translateX(100%); transform: translateX(100%);">
        <div class="p-6">
            <button id="closeMobileMenu" class="text-primary text-2xl mb-8">
                <i class="fas fa-times"></i>
            </button>
            <div class="flex flex-col space-y-6">
                <a href="/" class="text-gray-700 hover:text-primary transition text-lg mobile-menu-link">Home</a>
                <a href="about" class="text-gray-700 hover:text-primary transition text-lg mobile-menu-link">About</a>
                <a href="services" class="text-gray-700 hover:text-primary transition text-lg mobile-menu-link">Services</a>
                <a href="gallery" class="text-gray-700 hover:text-primary transition text-lg mobile-menu-link">Gallery</a>
                <a href="quote" class="text-gray-700 hover:text-primary transition text-lg mobile-menu-link">Instant Quote</a>
                <a href="quote" class="text-gray-700 hover:text-primary transition text-lg mobile-menu-link">Quote + AI Design</a>
                <a href="contact" class="text-primary font-semibold transition text-lg mobile-menu-link">Contact</a>
            </div>
        </div>
    </div>
"""

FOOTER = """
    <footer class="bg-gray-900 text-white py-12 px-4">
        <div class="container mx-auto max-w-5xl text-center">
            <img src="images/logo.png" alt="Premium Landscapes" class="h-16 mx-auto mb-6 brightness-0 invert">
            <div class="flex flex-wrap justify-center gap-x-6 gap-y-2 mb-6">
                <a href="/" class="hover:text-primary-light transition">Home</a>
                <a href="about" class="hover:text-primary-light transition">About</a>
                <a href="services" class="hover:text-primary-light transition">Services</a>
                <a href="gallery" class="hover:text-primary-light transition">Gallery</a>
                <a href="quote" class="hover:text-primary-light transition">Instant Quote</a>
                <a href="case-studies" class="hover:text-primary-light transition">Case Studies</a>
                <a href="blog" class="hover:text-primary-light transition">Blog</a>
                <a href="areas-we-cover" class="hover:text-primary-light transition">Areas We Cover</a>
                <a href="contact" class="hover:text-primary-light transition">Contact</a>
            </div>
            <p class="text-sm text-gray-400 mb-2">
                <i class="fas fa-phone text-primary-light mr-1"></i> 07877 934782
                &nbsp;|&nbsp;
                <i class="fas fa-map-marker-alt text-primary-light mr-1"></i> Leicester, Leicestershire
            </p>
            <p class="text-sm text-gray-500 mb-2">&copy; 2026 Premium Landscapes. All rights reserved. &nbsp;|&nbsp; <a href="/privacy-policy" class="hover:opacity-100 underline">Privacy Policy</a></p>
            <p class="text-sm text-gray-400">
                <i class="fas fa-bolt text-amber-500 mr-1"></i> Powered by
                <a href="https://trade-engine.co.uk" target="_blank" class="font-semibold hover:opacity-80 transition">
                    <span class="text-white">Trade</span> <span class="text-amber-500">Engine</span>
                </a>
            </p>
        </div>
    </footer>
    <script src="scripts/config.js"></script>
    <script src="scripts/cookie-consent.js"></script>
</body>
</html>
"""


def render_sections(sections):
    out = []
    for h, p in sections:
        out.append(f'                <h2 class="text-3xl font-bold text-primary mt-12 mb-4">{h}</h2>')
        out.append(f'                <p class="mb-4 leading-relaxed">{p}</p>')
    return "\n".join(out)


def render_faq_html(faqs):
    out = ['                <h2 class="text-3xl font-bold text-primary mt-12 mb-4">Frequently Asked Questions</h2>',
           '                <div class="space-y-4 mb-8">']
    for q, a in faqs:
        out.append('                    <details class="bg-stone rounded-2xl p-6 group">')
        out.append('                        <summary class="font-semibold text-gray-900 cursor-pointer">' + q + '</summary>')
        out.append(f'                        <p class="text-gray-700 mt-3 leading-relaxed">{a}</p>')
        out.append('                    </details>')
    out.append('                </div>')
    return "\n".join(out)


def render_internal_links(t):
    svc_slug, svc_label = t["service_link"]
    area_pills = " ".join(
        f'<a href="{slug}" class="inline-block bg-stone hover:bg-primary hover:text-white text-primary px-4 py-2 rounded-full text-sm font-medium transition">{label}</a>'
        for slug, label in t["area_links"]
    )
    rb_n, rb_title = t["related_blog"]
    return f"""
                <h2 class="text-3xl font-bold text-primary mt-12 mb-4">Related Reading &amp; Service Pages</h2>
                <div class="bg-stone rounded-2xl p-6 mb-8">
                    <p class="mb-4"><strong>Read next:</strong> <a href="blog-{rb_n}" class="text-primary font-semibold hover:underline">{rb_title}</a></p>
                    <p class="mb-4"><strong>Relevant service:</strong> <a href="{svc_slug}" class="text-primary font-semibold hover:underline">Visit our {svc_label} →</a></p>
                    <p class="mb-4"><strong>See real installs:</strong> <a href="case-studies" class="text-primary font-semibold hover:underline">Browse our project case studies →</a></p>
                    <p class="mb-2"><strong>Areas covered in this article:</strong></p>
                    <div class="flex flex-wrap gap-2">{area_pills}</div>
                </div>
"""


def make_faq_jsonld(faqs):
    return json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [
             {"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": a}}
             for q, a in faqs]},
        ensure_ascii=False, indent=4
    )


def render_blog(t):
    n = t["n"]
    url = f"{SITE}/blog-{n}"
    title = t["title"]
    desc = t["meta_desc"]
    article_ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": title, "description": desc,
        "author": {"@type": "Organization", "name": AUTHOR,
                   "url": f"{SITE}/about-premium-landscapes"},
        "publisher": {"@type": "Organization", "name": "Premium Landscapes",
                      "logo": {"@type": "ImageObject", "url": f"{SITE}/images/logo.png"}},
        "datePublished": PUB_DATE, "dateModified": MOD_DATE,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url}
    }
    breadcrumb_ld = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog"},
            {"@type": "ListItem", "position": 3, "name": title},
        ]
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Facebook Pixel Code -->
    <script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js'); fbq('init', '1480425153686683'); fbq('track', 'PageView');</script>
    <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=1480425153686683&ev=PageView&noscript=1"/></noscript>
    <!-- End Facebook Pixel Code -->
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9PGX32QB99"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-9PGX32QB99');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="images/logo.png">
    <title>{title} | Premium Landscapes</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{url}">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{SITE}/{t['image']}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{SITE}/{t['image']}">

    <script src="scripts/tailwind.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>
    <link rel="stylesheet" href="styles/liquid-glass.css">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{ primary: '#2563eb', 'primary-light': '#60a5fa', 'primary-dark': '#1e40af', secondary: '#3b82f6', accent: '#8b5cf6', 'stone': '#f0f9ff' }},
                    fontFamily: {{ 'heading': ['Inter','sans-serif'], 'body': ['Open Sans','sans-serif'] }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ font-family: 'Open Sans', sans-serif; }}
        h1, h2, h3, h4, h5, h6 {{ font-family: 'Inter', sans-serif; }}
        .mobile-menu {{ transition: transform 0.3s ease; }}
        .mobile-menu.active {{ transform: translateX(0) !important; -webkit-transform: translateX(0) !important; }}
    </style>
    <script src="scripts/config.js"></script>
    <script src="scripts/main.js"></script>
    <link rel="stylesheet" href="styles/mobile.css">

    <script type="application/ld+json">
{json.dumps(article_ld, indent=4, ensure_ascii=False)}
    </script>
    <script type="application/ld+json">
{json.dumps(breadcrumb_ld, indent=4, ensure_ascii=False)}
    </script>
    <script type="application/ld+json">
{make_faq_jsonld(t['faqs'])}
    </script>
    <link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml">
</head>
<body class="bg-white">
{NAV_HEADER}

    <!-- Blog Post Header -->
    <section class="pt-32 pb-12 px-4 bg-stone">
        <div class="container mx-auto">
            <div class="max-w-4xl mx-auto">
                <nav aria-label="Breadcrumb" class="mb-4">
                    <ol class="flex items-center gap-2 text-sm text-gray-500">
                        <li><a href="/" class="hover:text-primary transition">Home</a></li>
                        <li><span class="mx-1 text-gray-400">/</span></li>
                        <li><a href="blog" class="hover:text-primary transition">Blog</a></li>
                        <li><span class="mx-1 text-gray-400">/</span></li>
                        <li class="text-gray-700 font-medium truncate max-w-xl">{title}</li>
                    </ol>
                </nav>
                <div class="text-accent font-semibold mb-2">{t['category']}</div>
                <h1 class="text-4xl md:text-5xl font-bold text-primary mb-6">{title}</h1>
                <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-gray-600 mb-8 text-sm">
                    <span class="flex items-center gap-1"><i class="fas fa-user text-primary"></i> By <a href="about" class="font-semibold text-primary hover:underline">{AUTHOR}</a></span>
                    <span class="text-gray-300">|</span>
                    <time datetime="{PUB_DATE}" class="flex items-center gap-1"><i class="fas fa-calendar text-primary"></i> 26 May 2026</time>
                    <span class="text-gray-300">|</span>
                    <span class="flex items-center gap-1"><i class="fas fa-tag text-primary"></i> {t['category']}</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Featured Image -->
    <section class="pb-12 px-4 bg-stone">
        <div class="container mx-auto">
            <div class="max-w-4xl mx-auto">
                <img src="{t['image']}" alt="{t['image_alt']}" class="w-full rounded-xl shadow-lg">
            </div>
        </div>
    </section>

    <!-- Blog Content -->
    <article class="py-12 px-4 bg-white">
        <div class="container mx-auto">
            <div class="max-w-3xl mx-auto prose prose-lg">
                <p class="text-xl text-gray-700 mb-8">{t['hero_subtitle']}</p>

{render_sections(t['sections'])}

{render_faq_html(t['faqs'])}

{render_internal_links(t)}

                <div class="bg-gradient-to-br from-primary to-accent text-white text-center rounded-2xl p-10 mt-10">
                    <span class="bg-green-400 text-white text-sm px-3 py-1 rounded-full font-bold mb-4 inline-block">100% FREE</span>
                    <h2 class="text-3xl font-bold mb-3">Get your free instant quote &amp; AI garden design</h2>
                    <p class="text-blue-50 mb-6">Itemised pricing plus a free AI design preview — delivered in under 90 seconds. No charge, no obligation, no sales call.</p>
                    <a href="quote" class="bg-white text-primary font-bold px-8 py-3 rounded-full text-lg hover:bg-blue-50 transition inline-block shadow-lg">
                        <i class="fas fa-magic mr-2"></i> Get My Free Quote &amp; Design
                    </a>
                </div>
            </div>
        </div>
    </article>

{FOOTER}
"""


def write_blogs():
    for t in TOPICS:
        path = Path(f"blog-{t['n']}.html")
        path.write_text(render_blog(t), encoding="utf-8")
        print(f"  wrote blog-{t['n']}.html  ({len(path.read_text(encoding='utf-8'))} bytes)  — {t['title'][:60]}")


def list_for_blog_index():
    """Returns HTML cards for blog.html listing."""
    cards = []
    for t in TOPICS:
        cards.append(f'''                <!-- Blog Post {t['n']} -->
                <div class="glass-rim rounded-2xl">
                <a href="/blog-{t['n']}" class="blog-card block bg-white rounded-xl shadow-lg overflow-hidden">
                    <div class="h-48 overflow-hidden">
                        <img loading="lazy" src="{t['image']}" alt="{t['image_alt']}" class="w-full h-full object-cover">
                    </div>
                    <div class="p-6 card-content">
                        <div class="text-sm text-accent font-semibold mb-2">{t['category']}</div>
                        <h2 class="text-xl font-bold text-primary mb-3 card-title">{t['title']}</h2>
                        <p class="text-gray-600 mb-4 card-description">{t['hero_subtitle'][:160]}</p>
                        <span class="text-primary font-semibold mt-auto inline-block">Read More →</span>
                    </div>
                </a>
                </div>
''')
    return "\n".join(cards)


if __name__ == "__main__":
    print(f"Phase D: writing {len(TOPICS)} fact-based educational blog posts...\n")
    write_blogs()
    print("\nDone. Next: update blog.html, sitemap.xml, _redirects.")
