#!/usr/bin/env python3
"""Phase I — Full service-page SEO clean-up across all 16 service pages."""

import re

FAQ_ANCHOR = '    <section class="py-16">\n        <div class="max-w-4xl mx-auto px-4">\n            <div class="text-center mb-12">\n                <h2 class="text-3xl font-bold mb-4">Frequently Asked Questions</h2>'


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Written: {path}')


# ─────────────────────────────────────────────────────────────────────────────
# 1. services.html
# ─────────────────────────────────────────────────────────────────────────────
def fix_services():
    p = 'services.html'
    h = read(p)

    # H2 wording
    h = h.replace(
        'Landscaping Services Across Leicester &amp; the Midlands',
        'Landscaping Services Across Leicester &amp; Leicestershire'
    )

    # Service card heading
    h = h.replace(
        '<h3 class="text-2xl font-bold text-white">Lawn Installation</h3>',
        '<h3 class="text-2xl font-bold text-white">Artificial Grass &amp; Lawn Installation Leicester</h3>'
    )
    h = h.replace(
        'aria-label="View Lawn Installation service details"',
        'aria-label="View Artificial Grass &amp; Lawn Installation Leicester service details"'
    )

    # Stronger intro — replace both paragraphs in the intro block
    old_intro = (
        '<p class="text-lg text-gray-700 mb-4 leading-relaxed">Premium Landscapes is a full-service landscaping company based in Kirby Muxloe, Leicester. We design and install patios, artificial grass, composite decking, driveways, garden lighting and complete garden makeovers — delivering a professional, tidy finish on every project, every time.</p>\n'
        '                <p class="text-gray-600 leading-relaxed">Every service we offer comes with a free instant quote powered by our AI tool, available 24/7 and delivered in under 90 seconds. No waiting, no pushy sales — just transparent pricing and a photorealistic design concept so you know exactly what you\'re getting before committing to anything.</p>'
    )
    new_intro = (
        '<p class="text-lg text-gray-700 mb-4 leading-relaxed">Premium Landscapes is a full-service landscaping company based in Kirby Muxloe, Leicester, covering Leicester city and across Leicestershire. We design and install <strong>patios</strong>, <strong>artificial grass</strong>, <strong>composite decking</strong>, <strong>driveways</strong>, <strong>garden lighting</strong>, <strong>fencing</strong>, <strong>pergolas</strong>, <strong>turfing</strong> and <strong>full garden makeovers</strong> — delivering a professional, tidy finish on every project, every time.</p>\n'
        '                <p class="text-gray-600 leading-relaxed">Every service comes with a free instant quote, available 24/7 and delivered in under 90 seconds. No waiting, no pushy sales calls — just transparent pricing and a free AI garden design concept so you can see exactly what your garden could look like before committing to anything.</p>'
    )
    h = h.replace(old_intro, new_intro)

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 2. patios.html
# ─────────────────────────────────────────────────────────────────────────────
DRAINAGE_SECTION = '''
    <!-- Drainage & Sub-base Section -->
    <section class="py-16 bg-gray-50">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-6">Patio Drainage, Sub-Base &amp; Leicestershire Clay Soil</h2>
            <div class="prose max-w-none space-y-4 text-gray-700">
                <p class="leading-relaxed">A patio is only as good as what's underneath it. Across Leicester and Leicestershire, the underlying soil is predominantly Mercia Mudstone and heavy clay — both of which move seasonally and drain poorly. Without a correctly designed sub-base, even expensive patio slabs will crack, settle unevenly or lift within a few years.</p>
                <p class="leading-relaxed">Every patio we install begins with excavation to a minimum depth of 150mm (deeper on heavy clay ground), followed by a compacted MOT Type 1 crushed limestone sub-base. This provides a stable, free-draining foundation that moves as a unit rather than cracking under freeze-thaw cycles.</p>
                <p class="leading-relaxed"><strong>Falls and drainage:</strong> All patios are laid to a minimum 1:80 fall (approximately 1.25cm per metre) away from the house, directing rainwater to a lawn, border or suitable drainage channel. On enclosed courtyard patios we install a linear drain or ACO channel connected to a soakaway. This is a building regulation requirement for any surface adjacent to a dwelling.</p>
                <div class="grid md:grid-cols-3 gap-6 mt-6">
                    <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
                        <h3 class="font-bold text-gray-900 mb-2">Sub-base depth</h3>
                        <p class="text-gray-600 text-sm">150–200mm compacted MOT Type 1 on Leicestershire clay ground. Deeper where ground investigations indicate soft spots.</p>
                    </div>
                    <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
                        <h3 class="font-bold text-gray-900 mb-2">Drainage fall</h3>
                        <p class="text-gray-600 text-sm">Minimum 1:80 gradient away from the property. Fully enclosed patios include a linear drain or ACO channel to a soakaway.</p>
                    </div>
                    <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
                        <h3 class="font-bold text-gray-900 mb-2">Jointing</h3>
                        <p class="text-gray-600 text-sm">Porcelain and stone patios jointed with a flexible, polymeric jointing compound rated for UK freeze-thaw conditions — not standard mortar.</p>
                    </div>
                </div>
                <p class="leading-relaxed mt-4">See our <a href="patio-cost-per-m2" class="text-primary font-medium hover:underline">patio cost guide</a> for a full breakdown of material and installation costs in Leicester, or explore our <a href="porcelain-patios-leicester" class="text-primary font-medium hover:underline">porcelain patio installation page</a> for specification details.</p>
            </div>
        </div>
    </section>

'''


