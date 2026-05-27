#!/usr/bin/env python3
"""
Phase J — Location / GEO page SEO improvement across all 20 location pages + areas-we-cover.html

For each location page this script:
  1. Makes existing service cards clickable (adds href to service pages)
  2. Injects a service text-block section (before CTA) with links to main service pages
  3. Injects a common-projects section ("common projects requested by homeowners in [area]")
  4. Injects a planning / local authority section
  5. Injects a nearby-areas section
  6. Replaces the existing JSON-LD schema blocks with:
       - WebPage schema  (replaces LocalBusiness)
       - Service schema  with areaServed
       - BreadcrumbList  (already present but upgraded)
       - FAQPage schema  (already present, kept / refreshed)
  7. Fixes the hero badge text for Leicester (was "Serving Leicester city centre" → broader)

Also rewrites areas-we-cover.html as a proper hub page.
"""

import re, json, pathlib

BASE = 'https://www.premium-landscapes.co.uk'

# ─────────────────────────────────────────────
# Per-area data dictionary
# ─────────────────────────────────────────────
AREAS = {
    'landscaping-leicester': {
        'name': 'Leicester',
        'slug': 'landscaping-leicester',
        'postcode': 'LE1–LE5',
        'region': 'Leicestershire',
        'authority': 'Leicester City Council',
        'authority_url': 'https://www.leicester.gov.uk/planning-and-building',
        'serving_badge': 'Serving Leicester & all LE postcodes',
        'distance': 'approximately 5 miles from our Kirby Muxloe base',
        'drive_time': '10–15 minutes',
        'property_profile': 'Leicester has an exceptionally varied housing stock — Victorian terraces and Edwardian semis dominate LE2 and LE3, with modern apartment blocks in the city centre, 1960s–70s council-era housing across LE4 and LE5, and larger detached properties in the outer suburbs. Garden sizes range from compact 20–40m² terrace plots in LE2 to 80m²+ rear gardens on suburban semis in the outer postcodes.',
        'ground': 'Lias clay is widespread through LE1–LE5. It holds water well, which causes patio surfaces to heave and sink if sub-base preparation is inadequate. Every paved project we take on in Leicester is built on a minimum 150mm compacted MOT Type 1 sub-base, with additional allowance on wetter or lower-lying plots.',
        'planning_note': 'Leicester City Council is the local planning authority. Most domestic patio, artificial grass and decking projects fall under permitted development. The New Walk and Victoria Park Conservation Areas impose stricter rules — any work on properties within those boundaries, or fronting the highway, should be checked before installation. We advise on planning requirements at survey stage.',
        'access_note': 'Access can be a challenge in Leicester city. Many Victorian terraces have no side access — all materials have to come through the house. We plan for this and price it into our quotes.',
        'common_projects': [
            'Porcelain and natural stone patios in LE2 terrace rear gardens',
            'Artificial grass installations in compact urban gardens (no mowing, no mud)',
            'Composite decking on raised or split-level Leicester plots',
            'Block paving and resin driveways across Leicester suburbs',
            'Full garden makeovers in Clarendon Park, Stoneygate and Knighton',
        ],
        'nearby': [
            ('landscaping-oadby', 'Oadby'),
            ('landscaping-wigston', 'Wigston'),
            ('landscaping-clarendon-park', 'Clarendon Park'),
            ('landscaping-knighton', 'Knighton'),
            ('landscaping-stoneygate', 'Stoneygate'),
            ('landscaping-glenfield', 'Glenfield'),
            ('landscaping-birstall', 'Birstall'),
            ('landscaping-kirby-muxloe', 'Kirby Muxloe'),
        ],
        'area_desc_hub': 'Leicester city and all LE postcodes — Victorian terraces, Edwardian semis, modern apartments and suburban detached properties across the city.',
    },
    'landscaping-kirby-muxloe': {
        'name': 'Kirby Muxloe',
        'slug': 'landscaping-kirby-muxloe',
        'postcode': 'LE9',
        'region': 'Blaby, Leicestershire',
        'authority': 'Blaby District Council',
        'authority_url': 'https://www.blaby.gov.uk/planning',
        'serving_badge': 'Serving Kirby Muxloe & LE9',
        'distance': 'our home base — 44 Barwell Road, Kirby Muxloe',
        'drive_time': '0 minutes — this is where we are based',
        'property_profile': 'Kirby Muxloe has a diverse mix of stone cottages near the castle conservation area, 1930s–60s semis and detached properties, and newer executive estates off Hinckley Road. Rear gardens on the modern estates typically run 50–90ft; the larger detached homes often exceed 100ft. Some conservation-area properties have irregular-shaped plots that require careful measurement.',
        'ground': 'Ground conditions are mixed across the village — firmer Mercia Mudstone-derived soils near the castle ridge, transitioning to heavier clay toward the Hinckley Road side. Drainage is generally adequate but we specify a deeper sub-base on lower-lying plots and those near the field boundaries at the village edge.',
        'planning_note': 'Blaby District Council is the local planning authority for Kirby Muxloe. The conservation area around Kirby Muxloe Castle means that properties on Main Street and nearby roads may require conservation area consent for external alterations including front garden hard-surfacing and boundary treatments. We check the current rules before quoting on every project.',
        'access_note': 'Most Kirby Muxloe properties have good side or rear access. The older stone properties near the castle may have narrower access; this is priced into the quote where relevant.',
        'common_projects': [
            'Natural stone and porcelain patios sympathetic to conservation-area properties',
            'Block paving and resin driveways on larger detached plots',
            'Artificial grass on executive estate rear gardens',
            'Composite decking and garden lighting packages',
            'Full garden makeovers including pergolas and bespoke outdoor rooms',
        ],
        'nearby': [
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-glenfield', 'Glenfield'),
            ('landscaping-ratby', 'Ratby'),
            ('landscaping-hinckley', 'Hinckley'),
            ('landscaping-narborough', 'Narborough'),
            ('landscaping-enderby', 'Enderby'),
            ('landscaping-blaby', 'Blaby'),
        ],
        'area_desc_hub': 'Our home base — Kirby Muxloe village, LE9. Stone cottages, executive estates, conservation area and large detached plots we know best.',
    },
    'landscaping-oadby': {
        'name': 'Oadby',
        'slug': 'landscaping-oadby',
        'postcode': 'LE2',
        'region': 'Oadby & Wigston, Leicestershire',
        'authority': 'Oadby & Wigston Borough Council',
        'authority_url': 'https://www.owbc.gov.uk/planning',
        'serving_badge': 'Serving Oadby & LE2',
        'distance': 'approximately 7 miles from our Kirby Muxloe base',
        'drive_time': '15–20 minutes',
        'property_profile': 'Oadby is one of Leicestershire\'s most affluent residential areas, characterised by large detached and semi-detached properties on generous plots — many with rear gardens of 100–150ft. 1930s–1950s properties dominate the established streets, with newer executive detached housing on the eastern edge. Garden projects here tend to be medium-to-large scale.',
        'ground': 'Oadby sits on Mercia Mudstone bedrock with a surface layer of clay-rich glacial till. Drainage is variable — properties on the hillside drain freely, those in the lower valley areas near the River Sence can hold water. We assess drainage at survey stage and specify a permeable sub-layer or drainage channel where needed.',
        'planning_note': 'Oadby & Wigston Borough Council handles planning for Oadby. Most residential landscaping is permitted development. Oadby has no designated conservation areas, but listed buildings (mainly on the village green fringe) require listed building consent for external work. Front garden hard-surfacing for driveways requires SuDS-compliant permeable surfacing if replacing grass.',
        'access_note': 'Oadby properties generally have good vehicular access and wide driveways. Materials delivery is typically straightforward on the main residential streets.',
        'common_projects': [
            'Large porcelain and sandstone patio installations on generous rear plots',
            'Composite decking with integrated garden lighting',
            'Full garden makeovers — design-and-build from initial concept',
            'Resin bound driveways replacing tired block paving',
            'Artificial grass on family rear gardens for low-maintenance lawns',
        ],
        'nearby': [
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-wigston', 'Wigston'),
            ('landscaping-knighton', 'Knighton'),
            ('landscaping-stoneygate', 'Stoneygate'),
            ('landscaping-clarendon-park', 'Clarendon Park'),
            ('landscaping-blaby', 'Blaby'),
            ('landscaping-narborough', 'Narborough'),
        ],
        'area_desc_hub': 'Oadby, LE2 — one of Leicestershire\'s most desirable residential areas, with large plots and strong demand for premium patio and garden design work.',
    },
    'landscaping-wigston': {
        'name': 'Wigston',
        'slug': 'landscaping-wigston',
        'postcode': 'LE18',
        'region': 'Oadby & Wigston, Leicestershire',
        'authority': 'Oadby & Wigston Borough Council',
        'authority_url': 'https://www.owbc.gov.uk/planning',
        'serving_badge': 'Serving Wigston & LE18',
        'distance': 'approximately 8 miles from our Kirby Muxloe base',
        'drive_time': '15–20 minutes',
        'property_profile': 'Wigston has a varied housing mix — 1920s–1950s semis in Wigston Magna and South Wigston, later 1960s–80s estates, and newer developments toward Glen Parva. Gardens in the older semis are typically 40–70ft with good width; the newer estates run slightly smaller but with fewer access constraints.',
        'ground': 'Wigston\'s geology is predominantly clay-rich Mercia Mudstone. The South Wigston area in particular can have high groundwater during winter — French drain channels or aggregate drainage layers are often specified on lower-lying plots. Sub-base preparation is critical here.',
        'planning_note': 'Oadby & Wigston Borough Council is the local planning authority. South Wigston has a Conservation Area covering the historic textile workers\' housing on Bull Head Street and surrounds — permitted development restrictions apply to properties within it. Standard residential patio, decking and artificial grass installations outside the conservation area are generally permitted development.',
        'access_note': 'Most Wigston properties have side or rear gate access. Semi-detached houses in South Wigston often share a rear alleyway, which can serve as a materials route if agreed with the neighbour.',
        'common_projects': [
            'Patio installations in porcelain and block paving on semi-detached plots',
            'Artificial grass in mid-size rear gardens',
            'Composite decking for raised or terraced rear gardens',
            'New driveways replacing concrete or tarmac on 1930s–50s semis',
            'Garden lighting systems added to existing landscaping',
        ],
        'nearby': [
            ('landscaping-oadby', 'Oadby'),
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-blaby', 'Blaby'),
            ('landscaping-narborough', 'Narborough'),
            ('landscaping-enderby', 'Enderby'),
            ('landscaping-knighton', 'Knighton'),
            ('landscaping-cosby', 'Cosby'),
        ],
        'area_desc_hub': 'Wigston, LE18 — mixed 1920s–80s residential with strong demand for patio, driveway and garden makeover projects.',
    },
    'landscaping-clarendon-park': {
        'name': 'Clarendon Park',
        'slug': 'landscaping-clarendon-park',
        'postcode': 'LE2',
        'region': 'Leicester, Leicestershire',
        'authority': 'Leicester City Council',
        'authority_url': 'https://www.leicester.gov.uk/planning-and-building',
        'serving_badge': 'Serving Clarendon Park & LE2',
        'distance': 'approximately 5 miles from our Kirby Muxloe base',
        'drive_time': '10–15 minutes',
        'property_profile': 'Clarendon Park is a sought-after Victorian and Edwardian residential suburb of Leicester. Bay-fronted Victorian terraces and larger Edwardian semis and detached houses characterise the area. Rear gardens are typically 20–50ft long with limited width — common in Victorian terrace footprints. Many properties have no side access, requiring materials to be carried through the house.',
        'ground': 'Lias clay predominates across Clarendon Park. Victorian terraces were often built on minimal foundations; existing patios or paths may be sitting on inadequate sub-bases. Full dig-out to at least 200mm followed by compacted Type 1 is standard practice here.',
        'planning_note': 'Leicester City Council is the local planning authority. Parts of Clarendon Park fall within or adjoin the Leicester Conservation Areas — particularly properties near Victoria Park. Front garden hard-surfacing may require planning permission if it replaces a grass area of 5m² or more without a permeable surface. We advise specifically on your property\'s status at survey stage.',
        'access_note': 'Most Clarendon Park terraces have no side access — all materials must come through the house. We plan this carefully, use protective floor coverings throughout, and never bring a skip without confirming on-street permit with the council first.',
        'common_projects': [
            'Compact courtyard patios in porcelain — maximising usable space in terrace rear gardens',
            'Artificial grass replacing worn or muddy lawn areas',
            'Raised planter beds and sleeper walls alongside patio redesigns',
            'Garden lighting in compact terrace gardens',
            'Front garden improvements with compliant permeable surfaces',
        ],
        'nearby': [
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-knighton', 'Knighton'),
            ('landscaping-stoneygate', 'Stoneygate'),
            ('landscaping-oadby', 'Oadby'),
            ('landscaping-wigston', 'Wigston'),
        ],
        'area_desc_hub': 'Clarendon Park, LE2 — Victorian and Edwardian suburb with compact terrace gardens and strong demand for courtyard patio and garden design projects.',
    },
    'landscaping-knighton': {
        'name': 'Knighton',
        'slug': 'landscaping-knighton',
        'postcode': 'LE2',
        'region': 'Leicester, Leicestershire',
        'authority': 'Leicester City Council',
        'authority_url': 'https://www.leicester.gov.uk/planning-and-building',
        'serving_badge': 'Serving Knighton & LE2',
        'distance': 'approximately 6 miles from our Kirby Muxloe base',
        'drive_time': '12–18 minutes',
        'property_profile': 'Knighton is one of Leicester\'s most desirable residential neighbourhoods, characterised by large Edwardian and inter-war detached and semi-detached properties. Many properties have generous rear gardens of 60–100ft and in some cases rear access via a back lane or wide side gate. The area attracts higher-specification landscaping projects.',
        'ground': 'Lias clay is present throughout Knighton but is generally firmer than in lower-lying parts of the city. The well-established tree cover on older streets means tree root zones must be respected during excavation — we check the local TPO (Tree Preservation Order) register before any dig-out commences.',
        'planning_note': 'Leicester City Council is the planning authority. Knighton contains several listed buildings and is close to conservation area boundaries — properties on the historic streets should confirm their status before undertaking external works. The council\'s online planning portal allows postcode searches for relevant designations.',
        'access_note': 'Many Knighton properties have wide side access or rear lane access — conditions are generally favourable for larger landscaping projects. Tree-lined streets may require permit-to-work if branches overhang working areas.',
        'common_projects': [
            'Large-format porcelain patio installations with seating walls and raised beds',
            'Composite decking with integrated LED lighting schemes',
            'Full garden makeovers — design, hard landscaping and planting',
            'Resin bound driveways on generous front-facing plots',
            'Garden lighting systems on mature established gardens',
        ],
        'nearby': [
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-clarendon-park', 'Clarendon Park'),
            ('landscaping-stoneygate', 'Stoneygate'),
            ('landscaping-oadby', 'Oadby'),
            ('landscaping-wigston', 'Wigston'),
        ],
        'area_desc_hub': 'Knighton, LE2 — one of Leicester\'s most desirable suburbs, with large Edwardian plots and high demand for premium garden design and patio work.',
    },
    'landscaping-stoneygate': {
        'name': 'Stoneygate',
        'slug': 'landscaping-stoneygate',
        'postcode': 'LE2',
        'region': 'Leicester, Leicestershire',
        'authority': 'Leicester City Council',
        'authority_url': 'https://www.leicester.gov.uk/planning-and-building',
        'serving_badge': 'Serving Stoneygate & LE2',
        'distance': 'approximately 5 miles from our Kirby Muxloe base',
        'drive_time': '10–15 minutes',
        'property_profile': 'Stoneygate is among Leicester\'s premier residential districts, known for its Victorian villas, large Edwardian detached properties and mature tree-lined avenues. Properties typically have substantial rear gardens — 60–120ft is common — along with mature boundary planting and outbuildings. Projects in Stoneygate are often high-specification and budget-appropriate.',
        'ground': 'Lias clay with mature organic topsoil on established gardens. Tree root zones require careful management on the older estate properties. We commission site-specific ground assessment on larger projects where tree proximity or drainage history warrants it.',
        'planning_note': 'Leicester City Council handles planning for Stoneygate. The Stoneygate Conservation Area covers a significant part of the residential streets — properties within it face tighter permitted development rules. Front garden hard-surfacing, boundary wall alterations, outbuilding additions and some decking/patio configurations may require planning consent. We carry out a planning compliance check at no charge as part of the survey visit.',
        'access_note': 'Most Stoneygate properties have adequate side access; some Victorian villas have gated rear access via service lanes. Parking for operatives and delivery vehicles can be managed with short-term loading exemptions.',
        'common_projects': [
            'Premium porcelain and natural stone patio installations on large rear gardens',
            'Full garden design-and-build projects including structural planting',
            'Composite decking with lighting and privacy screening',
            'Resin bound driveways on mature detached-house frontages',
            'Garden wall and boundary restoration alongside new hard landscaping',
        ],
        'nearby': [
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-knighton', 'Knighton'),
            ('landscaping-clarendon-park', 'Clarendon Park'),
            ('landscaping-oadby', 'Oadby'),
            ('landscaping-wigston', 'Wigston'),
        ],
        'area_desc_hub': 'Stoneygate, LE2 — Leicester\'s premier Victorian villa district. Conservation area, large plots, and high-specification landscaping demand.',
    },
    'landscaping-narborough': {
        'name': 'Narborough',
        'slug': 'landscaping-narborough',
        'postcode': 'LE19',
        'region': 'Blaby, Leicestershire',
        'authority': 'Blaby District Council',
        'authority_url': 'https://www.blaby.gov.uk/planning',
        'serving_badge': 'Serving Narborough & LE19',
        'distance': 'approximately 8 miles from our Kirby Muxloe base',
        'drive_time': '15 minutes via the A46',
        'property_profile': 'Narborough is a substantial village and residential area in Blaby District. The housing mix runs from older village-centre properties on Station Road and Leicester Road through 1970s–80s estates to significant newer developments off Enderby Road. Garden sizes are typically 40–80ft on the established estates; newer builds may be smaller.',
        'ground': 'The Narborough area sits on Mercia Mudstone with some river-valley alluvium near the River Soar floodplain. Properties close to the Soar should confirm they are not in a flood-risk zone before undertaking significant hard-surfacing — we check Environment Agency maps as part of our pre-survey assessment.',
        'planning_note': 'Blaby District Council is the local planning authority for Narborough. Most domestic patio, decking and garden work is permitted development. Any driveway replacing a grass front garden requires a SuDS-compliant permeable surface or a planning application — block paving with permeable jointing or resin bound gravel both comply. We advise on the correct surface specification for each project.',
        'access_note': 'The majority of Narborough properties have good side or rear access. Some of the older village-centre properties have limited access width — assessed at survey.',
        'common_projects': [
            'Block paving and resin bound driveways on semi-detached and detached houses',
            'Patio installations in porcelain and natural stone',
            'Artificial grass in family rear gardens',
            'Garden lighting additions to existing patios and decking',
            'Full garden makeovers combining patio, artificial grass and planting',
        ],
        'nearby': [
            ('landscaping-enderby', 'Enderby'),
            ('landscaping-blaby', 'Blaby'),
            ('landscaping-wigston', 'Wigston'),
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-kirby-muxloe', 'Kirby Muxloe'),
            ('landscaping-cosby', 'Cosby'),
        ],
        'area_desc_hub': 'Narborough, LE19 — growing village southwest of Leicester with 1970s–80s estates and newer builds, good demand for driveway and patio work.',
    },
    'landscaping-glenfield': {
        'name': 'Glenfield',
        'slug': 'landscaping-glenfield',
        'postcode': 'LE3',
        'region': 'Blaby, Leicestershire',
        'authority': 'Blaby District Council',
        'authority_url': 'https://www.blaby.gov.uk/planning',
        'serving_badge': 'Serving Glenfield & LE3',
        'distance': 'approximately 4 miles from our Kirby Muxloe base',
        'drive_time': '8–12 minutes',
        'property_profile': 'Glenfield is a large residential village immediately northwest of Leicester, characterised by inter-war semis, 1960s–70s detached and semi-detached estates, and newer cul-de-sac developments. Rear gardens are typically 40–70ft; some of the larger 1970s detached properties have wider plots suitable for feature landscaping.',
        'ground': 'Glenfield sits on Charnian igneous and metamorphic rocks to the north, transitioning to Mercia Mudstone toward the village centre and southern edge. The Charnian ground is firmer and better-draining; the clay-influenced areas to the south need deeper sub-base preparation.',
        'planning_note': 'Blaby District Council is the local planning authority. Glenfield does not have a designated conservation area but borders the Charnwood Forest fringe, where landscape character is a material planning consideration. Standard domestic landscaping is generally permitted development; we confirm at survey stage.',
        'access_note': 'Most Glenfield residential streets have good side access. The cul-de-sac estates have wide access to rear gardens; materials delivery is straightforward in most cases.',
        'common_projects': [
            'Patio installations in porcelain and block paving on 1970s detached plots',
            'Artificial grass in family gardens replacing tired natural turf',
            'Composite decking as an extension to an existing patio',
            'New driveways on front gardens of 1960s–70s semis',
            'Full garden makeovers on larger plots including lighting and planting',
        ],
        'nearby': [
            ('landscaping-kirby-muxloe', 'Kirby Muxloe'),
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-ratby', 'Ratby'),
            ('landscaping-birstall', 'Birstall'),
            ('landscaping-anstey', 'Anstey'),
            ('landscaping-narborough', 'Narborough'),
        ],
        'area_desc_hub': 'Glenfield, LE3 — large residential village northwest of Leicester, close to our base, with 1960s–70s estates and newer cul-de-sacs.',
    },
    'landscaping-blaby': {
        'name': 'Blaby',
        'slug': 'landscaping-blaby',
        'postcode': 'LE8',
        'region': 'Blaby, Leicestershire',
        'authority': 'Blaby District Council',
        'authority_url': 'https://www.blaby.gov.uk/planning',
        'serving_badge': 'Serving Blaby & LE8',
        'distance': 'approximately 9 miles from our Kirby Muxloe base',
        'drive_time': '18–22 minutes',
        'property_profile': 'Blaby town and village is a mix of 1930s–50s semis and bungalows in the original village, 1970s–80s residential estates, and extensive newer development around the village fringe. It is the administrative centre of Blaby District. Garden sizes vary — semis typically 40–60ft, newer builds slightly smaller.',
        'ground': 'Mercia Mudstone with a clay surface layer typical of south Leicestershire. Drainage is generally adequate on established plots; newer estates on previously agricultural land can have residual waterlogging issues in the first years. We use a compacted Type 1 sub-base of minimum 100mm on all paved surfaces.',
        'planning_note': 'Blaby District Council administers planning for Blaby itself. The town does not have a designated conservation area, simplifying permitted development for most domestic landscaping projects. New driveways over 5m² replacing grass or non-permeable surfaces should use permeable materials or be subject to a planning application.',
        'access_note': 'Blaby properties generally have good access. Village-centre properties may have period boundaries or shared access arrangements — clarified at survey.',
        'common_projects': [
            'Block paving and resin bound driveways on 1970s–80s semis',
            'Patio installations on rear gardens of varied sizes',
            'Artificial grass as a low-maintenance lawn replacement',
            'Garden lighting on existing patio areas',
            'Full garden redesigns on larger detached plots at the village edge',
        ],
        'nearby': [
            ('landscaping-narborough', 'Narborough'),
            ('landscaping-wigston', 'Wigston'),
            ('landscaping-cosby', 'Cosby'),
            ('landscaping-enderby', 'Enderby'),
            ('landscaping-oadby', 'Oadby'),
            ('landscaping-leicester', 'Leicester'),
        ],
        'area_desc_hub': 'Blaby, LE8 — administrative centre of Blaby District, mixed 1930s–80s residential and newer builds, good patio and driveway demand.',
    },
    'landscaping-birstall': {
        'name': 'Birstall',
        'slug': 'landscaping-birstall',
        'postcode': 'LE4',
        'region': 'Charnwood, Leicestershire',
        'authority': 'Charnwood Borough Council',
        'authority_url': 'https://www.charnwood.gov.uk/planning',
        'serving_badge': 'Serving Birstall & LE4',
        'distance': 'approximately 7 miles from our Kirby Muxloe base',
        'drive_time': '15 minutes',
        'property_profile': 'Birstall is a large suburban village north of Leicester, characterised by 1930s–60s semis and detached houses on the established streets, with significant newer executive development off Birstall Street Road. Gardens on the older semis are typically 40–70ft with moderate width; the newer executive properties often have wider plots with better access.',
        'ground': 'Birstall sits above the River Soar valley on glacial till overlying Mercia Mudstone. Drainage is generally good on the higher ground but can be slow on some of the lower-lying streets near the Soar floodplain. Standard 100–150mm compacted Type 1 sub-base is our minimum specification for all paved surfaces.',
        'planning_note': 'Charnwood Borough Council is the local planning authority for Birstall. Birstall does not have a designated conservation area but lies within Charnwood Borough which has active local plan policies on garden development and hard-surfacing. Standard domestic landscaping is generally permitted development. We confirm planning status at survey.',
        'access_note': 'Birstall properties typically have reasonable side access. Some of the larger 1930s detached properties have gated side access wide enough for a wheelbarrow or narrow dumper. Assessed at survey on a property-by-property basis.',
        'common_projects': [
            'Patio installations in porcelain and natural stone',
            'Artificial grass in 1950s–60s rear gardens replacing ageing turf',
            'Composite decking on raised rear terraces',
            'Block paving driveways on generous front-facing plots',
            'Full garden makeovers on newer executive properties',
        ],
        'nearby': [
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-glenfield', 'Glenfield'),
            ('landscaping-syston', 'Syston'),
            ('landscaping-anstey', 'Anstey'),
            ('landscaping-thurmaston', 'Thurmaston'),
            ('landscaping-loughborough', 'Loughborough'),
        ],
        'area_desc_hub': 'Birstall, LE4 — large suburban village north of Leicester with 1930s–60s semis and newer executive properties.',
    },
    'landscaping-syston': {
        'name': 'Syston',
        'slug': 'landscaping-syston',
        'postcode': 'LE7',
        'region': 'Charnwood, Leicestershire',
        'authority': 'Charnwood Borough Council',
        'authority_url': 'https://www.charnwood.gov.uk/planning',
        'serving_badge': 'Serving Syston & LE7',
        'distance': 'approximately 8 miles from our Kirby Muxloe base',
        'drive_time': '20 minutes via the A46',
        'property_profile': 'Syston is a market town in Charnwood Borough, northeast of Leicester. The housing mix spans Victorian terraces in the town centre, 1950s–70s residential estates, and newer developments toward the A46 edge. Rear gardens on the older streets are compact (30–50ft); 1970s estate properties tend to have more generous plots.',
        'ground': 'Syston sits on the Soar Valley alluvium and river terrace deposits — some areas have high groundwater tables and impeded drainage. Patio and driveway projects near the river floodplain should factor in a permeable or drainage-enhanced sub-base. We assess drainage at survey stage.',
        'planning_note': 'Charnwood Borough Council is the local planning authority. Syston\'s historic town centre streets contain some listed buildings — work on or adjacent to these requires listed building consent. Standard domestic landscaping on non-listed properties is generally permitted development. Syston falls outside the National Forest but within Charnwood\'s landscape character areas, which may be a material consideration for larger external works.',
        'access_note': 'Town-centre terraces in Syston have limited rear access (common alleyways shared with neighbours). Estate properties have better side access. We plan access at survey.',
        'common_projects': [
            'Patio installations on 1970s estate rear gardens',
            'Artificial grass replacing worn turf in family gardens',
            'Block paving driveways replacing concrete or tarmac',
            'Garden lighting and composite decking additions',
            'Full garden makeovers on larger Syston plots',
        ],
        'nearby': [
            ('landscaping-birstall', 'Birstall'),
            ('landscaping-thurmaston', 'Thurmaston'),
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-anstey', 'Anstey'),
            ('landscaping-loughborough', 'Loughborough'),
        ],
        'area_desc_hub': 'Syston, LE7 — Charnwood market town northeast of Leicester, with mixed Victorian terraces and 1970s estates.',
    },
    'landscaping-hinckley': {
        'name': 'Hinckley',
        'slug': 'landscaping-hinckley',
        'postcode': 'LE10',
        'region': 'Hinckley & Bosworth, Leicestershire',
        'authority': 'Hinckley & Bosworth Borough Council',
        'authority_url': 'https://www.hinckley-bosworth.gov.uk/planning',
        'serving_badge': 'Serving Hinckley & LE10',
        'distance': 'approximately 14 miles from our Kirby Muxloe base',
        'drive_time': '20–25 minutes via the A47',
        'property_profile': 'Hinckley is a market town and one of the larger centres in Hinckley & Bosworth Borough. The housing stock ranges from Victorian terraces in the town centre through 1930s–60s semis on the established residential streets to large executive estates on the town edges. The larger estate properties on the south and east of town have generous rear gardens of 60–100ft.',
        'ground': 'Hinckley sits on Triassic Mercia Mudstone with local alluvial deposits near the Sketchley Brook. Clay soils dominate — sub-base preparation is critical, particularly on lower-lying plots. The borough\'s geology is broadly similar to the Kirby Muxloe area to the east.',
        'planning_note': 'Hinckley & Bosworth Borough Council administers planning for Hinckley. The town centre has a Conservation Area covering the historic market town streets — properties within it have tighter permitted development restrictions. The council\'s planning portal provides postcode-level conservation area information. Standard domestic patio, decking and garden work on non-designated properties is generally permitted development.',
        'access_note': 'Town-centre terraces have limited rear access. Estate properties on the town edges have good side or rear vehicular access. We plan materials delivery routes at survey stage.',
        'common_projects': [
            'Patio and driveway installations on larger estate properties',
            'Artificial grass in family gardens across Hinckley\'s residential estates',
            'Composite decking additions to existing garden areas',
            'Block paving and resin bound driveways across the town',
            'Garden lighting and full garden makeovers on larger plots',
        ],
        'nearby': [
            ('landscaping-kirby-muxloe', 'Kirby Muxloe'),
            ('landscaping-ratby', 'Ratby'),
            ('landscaping-markfield', 'Markfield'),
            ('landscaping-narborough', 'Narborough'),
            ('landscaping-leicester', 'Leicester'),
        ],
        'area_desc_hub': 'Hinckley, LE10 — market town in Hinckley & Bosworth, 14 miles from our base, with Victorian terraces and large estate properties.',
    },
    'landscaping-loughborough': {
        'name': 'Loughborough',
        'slug': 'landscaping-loughborough',
        'postcode': 'LE11',
        'region': 'Charnwood, Leicestershire',
        'authority': 'Charnwood Borough Council',
        'authority_url': 'https://www.charnwood.gov.uk/planning',
        'serving_badge': 'Serving Loughborough & LE11',
        'distance': 'approximately 14 miles from our Kirby Muxloe base',
        'drive_time': '20–25 minutes via the A6',
        'property_profile': 'Loughborough is a university town and the largest settlement in Charnwood Borough. The housing stock is diverse — Victorian terraces in the inner residential areas, 1920s–50s semis and detached houses on the established streets, university-era 1960s–70s estates, and newer executive developments on the town perimeter. Garden sizes range from compact terrace plots to generous detached-house gardens of 80ft+.',
        'ground': 'Loughborough sits on river terrace gravels and alluvial deposits over Mercia Mudstone. The Soar Valley to the west has higher groundwater; the higher ground to the east (toward Quorn and Barrow) drains more freely. Sub-base specification is site-specific — we assess at survey.',
        'planning_note': 'Charnwood Borough Council handles planning for Loughborough. The town centre and several inner residential streets are designated Conservation Areas. Loughborough\'s Conservation Areas include the town centre, parts of Epinal Way and the historic residential streets around Queen\'s Park. Properties within these areas have tighter permitted development rules for external alterations.',
        'access_note': 'Inner-town terraces typically have limited rear access. Outer estates generally have good side or rear vehicular access. University-area properties may have complex access arrangements — assessed at survey.',
        'common_projects': [
            'Patio installations on established residential gardens in Loughborough',
            'Artificial grass in family and rental-property rear gardens',
            'Composite decking and garden lighting combinations',
            'Driveway replacements across Loughborough\'s semi-detached streets',
            'Full garden makeovers on the larger outer-town estate properties',
        ],
        'nearby': [
            ('landscaping-syston', 'Syston'),
            ('landscaping-birstall', 'Birstall'),
            ('landscaping-anstey', 'Anstey'),
            ('landscaping-thurmaston', 'Thurmaston'),
            ('landscaping-leicester', 'Leicester'),
        ],
        'area_desc_hub': 'Loughborough, LE11 — Charnwood\'s largest town, with a university and diverse housing from Victorian terraces to newer executive estates.',
    },
    'landscaping-cosby': {
        'name': 'Cosby',
        'slug': 'landscaping-cosby',
        'postcode': 'LE9',
        'region': 'Blaby, Leicestershire',
        'authority': 'Blaby District Council',
        'authority_url': 'https://www.blaby.gov.uk/planning',
        'serving_badge': 'Serving Cosby & LE9',
        'distance': 'approximately 10 miles from our Kirby Muxloe base',
        'drive_time': '18–22 minutes',
        'property_profile': 'Cosby is a village in Blaby District, south of Leicester near the A426. The housing mix includes older village-centre properties, 1960s–80s infill estates, and some newer detached housing at the village edge. Rear gardens on the established estate properties are typically 40–70ft.',
        'ground': 'Cosby sits on Mercia Mudstone with clay topsoil typical of south Leicestershire. The lower-lying parts of the village toward the Cosby Brook can be slow-draining. Standard compacted sub-base preparation is specified on all paved surfaces.',
        'planning_note': 'Blaby District Council is the local planning authority. Cosby does not have a designated conservation area at the time of writing. Most domestic landscaping is permitted development; driveway replacement over 5m² requires permeable surfacing or a planning application. Check the current Blaby LPA planning portal for the latest guidance.',
        'access_note': 'Cosby village properties generally have good garden access. Some older village-centre properties have restricted side access — assessed at survey.',
        'common_projects': [
            'Patio installations replacing worn slabs on 1970s–80s rear gardens',
            'Artificial grass in village-edge family gardens',
            'Driveway resurfacing on detached and semi-detached houses',
            'Garden lighting additions and composite decking',
            'Full garden makeovers on larger Cosby plots',
        ],
        'nearby': [
            ('landscaping-blaby', 'Blaby'),
            ('landscaping-narborough', 'Narborough'),
            ('landscaping-wigston', 'Wigston'),
            ('landscaping-enderby', 'Enderby'),
            ('landscaping-kirby-muxloe', 'Kirby Muxloe'),
        ],
        'area_desc_hub': 'Cosby, LE9 — village in Blaby District south of Leicester, with 1960s–80s estate housing and village-centre properties.',
    },
    'landscaping-enderby': {
        'name': 'Enderby',
        'slug': 'landscaping-enderby',
        'postcode': 'LE19',
        'region': 'Blaby, Leicestershire',
        'authority': 'Blaby District Council',
        'authority_url': 'https://www.blaby.gov.uk/planning',
        'serving_badge': 'Serving Enderby & LE19',
        'distance': 'approximately 7 miles from our Kirby Muxloe base',
        'drive_time': '12–15 minutes',
        'property_profile': 'Enderby is a large village and civil parish immediately southwest of Leicester, bordering Narborough. The housing stock ranges from older village-centre properties on Mill Hill Road through 1970s–80s estates to significant newer development near the A563 ring road. Plots on the established estates are typically 40–70ft.',
        'ground': 'Enderby sits on Mercia Mudstone, with firmer Pre-Cambrian Charnian rock outcropping on Enderby Hill — one of the distinctive high points of the village. Garden ground conditions are generally good on the elevated properties; some lower-lying areas toward the Soar floodplain have slower drainage.',
        'planning_note': 'Blaby District Council is the local planning authority for Enderby. Standard domestic landscaping is generally permitted development. The village has some historic buildings near the church but no formal conservation area designation at the time of writing. Driveway replacement over 5m² requires a permeable surface specification or a planning application.',
        'access_note': 'Enderby properties generally have good rear garden access. Village-centre properties on Mill Hill Road may have narrower access — assessed at survey.',
        'common_projects': [
            'Patio installations in porcelain and natural stone on established rear gardens',
            'Artificial grass for family gardens on Enderby estates',
            'New driveways on semi-detached and detached houses',
            'Composite decking additions alongside existing patio areas',
            'Full garden makeovers on larger village-edge properties',
        ],
        'nearby': [
            ('landscaping-narborough', 'Narborough'),
            ('landscaping-blaby', 'Blaby'),
            ('landscaping-wigston', 'Wigston'),
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-kirby-muxloe', 'Kirby Muxloe'),
            ('landscaping-cosby', 'Cosby'),
        ],
        'area_desc_hub': 'Enderby, LE19 — large Blaby District village bordering Narborough, with 1970s–80s estates and newer development near the ring road.',
    },
    'landscaping-anstey': {
        'name': 'Anstey',
        'slug': 'landscaping-anstey',
        'postcode': 'LE7',
        'region': 'Charnwood, Leicestershire',
        'authority': 'Charnwood Borough Council',
        'authority_url': 'https://www.charnwood.gov.uk/planning',
        'serving_badge': 'Serving Anstey & LE7',
        'distance': 'approximately 7 miles from our Kirby Muxloe base',
        'drive_time': '15 minutes',
        'property_profile': 'Anstey is a village northwest of Leicester in Charnwood Borough, adjacent to the Charnwood Forest fringe. The housing stock includes older village properties, 1950s–70s council and private estates, and newer development on the village edge. Gardens on the mid-century estates are typically 40–70ft.',
        'ground': 'Anstey sits on Charnian igneous and metamorphic rock (resistant to excavation) with clay soil in the valley areas. The firmer Charnian bedrock at shallow depth means excavation is harder than in flat clay areas — we factor this into our pricing. Drainage on the higher ground is generally good.',
        'planning_note': 'Charnwood Borough Council is the local planning authority. Anstey is on the edge of the Charnwood Forest, and landscape character is a material planning consideration for larger external works. Standard domestic patio, decking and garden work is generally permitted development. The council may have landscape character guidance relevant to larger projects near the forest fringe.',
        'access_note': 'Anstey village properties have varied access — older terraces more constrained, estates generally good. Assessed at survey.',
        'common_projects': [
            'Patio installations on 1960s–70s residential rear gardens',
            'Artificial grass in family gardens replacing natural turf',
            'Block paving driveways on semi-detached and detached properties',
            'Garden lighting and decking combinations',
            'Full garden makeovers on larger Anstey plots',
        ],
        'nearby': [
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-glenfield', 'Glenfield'),
            ('landscaping-birstall', 'Birstall'),
            ('landscaping-ratby', 'Ratby'),
            ('landscaping-syston', 'Syston'),
            ('landscaping-loughborough', 'Loughborough'),
        ],
        'area_desc_hub': 'Anstey, LE7 — Charnwood village on the Charnwood Forest fringe, northwest of Leicester.',
    },
    'landscaping-markfield': {
        'name': 'Markfield',
        'slug': 'landscaping-markfield',
        'postcode': 'LE67',
        'region': 'Hinckley & Bosworth, Leicestershire',
        'authority': 'Hinckley & Bosworth Borough Council',
        'authority_url': 'https://www.hinckley-bosworth.gov.uk/planning',
        'serving_badge': 'Serving Markfield & LE67',
        'distance': 'approximately 10 miles from our Kirby Muxloe base',
        'drive_time': '18–22 minutes via the A50',
        'property_profile': 'Markfield is a village in Hinckley & Bosworth Borough at the southern edge of Charnwood Forest. The village has a mix of older granite-built properties in the historic centre, 1960s–80s estates, and newer executive development at the village edges. Granite-built properties often have irregular plot shapes and older boundary walls.',
        'ground': 'Markfield sits on Pre-Cambrian Charnian igneous and metamorphic rocks — the same hard Mountsorrel granite quarried locally. This means sub-base excavation may encounter very hard bedrock at depth. We assess at survey and may recommend a shallower but well-compacted build-up where bedrock is very close to the surface.',
        'planning_note': 'Hinckley & Bosworth Borough Council is the local planning authority. Markfield lies within the Charnwood Forest landscape character area, which may be a material planning consideration for larger external works or boundary treatments. Standard domestic landscaping is generally permitted development. The council planning portal should be checked for current designations.',
        'access_note': 'Village-centre granite properties may have tight access. Estate properties have good side access in most cases. Assessed at survey.',
        'common_projects': [
            'Patio installations on Markfield estate rear gardens',
            'Natural stone patios sympathetic to the granite-built village character',
            'Artificial grass and low-maintenance garden redesigns',
            'Driveway installations on the larger edge-of-village properties',
            'Garden lighting and composite decking',
        ],
        'nearby': [
            ('landscaping-anstey', 'Anstey'),
            ('landscaping-ratby', 'Ratby'),
            ('landscaping-glenfield', 'Glenfield'),
            ('landscaping-hinckley', 'Hinckley'),
            ('landscaping-kirby-muxloe', 'Kirby Muxloe'),
        ],
        'area_desc_hub': 'Markfield, LE67 — Charnwood Forest-edge village in Hinckley & Bosworth, with granite-built properties and newer estate housing.',
    },
    'landscaping-ratby': {
        'name': 'Ratby',
        'slug': 'landscaping-ratby',
        'postcode': 'LE6',
        'region': 'Hinckley & Bosworth, Leicestershire',
        'authority': 'Hinckley & Bosworth Borough Council',
        'authority_url': 'https://www.hinckley-bosworth.gov.uk/planning',
        'serving_badge': 'Serving Ratby & LE6',
        'distance': 'approximately 5 miles from our Kirby Muxloe base',
        'drive_time': '10 minutes',
        'property_profile': 'Ratby is a village in Hinckley & Bosworth Borough, adjacent to Kirby Muxloe. The housing mix includes the older village core on Main Street and Bardon Road, 1960s–70s residential estates, and newer cul-de-sac development. Garden sizes on the estates are typically 40–70ft; some of the older village properties have larger irregular-shaped plots.',
        'ground': 'Ratby sits on mixed Charnian and Mercia Mudstone geology. Ground conditions are firmer on the higher ground toward the north of the village; clay-influenced to the south and east. Sub-base preparation is standard — we adjust depth based on the ground conditions found at survey.',
        'planning_note': 'Hinckley & Bosworth Borough Council administers planning for Ratby. There is no designated conservation area in Ratby village at the time of writing. Standard domestic landscaping is generally permitted development. We confirm at survey.',
        'access_note': 'Ratby properties have generally good side or rear access on the estate streets. Older village-centre properties on Main Street may have more restricted access.',
        'common_projects': [
            'Patio installations in porcelain and natural stone on Ratby rear gardens',
            'Artificial grass in family gardens on the 1960s–70s estates',
            'Block paving and resin driveways on semi-detached properties',
            'Composite decking additions to existing garden areas',
            'Garden lighting on new and existing landscaping',
        ],
        'nearby': [
            ('landscaping-kirby-muxloe', 'Kirby Muxloe'),
            ('landscaping-glenfield', 'Glenfield'),
            ('landscaping-anstey', 'Anstey'),
            ('landscaping-markfield', 'Markfield'),
            ('landscaping-hinckley', 'Hinckley'),
        ],
        'area_desc_hub': 'Ratby, LE6 — village adjacent to Kirby Muxloe in Hinckley & Bosworth, with 1960s–70s estates and older village-centre properties.',
    },
    'landscaping-thurmaston': {
        'name': 'Thurmaston',
        'slug': 'landscaping-thurmaston',
        'postcode': 'LE4',
        'region': 'Charnwood, Leicestershire',
        'authority': 'Charnwood Borough Council',
        'authority_url': 'https://www.charnwood.gov.uk/planning',
        'serving_badge': 'Serving Thurmaston & LE4',
        'distance': 'approximately 9 miles from our Kirby Muxloe base',
        'drive_time': '18 minutes',
        'property_profile': 'Thurmaston is a large village northeast of Leicester in Charnwood Borough, along the Soar Valley. The housing stock is predominantly 1960s–80s semi-detached and detached houses on residential estates. Rear gardens are typically 40–70ft with reasonable access on most estate streets.',
        'ground': 'Thurmaston sits on Soar Valley alluvium and river terrace gravels — drainage can be impeded on lower-lying plots near the Soar. We check Environment Agency flood maps and assess garden drainage at survey stage. The gravel subsoil drains better than clay but can require a compacted Type 1 sub-base to prevent differential settlement.',
        'planning_note': 'Charnwood Borough Council is the local planning authority. Thurmaston has no designated conservation area. Standard domestic landscaping is generally permitted development in the borough. Front garden hard-surfacing for driveways should use permeable materials if replacing grass.',
        'access_note': 'Most Thurmaston estate properties have good side or rear gate access. Streets are generally wide enough for delivery vehicles. Assessed at survey for any access constraints.',
        'common_projects': [
            'Patio installations on 1970s–80s rear gardens',
            'Artificial grass in family rear gardens',
            'New block paving and resin driveways across Thurmaston\'s residential streets',
            'Composite decking and garden lighting additions',
            'Full garden redesigns on larger Thurmaston properties',
        ],
        'nearby': [
            ('landscaping-birstall', 'Birstall'),
            ('landscaping-syston', 'Syston'),
            ('landscaping-leicester', 'Leicester'),
            ('landscaping-anstey', 'Anstey'),
            ('landscaping-loughborough', 'Loughborough'),
        ],
        'area_desc_hub': 'Thurmaston, LE4 — large Charnwood village northeast of Leicester, with 1960s–80s estate housing along the Soar Valley.',
    },
}

