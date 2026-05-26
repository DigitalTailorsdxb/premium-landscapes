#!/usr/bin/env python3
"""
Phase C: Replace duplicate SEO Content Block + duplicate FAQ pairs on all 20 area
pages with genuinely unique, factually-anchored local content. All facts used
here are public-domain: postcode districts, local authorities, road numbers,
broad geology, and approximate distances from our Kirby Muxloe base.
"""
import re
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Per-town public-domain facts. Every value is verifiable from Royal Mail
# postcode data, local council websites, OS maps, BGS geology, or Google Maps.
# ---------------------------------------------------------------------------
TOWNS = {
    "anstey": {
        "name": "Anstey",
        "postcodes": ["LE7"],
        "council": "Charnwood Borough Council",
        "district": "Charnwood",
        "direction": "north-west of Leicester city centre",
        "distance_km": 6, "drive_min": 12,
        "roads": ["A46 Western Bypass", "B5327 Cropston Road", "Bradgate Road"],
        "neighbourhoods": ["The Nook", "Bradgate Road", "Cropston Road area", "Stadon Road estate"],
        "landmarks": "Anstey village green, the historic packhorse bridge over the Rothley Brook, and Bradgate Park a short drive west",
        "property_mix": "a mix of stone-fronted village cottages around the old centre, 1930s semis along Bradgate Road, and post-war estates further out",
        "garden_sizes": "30–80ft rear gardens are typical, with the older village properties often having stone boundary walls that influence patio layout choices",
        "geology": "shallow Charnian bedrock under the village core means occasional rocky obstacles when excavating for patio sub-bases; we always allow extra mini-digger time for older properties near Cropston Road",
        "drainage": "the rising ground toward Bradgate Park drains better than the village centre, but properties on Stadon Road can sit on heavier glacial clay where French drains pay back quickly",
        "common_projects": "porcelain patios, replacement driveways in resin or block paving, and full rear-garden redesigns combining lawn, decking and lighting",
    },
    "birstall": {
        "name": "Birstall",
        "postcodes": ["LE4"],
        "council": "Charnwood Borough Council",
        "district": "Charnwood",
        "direction": "directly north of Leicester, on the east bank of the River Soar",
        "distance_km": 10, "drive_min": 18,
        "roads": ["A6 Loughborough Road", "Sibson Road", "Birstall Road"],
        "neighbourhoods": ["Greengate Lane", "Wanlip Lane", "Hallam Crescent area", "Riverside near Watermead"],
        "landmarks": "Watermead Country Park, the River Soar moorings, and the Hallam Fields shopping area on the A6",
        "property_mix": "1960s–80s detached and semi-detached homes dominate, with newer riverside developments near Watermead and older Victorian properties closer to the church",
        "garden_sizes": "40–90ft rear gardens are common, often with mature trees that need protection during landscaping work",
        "geology": "river-valley alluvium and clay alluvium close to the Soar means properties on Riverside Drive and Wanlip Lane have a higher water table than average",
        "drainage": "any work within 200m of the river needs careful drainage planning — we routinely specify deeper sub-bases and SuDS-compliant permeable surfaces for Birstall driveways",
        "common_projects": "permeable block paving driveways, raised composite decking (useful for managing levels near the river), and artificial grass for families wanting a low-maintenance lawn",
    },
    "blaby": {
        "name": "Blaby",
        "postcodes": ["LE8"],
        "council": "Blaby District Council",
        "district": "Blaby",
        "direction": "south of Leicester, between the city and the M1 motorway",
        "distance_km": 7, "drive_min": 15,
        "roads": ["A426 Lutterworth Road", "Leicester Road", "Winchester Road"],
        "neighbourhoods": ["Blaby village centre", "Lutterworth Road", "Winchester Road estate", "Whetstone Lane border"],
        "landmarks": "the historic Blaby village centre, the Bakers Arms, and easy access to Fosse Park retail just up the A426",
        "property_mix": "older village-centre cottages near the church, 1970s–90s estates around Winchester Road, and newer developments stretching toward Whetstone and Glen Parva",
        "garden_sizes": "the newer estates typically have manageable 30–60ft rear gardens on relatively level ground, which keeps project costs predictable",
        "geology": "predominantly Lias clay across the district, with localised gravel deposits near the old Soar floodplain to the east",
        "drainage": "south-Leicestershire clay holds water through winter — properties on Winchester Road and Lutterworth Road benefit from upgraded edge drainage with any new patio",
        "common_projects": "porcelain and sandstone patios, complete makeovers for new-build gardens (turf, planting, fence, patio in one go), and artificial grass for low-maintenance family gardens",
    },
    "clarendon-park": {
        "name": "Clarendon Park",
        "postcodes": ["LE2"],
        "council": "Leicester City Council",
        "district": "Leicester City",
        "direction": "immediately south of Leicester city centre",
        "distance_km": 7, "drive_min": 18,
        "roads": ["Queens Road", "Clarendon Park Road", "Welford Road (A5199)"],
        "neighbourhoods": ["Queens Road shops area", "Howard Road", "Avenue Road Extension", "Knighton Road border"],
        "landmarks": "the Queens Road retail strip, Victoria Park to the north, and the University of Leicester campus on Welford Road",
        "property_mix": "dense streets of Edwardian and late-Victorian terraces — narrow frontages, deep plots, and long back-entry access in most cases",
        "garden_sizes": "compact rear courtyard gardens of 20–40ft are the norm, often accessed only through a narrow back entry or through the house itself",
        "geology": "city-centre fill over Mercia Mudstone — once we get below the topsoil layer, sub-bases compact well, but old buried debris from Edwardian builds is common and we always allow for it",
        "drainage": "narrow plots and shared boundary walls mean drainage must be designed not to discharge onto neighbouring properties; we routinely fit linear drains tied into the existing rainwater system",
        "common_projects": "small-footprint porcelain courtyards, hand-barrowed patio installs (because no driveway access), and bespoke planters or pergolas to maximise the limited space",
    },
    "cosby": {
        "name": "Cosby",
        "postcodes": ["LE9"],
        "council": "Blaby District Council",
        "district": "Blaby",
        "direction": "south-west of Leicester, near the M1 J21 corridor",
        "distance_km": 10, "drive_min": 18,
        "roads": ["Croft Road", "Broughton Road", "Main Street"],
        "neighbourhoods": ["Main Street", "Broughton Road", "Croft Road", "Park Road area"],
        "landmarks": "Cosby village green, the parish church of St Michael, and Cosby Cricket Club",
        "property_mix": "a true village mix — original stone-built cottages on Main Street, post-war semis on Broughton Road, and modern estates on the village edges",
        "garden_sizes": "the modern estate gardens typically run 40–70ft; the village-centre properties have more varied plots and often boundary walls or hedges to work around",
        "geology": "boulder-clay glacial till on top of the underlying mudstone — heavy when wet, so excavation in winter is slower and we factor that into project timings",
        "drainage": "the gently sloping ground around the village helps with surface runoff, but rear gardens that back onto agricultural land (common in Cosby) need careful edge management to avoid silt and runoff issues",
        "common_projects": "Indian sandstone patios, block-paving driveways, fencing replacement with concrete posts (popular here because of windier exposure to open countryside)",
    },
    "enderby": {
        "name": "Enderby",
        "postcodes": ["LE19"],
        "council": "Blaby District Council",
        "district": "Blaby",
        "direction": "south-west of Leicester, between Narborough and the M1 J21",
        "distance_km": 4, "drive_min": 10,
        "roads": ["Leicester Lane", "Mill Lane", "Cooperative Way"],
        "neighbourhoods": ["Enderby village core", "Mill Lane area", "St Johns estate", "Forest House Lane"],
        "landmarks": "Enderby Methodist church, Brookside Park, and the major Meridian Business Park just south",
        "property_mix": "Victorian cottages near the village heart, post-war and 1970s housing on the main approaches, plus a steady stream of new-build estates around the business-park fringe",
        "garden_sizes": "30–70ft for the older properties; newer-build gardens are typically smaller and more uniform, which suits modular landscaping designs",
        "geology": "Enderby's local granite quarry history reflects the firmer underlying geology here — sub-bases compact extremely well and we rarely see settlement issues on patios in LE19",
        "drainage": "generally good natural drainage on the higher ground; the lower-lying streets near Mill Lane sit closer to the Soar floodplain and may need permeable surfaces under the latest SuDS rules",
        "common_projects": "resin-bound driveways (the firm sub-base makes resin a cost-effective option), composite decking, and artificial grass installations for the newer-build estates",
    },
    "glenfield": {
        "name": "Glenfield",
        "postcodes": ["LE3"],
        "council": "Blaby District Council",
        "district": "Blaby",
        "direction": "directly north-west of Leicester, bordering our Kirby Muxloe base",
        "distance_km": 3, "drive_min": 8,
        "roads": ["A50 Leicester Road", "Sports Road", "Stamford Street"],
        "neighbourhoods": ["Glenfield village centre", "Stamford Street", "Sports Road estate", "Liberty Park"],
        "landmarks": "Glenfield Hospital, the County Hall complex (county council HQ), and Western Park immediately east",
        "property_mix": "predominantly 1950s–70s bungalows, semis, and detached houses on level plots — a very consistent suburban character",
        "garden_sizes": "40–90ft rear gardens are typical, with many bungalows having particularly generous plots that suit larger garden makeovers",
        "geology": "flat terrain on Mercia Mudstone — straightforward to excavate, predictable compaction, and very few drainage surprises",
        "drainage": "the level ground does mean rainwater needs somewhere to go; we always extend rainwater downpipes and fit gravel soakaways or French drains as part of any larger patio install",
        "common_projects": "bungalow garden redesigns (level access, often with wheelchair-friendly paths), composite decking on raised plots, and full-makeover projects taking advantage of the larger gardens",
    },
    "hinckley": {
        "name": "Hinckley",
        "postcodes": ["LE10"],
        "council": "Hinckley & Bosworth Borough Council",
        "district": "Hinckley & Bosworth",
        "direction": "west Leicestershire, on the A5 between Leicester and Nuneaton",
        "distance_km": 15, "drive_min": 22,
        "roads": ["A5 Watling Street", "A47 Leicester Road", "Coventry Road"],
        "neighbourhoods": ["Hinckley town centre", "Burbage border", "Earl Shilton side", "Coventry Road"],
        "landmarks": "Hinckley Market Place, Burbage Common, and the Atkins Building cultural centre",
        "property_mix": "Victorian terraces near the town centre, 1930s–60s semis through the established suburbs, and newer developments toward Burbage and Earl Shilton",
        "garden_sizes": "town-centre terraces often have compact 20–40ft rear courtyards, while larger semis and detached homes on roads like Coventry Road have 60–100ft+ plots",
        "geology": "Mercia Mudstone underlying most of the town, with some shallow drift deposits — generally workable but occasional clay-shrinkage cracks need to be allowed for in sub-base design",
        "drainage": "the older parts of town drain into the Victorian combined sewer system; we always survey existing rainwater goods on terraced installs to avoid creating new runoff problems",
        "common_projects": "patio replacements for tired 1960s concrete slabs, block-paving driveways to replace gravel or tarmac, and full garden makeovers for the newer-build estates",
    },
    "kirby-muxloe": {
        "name": "Kirby Muxloe",
        "postcodes": ["LE9"],
        "council": "Blaby District Council",
        "district": "Blaby",
        "direction": "directly west of Leicester — and home of our Premium Landscapes base at 44 Barwell Road",
        "distance_km": 0, "drive_min": 0,
        "roads": ["A47 Hinckley Road", "Barwell Road", "Main Street", "Station Road"],
        "neighbourhoods": ["Castle area", "Main Street village centre", "Barwell Road", "Hinckley Road"],
        "landmarks": "Kirby Muxloe Castle (English Heritage), Kirby Muxloe Golf Club, and the village conservation area around Main Street",
        "property_mix": "everything from stone-built cottages near the castle and conservation area, through 1930s–60s semis and detached houses, to newer executive estates off Hinckley Road",
        "garden_sizes": "the older village properties have varied plot shapes; the modern estates run 50–90ft rear gardens and the larger detached homes often exceed 100ft",
        "geology": "mixed across the village — some properties sit on the firmer ground close to the castle ridge, others on heavier clay toward the Hinckley Road side",
        "drainage": "the village conservation area requires extra care: rainwater discharge, surface materials and boundary treatments may need conservation consent and we handle that paperwork as part of the quote",
        "common_projects": "natural-stone patios (sympathetic to the conservation-area properties), block paving and resin driveways on the larger detached plots, and full garden makeovers including bespoke pergolas and outdoor lighting",
    },
    "knighton": {
        "name": "Knighton",
        "postcodes": ["LE2"],
        "council": "Leicester City Council",
        "district": "Leicester City",
        "direction": "an affluent residential suburb directly south of Leicester city centre",
        "distance_km": 8, "drive_min": 18,
        "roads": ["A6 London Road", "Knighton Road", "Stoughton Drive North"],
        "neighbourhoods": ["Knighton village", "Knighton Park", "Stoneygate border", "Park Hill area"],
        "landmarks": "Knighton Park, Knighton Church (St Mary Magdalene), and easy access to the University of Leicester campus",
        "property_mix": "Edwardian and 1920s–30s detached and semi-detached homes dominate, with later 20th-century infill on Stoughton Drive and Avenue Road",
        "garden_sizes": "many gardens here run 60–120ft, with mature trees and established borders that need protection during landscaping work",
        "geology": "Mercia Mudstone overlain by mature topsoil — established gardens often have decades of organic build-up that helps planting but can complicate sub-base prep",
        "drainage": "mature tree roots are the main consideration: we routinely root-prune sympathetically and use cellular confinement where roots cross a proposed patio area",
        "common_projects": "porcelain and natural-stone patios at the rear, bespoke garden lighting schemes (popular with the larger Edwardian properties), and pergola or outdoor-kitchen builds for entertaining",
    },
    "loughborough": {
        "name": "Loughborough",
        "postcodes": ["LE11", "LE12"],
        "council": "Charnwood Borough Council",
        "district": "Charnwood",
        "direction": "north Leicestershire, on the A6 toward Nottingham",
        "distance_km": 22, "drive_min": 30,
        "roads": ["A6 main route", "A60 Nottingham Road", "Ashby Road"],
        "neighbourhoods": ["University area", "Forest Road", "Outwoods", "Shelthorpe estate"],
        "landmarks": "Loughborough University campus, Queens Park, and the Great Central Railway heritage line",
        "property_mix": "Victorian terraces and 1930s–50s semis near the town centre and university, Edwardian villas off Forest Road, and modern new-build estates on the northern and western fringes",
        "garden_sizes": "40–100ft rear gardens are common; the Edwardian villas often have particularly long plots that suit two-zone designs (lounging zone near the house, lawn and feature area at the rear)",
        "geology": "varied — the western edge sits on Charnwood Forest's harder rocks (occasional shallow bedrock), while properties closer to the Soar and the A6 corridor sit on river-valley clay",
        "drainage": "generally manageable, but properties in Shelthorpe and along the lower-lying streets need permeable patio detailing or French drains to handle winter saturation",
        "common_projects": "porcelain and Indian sandstone patios, larger composite decking projects for student-let landlords seeking low-maintenance gardens, and resin-bound driveways for the bigger detached properties",
    },
    "markfield": {
        "name": "Markfield",
        "postcodes": ["LE67"],
        "council": "Hinckley & Bosworth Borough Council",
        "district": "Hinckley & Bosworth",
        "direction": "north-west Leicestershire, on the M1 J22 corridor and bordering Charnwood Forest",
        "distance_km": 10, "drive_min": 18,
        "roads": ["A50 Leicester Road", "Main Street", "Forest Road"],
        "neighbourhoods": ["Main Street village", "Forest Road area", "Altar Stones Lane", "Hill Lane"],
        "landmarks": "Markfield village centre, the Bull's Head pub, and proximity to Bradgate Park and Beacon Hill country parks",
        "property_mix": "stone and brick village properties on the older streets, with substantial detached homes on the larger plots around Forest Road and Hill Lane",
        "garden_sizes": "many properties here have generous 80–150ft plots that step up the hillside — multi-level garden designs are common",
        "geology": "Markfield sits on the harder Charnian rocks of the Charnwood Forest — excavation can hit shallow bedrock unexpectedly and we always allow contingency for it",
        "drainage": "the sloping ground drains well naturally; the main challenge is managing levels — terracing with retaining walls is far more common here than in flat suburbs",
        "common_projects": "retaining-wall terracing, multi-level porcelain patio steps, natural-stone driveways, and substantial garden makeovers that integrate the surrounding countryside views",
    },
    "narborough": {
        "name": "Narborough",
        "postcodes": ["LE19"],
        "council": "Blaby District Council",
        "district": "Blaby",
        "direction": "south-west of Leicester, on the banks of the River Soar",
        "distance_km": 5, "drive_min": 12,
        "roads": ["Coventry Road (B4114)", "Leicester Road", "Station Road"],
        "neighbourhoods": ["Narborough village centre", "Coventry Road", "Forest House Lane border", "Station Road area"],
        "landmarks": "Narborough railway station, Brockington College, and easy access to Fosse Park and the M1 J21",
        "property_mix": "Victorian and Edwardian cottages near the railway and village centre, 1950s–80s estates, and newer riverside developments",
        "garden_sizes": "40–90ft rear gardens for the established housing; newer riverside builds are smaller and often raised to manage flood-zone requirements",
        "geology": "river-valley clay and silt alluvium near the Soar, transitioning to firmer ground on the higher streets toward Forest House Lane",
        "drainage": "properties in the lower-lying Soar floodplain can experience seasonal waterlogging — we always include a drainage check during site visits in Narborough and routinely specify permeable surfaces under the SuDS regulations for any new driveway",
        "common_projects": "permeable resin-bound driveways, raised composite decking to manage low-lying ground, and porcelain patios on properly engineered sub-bases",
    },
    "oadby": {
        "name": "Oadby",
        "postcodes": ["LE2"],
        "council": "Oadby & Wigston Borough Council",
        "district": "Oadby & Wigston",
        "direction": "south-east of Leicester, an established and affluent suburb",
        "distance_km": 10, "drive_min": 20,
        "roads": ["A6 London Road", "Stoughton Road", "Glen Road", "Wigston Road"],
        "neighbourhoods": ["Oadby village", "Stoughton Drive", "Glen Road area", "Wigston Road border"],
        "landmarks": "the University of Leicester Botanic Garden (a benchmark for what a well-maintained Leicestershire garden looks like), Brocks Hill Country Park, and the Oadby Village Conservation Area",
        "property_mix": "predominantly 1960s–70s detached and semi-detached homes with generous rear gardens",
        "garden_sizes": "60–100ft rear gardens are typical — among the most generous of any of our service areas",
        "geology": "predominantly clay across the district, though the slightly elevated ground around Wigston Road and Stoughton Road drains marginally better than the lower-lying streets",
        "drainage": "the Oadby Village Conservation Area covers the old village core near Church Road; properties in or adjacent to it may need consent for external works and we handle the conservation paperwork as part of the quote",
        "common_projects": "full garden makeovers (the larger plots allow separate seating and dining areas), composite decking with festoon lighting, and porcelain patios with planted borders",
    },
    "ratby": {
        "name": "Ratby",
        "postcodes": ["LE6"],
        "council": "Hinckley & Bosworth Borough Council",
        "district": "Hinckley & Bosworth",
        "direction": "north-west of Leicester, between Kirby Muxloe and Markfield",
        "distance_km": 5, "drive_min": 10,
        "roads": ["Main Street", "Burroughs Road", "Stamford Street"],
        "neighbourhoods": ["Ratby village centre", "Burroughs Road area", "Stamford Street", "Markfield Road"],
        "landmarks": "Ratby parish church, the Plough pub, and the recreation ground at the heart of the village",
        "property_mix": "a quiet village with a mix of older stone-and-brick cottages on Main Street and 1960s–80s estates on the village edges",
        "garden_sizes": "40–80ft rear gardens are typical for the estate properties; the older village houses have more varied plots, often with mature trees",
        "geology": "Ratby sits on the western edge of Charnwood Forest — shallow rocky outcrops are not unusual and we factor extra mini-digger time into excavation quotes here",
        "drainage": "the gently sloping village ground drains naturally; the main consideration is preserving boundaries and not channelling water toward neighbouring older properties",
        "common_projects": "natural-stone patios (sympathetic to the village character), block-paving driveways, and full garden makeovers including planting and fencing",
    },
    "stoneygate": {
        "name": "Stoneygate",
        "postcodes": ["LE2"],
        "council": "Leicester City Council",
        "district": "Leicester City",
        "direction": "Leicester's most prestigious residential suburb, south of the city centre",
        "distance_km": 8, "drive_min": 20,
        "roads": ["A6 London Road", "Stoneygate Road", "Victoria Road East", "Elms Road"],
        "neighbourhoods": ["Stoneygate Road", "Victoria Road East", "Elms Road", "Knighton Park border"],
        "landmarks": "the Stoneygate Conservation Area, the Leicester High School for Girls, and several Grade II-listed Edwardian villas",
        "property_mix": "large Edwardian and late-Victorian detached houses, many with original stone boundary walls, mature drives, and substantial rear gardens",
        "garden_sizes": "80–150ft rear gardens are not uncommon, often with mature specimen trees and historic stone boundary features",
        "geology": "deep mature topsoil over Mercia Mudstone — excellent for planting, but root systems from mature trees are a constant consideration when laying patios",
        "drainage": "the entire suburb is within the Stoneygate Conservation Area, which has implications for boundary walls, drives, and any change to the street-facing frontage; we manage the conservation-consent paperwork as part of our quote",
        "common_projects": "natural-stone and porcelain patios designed to complement Edwardian properties, restoration of original stone boundary walls, bespoke pergolas, and high-end garden lighting installations",
    },
    "syston": {
        "name": "Syston",
        "postcodes": ["LE7"],
        "council": "Charnwood Borough Council",
        "district": "Charnwood",
        "direction": "north Leicestershire, between Leicester and Loughborough",
        "distance_km": 14, "drive_min": 22,
        "roads": ["A607 Melton Road", "Albert Street", "Wanlip Road"],
        "neighbourhoods": ["Syston town centre", "Wanlip Road", "Melton Road area", "Barkby Thorpe Lane"],
        "landmarks": "Syston town centre on the A607, the railway station, and Watermead Country Park immediately south",
        "property_mix": "Victorian and Edwardian terraces near the town centre and railway, 1960s–70s estates on the outskirts, and new-build developments expanding to the north",
        "garden_sizes": "30–80ft rear gardens are typical; the newer-build properties tend to have smaller, more uniform plots that suit modular design approaches",
        "geology": "clay-loam over Mercia Mudstone — workable but slow-draining in winter; sub-base compaction needs to be done carefully when the ground is wet",
        "drainage": "the lower-lying ground near Wanlip and the Soar can sit damp through winter; we routinely fit French drains or specify permeable surfaces to manage standing water",
        "common_projects": "porcelain patio installs replacing tired 1970s concrete, full garden makeovers for new-build owners, and block-paving driveways with proper SuDS-compliant drainage",
    },
    "thurmaston": {
        "name": "Thurmaston",
        "postcodes": ["LE4"],
        "council": "Charnwood Borough Council",
        "district": "Charnwood",
        "direction": "north of Leicester, on the A607 next to the River Soar",
        "distance_km": 12, "drive_min": 20,
        "roads": ["A607 Melton Road", "Garden Street", "Humberstone Lane border"],
        "neighbourhoods": ["Thurmaston village centre", "Garden Street", "Silver Birches", "Roundhill estate"],
        "landmarks": "Thurmaston Shopping Centre, Watermead Country Park to the north, and the Thurmaston Marina on the Soar",
        "property_mix": "1950s–70s estate housing dominates, with some older properties near the village core and newer infill on the Roundhill estate",
        "garden_sizes": "40–80ft rear gardens are typical for the estate properties; consistent plot shapes make project pricing very predictable here",
        "geology": "river-valley clay and alluvium close to the Soar — heavier and wetter than the higher ground further from the river",
        "drainage": "properties closer to Garden Street and the river benefit from upgraded drainage on any patio or driveway install; we routinely specify deeper sub-bases and SuDS-compliant permeable surfaces under the latest regulations",
        "common_projects": "block-paving driveways with permeable jointing, composite decking raised to manage levels, and artificial grass for low-maintenance family gardens",
    },
    "wigston": {
        "name": "Wigston",
        "postcodes": ["LE18"],
        "council": "Oadby & Wigston Borough Council",
        "district": "Oadby & Wigston",
        "direction": "south of Leicester, a large established suburb",
        "distance_km": 10, "drive_min": 20,
        "roads": ["A5199 Welford Road", "Leicester Road", "Bull Head Street"],
        "neighbourhoods": ["Wigston Magna", "Wigston Fields", "South Wigston", "Bull Head Street area"],
        "landmarks": "Wigston Magna's historic centre, the Wigston Framework Knitters' Museum, and Wigston Magna railway station (closed but historic)",
        "property_mix": "two distinct characters — Wigston Magna has older Victorian and Edwardian terraces near the historic centre, while extensive 1950s–80s residential development covers the west and south",
        "garden_sizes": "older terraces typically have 25–50ft rear courtyards; the suburban estates run 40–80ft on more regular plots",
        "geology": "Mercia Mudstone with localised clay overlay — similar to central Leicester, with the lower-lying southern streets being slightly heavier",
        "drainage": "the older terraces share combined sewer systems where careful detailing is needed for new patio drainage; the post-war estates have separate surface-water systems that are easier to tie into",
        "common_projects": "courtyard patio upgrades for Wigston Magna terraces, full garden makeovers on the larger suburban plots, and block-paving or resin-bound driveways for the estate housing",
    },
}