def fix_patios():
    p = 'patios.html'
    h = read(p)

    # Soften "most popular patio material"
    h = h.replace(
        'Porcelain is now the most popular patio material for Leicester homeowners',
        'Porcelain is one of the most widely chosen patio materials for Leicester homeowners'
    )

    # Soften "most popular choice" in material cards
    h = h.replace(
        '<p class="text-gray-600 text-center mb-10 max-w-2xl mx-auto">Explore our detailed guides for the most popular patio surface options in Leicester.</p>',
        '<p class="text-gray-600 text-center mb-10 max-w-2xl mx-auto">Explore our detailed guides for every patio surface option we install across Leicester and Leicestershire.</p>'
    )

    # Soften property value FAQ answer
    h = h.replace(
        'Yes — a well-installed patio in Leicester typically adds more value than it costs, particularly if it extends usable outdoor living space. Estate agents consistently report that quality hard landscaping is one of the top features buyers notice.',
        'A well-installed patio can improve the appeal and usability of your outdoor space. Buyers do notice quality hard landscaping, particularly when it extends practical living space — though the impact on market value will always depend on the wider property and local market conditions.'
    )

    # Insert drainage section before FAQ
    h = h.replace(FAQ_ANCHOR, DRAINAGE_SECTION + FAQ_ANCHOR)

    # Add fencing and pergolas to Related Services
    h = h.replace(
        '<a href="artificial-grass" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Artificial Grass Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>',
        '<a href="artificial-grass" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Artificial Grass Leicester</a>\n                <a href="fencing-leicester" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Fencing Leicester</a>\n                <a href="pergolas-leicester" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Pergolas Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>'
    )

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 3. artificial-grass.html
# ─────────────────────────────────────────────────────────────────────────────
AG_SECTIONS = '''
    <!-- Pet, New-Build, Drainage, vs Natural Turf -->
    <section class="py-16 bg-white">
        <div class="max-w-5xl mx-auto px-4 space-y-16">

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Pet-Friendly Artificial Grass in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Dogs and cats are hard on lawns. Muddy paws, digging, toilet patches and heavy use all combine to leave natural grass looking worn within a season. A pet-compatible artificial grass system uses a pile height of 30–35mm with a permeable backing that allows liquid to drain freely — odours don't linger and the surface stays clean with a weekly brush and an occasional rinse. We can add a deodorising infill layer for households with multiple dogs. All installations include a 100g/m² weed membrane and a well-compacted sub-base so there are no lumps or soft areas for dogs to dig into.</p>
                <p class="text-gray-700 leading-relaxed">We've installed pet-friendly artificial grass across Leicester, Oadby, Wigston, Blaby and Narborough — if you'd like to see examples, our <a href="gallery" class="text-primary font-medium hover:underline">gallery page</a> shows recent lawn projects.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Artificial Grass for Muddy New-Build Gardens in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">New-build gardens across Leicestershire are frequently handed over with compacted builder's spoil, a thin covering of topsoil and drainage that doesn't work. Natural turf struggles in these conditions because the soil profile isn't right. Artificial grass solves this in a single installation: we remove the existing sub-standard material, bring the levels up with sharp sand or MOT Type 1 as required, lay a robust geotextile weed membrane and install the artificial turf on top. The result is a level, green, year-round lawn from day one — without waiting years for natural grass to establish.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Artificial Grass Drainage on Leicestershire Clay Soil</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Much of Leicestershire sits on Mercia Mudstone and heavy clay subsoil, which drains slowly and can become waterlogged in autumn and winter. All artificial grass systems we install use a fully permeable backing that allows surface water to pass through. We also install a free-draining sub-base (compacted sharp sand over a layer of MOT Type 1 where ground conditions require it) to carry that water away from the surface and prevent pooling beneath the turf.</p>
                <p class="text-gray-700 leading-relaxed">On gardens with an existing drainage problem, we assess whether a perimeter drain or soakaway is needed before the turf goes down — this is included in our free site survey.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Artificial Grass vs Natural Turf in Leicester</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-sm border-collapse">
                        <thead>
                            <tr class="bg-primary text-white">
                                <th class="text-left py-3 px-4 font-semibold">Feature</th>
                                <th class="text-left py-3 px-4 font-semibold">Artificial Grass</th>
                                <th class="text-left py-3 px-4 font-semibold">Natural Turf</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Maintenance</td><td class="py-3 px-4 text-gray-700">Brush monthly, rinse as needed</td><td class="py-3 px-4 text-gray-700">Mow weekly, feed, aerate, scarify</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Appearance year-round</td><td class="py-3 px-4 text-gray-700">Consistent green all year</td><td class="py-3 px-4 text-gray-700">Can go brown in dry summers</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Child &amp; pet use</td><td class="py-3 px-4 text-gray-700">No mud, suitable for heavy use</td><td class="py-3 px-4 text-gray-700">Can become muddy and worn</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Lifespan</td><td class="py-3 px-4 text-gray-700">10–15+ years</td><td class="py-3 px-4 text-gray-700">Ongoing — reseeding as required</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Environment</td><td class="py-3 px-4 text-gray-700">No mowing emissions; non-recyclable at end of life</td><td class="py-3 px-4 text-gray-700">Supports biodiversity; sequesters carbon</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Cost</td><td class="py-3 px-4 text-gray-700">Higher upfront, lower ongoing</td><td class="py-3 px-4 text-gray-700">Lower upfront, higher ongoing</td></tr>
                        </tbody>
                    </table>
                </div>
                <p class="text-gray-600 text-sm mt-4">Prefer natural turf? See our <a href="turfing-leicester" class="text-primary font-medium hover:underline">turfing and lawn installation service</a>.</p>
            </div>

        </div>
    </section>

'''


def fix_artificial_grass():
    p = 'artificial-grass.html'
    h = read(p)

    # Soften "most popular choice" in material card
    h = h.replace(
        '<p class="text-gray-600 text-sm leading-relaxed">Our most popular choice. Lush, natural appearance with a soft underfoot feel. Ideal for family gardens and play areas.</p>',
        '<p class="text-gray-600 text-sm leading-relaxed">A popular choice for family gardens. Lush, natural appearance with a soft underfoot feel. Ideal for both children and adults.</p>'
    )

    # Soften "pays for itself" on composite decking page — dealt with below; here it's AG
    # (AG page doesn't have "pays for itself" per our grep)

    # Insert 4 new H2 sections before FAQ
    h = h.replace(FAQ_ANCHOR, AG_SECTIONS + FAQ_ANCHOR)

    # Add turfing + commercial-astroturf to Related Services
    h = h.replace(
        '<a href="composite-decking" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Composite Decking Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>',
        '<a href="composite-decking" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Composite Decking Leicester</a>\n                <a href="turfing-leicester" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Natural Turfing Leicester</a>\n                <a href="commercial-astroturf-leicester" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Commercial Astroturf Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>'
    )

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 4. composite-decking.html
# ─────────────────────────────────────────────────────────────────────────────
DECKING_SECTIONS = '''
    <!-- Raised Decking, Subframe, Lighting, Anti-slip -->
    <section class="py-16 bg-white">
        <div class="max-w-5xl mx-auto px-4 space-y-16">

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Raised Decking and Planning Permission in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Most domestic decking falls within Permitted Development rights and does not require planning permission. However, raised decking over 300mm above ground level, or decking in a conservation area, may require an application. The key rules under the General Permitted Development Order (GPDO) Class E are that decking must not cover more than 50% of the curtilage (garden area excluding the house), must not be to the front of the house and must not exceed 300mm above the existing ground level without consent.</p>
                <p class="text-gray-700 leading-relaxed">If your project is in a Leicestershire conservation area (such as parts of Oadby, Stoneygate or the Market Harborough edge), we recommend checking with Blaby, Oadby &amp; Wigston, or Leicester City Council before proceeding. We can advise during the survey.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Timber Subframe vs Aluminium Subframe for Composite Decking</h2>
                <div class="overflow-x-auto mb-4">
                    <table class="w-full text-sm border-collapse">
                        <thead>
                            <tr class="bg-primary text-white">
                                <th class="text-left py-3 px-4 font-semibold">Factor</th>
                                <th class="text-left py-3 px-4 font-semibold">Treated Timber Subframe</th>
                                <th class="text-left py-3 px-4 font-semibold">Aluminium Subframe</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Lifespan</td><td class="py-3 px-4 text-gray-700">15–20 years with correct treatment</td><td class="py-3 px-4 text-gray-700">30–40+ years, corrosion-resistant</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Cost</td><td class="py-3 px-4 text-gray-700">Lower upfront</td><td class="py-3 px-4 text-gray-700">Higher upfront</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Moisture resistance</td><td class="py-3 px-4 text-gray-700">Requires pressure-treated timber, still susceptible over time</td><td class="py-3 px-4 text-gray-700">Fully moisture and rot proof</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Warranty compatibility</td><td class="py-3 px-4 text-gray-700">Acceptable for most board warranties</td><td class="py-3 px-4 text-gray-700">Recommended by premium board manufacturers</td></tr>
                        </tbody>
                    </table>
                </div>
                <p class="text-gray-600 text-sm">We recommend aluminium subframes for ground-level decking where ventilation is restricted, and for any decking over water features or on roof terraces.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Composite Decking with Built-In Garden Lighting</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Combining composite decking with integrated LED lighting is one of the most popular upgrades we carry out in Leicester. Decking lights can be recessed into the board fascia, fitted into the subframe riser boards or installed as post cap lights — all running from a low-voltage (12V or 24V) transformer that's safe to install near water features and in wet conditions.</p>
                <p class="text-gray-700 leading-relaxed">Step lights and fascia lights are the most practical option: they mark the edge of the deck at night without creating glare and require no additional cabling run across the surface. We plan and install all garden lighting as part of the decking project so the cable is concealed within the subframe before the boards go down. See our <a href="garden-lighting" class="text-primary font-medium hover:underline">garden lighting service</a> for more detail.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Anti-Slip Composite Decking for UK Gardens</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Slip resistance is a practical concern for UK gardens, where rain, fallen leaves and algae growth all reduce grip on outdoor surfaces. All composite decking boards we supply have an embossed or brushed surface texture that maintains grip when wet. Full-cap composite boards with a co-extruded polymer surface are particularly resistant to algae because moisture cannot penetrate the outer layer.</p>
                <p class="text-gray-700 leading-relaxed">For additional peace of mind around pools, hot tubs or steps, we can specify boards with a higher R-value slip rating and install non-slip nosing strips on step edges. If you have a specific use-case concern, mention it during the quote and we'll specify accordingly.</p>
            </div>

        </div>
    </section>

'''