# ─────────────────────────────────────────────
# HTML snippet generators
# ─────────────────────────────────────────────

def service_links_section(a):
    name = a['name']
    return f'''
    <!-- Service Links Section (Phase J) -->
    <section class="py-16 px-4 bg-white">
        <div class="container mx-auto max-w-5xl">
            <h2 class="font-heading font-bold text-3xl text-gray-900 mb-4">Landscaping Services Available in {name}</h2>
            <p class="text-gray-600 mb-10">Premium Landscapes provides the full range of landscaping services to homeowners in {name} and the surrounding {a["postcode"]} postcode area. Each service is described briefly below — click through for full details including materials, timescales and pricing guidance.</p>
            <div class="space-y-8">
                <div class="border-l-4 border-primary pl-6">
                    <h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/patios" class="hover:text-primary transition">Patio Installation {name}</a></h3>
                    <p class="text-gray-700 leading-relaxed">We install patios in porcelain, natural sandstone, limestone, granite and block paving across {name}. Every installation starts with correct ground preparation — excavation, compacted MOT Type 1 sub-base, and sharp sand or mortar bed depending on the material. Most patio projects in {name} complete within 3–5 days. <a href="/patios" class="text-primary font-semibold hover:underline">Full patio information →</a></p>
                </div>
                <div class="border-l-4 border-green-500 pl-6">
                    <h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/artificial-grass" class="hover:text-primary transition">Artificial Grass {name}</a></h3>
                    <p class="text-gray-700 leading-relaxed">We supply and install premium synthetic turf in {name} — child-safe, pet-friendly, all-weather usable and virtually maintenance-free. We install on a compacted sub-base with integrated weed membrane and drainage layer. Product warranties of 10 years are standard. <a href="/artificial-grass" class="text-primary font-semibold hover:underline">Full artificial grass information →</a></p>
                </div>
                <div class="border-l-4 border-purple-500 pl-6">
                    <h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/composite-decking" class="hover:text-primary transition">Composite Decking {name}</a></h3>
                    <p class="text-gray-700 leading-relaxed">Composite decking requires no sanding, staining or painting — just an occasional wash. We install in {name} using leading brands including Millboard and Trex on a treated timber or aluminium subframe. Available in a wide range of colours and board profiles. <a href="/composite-decking" class="text-primary font-semibold hover:underline">Full composite decking information →</a></p>
                </div>
                <div class="border-l-4 border-amber-500 pl-6">
                    <h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/driveways" class="hover:text-primary transition">Driveways {name}</a></h3>
                    <p class="text-gray-700 leading-relaxed">We install block paving, resin bound, tarmac and porcelain driveways across {name} and the {a["postcode"]} postcode area. All driveway installations are SuDS-compliant where permeable surfacing is required. <a href="/driveways" class="text-primary font-semibold hover:underline">Full driveway information →</a></p>
                </div>
                <div class="border-l-4 border-blue-400 pl-6">
                    <h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/garden-lighting" class="hover:text-primary transition">Garden Lighting {name}</a></h3>
                    <p class="text-gray-700 leading-relaxed">Low-voltage LED garden lighting systems installed in {name} — path lights, uplighters, step lights, decking lights and smart controller systems. All installations are Part P compliant where mains voltage is involved. <a href="/garden-lighting" class="text-primary font-semibold hover:underline">Full garden lighting information →</a></p>
                </div>
                <div class="border-l-4 border-rose-500 pl-6">
                    <h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/full-garden-makeover" class="hover:text-primary transition">Full Garden Makeover {name}</a></h3>
                    <p class="text-gray-700 leading-relaxed">For homeowners in {name} wanting a complete garden transformation, we manage the entire project — from initial design (including free AI visualisation) through to all groundworks, hard landscaping, lighting and planting. One point of contact, fully costed upfront. <a href="/full-garden-makeover" class="text-primary font-semibold hover:underline">Full garden makeover information →</a></p>
                </div>
            </div>
        </div>
    </section>
'''

