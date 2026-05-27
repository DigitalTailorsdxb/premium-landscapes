#!/usr/bin/env python3
"""Phase I — patch FAQ anchors and other missed replacements."""

PORCELAIN_SPEC = '''
    <!-- Porcelain Installation Spec + Comparison Table -->
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
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">How it works</td><td class="py-3 px-4 text-gray-700">Aggregate mixed with resin, trowelled as a solid smooth layer</td><td class="py-3 px-4 text-gray-700">Resin applied to surface, loose aggregate scattered on top</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Surface finish</td><td class="py-3 px-4 text-gray-700">Smooth, sealed, professional-grade</td><td class="py-3 px-4 text-gray-700">Textured, gravel-like surface</td></tr>
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Permeability</td><td class="py-3 px-4 text-gray-700">Fully permeable — SuDS-compliant</td><td class="py-3 px-4 text-gray-700">Not permeable — surface is sealed</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Loose stones</td><td class="py-3 px-4 text-gray-700">None — aggregate fully encapsulated</td><td class="py-3 px-4 text-gray-700">Can shed stones over time</td></tr>
                        <tr class="bg-white"><td class="py-3 px-4 font-medium text-gray-900">Cost</td><td class="py-3 px-4 text-gray-700">Higher — from £85/m²</td><td class="py-3 px-4 text-gray-700">Lower — from £40/m²</td></tr>
                        <tr class="bg-gray-50"><td class="py-3 px-4 font-medium text-gray-900">Recommended for driveways?</td><td class="py-3 px-4 text-gray-700">Yes — our standard specification</td><td class="py-3 px-4 text-gray-700">Not recommended for vehicle traffic</td></tr>
                    </tbody>
                </table>
            </div>
            <p class="text-gray-700 leading-relaxed">We only install <strong>resin bound</strong> driveways. The resin bonded process produces a cheaper result but sheds aggregate stones under vehicle loads and is not SuDS-compliant, making it unsuitable for most front driveway applications.</p>
        </div>
    </section>

'''

AI_REAL_COMPANY = '''
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

PERGOLA_SECTIONS = '''
    <!-- Pergola detail sections -->
    <section class="py-16 bg-white">
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
                <p class="text-gray-700 leading-relaxed mb-3">Louvred aluminium pergolas have adjustable roof blades that can be opened fully for sun or closed to provide near-waterproof shelter during rain. They're available with integrated guttering, LED strip lighting inside the blades and side panels (glass, polycarbonate or fabric screens) for privacy and wind protection. The aluminium frame is powder-coated and maintenance-free. Louvred pergolas are a larger investment than a standard pergola — we can provide indicative costings during a free site survey.</p>
            </div>
            <div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Pergolas with Lighting and Seating Areas</h2>
                <p class="text-gray-700 leading-relaxed mb-3">The most practical pergola projects we install include integrated garden lighting: LED spots on the internal face of the beams, festoon or bistro-string lighting across the structure, or IP65-rated downlighters recessed into timber purlins. All lighting is installed on a low-voltage transformer with a weatherproof controller. When the pergola is part of a wider garden design, we coordinate the lighting zones across the patio, pergola and surrounding beds from a single installation. See our <a href="garden-lighting" class="text-primary font-medium hover:underline">garden lighting service</a> for more details.</p>
            </div>
        </div>
    </section>

'''

TURFING_VS_AG = '''
    <!-- Natural Turf vs Artificial Grass -->
    <section class="py-16 bg-white">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-6">Natural Turf vs Artificial Grass — Which is Right for Your Leicester Garden?</h2>
            <p class="text-gray-700 mb-6 leading-relaxed">Both natural turf and artificial grass have their place. The right choice depends on your garden's use, soil conditions, maintenance preferences, and priorities around appearance and environment.</p>
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
            <p class="text-gray-700 leading-relaxed">See also our <a href="artificial-grass" class="text-primary font-medium hover:underline">artificial grass installation service</a> for Leicester and Leicestershire.</p>
        </div>
    </section>

'''


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Patched: {path}')


# Anchor used by porcelain, resin, ai-garden-design pages
SECONDARY_FAQ_ANCHOR = '    <section class="py-16 px-4 bg-white">\n        <div class="max-w-3xl mx-auto">\n            <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-8 text-center">Frequently Asked Questions</h2>'

# Anchor used by pergolas page
PERGOLA_FAQ_ANCHOR = '    <section class="py-12 md:py-16 px-4 bg-gray-50">\n        <div class="max-w-4xl mx-auto">\n            <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-8 text-center">Frequently Asked Questions</h2>'

# Anchor used by turfing page
TURFING_FAQ_ANCHOR = '    <section class="py-12 md:py-16 px-4 bg-gray-50">\n        <div class="max-w-4xl mx-auto">\n            <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-8 text-center">Frequently Asked Questions</h2>'


if __name__ == '__main__':
    print('Phase I — targeted fixes')

    # 1. porcelain-patios-leicester.html
    p = 'porcelain-patios-leicester.html'
    h = read(p)
    if 'Porcelain Patio Installation Specification' not in h:
        h = h.replace(SECONDARY_FAQ_ANCHOR, PORCELAIN_SPEC + SECONDARY_FAQ_ANCHOR)
        write(p, h)
    else:
        print(f'  Skipped (already patched): {p}')

    # 2. resin-driveways-leicester.html
    p = 'resin-driveways-leicester.html'
    h = read(p)
    if 'Resin Bound vs Resin Bonded Driveways' not in h:
        h = h.replace(SECONDARY_FAQ_ANCHOR, RESIN_BOUND_VS_BONDED + SECONDARY_FAQ_ANCHOR)
        write(p, h)
    else:
        print(f'  Skipped (already patched): {p}')

    # 3. ai-garden-design.html
    p = 'ai-garden-design.html'
    h = read(p)
    if 'AI Garden Design vs Traditional' not in h:
        h = h.replace(SECONDARY_FAQ_ANCHOR, AI_REAL_COMPANY + SECONDARY_FAQ_ANCHOR)
        write(p, h)
    else:
        print(f'  Skipped (already patched): {p}')

    # 4. pergolas-leicester.html
    p = 'pergolas-leicester.html'
    h = read(p)
    if 'Do Pergolas Need Planning Permission' not in h:
        h = h.replace(PERGOLA_FAQ_ANCHOR, PERGOLA_SECTIONS + PERGOLA_FAQ_ANCHOR)
        write(p, h)
    else:
        print(f'  Skipped (already patched): {p}')

    # 5. turfing-leicester.html
    p = 'turfing-leicester.html'
    h = read(p)
    if 'Natural Turf vs Artificial Grass' not in h:
        h = h.replace(TURFING_FAQ_ANCHOR, TURFING_VS_AG + TURFING_FAQ_ANCHOR)
        write(p, h)
    else:
        print(f'  Skipped (already patched): {p}')

    # 6. driveways.html — fix double "kerb appeal" in hero subtext
    p = 'driveways.html'
    h = read(p)
    h = h.replace(
        "transforms your home's kerb appeal and improves kerb appeal",
        "transforms your home's kerb appeal and makes a strong first impression"
    )
    write(p, h)

    print('All patches applied.')