def fix_composite_decking():
    p = 'composite-decking.html'
    h = read(p)

    # Soften "pays for itself"
    h = h.replace(
        'a long-term investment that pays for itself',
        'a durable long-term choice'
    )

    # Soften "most popular premium choice"
    h = h.replace(
        '<p class="text-gray-600 text-sm leading-relaxed">Four-sided polymer capping protects every board. Maximum resistance to staining, fading and moisture. Our most popular premium choice.</p>',
        '<p class="text-gray-600 text-sm leading-relaxed">Four-sided polymer capping protects every board. Maximum resistance to staining, fading and moisture. A premium full-cap board option.</p>'
    )

    # Insert 4 new sections before FAQ
    h = h.replace(FAQ_ANCHOR, DECKING_SECTIONS + FAQ_ANCHOR)

    # Add pergolas to Related Services
    h = h.replace(
        '<a href="full-garden-makeover" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Full Garden Makeover Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>',
        '<a href="full-garden-makeover" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Full Garden Makeover Leicester</a>\n                <a href="pergolas-leicester" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Pergolas Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>'
    )

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 5. driveways.html
# ─────────────────────────────────────────────────────────────────────────────
DRIVEWAY_COMPARISON = '''
    <!-- Driveway Comparison Table -->
    <section class="py-16 bg-gray-50">
        <div class="max-w-5xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-4 text-center">Block Paving vs Resin Bound vs Tarmac vs Gravel</h2>
            <p class="text-gray-600 text-center mb-8 max-w-2xl mx-auto">Every driveway surface has a different combination of cost, appearance, drainage and maintenance. Here's a straightforward comparison for Leicester homeowners.</p>
            <div class="overflow-x-auto">
                <table class="w-full text-sm border-collapse">
                    <thead>
                        <tr class="bg-primary text-white">
                            <th class="text-left py-3 px-4 font-semibold">Surface</th>
                            <th class="text-left py-3 px-4 font-semibold">Typical cost (supply &amp; install)</th>
                            <th class="text-left py-3 px-4 font-semibold">Permeable?</th>
                            <th class="text-left py-3 px-4 font-semibold">Lifespan</th>
                            <th class="text-left py-3 px-4 font-semibold">Maintenance</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Block paving</td><td class="py-3 px-4 text-gray-700">£70–£120/m²</td><td class="py-3 px-4 text-gray-700">Yes (permeable jointing)</td><td class="py-3 px-4 text-gray-700">25–30 years</td><td class="py-3 px-4 text-gray-700">Re-joint every 5–10 years; individual blocks replaceable</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Resin bound</td><td class="py-3 px-4 text-gray-700">£85–£140/m²</td><td class="py-3 px-4 text-gray-700">Yes (inherently permeable)</td><td class="py-3 px-4 text-gray-700">15–25 years</td><td class="py-3 px-4 text-gray-700">Occasional weed treatment; re-coat if surface wears</td></tr>
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Tarmac</td><td class="py-3 px-4 text-gray-700">£50–£80/m²</td><td class="py-3 px-4 text-gray-700">No (standard tarmac)</td><td class="py-3 px-4 text-gray-700">20–30 years</td><td class="py-3 px-4 text-gray-700">Re-seal every 3–5 years; repair cracks promptly</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Gravel</td><td class="py-3 px-4 text-gray-700">£30–£50/m²</td><td class="py-3 px-4 text-gray-700">Yes</td><td class="py-3 px-4 text-gray-700">Indefinite (replenish gravel)</td><td class="py-3 px-4 text-gray-700">Rake regularly; top up gravel annually</td></tr>
                    </tbody>
                </table>
            </div>
            <p class="text-gray-500 text-xs mt-3 text-center">Indicative costs for Leicester and Leicestershire. Final price depends on access, excavation depth and disposal costs. <a href="garden-landscaping-cost-calculator" class="text-primary hover:underline">Use our free calculator</a> for a personalised estimate.</p>
        </div>
    </section>

'''

DRIVEWAY_PLANNING_SECTION = '''
    <!-- Planning Permission & Drainage -->
    <section class="py-16 bg-white">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-6">Driveway Planning Permission &amp; Drainage Rules in Leicester</h2>
            <div class="prose max-w-none space-y-4 text-gray-700">
                <p class="leading-relaxed">Permitted development rules in England require that front driveways over 5m² use a permeable surface, or that surface water drains to a lawn, border or soakaway — rather than running directly onto the highway or into the public drain. This applies to residential properties in Leicester, Oadby &amp; Wigston, Blaby and the wider Leicestershire area.</p>
                <p class="leading-relaxed"><strong>Permeable block paving</strong> (using open-jointed blocks or permeable mortar-free jointing) and <strong>resin bound gravel</strong> both satisfy the permitted development drainage requirements. Standard impermeable block paving with a solid mortar bed, or standard tarmac, may require planning permission if water cannot be directed to a permeable area or soakaway.</p>
                <p class="leading-relaxed">If your property is in a designated conservation area, an AONB or if you have a listed building consent requirement, additional rules may apply. We advise on this as part of every free site survey.</p>
                <div class="bg-blue-50 border border-blue-100 rounded-xl p-5 mt-4">
                    <p class="text-blue-900 font-medium text-sm">Relevant guidance: DCLG "Guidance on the permeable surfacing of front gardens" (2008) and the General Permitted Development Order (England) 2015, Class F.</p>
                </div>
            </div>
        </div>
    </section>

'''