def common_projects_section(a):
    name = a['name']
    items_html = ''.join(f'<li class="flex items-start gap-2"><span class="text-primary mt-1">&#10003;</span><span>{p}</span></li>' for p in a['common_projects'])
    return f'''
    <!-- Common Projects Section (Phase J) -->
    <section class="py-16 px-4 bg-gray-50">
        <div class="container mx-auto max-w-4xl">
            <h2 class="font-heading font-bold text-3xl text-gray-900 mb-4">Common Projects Requested by Homeowners in {name}</h2>
            <p class="text-gray-600 mb-6">The following represents the types of landscaping projects commonly requested by homeowners in {name} — based on the nature of the local housing stock, garden sizes and ground conditions described above. These are types of work we carry out in this area, not invented completed projects.</p>
            <ul class="space-y-3 text-gray-700">
                {items_html}
            </ul>
            <div class="mt-8">
                <a href="/quote" class="inline-flex items-center gap-2 bg-primary text-white px-8 py-4 rounded-full font-bold hover:bg-primary-dark transition">
                    <i class="fas fa-bolt text-yellow-300"></i> Get a Free Instant Quote for Your {name} Garden
                </a>
            </div>
        </div>
    </section>
'''

def planning_section(a):
    name = a['name']
    return f'''
    <!-- Planning & Local Authority Section (Phase J) -->
    <section class="py-16 px-4 bg-white">
        <div class="container mx-auto max-w-4xl">
            <h2 class="font-heading font-bold text-3xl text-gray-900 mb-4">Planning Permission & {name}</h2>
            <div class="bg-blue-50 border border-blue-100 rounded-2xl p-6 mb-6">
                <p class="font-semibold text-gray-900 mb-1">Local Planning Authority: <a href="{a["authority_url"]}" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline">{a["authority"]}</a></p>
                <p class="text-gray-600 text-sm">Responsible for planning decisions in {name} and the surrounding {a["postcode"]} area.</p>
            </div>
            <div class="prose max-w-none text-gray-700 space-y-4">
                <p>{a["planning_note"]}</p>
                <h3 class="font-bold text-xl text-gray-900 mt-4">What typically does not need planning permission in {name}</h3>
                <ul class="space-y-1 list-disc list-inside text-gray-700">
                    <li>Rear garden patio and hard landscaping at ground level</li>
                    <li>Artificial grass in rear or front gardens (replacing natural grass)</li>
                    <li>Composite or timber decking up to 30cm above ground level and not more than 50% of the rear garden</li>
                    <li>Garden lighting using low-voltage (12V) transformers</li>
                    <li>Rear garden fencing up to 2 metres high</li>
                </ul>
                <h3 class="font-bold text-xl text-gray-900 mt-4">What may require planning consent in {name}</h3>
                <ul class="space-y-1 list-disc list-inside text-gray-700">
                    <li>Decking over 30cm high or covering more than 50% of the rear garden</li>
                    <li>Front garden hard-surfacing over 5m² replacing grass (must use permeable surface or obtain permission)</li>
                    <li>Work in a designated conservation area or on a listed building</li>
                    <li>Large outbuildings or pergolas exceeding the permitted development size limits</li>
                </ul>
                <p class="text-sm text-gray-500 mt-4">Planning rules can change and are subject to local variations. We provide planning guidance at no charge during our survey visit — if in doubt, always verify with <a href="{a["authority_url"]}" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline">{a["authority"]}</a> directly before proceeding.</p>
            </div>
        </div>
    </section>
'''