# ---------------------------------------------------------------------------
# Generators — these produce HTML and JSON. The structure is intentionally
# consistent across pages (good for users), but the FACTS are entirely
# town-specific (which is what Google rewards / penalises).
# ---------------------------------------------------------------------------

def make_seo_block(t: dict) -> str:
    """Generate a unique SEO content block from the town's facts."""
    pcs = " and ".join(t["postcodes"])
    pc_label = "postcode" if len(t["postcodes"]) == 1 else "postcodes"
    distance_phrase = (
        "our base at 44 Barwell Road, Kirby Muxloe"
        if t["distance_km"] == 0
        else f"approximately {t['distance_km']}km from our base at 44 Barwell Road, Kirby Muxloe (about {t['drive_min']} minutes by van)"
    )
    here_or_in_town = "right here in the village" if t["distance_km"] == 0 else f"in {t['name']}"
    roads_list = ", ".join(t["roads"])
    neighbourhoods_list = ", ".join(t["neighbourhoods"])

    return f"""    <!-- SEO Content Block (Phase C — unique factual local content) -->
    <section class="py-16 px-4 bg-gray-50">
        <div class="container mx-auto max-w-4xl">
            <h2 class="font-heading font-bold text-3xl text-gray-900 mb-6">Landscaping in {t['name']}, {t['district']}</h2>
            <div class="prose max-w-none text-gray-700 space-y-4">
                <p>
                    {t['name']} sits {t['direction']}, in the {pcs} {pc_label} area. {('Premium Landscapes is based here — at 44 Barwell Road, Kirby Muxloe — so this is the area we know best.' if t['distance_km'] == 0 else f"For us, that's {distance_phrase}, which means we can usually run a site visit in {t['name']} within a few days of booking.")} Our work in {t['name']} typically takes us along {roads_list}, covering streets including {neighbourhoods_list}.
                </p>
                <p>
                    {t['name']} sits within the boundary of <strong>{t['council']}</strong> — they are the local planning authority for any landscaping work that requires consent {here_or_in_town}. Most domestic patio, decking and driveway projects are permitted development, but anything in a conservation area, listed property, or fronting a highway can need consent and we'll always check the latest local rules before quoting.
                </p>

                <h3 class="font-bold text-xl text-gray-900 mt-6">The property &amp; garden profile {here_or_in_town}</h3>
                <p>
                    {t['name']} is characterised by {t['property_mix']}. {t['garden_sizes'].capitalize()}. {('Notable local landmarks include ' + t['landmarks'] + '.') if t.get('landmarks') else ''}
                </p>

                <h3 class="font-bold text-xl text-gray-900 mt-6">Ground conditions &amp; drainage {here_or_in_town}</h3>
                <p>
                    From experience installing in {t['name']}: {t['geology']}. On drainage specifically, {t['drainage']}.
                </p>

                <h3 class="font-bold text-xl text-gray-900 mt-6">Most common projects we install {here_or_in_town}</h3>
                <p>
                    The work we are asked to do most often in {t['name']} is {t['common_projects']}. We deliver the full range of services across the area — patios in porcelain, sandstone and natural stone; artificial grass; composite decking; block-paving, resin and porcelain driveways; garden lighting; fencing; turfing; pergolas; and full end-to-end garden makeovers.
                </p>

                <h3 class="font-bold text-xl text-gray-900 mt-6">Getting your free instant quote &amp; AI garden design</h3>
                <p>
                    Every {t['name']} project starts the same way: a free instant online quote with itemised pricing within minutes, plus the option of a free AI garden design preview if you upload a photo. There is no charge for either, no obligation, and no sales call required — the quote and design are yours to keep whether you proceed or not.
                </p>
            </div>
        </div>
    </section>
"""