def fix_driveways():
    p = 'driveways.html'
    h = read(p)

    # Soften "5–10% to a property's value"
    h = h.replace(
        'while a fresh, well-designed driveway adds immediate kerb appeal and is estimated to add 5–10% to a property\'s value.',
        'while a fresh, well-designed driveway adds immediate kerb appeal and makes a strong first impression.'
    )

    # Soften "returning 70–100% of its cost in added property value"
    h = h.replace(
        'A new driveway is one of the highest-ROI improvements you can make to a Leicestershire home — typically returning 70–100% of its cost in added property value.',
        'A new driveway is one of the most practical improvements you can make to a Leicestershire home — improving kerb appeal, drainage and everyday usability.'
    )

    # Soften "UK's most popular driveway choice"
    h = h.replace(
        '<p class="text-gray-600 text-sm leading-relaxed">The UK\'s most popular driveway choice. Highly durable, repairable and available in a huge range of colours and patterns. Classic herringbone or stretcher bond.</p>',
        '<p class="text-gray-600 text-sm leading-relaxed">A widely installed driveway surface. Highly durable, fully repairable and available in a huge range of colours and patterns. Classic herringbone or stretcher bond.</p>'
    )

    # Soften "UK's most popular" in prose
    h = h.replace(
        'Block paving remains the most popular driveway surface across Leicester and Leicestershire',
        'Block paving is a widely chosen driveway surface across Leicester and Leicestershire'
    )

    # Fix "no planning permission required" in resin card on driveways page
    h = h.replace(
        'SUDS-compliant — no planning permission required.',
        'SuDS-compliant — meets permitted development drainage requirements for front drives.'
    )

    # "highest-ROI" softening in hero subtext
    h = h.replace(
        'adds real value',
        'improves kerb appeal'
    )

    # Insert planning section + comparison table before FAQ
    h = h.replace(FAQ_ANCHOR, DRIVEWAY_PLANNING_SECTION + DRIVEWAY_COMPARISON + FAQ_ANCHOR)

    # Add block paving / resin links to Related Services
    h = h.replace(
        '<a href="garden-lighting" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Garden Lighting Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>',
        '<a href="garden-lighting" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Garden Lighting Leicester</a>\n                <a href="block-paving-driveways-leicester" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Block Paving Driveways Leicester</a>\n                <a href="resin-driveways-leicester" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Resin Bound Driveways Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>'
    )

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 6. garden-lighting.html
# ─────────────────────────────────────────────────────────────────────────────
LIGHTING_SECTIONS = '''
    <!-- Lighting type sections -->
    <section class="py-16 bg-white">
        <div class="max-w-5xl mx-auto px-4 space-y-16">

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Patio and Pergola Lighting in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">A patio or pergola is used most on warm evenings — so lighting isn't an optional extra, it's what makes the space functional after sunset. We install IP65-rated LED spotlights on pergola uprights and beams, recessed low-level lights into patio walls and steps, and colour-temperature adjustable strips that let you switch between warm white (relaxed evening mood) and cool white (working or cooking). All lighting is installed on a dedicated low-voltage (12V or 24V) transformer with a weatherproof outdoor controller so you can dim, switch zones and set timers without going inside.</p>
                <p class="text-gray-600 text-sm">See our <a href="pergolas-leicester" class="text-primary font-medium hover:underline">pergola installation page</a> for examples of combined pergola and lighting projects.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Decking Lights and Step Lighting</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Recessed decking lights and riser lights are the most practical form of garden lighting for composite or timber decking: they mark the edge of each step clearly, eliminate trip hazards at night and require no additional cabling run across the surface. We plan and install all decking lights as part of the decking project so the cable is concealed in the subframe before the boards go down. Fascia-mounted lights are also popular — fitted into the horizontal board below each deck level, creating a strip of warm light that outlines the deck without glare.</p>
                <p class="text-gray-600 text-sm">See our <a href="composite-decking" class="text-primary font-medium hover:underline">composite decking page</a> for combined decking and lighting projects.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Smart Garden Lighting Systems</h2>
                <p class="text-gray-700 leading-relaxed mb-3">We install smart garden lighting systems compatible with the major platforms — including systems that can be controlled via a smartphone app, set to respond to dusk/dawn sensors or programmed with weekly schedules. Smart controllers can manage multiple lighting zones independently, so your patio, pathway, driveway and pergola lighting can all be on different schedules and brightness levels. All smart systems we install use low-voltage transformers and are suitable for permanent outdoor installation across Leicestershire's climate.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Garden Lighting as Part of a Full Garden Makeover</h2>
                <p class="text-gray-700 leading-relaxed mb-3">The most cost-effective time to install garden lighting is during a full garden makeover, before paving, decking or rendered walls are finished. Cable can be laid under hard surfaces before they go down and conduit can be built into walls during construction — a significant saving compared to retrofitting lighting into a finished garden later. If you're planning a full garden transformation, we plan the lighting scheme at the design stage and install it as a single coordinated project. See our <a href="full-garden-makeover" class="text-primary font-medium hover:underline">full garden makeover page</a> for how this works in practice.</p>
            </div>

        </div>
    </section>

'''


def fix_garden_lighting():
    p = 'garden-lighting.html'
    h = read(p)

    # Soften burglary claim
    h = h.replace(
        'A well-lit property is significantly less likely to be targeted by opportunist burglars, and buyers consistently rate quality outdoor lighting as one of the features that make a property feel premium and well-cared-for.',
        'A well-lit garden can make your property more visible and welcoming at night, and buyers consistently rate quality outdoor lighting as one of the features that make a property feel well-maintained and cared-for.'
    )

    # Insert 4 lighting sections before FAQ
    h = h.replace(FAQ_ANCHOR, LIGHTING_SECTIONS + FAQ_ANCHOR)

    # Add pergolas to Related Services
    old_gl_related = '<a href="artificial-grass" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Artificial Grass Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>'
    new_gl_related = '<a href="artificial-grass" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Artificial Grass Leicester</a>\n                <a href="pergolas-leicester" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Pergolas Leicester</a>\n            </div>\n            <p class="text-sm text-gray-500 mb-3">Areas we cover</p>'
    h = h.replace(old_gl_related, new_gl_related)

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 7. full-garden-makeover.html
# ─────────────────────────────────────────────────────────────────────────────
MAKEOVER_PROJECTS_SECTION = '''
    <!-- Project Examples Structure -->
    <section class="py-16 bg-gray-50">
        <div class="max-w-5xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">Full Garden Makeover Projects in Leicester &amp; Leicestershire</h2>
            <p class="text-gray-700 mb-8 leading-relaxed">The projects below illustrate the kinds of transformations we carry out across Leicester and Leicestershire — from compact urban courtyard gardens to larger family spaces on new-build estates. We do not use stock photography or invented examples: the images and descriptions on our gallery and case study pages reflect work we have actually completed. As our case study library grows, we will link individual projects here.</p>
            <div class="grid md:grid-cols-3 gap-6 mb-8">
                <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                    <div class="text-3xl mb-3">🏡</div>
                    <h3 class="font-bold text-gray-900 mb-2">Patio + artificial grass combination</h3>
                    <p class="text-gray-600 text-sm leading-relaxed">Our most common project type. Typically a porcelain or natural stone patio to one end, artificial grass to the other, with a clear edge restraint. Works on most garden sizes and orientations.</p>
                </div>
                <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                    <div class="text-3xl mb-3">🌿</div>
                    <h3 class="font-bold text-gray-900 mb-2">Multi-zone garden design</h3>
                    <p class="text-gray-600 text-sm leading-relaxed">Patio, decking, lighting, fencing and planting combined into a single designed space. Suited to larger gardens where different functional zones are needed — relaxing, dining, play, storage.</p>
                </div>
                <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                    <div class="text-3xl mb-3">🆕</div>
                    <h3 class="font-bold text-gray-900 mb-2">New-build garden from scratch</h3>
                    <p class="text-gray-600 text-sm leading-relaxed">New builds across Leicestershire are often handed over with unfinished gardens — builder's spoil, poor drainage and no level. We design and build the complete garden in a single project.</p>
                </div>
            </div>
            <div class="text-center">
                <a href="gallery" class="inline-block bg-primary text-white px-6 py-3 rounded-full font-semibold hover:bg-blue-700 transition mr-3">View Project Gallery</a>
                <a href="case-studies" class="inline-block bg-white border border-primary text-primary px-6 py-3 rounded-full font-semibold hover:bg-blue-50 transition">View Case Studies</a>
            </div>
        </div>
    </section>

'''