def nearby_areas_section(a):
    name = a['name']
    cards = ''.join(
        f'<a href="/{slug}" class="block bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md hover:border-primary transition text-center"><span class="font-semibold text-primary">{label}</span><br><span class="text-xs text-gray-500">Landscaping →</span></a>'
        for slug, label in a['nearby']
    )
    return f'''
    <!-- Nearby Areas Section (Phase J) -->
    <section class="py-16 px-4 bg-gray-50">
        <div class="container mx-auto max-w-4xl">
            <h2 class="font-heading font-bold text-3xl text-gray-900 mb-4">Nearby Areas We Also Cover</h2>
            <p class="text-gray-600 mb-8">Premium Landscapes covers a 20-mile radius from our Kirby Muxloe base. As well as {name}, we serve all the surrounding villages, towns and suburbs across Leicestershire. See your nearest area page for local details.</p>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {cards}
            </div>
            <p class="mt-6 text-gray-500 text-sm text-center">Don't see your area? <a href="/areas-we-cover" class="text-primary hover:underline">View all areas we cover</a> or call us on <a href="tel:07877934782" class="text-primary hover:underline">07877 934782</a>.</p>
        </div>
    </section>
'''

def build_schema(a):
    """Build replacement JSON-LD: WebPage + Service + BreadcrumbList array"""
    name = a['name']
    slug = a['slug']
    url = f'{BASE}/{slug}'
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{url}#page",
                "url": url,
                "name": f"Landscaping {name} | Patios, Artificial Grass, Driveways & Garden Design | Premium Landscapes",
                "description": f"Professional landscaping services in {name}, {a['postcode']}. Patios, artificial grass, composite decking, driveways & full garden transformations. Free instant quote online.",
                "inLanguage": "en-GB",
                "breadcrumb": {"@id": f"{url}#breadcrumb"}
            },
            {
                "@type": "Service",
                "name": f"Landscaping Services {name}",
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
                    "name": name,
                    "containedInPlace": {
                        "@type": "Place",
                        "name": "Leicestershire"
                    }
                },
                "hasOfferCatalog": {
                    "@type": "OfferCatalog",
                    "name": f"Landscaping Services {name}",
                    "itemListElement": [
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Patio Installation {name}", "url": f"{BASE}/patios"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Artificial Grass {name}", "url": f"{BASE}/artificial-grass"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Composite Decking {name}", "url": f"{BASE}/composite-decking"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Driveways {name}", "url": f"{BASE}/driveways"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Garden Lighting {name}", "url": f"{BASE}/garden-lighting"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Full Garden Makeover {name}", "url": f"{BASE}/full-garden-makeover"}}
                    ]
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Areas We Cover", "item": f"{BASE}/areas-we-cover"},
                    {"@type": "ListItem", "position": 3, "name": f"Landscaping {name}", "item": url}
                ]
            }
        ]
    }
    return json.dumps(schema, indent=2, ensure_ascii=False)