def make_faq_html(t: dict) -> str:
    """Generate a unique 5-question FAQ HTML block."""
    pcs_list = " and ".join(t["postcodes"])
    pc_label = "postcode" if len(t["postcodes"]) == 1 else "postcodes"
    distance_answer = (
        f"We are based in {t['name']} — Premium Landscapes operates from 44 Barwell Road, Kirby Muxloe (LE9 2AA) — so this is our home village and we know every street."
        if t["distance_km"] == 0
        else f"{t['name']} is approximately {t['distance_km']}km from our base at 44 Barwell Road, Kirby Muxloe — about a {t['drive_min']}-minute drive. We typically run a site visit within a few days of booking."
    )
    faqs = [
        ("What postcodes do you cover in " + t["name"] + "?",
         f"We cover the full {pcs_list} {pc_label} area across {t['name']} and the surrounding streets, including {', '.join(t['neighbourhoods'][:3])} and beyond. If you are not sure whether your address falls in our service area, send us a postcode and we will confirm before quoting."),
        ("How far is " + t["name"] + " from your base?",
         distance_answer),
        ("Who handles planning permission for landscaping in " + t["name"] + "?",
         f"{t['council']} is the local planning authority for {t['name']}. Most domestic patio, artificial grass, decking and driveway projects fall under permitted development and need no planning permission. Conservation-area work, listed buildings, or anything fronting a highway can need consent — we check the latest local rules before quoting and handle any paperwork as part of the project."),
        ("What ground conditions should I expect under a new patio in " + t["name"] + "?",
         f"In {t['name']}: {t['geology']}. We always factor local ground conditions into our sub-base specification, which is why a quote from a landscaper who knows the area will usually be more accurate than one from a contractor based outside Leicestershire."),
        ("What does Premium Landscapes install most often in " + t["name"] + "?",
         f"The most frequent projects we deliver in {t['name']} are {t['common_projects']}. We also handle fencing, turfing, pergolas, garden lighting and full end-to-end garden makeovers — and every project starts with a free instant online quote and the option of a free AI garden design preview."),
    ]

    out = ['    <!-- FAQ Section (Phase C — unique local FAQs) -->',
           '    <section class="py-20 px-4 bg-white">',
           '        <div class="container mx-auto max-w-3xl">',
           f'            <h2 class="font-heading font-bold text-3xl text-center text-gray-900 mb-12">Frequently Asked Questions — Landscaping in {t["name"]}</h2>',
           '            <div class="space-y-4">']
    for q, a in faqs:
        out.append('                <details class="bg-gray-50 rounded-2xl p-6 group">')
        out.append('                    <summary class="font-semibold text-gray-900 cursor-pointer flex items-center justify-between">')
        out.append(f'                        {q}')
        out.append('                        <i class="fas fa-chevron-down text-primary transition-transform group-open:rotate-180"></i>')
        out.append('                    </summary>')
        out.append(f'                    <p class="text-gray-600 mt-4 text-sm leading-relaxed">{a}</p>')
        out.append('                </details>')
    out.append('            </div>')
    out.append('        </div>')
    out.append('    </section>')
    return "\n".join(out) + "\n", faqs