def fix_full_garden_makeover():
    p = 'full-garden-makeover.html'
    h = read(p)

    # Insert project examples before FAQ
    h = h.replace(FAQ_ANCHOR, MAKEOVER_PROJECTS_SECTION + FAQ_ANCHOR)

    # Add gallery, case studies, garden design, cost guide to Related Services
    old_related = (
        '<a href="garden-design" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Garden Design</a>\n'
        '                <a href="patios" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Patios Leicester</a>\n'
        '                <a href="artificial-grass" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Artificial Grass Leicester</a>\n'
        '                <a href="composite-decking" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Composite Decking Leicester</a>\n'
        '                <a href="garden-lighting" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Garden Lighting Leicester</a>'
    )
    new_related = (
        '<a href="garden-design-leicester" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Garden Design Leicester</a>\n'
        '                <a href="patios" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Patios Leicester</a>\n'
        '                <a href="artificial-grass" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Artificial Grass Leicester</a>\n'
        '                <a href="composite-decking" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Composite Decking Leicester</a>\n'
        '                <a href="garden-lighting" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Garden Lighting Leicester</a>\n'
        '                <a href="driveways" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Driveways Leicester</a>\n'
        '                <a href="cost-guide" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Landscaping Cost Guide</a>\n'
        '                <a href="case-studies" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Case Studies</a>'
    )
    h = h.replace(old_related, new_related)

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 8. ai-garden-design.html
# ─────────────────────────────────────────────────────────────────────────────
AI_REAL_COMPANY_SECTION = '''
    <!-- Real Company + AI vs Traditional -->
    <section class="py-16 bg-gray-50">
        <div class="max-w-5xl mx-auto px-4 space-y-16">

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Premium Landscapes: A Real Leicester Landscaping Company Using AI Design</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Premium Landscapes is a Leicester-based landscaping and garden design company, not an AI software tool or online-only service. We design and physically build patios, driveways, artificial grass, composite decking, garden lighting, fencing, pergolas and full garden makeovers across Leicester and Leicestershire. Our AI garden design tool is part of the quote process — it gives you a photorealistic visualisation of your garden so you can see the result before a single slab is laid.</p>
                <p class="text-gray-700 leading-relaxed">The design is created using the photo you submit of your current garden. It's not a generic simulation — it's your garden, transformed. Once you have the design concept, our team carry out a site survey, agree a final specification and build the project. The AI design is a starting point and discussion tool, not a binding construction drawing.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">AI Garden Design vs Traditional Landscaping Quotes</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-sm border-collapse">
                        <thead>
                            <tr class="bg-primary text-white">
                                <th class="text-left py-3 px-4 font-semibold">Factor</th>
                                <th class="text-left py-3 px-4 font-semibold">Traditional quote process</th>
                                <th class="text-left py-3 px-4 font-semibold">Our AI-assisted process</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">First contact to design concept</td><td class="py-3 px-4 text-gray-700">Days to weeks (site visit first)</td><td class="py-3 px-4 text-gray-700">90 seconds after submitting your photo</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Cost of initial design</td><td class="py-3 px-4 text-gray-700">Often charged separately (£200–£800+)</td><td class="py-3 px-4 text-gray-700">Free — included in the quote process</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Can you see the result beforehand?</td><td class="py-3 px-4 text-gray-700">Mood boards or hand sketches</td><td class="py-3 px-4 text-gray-700">Photorealistic visualisation of your own garden</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Obligation</td><td class="py-3 px-4 text-gray-700">Often expected after a site visit</td><td class="py-3 px-4 text-gray-700">None — design and quote are free</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Site survey still needed?</td><td class="py-3 px-4 text-gray-700">Yes</td><td class="py-3 px-4 text-gray-700">Yes — before finalising specification and price</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </section>

'''


def fix_ai_garden_design():
    p = 'ai-garden-design.html'
    h = read(p)

    # Insert before FAQ section
    h = h.replace(FAQ_ANCHOR, AI_REAL_COMPANY_SECTION + FAQ_ANCHOR)

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 9. garden-design-leicester.html
# ─────────────────────────────────────────────────────────────────────────────
GARDEN_DESIGN_SECTIONS = '''
    <!-- Design and Build + Garden Type sections -->
    <section class="py-16 bg-gray-50">
        <div class="max-w-5xl mx-auto px-4 space-y-16">

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Garden Design and Build — Not Just Drawings</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Most garden design work we carry out in Leicester is part of a complete design-and-build project — not a standalone drawing service. We don't typically produce a set of plans for you to pass to another contractor. Instead, we work with you from initial concept to the finished garden: visiting the site, agreeing the design and materials, managing all the groundworks and installation, and leaving the site clean and complete.</p>
                <p class="text-gray-700 leading-relaxed">This approach is more practical for most Leicester homeowners because it avoids the coordination problems that come from separating design from build, and it ensures that what we design is actually buildable within your budget and site constraints.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Small Garden Design in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Many gardens in Leicester's Victorian terraces, 1930s semis and inner-city new builds are compact — often 30–60m². The design challenge in a small garden is to make every square metre work: a seating area, a lawn or planted space, storage and somewhere to put the bins — all without the garden feeling crowded. We work with small gardens regularly across Clarendon Park, Stoneygate, Birstall and Oadby, and the design principles we apply are simple: clean lines, fewer materials, higher-quality finishes and multi-purpose elements like seating walls that double as planters.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Modern Garden Design in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">A modern garden design typically uses a limited palette of contemporary materials — large-format porcelain paving, composite decking, steel-edged planted borders and low-voltage LED lighting — combined with clean, geometric lines and minimal ornament. We install modern garden designs across Leicester and Leicestershire, from compact urban courtyards to larger plots in Oadby, Wigston and the Blaby district. The AI design tool we offer as part of the free quote process is particularly useful for visualising a modern garden: the rendered result shows exactly how the materials and proportions will look in your specific garden.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Low-Maintenance Garden Design in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">The most common brief we receive for Leicester garden designs is some version of "we want it to look great but we don't want to spend every weekend maintaining it." Low-maintenance doesn't mean no planting — it means choosing the right hard landscaping materials (porcelain, composite, artificial grass) paired with carefully selected, slow-growing or drought-tolerant planting that doesn't need constant attention. We design and build low-maintenance gardens across Leicestershire that look well-kept year-round without demanding time the homeowner doesn't have.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Family Garden Design in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">A family garden needs to serve multiple ages and uses simultaneously: a safe surface for young children, a lawn or grass area for play, an outdoor dining area for adults, and somewhere to put bikes, trampolines and garden toys without them taking over the whole space. We design family gardens across Leicester that balance these needs practically — using artificial grass for the play lawn (no mud, all weather), a patio for dining, and considered zoning so the garden works for children now and adapts as they grow up.</p>
            </div>

        </div>
    </section>

'''


def fix_garden_design():
    p = 'garden-design-leicester.html'
    h = read(p)
    h = h.replace(FAQ_ANCHOR, GARDEN_DESIGN_SECTIONS + FAQ_ANCHOR)
    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 10. porcelain-patios-leicester.html