def make_service_cards_clickable(html, a):
    """Wrap service card h3 titles with links to service pages."""
    replacements = [
        (f'<h3 class="font-bold text-xl text-gray-900 mb-2">Patio Installation {a["name"]}</h3>',
         f'<h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/patios" class="hover:text-primary transition">Patio Installation {a["name"]}</a></h3>'),
        (f'<h3 class="font-bold text-xl text-gray-900 mb-2">Artificial Grass {a["name"]}</h3>',
         f'<h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/artificial-grass" class="hover:text-primary transition">Artificial Grass {a["name"]}</a></h3>'),
        (f'<h3 class="font-bold text-xl text-gray-900 mb-2">Composite Decking {a["name"]}</h3>',
         f'<h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/composite-decking" class="hover:text-primary transition">Composite Decking {a["name"]}</a></h3>'),
        (f'<h3 class="font-bold text-xl text-gray-900 mb-2">Garden Lighting {a["name"]}</h3>',
         f'<h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/garden-lighting" class="hover:text-primary transition">Garden Lighting {a["name"]}</a></h3>'),
        (f'<h3 class="font-bold text-xl text-gray-900 mb-2">Driveways {a["name"]}</h3>',
         f'<h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/driveways" class="hover:text-primary transition">Driveways {a["name"]}</a></h3>'),
        (f'<h3 class="font-bold text-xl text-gray-900 mb-2">Full Garden Makeover {a["name"]}</h3>',
         f'<h3 class="font-bold text-xl text-gray-900 mb-2"><a href="/full-garden-makeover" class="hover:text-primary transition">Full Garden Makeover {a["name"]}</a></h3>'),
    ]
    for old, new in replacements:
        html = html.replace(old, new, 1)
    return html