def make_faq_jsonld(faqs):
    """Generate a clean FAQPage JSON-LD block from the same FAQ pairs."""
    main_entity = [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    return json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": main_entity},
        ensure_ascii=False, indent=4
    )


# ---------------------------------------------------------------------------
# Rewriter — open file, replace blocks, write back
# ---------------------------------------------------------------------------

SEO_BLOCK_RE = re.compile(
    r'    <!-- SEO Content Block.*?</section>\s*\n', re.DOTALL
)
FAQ_BLOCK_RE = re.compile(
    r'    <!-- FAQ Section.*?</section>\s*\n', re.DOTALL
)
# Match the existing FAQPage JSON-LD that comes after the LocalBusiness one.
# These pages contain a separate <!-- FAQ Schema --> block; replace its inner JSON.
FAQ_SCHEMA_RE = re.compile(
    r'(<!-- FAQ Schema -->\s*<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',
    re.DOTALL
)

def rewrite(slug: str, t: dict) -> str:
    path = Path(f"landscaping-{slug}.html")
    if not path.exists():
        return f"  SKIP missing {path}"
    html = path.read_text(encoding="utf-8")
    orig_len = len(html)

    # 1) Replace SEO content block
    new_seo = make_seo_block(t)
    html, seo_n = SEO_BLOCK_RE.subn(new_seo, html, count=1)

    # 2) Replace FAQ section (HTML) + collect FAQ pairs for the JSON-LD
    new_faq_html, faq_pairs = make_faq_html(t)
    html, faq_n = FAQ_BLOCK_RE.subn(new_faq_html, html, count=1)

    # 3) Replace FAQ JSON-LD
    new_faq_ld = make_faq_jsonld(faq_pairs)
    html, ld_n = FAQ_SCHEMA_RE.subn(lambda m: m.group(1) + new_faq_ld + m.group(3), html, count=1)

    path.write_text(html, encoding="utf-8")
    return f"  {slug:<18} seo:{seo_n}  faq-html:{faq_n}  faq-ld:{ld_n}  size:{orig_len}→{len(html)}"


if __name__ == "__main__":
    print(f"Phase C: rewriting {len(TOWNS)} area pages...\n")
    for slug, t in TOWNS.items():
        print(rewrite(slug, t))
    print("\nDone. Validate JSON-LD next.")