# ─────────────────────────────────────────────────────────────────────────────
PORCELAIN_SPEC_SECTION = '''
    <!-- Spec section + comparison table -->
    <section class="py-16 bg-gray-50">
        <div class="max-w-5xl mx-auto px-4 space-y-16">

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-6">Porcelain Patio Installation Specification</h2>
                <div class="overflow-x-auto mb-6">
                    <table class="w-full text-sm border-collapse">
                        <tbody class="divide-y divide-gray-100">
                            <tr class="bg-white"><td class="py-3 px-4 font-semibold text-gray-900 w-1/3">Excavation depth</td><td class="py-3 px-4 text-gray-700">Minimum 150mm (deeper on Leicestershire clay subsoil where required)</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-semibold text-gray-900">Sub-base</td><td class="py-3 px-4 text-gray-700">MOT Type 1 crushed limestone, compacted in 75mm layers to a minimum 100mm finished depth</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-semibold text-gray-900">Priming</td><td class="py-3 px-4 text-gray-700">Porcelain slabs back-primed with a porcelain bonding slurry to ensure full adhesion to the mortar bed</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-semibold text-gray-900">Mortar bed</td><td class="py-3 px-4 text-gray-700">Full, solid mortar bed (semi-dry mix) — no spot-bedding; eliminates hollow spots and future cracking</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-semibold text-gray-900">Fall / drainage</td><td class="py-3 px-4 text-gray-700">Minimum 1:80 gradient away from the dwelling; linear drain or ACO channel on enclosed patios</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-semibold text-gray-900">Jointing</td><td class="py-3 px-4 text-gray-700">Flexible polymeric jointing compound rated for UK freeze-thaw cycles — not standard mortar</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-semibold text-gray-900">Edge restraint</td><td class="py-3 px-4 text-gray-700">Concrete haunch to all perimeter edges; no unsupported slab overhangs</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-6">Porcelain vs Sandstone: Which is Right for Your Leicester Garden?</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-sm border-collapse">
                        <thead>
                            <tr class="bg-primary text-white">
                                <th class="text-left py-3 px-4 font-semibold">Feature</th>
                                <th class="text-left py-3 px-4 font-semibold">Porcelain</th>
                                <th class="text-left py-3 px-4 font-semibold">Sandstone</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Maintenance</td><td class="py-3 px-4 text-gray-700">Virtually none — wipe clean, no sealing</td><td class="py-3 px-4 text-gray-700">Annual sealing recommended; absorbs oils and algae</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Frost resistance</td><td class="py-3 px-4 text-gray-700">Fully frost-proof (vitrified tile)</td><td class="py-3 px-4 text-gray-700">Some grades susceptible to spalling in hard frosts</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Appearance</td><td class="py-3 px-4 text-gray-700">Consistent colour and texture, contemporary</td><td class="py-3 px-4 text-gray-700">Natural variation, warm/traditional character</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Slip resistance</td><td class="py-3 px-4 text-gray-700">Specify R11 or textured finish for wet areas</td><td class="py-3 px-4 text-gray-700">Naturally textured — generally good grip when wet</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Cost (supply &amp; install)</td><td class="py-3 px-4 text-gray-700">From £90–£140/m²</td><td class="py-3 px-4 text-gray-700">From £75–£120/m²</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Lifespan</td><td class="py-3 px-4 text-gray-700">30+ years with correct installation</td><td class="py-3 px-4 text-gray-700">20–25 years with maintenance</td></tr>
                        </tbody>
                    </table>
                </div>
                <p class="text-gray-600 text-sm mt-4">See also: <a href="sandstone-patios-leicester" class="text-primary font-medium hover:underline">Sandstone Patios Leicester</a> · <a href="patios" class="text-primary font-medium hover:underline">All Patio Options</a> · <a href="patio-cost-per-m2" class="text-primary font-medium hover:underline">Patio Cost Guide 2026</a></p>
            </div>

        </div>
    </section>

'''


def fix_porcelain_patios():
    p = 'porcelain-patios-leicester.html'
    h = read(p)
    h = h.replace(FAQ_ANCHOR, PORCELAIN_SPEC_SECTION + FAQ_ANCHOR)
    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 11. block-paving-driveways-leicester.html
# ─────────────────────────────────────────────────────────────────────────────
def fix_block_paving():
    p = 'block-paving-driveways-leicester.html'
    h = read(p)

    # Tighten planning wording — find and replace the FAQ answer about planning
    h = h.replace(
        'most chosen driveway surface across Leicester and Leicestershire — and for good reason. It\'s hard-wearing, fully repairable, available in a huge range of colours and patterns, and when properly installed adds immediate kerb appeal and real property value.',
        'a widely installed driveway surface across Leicester and Leicestershire — hard-wearing, fully repairable and available in a huge range of colours and patterns.'
    )

    # Soften "most popular pattern"
    h = h.replace(
        '<p>The most popular pattern for driveways — interlocking at 45° or 90°, herringbone distributes vehicle load evenly across the surface and is the most structurally stable pattern. Classic look, suits all property types.</p>',
        '<p>A widely used pattern for driveways — interlocking at 45° or 90°, herringbone distributes vehicle load evenly across the surface and is structurally stable. Classic look, suits all property types.</p>'
    )

    # Tighten planning permission wording
    h = h.replace(
        "planning permission isn't required for permeable jointing",
        'permeable block paving systems satisfy SuDS requirements for front driveways under 5m², and permeable jointing on standard block paving can also meet these requirements'
    )

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 12. resin-driveways-leicester.html
# ─────────────────────────────────────────────────────────────────────────────
RESIN_BOUND_VS_BONDED = '''
    <!-- Resin Bound vs Resin Bonded -->
    <section class="py-16 bg-gray-50">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-6">Resin Bound vs Resin Bonded Driveways: What's the Difference?</h2>
            <div class="overflow-x-auto mb-6">
                <table class="w-full text-sm border-collapse">
                    <thead>
                        <tr class="bg-primary text-white">
                            <th class="text-left py-3 px-4 font-semibold">Feature</th>
                            <th class="text-left py-3 px-4 font-semibold">Resin Bound</th>
                            <th class="text-left py-3 px-4 font-semibold">Resin Bonded</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">How it works</td><td class="py-3 px-4 text-gray-700">Aggregate mixed with resin, trowelled as a solid, smooth layer</td><td class="py-3 px-4 text-gray-700">Resin applied to surface, loose aggregate scattered on top</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Surface finish</td><td class="py-3 px-4 text-gray-700">Smooth, sealed, professional-grade</td><td class="py-3 px-4 text-gray-700">Textured, gravel-like surface</td></tr>
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Permeability</td><td class="py-3 px-4 text-gray-700">Fully permeable — SuDS-compliant</td><td class="py-3 px-4 text-gray-700">Not permeable — surface is sealed</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Loose stones</td><td class="py-3 px-4 text-gray-700">None — aggregate is fully encapsulated</td><td class="py-3 px-4 text-gray-700">Can shed stones over time</td></tr>
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Cost</td><td class="py-3 px-4 text-gray-700">Higher — from £85/m²</td><td class="py-3 px-4 text-gray-700">Lower — from £40/m²</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Recommended for driveways?</td><td class="py-3 px-4 text-gray-700">Yes — our standard specification</td><td class="py-3 px-4 text-gray-700">Not recommended for vehicle traffic</td></tr>
                    </tbody>
                </table>
            </div>
            <p class="text-gray-700 leading-relaxed">We only install <strong>resin bound</strong> driveways — not resin bonded. The resin bonded process produces a cheaper result but the surface sheds aggregate stones under vehicle loads and is not SuDS-compliant, making it unsuitable for most front driveway applications. All our resin driveways are installed over a sound, primed base (existing tarmac, concrete or new MOT Type 1 base) with UV-stable polyurethane resin that will not yellow over time.</p>
        </div>
    </section>

'''