def fix_hero_badge(html, a):
    """Fix the hero location badge to reflect broader coverage (not just 'city centre')."""
    # Replace any narrow serving badge text
    old = f'<span class="text-sm font-medium">Serving {a["name"]} city centre</span>'
    new = f'<span class="text-sm font-medium">{a["serving_badge"]}</span>'
    html = html.replace(old, new)
    # Also fix generic patterns
    old2 = f'<span class="text-sm font-medium">Serving Leicester city centre</span>'
    new2 = f'<span class="text-sm font-medium">{a["serving_badge"]}</span>'
    if a["slug"] == "landscaping-leicester":
        html = html.replace(old2, new2)
    return html

def inject_new_sections(html, a):
    """Inject service links, common projects, planning and nearby areas before <!-- CTA Section -->"""
    anchor = '    <!-- CTA Section -->'
    if anchor not in html:
        print(f"  WARNING: CTA anchor not found in {a['slug']}")
        return html
    injection = (
        service_links_section(a) +
        common_projects_section(a) +
        planning_section(a) +
        nearby_areas_section(a)
    )
    return html.replace(anchor, injection + '\n' + anchor, 1)

def replace_schema(html, a):
    """Replace ALL existing <script type="application/ld+json"> blocks with our new schema."""
    # Build new schema block
    new_schema_block = f'    <script type="application/ld+json">\n{build_schema(a)}\n    </script>\n'

    # Remove all existing ld+json blocks
    html = re.sub(
        r'\s*<script type="application/ld\+json">.*?</script>',
        '',
        html,
        flags=re.DOTALL
    )

    # Also remove standalone FAQPage blocks — we'll re-add a combined one
    # (already done above with the regex)

    # Now build the FAQPage schema from the visible FAQs
    # We extract the FAQ questions/answers from the HTML
    faq_pairs = extract_faqs(html, a)
    if faq_pairs:
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": ans}
                }
                for q, ans in faq_pairs
            ]
        }
        faq_block = f'\n    <script type="application/ld+json">\n{json.dumps(faq_schema, indent=2, ensure_ascii=False)}\n    </script>'
    else:
        faq_block = ''

    # Insert schemas just before </head>
    insert_before = '</head>'
    html = html.replace(insert_before, new_schema_block + faq_block + '\n' + insert_before, 1)
    return html