def fix_resin_driveways():
    p = 'resin-driveways-leicester.html'
    h = read(p)

    # Fix "no planning permission required" language
    h = h.replace(
        '<strong>Fully permeable — no planning permission required:</strong> Under UK regulations, front driveways over 5m² must use a permeable surface or drain to a soakaway. Resin bound gravel is naturally permeable — water passes straight through the surface, making it SuDS-compliant and exempt from planning permission requirements.',
        '<strong>SuDS-compliant when installed over a suitable permeable base or drainage system:</strong> Under UK planning guidance, front driveways over 5m² should use a permeable surface or direct water to a permeable area or soakaway. Resin bound gravel is inherently permeable — water passes through the surface — which means it generally satisfies the permitted development drainage requirement. Always confirm the position with your local planning authority if in doubt.'
    )

    # Insert resin bound vs bonded section before FAQ
    h = h.replace(FAQ_ANCHOR, RESIN_BOUND_VS_BONDED + FAQ_ANCHOR)

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 13. fencing-leicester.html — add FAQ items for cost, removal, posts, composite, storm
# ─────────────────────────────────────────────────────────────────────────────
FENCING_EXTRA_FAQS = '''                <div class="faq-item py-5">
                    <button onclick="toggleFaq(10)" class="flex items-center justify-between w-full text-left">
                        <h3 class="font-semibold text-gray-900 pr-4">How much does fencing cost per metre in Leicester?</h3>
                        <i id="faq-icon-10" class="fas fa-chevron-down text-primary transition-transform flex-shrink-0"></i>
                    </button>
                    <div id="faq-10" class="hidden mt-3 text-gray-600 leading-relaxed">Installed fencing costs in Leicester typically range from £60–£120 per metre for standard close-board panels on timber posts, rising to £120–£200+ per metre for composite fencing or decorative metal panels. The total depends on panel type, post specification (timber, concrete or steel), access and whether old fencing needs removing. We provide free itemised quotes for all fencing projects in Leicester and Leicestershire.</div>
                </div>
                <div class="faq-item py-5">
                    <button onclick="toggleFaq(11)" class="flex items-center justify-between w-full text-left">
                        <h3 class="font-semibold text-gray-900 pr-4">Do you remove old fencing before installing the new fence?</h3>
                        <i id="faq-icon-11" class="fas fa-chevron-down text-primary transition-transform flex-shrink-0"></i>
                    </button>
                    <div id="faq-11" class="hidden mt-3 text-gray-600 leading-relaxed">Yes — old fencing removal is included in most of our fencing quotes. We remove and dispose of existing panels, rails and posts (including concrete post extraction where needed). The disposal cost is factored into the quoted price so there are no surprises. If the existing concrete posts are still in good structural condition, we can sometimes reuse them, which reduces cost.</div>
                </div>
                <div class="faq-item py-5">
                    <button onclick="toggleFaq(12)" class="flex items-center justify-between w-full text-left">
                        <h3 class="font-semibold text-gray-900 pr-4">Concrete posts vs timber posts — which is better?</h3>
                        <i id="faq-icon-12" class="fas fa-chevron-down text-primary transition-transform flex-shrink-0"></i>
                    </button>
                    <div id="faq-12" class="hidden mt-3 text-gray-600 leading-relaxed">Concrete posts are more durable and longer-lasting than timber — they won't rot at ground level, which is the most common point of failure for timber fence posts. They do cost more upfront and are heavier to work with. For standard close-board fencing on a long run, concrete posts are generally the better long-term value. Timber posts are appropriate where flexibility is needed (curved runs, tight access) or for lower-specification temporary boundary fencing.</div>
                </div>
                <div class="faq-item py-5">
                    <button onclick="toggleFaq(13)" class="flex items-center justify-between w-full text-left">
                        <h3 class="font-semibold text-gray-900 pr-4">Do you install composite fencing in Leicester?</h3>
                        <i id="faq-icon-13" class="fas fa-chevron-down text-primary transition-transform flex-shrink-0"></i>
                    </button>
                    <div id="faq-13" class="hidden mt-3 text-gray-600 leading-relaxed">Yes — we install composite fencing panels alongside our composite decking service. Composite fencing uses the same wood-plastic composite material as decking boards: it won't rot, fade or splinter, requires no painting or staining, and maintains a consistent appearance year-round. It's a good match aesthetically with composite decking or patios in a modern garden design.</div>
                </div>
                <div class="faq-item py-5">
                    <button onclick="toggleFaq(14)" class="flex items-center justify-between w-full text-left">
                        <h3 class="font-semibold text-gray-900 pr-4">Can you replace storm-damaged fencing quickly?</h3>
                        <i id="faq-icon-14" class="fas fa-chevron-down text-primary transition-transform flex-shrink-0"></i>
                    </button>
                    <div id="faq-14" class="hidden mt-3 text-gray-600 leading-relaxed">We handle storm-damage fence replacement across Leicester and Leicestershire. Response time depends on the volume of storm damage in the area — in the immediate aftermath of a significant storm, there is typically a queue. Temporary boarding of vulnerable sections can be arranged while a permanent replacement is scheduled. Get in touch via our contact page or WhatsApp to discuss urgent fence repair in Leicester.</div>
                </div>
'''


def fix_fencing():
    p = 'fencing-leicester.html'
    h = read(p)

    # Find the closing div of the FAQ items section
    # We'll append new FAQs before the closing </div> of the FAQ container
    faq_end_marker = '            </div>\n        </div>\n    </section>\n    <script>\n        function toggleFaq'

    # Check if there's a close marker we can use
    if faq_end_marker in h:
        h = h.replace(faq_end_marker, FENCING_EXTRA_FAQS + faq_end_marker)
    else:
        # Fallback: just insert before </div>\n        </div>\n    </section> near the FAQ area
        # Find a reliable anchor near FAQ end
        anchor = '            </div>\n        </div>\n    </section>\n    <script>'
        if anchor in h:
            h = h.replace(anchor, FENCING_EXTRA_FAQS + anchor, 1)

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 14. turfing-leicester.html
# ─────────────────────────────────────────────────────────────────────────────
TURFING_VS_AG = '''
    <!-- Natural Turf vs Artificial Grass -->
    <section class="py-16 bg-white">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-6">Natural Turf vs Artificial Grass — Which is Right for Your Leicester Garden?</h2>
            <p class="text-gray-700 mb-6 leading-relaxed">Both natural turf and artificial grass have their place. The right choice depends on your garden's use, your soil conditions, how much maintenance you're willing to do, and your priorities around appearance and environment. Here's a straightforward comparison to help you decide.</p>
            <div class="overflow-x-auto mb-6">
                <table class="w-full text-sm border-collapse">
                    <thead>
                        <tr class="bg-primary text-white">
                            <th class="text-left py-3 px-4 font-semibold">Factor</th>
                            <th class="text-left py-3 px-4 font-semibold">Natural Turf</th>
                            <th class="text-left py-3 px-4 font-semibold">Artificial Grass</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Establishment</td><td class="py-3 px-4 text-gray-700">6–8 weeks before full use</td><td class="py-3 px-4 text-gray-700">Usable within days of installation</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Ongoing maintenance</td><td class="py-3 px-4 text-gray-700">Mow weekly in growing season, feed, aerate, scarify</td><td class="py-3 px-4 text-gray-700">Monthly brush; rinse as needed</td></tr>
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Appearance in dry summers</td><td class="py-3 px-4 text-gray-700">Can go brown in drought conditions</td><td class="py-3 px-4 text-gray-700">Stays green year-round</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Children &amp; pets</td><td class="py-3 px-4 text-gray-700">Can become worn and muddy under heavy use</td><td class="py-3 px-4 text-gray-700">Mud-free, durable under heavy use</td></tr>
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Environment</td><td class="py-3 px-4 text-gray-700">Supports biodiversity, sequesters carbon, fully recyclable</td><td class="py-3 px-4 text-gray-700">No mowing emissions; non-recyclable at end of life</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Leicestershire clay soil</td><td class="py-3 px-4 text-gray-700">Can become waterlogged in wet winters — drainage improvement helps</td><td class="py-3 px-4 text-gray-700">Permeable backing + free-draining sub-base addresses drainage</td></tr>
                    </tbody>
                </table>
            </div>
            <p class="text-gray-700 leading-relaxed">If you're unsure which is right for your garden, we're happy to discuss both options during a free site visit. See also our <a href="artificial-grass" class="text-primary font-medium hover:underline">artificial grass installation service</a> for Leicester and Leicestershire.</p>
        </div>
    </section>

'''