def extract_faqs(html, a):
    """Pull question/answer pairs from <details>/<summary> FAQ blocks."""
    name = a['name']
    pairs = []
    # Match <details> blocks
    blocks = re.findall(r'<details[^>]*>.*?</details>', html, re.DOTALL)
    for block in blocks:
        q_match = re.search(r'<summary[^>]*>(.*?)</summary>', block, re.DOTALL)
        p_match = re.search(r'</summary>\s*<p[^>]*>(.*?)</p>', block, re.DOTALL)
        if q_match and p_match:
            q = re.sub(r'<[^>]+>', '', q_match.group(1)).strip()
            ans = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
            # Remove the chevron icon text if any
            q = re.sub(r'\s*$', '', q)
            if q and ans:
                pairs.append((q, ans))
    return pairs[:8]  # Limit to 8 FAQ pairs

# ─────────────────────────────────────────────
# Process all location pages
# ─────────────────────────────────────────────

def process_page(slug, a):
    fname = f'{slug}.html'
    if not pathlib.Path(fname).exists():
        print(f'  SKIP: {fname} not found')
        return False

    with open(fname, encoding='utf-8') as f:
        html = f.read()

    original_len = len(html)

    # Skip if already processed in this run
    if '<!-- Service Links Section (Phase J) -->' in html:
        print(f'  Already processed: {fname}')
        return False

    html = make_service_cards_clickable(html, a)
    html = fix_hero_badge(html, a)
    html = inject_new_sections(html, a)
    html = replace_schema(html, a)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)

    added = len(html) - original_len
    print(f'  OK: {fname}  (+{added} chars)')
    return True


# ─────────────────────────────────────────────
# areas-we-cover.html hub rewrite
# ─────────────────────────────────────────────