def fix_turfing():
    p = 'turfing-leicester.html'
    h = read(p)

    # H1 already correct per explorer: "Turfing & Lawn Installation in Leicester"
    # Insert natural vs artificial section before FAQ
    h = h.replace(FAQ_ANCHOR, TURFING_VS_AG + FAQ_ANCHOR)

    # Add artificial-grass link to Related Services if not already there
    if 'href="artificial-grass"' not in h:
        h = h.replace(
            '<a href="full-garden-makeover"',
            '<a href="artificial-grass" class="inline-block bg-blue-50 text-primary px-4 py-2 rounded-full text-sm font-medium hover:bg-primary hover:text-white transition">Artificial Grass Leicester</a>\n                <a href="full-garden-makeover"'
        )

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 15. pergolas-leicester.html
# ─────────────────────────────────────────────────────────────────────────────
PERGOLA_SECTIONS = '''
    <!-- Pergola detail sections -->
    <section class="py-16 bg-gray-50">
        <div class="max-w-5xl mx-auto px-4 space-y-16">

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Do Pergolas Need Planning Permission in Leicester?</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Most garden pergolas in Leicester and Leicestershire are classed as permitted development and do not require planning permission, provided they fall within the GPDO Class E rules for garden structures: they must not cover more than 50% of the curtilage (garden excluding the house), must not be higher than 2.5m at the eaves (or 4m for a dual-pitched roof structure), and must not be positioned in front of the principal elevation of the house.</p>
                <p class="text-gray-700 leading-relaxed">If your property is in a conservation area — such as parts of Stoneygate, Oadby or Loughborough town centre — or if it's a listed building, different rules apply and you should check with the relevant local planning authority before proceeding. We advise on this during every free site survey.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Pergola Over a Patio in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Combining a pergola with a patio is one of the most popular garden upgrades we carry out in Leicester. The pergola defines the dining and entertaining zone, provides a structure to hang outdoor lighting from, and — with the right roofing option — gives partial weather protection so the patio is usable even on overcast evenings. We design pergola-over-patio combinations as a single project, so the patio slab layout, the post positions and the lighting installation are all planned together and built in the correct sequence.</p>
                <p class="text-gray-700 leading-relaxed">See our <a href="patios" class="text-primary font-medium hover:underline">patio installation page</a> for material options that work well under a pergola.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Louvred Aluminium Pergolas in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Louvred aluminium pergolas have adjustable roof blades that can be opened fully for sun or closed to provide near-waterproof shelter during rain. They're a significant step up from a traditional timber pergola and are available with integrated guttering, LED strip lighting inside the blades and side panels (glass, polycarbonate or fabric screens) for privacy and wind protection. The aluminium frame is powder-coated and maintenance-free. Louvred pergolas are a larger investment than a standard pergola — we can provide indicative costings during a free site survey.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Pergolas with Lighting and Seating Areas</h2>
                <p class="text-gray-700 leading-relaxed mb-3">The most practical pergola projects we install include integrated garden lighting from the outset: LED spots on the internal face of the beams, festoon or bistro-string lighting across the structure, or IP65-rated downlighters recessed into timber purlins. All lighting is installed on a low-voltage transformer with a weatherproof controller. When the pergola is part of a wider garden design, we coordinate the lighting zones across the patio, pergola and surrounding beds from a single installation. See our <a href="garden-lighting" class="text-primary font-medium hover:underline">garden lighting service</a> for more details.</p>
            </div>

        </div>
    </section>

'''


def fix_pergolas():
    p = 'pergolas-leicester.html'
    h = read(p)
    h = h.replace(FAQ_ANCHOR, PERGOLA_SECTIONS + FAQ_ANCHOR)
    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# 16. commercial-astroturf-leicester.html
# ─────────────────────────────────────────────────────────────────────────────
COMMERCIAL_SECTIONS = '''
    <!-- Schools, HMOs, Spec, RAMS sections -->
    <section class="py-16 bg-white">
        <div class="max-w-5xl mx-auto px-4 space-y-16">

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Artificial Grass for Schools and Nurseries in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">School and nursery grounds in Leicester and Leicestershire are typically subject to higher foot traffic, a need for all-weather usability and specific surface safety considerations. We install commercial-grade artificial grass on school grounds and nursery outdoor play areas across Leicestershire — specifying products with appropriate pile height, density and drainage capacity for outdoor play use. For play surfaces that must meet the BS EN 1177 critical fall height standard (relevant to use under play equipment), we can specify and install an appropriate shock-absorbing infill or sub-layer. Please confirm the specific safety certification required for your project and we will advise accordingly.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Artificial Grass for HMOs and Communal Gardens in Leicester</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Communal gardens in HMO properties and apartment blocks across Leicester are a recurring challenge: multiple occupants mean the lawn takes heavy, year-round use, maintenance is nobody's clear responsibility and the results are usually poor. Commercial-grade artificial grass eliminates the maintenance problem entirely — no mowing, no watering, no reseeding after wear. We specify a higher-density product (typically 30mm pile height, minimum 16,800 dtex) with a robust backing rated for shared-use areas. Site access, phased installation and minimising disruption to residents are all managed as part of the project.</p>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Commercial Artificial Grass Specification</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-sm border-collapse">
                        <tbody class="divide-y divide-gray-100">
                            <tr class="bg-white"><td class="py-3 px-4 font-semibold text-gray-900 w-1/3">Pile height</td><td class="py-3 px-4 text-gray-700">25–40mm depending on application</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-semibold text-gray-900">Fibre weight / dtex</td><td class="py-3 px-4 text-gray-700">Minimum 16,800 dtex for heavy-use commercial installations</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-semibold text-gray-900">Backing</td><td class="py-3 px-4 text-gray-700">Dual-layer backing with secondary latex coating for stability and longevity</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-semibold text-gray-900">Drainage rate</td><td class="py-3 px-4 text-gray-700">Minimum 60 litres/m²/hour through backing</td></tr>
                            <tr class="bg-white"><td class="py-3 px-4 font-semibold text-gray-900">Sub-base</td><td class="py-3 px-4 text-gray-700">Compacted MOT Type 1 minimum 100mm; shock pad where fall height standard required</td></tr>
                            <tr class="bg-gray-50"><td class="py-3 px-4 font-semibold text-gray-900">Warranty</td><td class="py-3 px-4 text-gray-700">Typically 8–10 years on commercial products</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">RAMS, Insurance and Site Access for Commercial Projects</h2>
                <p class="text-gray-700 leading-relaxed mb-3">Commercial artificial grass projects require a higher level of site management than domestic installations. We can provide a Method Statement and Risk Assessment (RAMS) for commercial projects on request. We hold appropriate public liability insurance and can provide certificates on request. For school, nursery and publicly accessible sites, we discuss site access, working hours, security and child/user exclusion zones during the surveying process to ensure our installation causes minimum disruption.</p>
                <p class="text-gray-700 leading-relaxed text-sm text-gray-500 mt-2">Please note: HIC (Head Injury Criterion) ratings and specific sports-surface compliance certifications are product-specific. We will confirm the certification status of any product we specify for safety-critical applications before installation.</p>
            </div>

        </div>
    </section>

'''


def fix_commercial_astroturf():
    p = 'commercial-astroturf-leicester.html'
    h = read(p)

    # Adjust CTA to suit commercial buyers
    h = h.replace(
        'Get a Free Quote',
        'Request a Commercial Astroturf Site Survey'
    )
    h = h.replace(
        'Get Free Quote',
        'Request Site Survey'
    )
    h = h.replace(
        'Get Instant Quote',
        'Request Site Survey'
    )

    # Insert commercial sections before FAQ
    h = h.replace(FAQ_ANCHOR, COMMERCIAL_SECTIONS + FAQ_ANCHOR)

    write(p, h)


# ─────────────────────────────────────────────────────────────────────────────
# Run all fixes
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Phase I — service page SEO clean-up')
    fix_services()
    fix_patios()
    fix_artificial_grass()
    fix_composite_decking()
    fix_driveways()
    fix_garden_lighting()
    fix_full_garden_makeover()
    fix_ai_garden_design()
    fix_garden_design()
    fix_porcelain_patios()
    fix_block_paving()
    fix_resin_driveways()
    fix_fencing()
    fix_turfing()
    fix_pergolas()
    fix_commercial_astroturf()
    print('All done.')