HUB_AREA_DESCRIPTIONS = {slug: d['area_desc_hub'] for slug, d in AREAS.items()}

def strengthen_areas_hub():
    """Inject a rich intro section, strengthen the hub page content."""
    fname = 'areas-we-cover.html'
    with open(fname, encoding='utf-8') as f:
        html = f.read()

    if '<!-- Hub Content (Phase J) -->' in html:
        print(f'  Already processed: {fname}')
        return

    # 1. Strengthen the hero section — inject a better subtitle
    old_hero_p = '<p class="text-xl text-white/85 max-w-2xl mx-auto">\n                Premium Landscapes serves Leicester and all surrounding towns across Leicestershire. Find your local page below for tailored pricing and services.\n            </p>'
    new_hero_p = '''<p class="text-xl text-white/85 max-w-2xl mx-auto">
                Premium Landscapes serves Leicester and all surrounding towns across Leicestershire — patios, artificial grass, composite decking, driveways, garden lighting and full garden makeovers. Based in Kirby Muxloe (LE9), we cover a 20-mile radius. Find your local page below.
            </p>
            <div class="flex flex-wrap justify-center gap-3 mt-6">
                <span class="bg-white/20 text-white text-sm px-4 py-2 rounded-full">&#128204; Kirby Muxloe (home base)</span>
                <span class="bg-white/20 text-white text-sm px-4 py-2 rounded-full">&#128205; 20-mile coverage radius</span>
                <span class="bg-white/20 text-white text-sm px-4 py-2 rounded-full">&#128314; 20+ locations served</span>
                <span class="bg-white/20 text-white text-sm px-4 py-2 rounded-full">&#9989; Free instant quote for any area</span>
            </div>'''
    html = html.replace(old_hero_p, new_hero_p)

    # 2. Add introductory hub content before the location grid
    old_grid_start = '    <!-- Location Grid -->\n    <section class="py-16 px-4 bg-white">'
    new_content = '''    <!-- Hub Content (Phase J) -->
    <section class="py-12 px-4 bg-gray-50 border-b border-gray-200">
        <div class="container mx-auto max-w-4xl">
            <h2 class="font-heading font-bold text-2xl text-gray-900 mb-4">Landscaping Across Leicester & Leicestershire</h2>
            <div class="prose max-w-none text-gray-700 space-y-3">
                <p>Premium Landscapes is a Leicester and Leicestershire landscaping company, based in Kirby Muxloe (LE9 2AA). We cover a 20-mile radius from our base, serving 20+ towns and villages across the county. Every area page includes local-specific information on property types, ground conditions, planning authority and the types of landscaping work commonly requested in that area.</p>
                <p>All services — patios, artificial grass, composite decking, driveways, garden lighting and full garden makeovers — are available in every area we cover. Pricing is consistent across the county (travel costs are not added for locations within our coverage area). Use the <a href="/quote" class="text-primary font-semibold hover:underline">free instant quote tool</a> to get an itemised price for your specific project, wherever you are in Leicestershire.</p>
            </div>
            <div class="grid md:grid-cols-3 gap-4 mt-8">
                <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm text-center">
                    <p class="text-2xl font-bold text-primary mb-1">20+</p>
                    <p class="text-gray-600 text-sm">Towns &amp; villages covered</p>
                </div>
                <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm text-center">
                    <p class="text-2xl font-bold text-primary mb-1">20 miles</p>
                    <p class="text-gray-600 text-sm">Coverage radius from Kirby Muxloe</p>
                </div>
                <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm text-center">
                    <p class="text-2xl font-bold text-primary mb-1">Free</p>
                    <p class="text-gray-600 text-sm">Instant quote for any area</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Location Grid -->
    <section class="py-16 px-4 bg-white">'''

    html = html.replace(old_grid_start, new_content)

    # 3. Add descriptions to the area cards by enriching the Leicester City group
    # The descriptions are already captured in HUB_AREA_DESCRIPTIONS
    # Add a short description under each area card
    for slug, desc in HUB_AREA_DESCRIPTIONS.items():
        short_desc = desc[:80] + '…' if len(desc) > 80 else desc
        # Find the card and add description
        # Cards look like: <h3 class="font-bold text-gray-900">Name</h3>\n<p class="text-xs text-gray-500 mt-1">postcode</p>
        # We'll add a title attribute for now (less intrusive) and enrich the postcode line
        pass  # Skip card-level changes to keep the diff manageable

    # 4. Add a services overview section before the footer
    old_footer = '    <!-- Footer -->\n    <footer'
    services_overview = '''    <!-- Services Overview for Hub (Phase J) -->
    <section class="py-16 px-4 bg-gray-50">
        <div class="container mx-auto max-w-5xl">
            <h2 class="font-heading font-bold text-2xl text-gray-900 mb-3 text-center">Services Available Across All Areas</h2>
            <p class="text-center text-gray-600 mb-10">Every service below is available across Leicester and Leicestershire. Click any service to see full details including materials, installation process and pricing guidance.</p>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                <a href="/patios" class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md hover:border-primary transition">
                    <i class="fas fa-border-all text-primary text-2xl mb-3"></i>
                    <h3 class="font-bold text-gray-900 mb-1">Patio Installation</h3>
                    <p class="text-gray-500 text-sm">Porcelain, sandstone, limestone &amp; block paving across Leicestershire.</p>
                </a>
                <a href="/artificial-grass" class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md hover:border-primary transition">
                    <i class="fas fa-leaf text-green-500 text-2xl mb-3"></i>
                    <h3 class="font-bold text-gray-900 mb-1">Artificial Grass</h3>
                    <p class="text-gray-500 text-sm">Premium synthetic turf — no mowing, no mud, all year round.</p>
                </a>
                <a href="/composite-decking" class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md hover:border-primary transition">
                    <i class="fas fa-layer-group text-purple-500 text-2xl mb-3"></i>
                    <h3 class="font-bold text-gray-900 mb-1">Composite Decking</h3>
                    <p class="text-gray-500 text-sm">Millboard, Trex &amp; leading brands. No maintenance, long life.</p>
                </a>
                <a href="/driveways" class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md hover:border-primary transition">
                    <i class="fas fa-car text-amber-500 text-2xl mb-3"></i>
                    <h3 class="font-bold text-gray-900 mb-1">Driveways</h3>
                    <p class="text-gray-500 text-sm">Block paving, resin bound, tarmac &amp; porcelain driveways.</p>
                </a>
                <a href="/garden-lighting" class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md hover:border-primary transition">
                    <i class="fas fa-lightbulb text-yellow-500 text-2xl mb-3"></i>
                    <h3 class="font-bold text-gray-900 mb-1">Garden Lighting</h3>
                    <p class="text-gray-500 text-sm">LED systems — path lights, uplighters, step lights &amp; smart controls.</p>
                </a>
                <a href="/full-garden-makeover" class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md hover:border-primary transition">
                    <i class="fas fa-seedling text-rose-500 text-2xl mb-3"></i>
                    <h3 class="font-bold text-gray-900 mb-1">Full Garden Makeover</h3>
                    <p class="text-gray-500 text-sm">Complete design-and-build garden transformations, AI design included.</p>
                </a>
            </div>
        </div>
    </section>

    <!-- Footer -->\n    <footer'''

    html = html.replace(old_footer, services_overview)

    # 5. Add schema to areas-we-cover.html — the current one already has WebPage + BreadcrumbList
    # Just verify it's there, add a Service schema for coverage
    hub_service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "Landscaping Services Leicester & Leicestershire",
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
        "areaServed": [
            {"@type": "Place", "name": "Leicester"},
            {"@type": "Place", "name": "Leicestershire"},
            {"@type": "Place", "name": "Kirby Muxloe"},
            {"@type": "Place", "name": "Oadby"},
            {"@type": "Place", "name": "Wigston"},
            {"@type": "Place", "name": "Narborough"},
            {"@type": "Place", "name": "Hinckley"},
            {"@type": "Place", "name": "Loughborough"},
            {"@type": "Place", "name": "Glenfield"},
            {"@type": "Place", "name": "Birstall"},
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Landscaping Services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Patio Installation Leicester"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Artificial Grass Leicester"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Composite Decking Leicester"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Driveways Leicester"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Garden Lighting Leicester"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Full Garden Makeover Leicester"}},
            ]
        }
    }
    hub_schema_block = f'\n    <script type="application/ld+json">\n{json.dumps(hub_service_schema, indent=2, ensure_ascii=False)}\n    </script>'
    html = html.replace('</head>', hub_schema_block + '\n</head>', 1)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {fname} (hub strengthened)')


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print('Phase J — Location page SEO improvements\n')
    updated = 0
    for slug, a in AREAS.items():
        print(f'Processing: {slug}')
        if process_page(slug, a):
            updated += 1

    print(f'\nProcessing: areas-we-cover.html')
    strengthen_areas_hub()

    print(f'\nDone. {updated} location pages updated.')
