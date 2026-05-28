#!/usr/bin/env python3
"""
Phase N — Add 2 postcode-anchored FAQ pairs to the existing FAQPage JSON-LD
on all 20 location pages.

New questions added per page:
  Q_new_1  "What part of Leicestershire is [area] in, and which postcode does it cover?"
             → geographic context (direction + postcode + council) drawn from hero facts
  Q_new_2  "Is there a travel surcharge for projects in [area]?"
             → confirms proximity / no extra charge — common homeowner concern

Insertion point: just before the closing  ]  of the FAQPage mainEntity array.

Run from project root:
    python3 scripts/phase_n_postcode_faq.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# Per-area data — postcodes, geography, council, distance from base
# ---------------------------------------------------------------------------
AREAS = [
    {
        "file": "landscaping-leicester.html",
        "name": "Leicester",
        "postcodes": "LE1, LE2, LE3, LE4, LE5 and surrounding LE districts",
        "postcode_short": "LE1–LE5",
        "direction": "the city of Leicester and its inner suburbs",
        "council": "Leicester City Council (city postcodes) and the surrounding borough councils for the outer suburbs",
        "distance_km": 7,
        "drive_min": 15,
        "distance_phrase": "approximately 7 km (around 15 minutes by van) from our base at 44 Barwell Road, Kirby Muxloe",
        "surcharge_note": "No — we treat Leicester city centre and all LE postcodes as part of our standard service area. There is no travel premium on any quote for a Leicester address.",
    },
    {
        "file": "landscaping-stoneygate.html",
        "name": "Stoneygate",
        "postcodes": "LE2",
        "postcode_short": "LE2",
        "direction": "one of Leicester's most prestigious residential suburbs, immediately south of the city centre",
        "council": "Leicester City Council",
        "distance_km": 8,
        "drive_min": 20,
        "distance_phrase": "approximately 8 km from our base at 44 Barwell Road, Kirby Muxloe — about a 20-minute drive",
        "surcharge_note": "No — Stoneygate LE2 is within our standard service area and is priced the same as any other address. The 20-minute drive from our Kirby Muxloe base is comfortably within our everyday working radius, so your quote will not carry any travel addition.",
    },
    {
        "file": "landscaping-knighton.html",
        "name": "Knighton",
        "postcodes": "LE2",
        "postcode_short": "LE2",
        "direction": "an affluent residential suburb directly south of Leicester city centre, within the LE2 postcode",
        "council": "Leicester City Council",
        "distance_km": 8,
        "drive_min": 18,
        "distance_phrase": "approximately 8 km from our base at 44 Barwell Road, Kirby Muxloe — about an 18-minute drive",
        "surcharge_note": "No — Knighton LE2 falls comfortably within our standard service area. There is no travel surcharge on any Knighton quote; the 18-minute drive from our base is part of our everyday working radius.",
    },
    {
        "file": "landscaping-clarendon-park.html",
        "name": "Clarendon Park",
        "postcodes": "LE2",
        "postcode_short": "LE2",
        "direction": "immediately south of Leicester city centre, within the LE2 postcode",
        "council": "Leicester City Council",
        "distance_km": 7,
        "drive_min": 18,
        "distance_phrase": "approximately 7 km from our base at 44 Barwell Road, Kirby Muxloe — about an 18-minute drive",
        "surcharge_note": "No — Clarendon Park LE2 is within our standard service area and every quote is priced the same as for any other address we cover. There is no travel premium.",
    },
    {
        "file": "landscaping-kirby-muxloe.html",
        "name": "Kirby Muxloe",
        "postcodes": "LE9",
        "postcode_short": "LE9",
        "direction": "directly west of Leicester — and the home of our Premium Landscapes base at 44 Barwell Road",
        "council": "Blaby District Council",
        "distance_km": 0,
        "drive_min": 0,
        "distance_phrase": "our base — Premium Landscapes is headquartered at 44 Barwell Road, Kirby Muxloe, LE9 2AA",
        "surcharge_note": "No — Kirby Muxloe LE9 is where we are based, so there is obviously no travel surcharge. We are typically on-site faster here than anywhere else in our coverage area.",
    },
    {
        "file": "landscaping-oadby.html",
        "name": "Oadby",
        "postcodes": "LE2",
        "postcode_short": "LE2",
        "direction": "south-east of Leicester city centre, an established and affluent suburb within the LE2 postcode",
        "council": "Oadby & Wigston Borough Council",
        "distance_km": 10,
        "drive_min": 20,
        "distance_phrase": "approximately 10 km from our base at 44 Barwell Road, Kirby Muxloe — about a 20-minute drive",
        "surcharge_note": "No — Oadby LE2 is a core part of our service area and is quoted at standard rates. The 20-minute drive from our Kirby Muxloe base means we visit Oadby regularly and factor no travel addition into our prices.",
    },
    {
        "file": "landscaping-wigston.html",
        "name": "Wigston",
        "postcodes": "LE18",
        "postcode_short": "LE18",
        "direction": "south of Leicester, a large established suburb in the LE18 postcode",
        "council": "Oadby & Wigston Borough Council",
        "distance_km": 10,
        "drive_min": 20,
        "distance_phrase": "approximately 10 km from our base at 44 Barwell Road, Kirby Muxloe — about a 20-minute drive",
        "surcharge_note": "No — Wigston LE18 falls within our standard service area. Every Wigston quote carries the same fixed pricing as any other area we cover; the 20-minute drive from base is well within our everyday working radius.",
    },
    {
        "file": "landscaping-anstey.html",
        "name": "Anstey",
        "postcodes": "LE7",
        "postcode_short": "LE7",
        "direction": "approximately 5 miles north-west of Leicester city centre in the LE7 postcode, bordering Charnwood Forest",
        "council": "Charnwood Borough Council",
        "distance_km": 6,
        "drive_min": 12,
        "distance_phrase": "approximately 6 km from our base at 44 Barwell Road, Kirby Muxloe — about a 12-minute drive",
        "surcharge_note": "No — Anstey LE7 is firmly within our standard service area, and no travel surcharge is added to any Anstey quote. At 12 minutes from our Kirby Muxloe base, it is one of our closer regular work areas.",
    },
    {
        "file": "landscaping-birstall.html",
        "name": "Birstall",
        "postcodes": "LE4",
        "postcode_short": "LE4",
        "direction": "directly north of Leicester in the LE4 postcode, on the east bank of the River Soar",
        "council": "Charnwood Borough Council",
        "distance_km": 10,
        "drive_min": 18,
        "distance_phrase": "approximately 10 km from our base at 44 Barwell Road, Kirby Muxloe — about an 18-minute drive",
        "surcharge_note": "No — Birstall LE4 is priced at our standard rates with no travel addition. We work in Birstall regularly, and the 18-minute drive from our base puts it comfortably within our core coverage zone.",
    },
    {
        "file": "landscaping-blaby.html",
        "name": "Blaby",
        "postcodes": "LE8",
        "postcode_short": "LE8",
        "direction": "south of Leicester in the LE8 postcode, between the city and the M1 motorway",
        "council": "Blaby District Council",
        "distance_km": 7,
        "drive_min": 15,
        "distance_phrase": "approximately 7 km from our base at 44 Barwell Road, Kirby Muxloe — about a 15-minute drive",
        "surcharge_note": "No — Blaby LE8 is part of our standard service area and carries no travel surcharge. At around 15 minutes from our base, it is one of our more frequently visited areas and is quoted at the same fixed rates as everywhere else we cover.",
    },
    {
        "file": "landscaping-cosby.html",
        "name": "Cosby",
        "postcodes": "LE9",
        "postcode_short": "LE9",
        "direction": "a quiet South Leicestershire village in the LE9 postcode, approximately 8 miles south-west of Leicester near the M1 J21 corridor",
        "council": "Blaby District Council",
        "distance_km": 10,
        "drive_min": 18,
        "distance_phrase": "approximately 10 km from our base at 44 Barwell Road, Kirby Muxloe — about an 18-minute drive",
        "surcharge_note": "No — Cosby LE9 is within our standard service area with no travel surcharge applied. We visit Cosby regularly and price all work there at the same fixed rates as any other area we cover.",
    },
    {
        "file": "landscaping-enderby.html",
        "name": "Enderby",
        "postcodes": "LE19",
        "postcode_short": "LE19",
        "direction": "south-west of Leicester in the LE19 postcode, adjacent to Fosse Park and the A563 ring road",
        "council": "Blaby District Council",
        "distance_km": 4,
        "drive_min": 10,
        "distance_phrase": "only approximately 4 km from our base at 44 Barwell Road, Kirby Muxloe — about a 10-minute drive",
        "surcharge_note": "No — Enderby LE19 is one of our closest work areas at just 10 minutes from base, so there is absolutely no travel surcharge. All Enderby quotes are priced at our standard fixed rates.",
    },
    {
        "file": "landscaping-glenfield.html",
        "name": "Glenfield",
        "postcodes": "LE3",
        "postcode_short": "LE3",
        "direction": "on the north-western fringe of Leicester in the LE3 postcode, bordering our Kirby Muxloe base",
        "council": "Hinckley & Bosworth Borough Council (outer sections) and Leicester City Council (areas nearer Beaumont Leys)",
        "distance_km": 3,
        "drive_min": 8,
        "distance_phrase": "only approximately 3 km from our base at 44 Barwell Road, Kirby Muxloe — about an 8-minute drive",
        "surcharge_note": "No — Glenfield LE3 neighbours our base directly, so there is no travel surcharge whatsoever. At 8 minutes away it is among the areas we visit most frequently, and all work is priced at standard fixed rates.",
    },
    {
        "file": "landscaping-hinckley.html",
        "name": "Hinckley",
        "postcodes": "LE10",
        "postcode_short": "LE10",
        "direction": "west Leicestershire in the LE10 postcode, approximately 15 miles from our base via the A47",
        "council": "Hinckley & Bosworth Borough Council",
        "distance_km": 15,
        "drive_min": 22,
        "distance_phrase": "approximately 15 km from our base at 44 Barwell Road, Kirby Muxloe — about a 22-minute drive via the A47",
        "surcharge_note": "No — Hinckley LE10 is within our standard service area and carries no travel surcharge. The 22-minute drive from our base is the outer edge of our regular working radius, but we price all Hinckley work at the same fixed rates as any closer area.",
    },
    {
        "file": "landscaping-loughborough.html",
        "name": "Loughborough",
        "postcodes": "LE11 and LE12",
        "postcode_short": "LE11 / LE12",
        "direction": "north Leicestershire in the LE11 postcode (LE12 covers surrounding villages), approximately 15 miles north of our base via the A6",
        "council": "Charnwood Borough Council",
        "distance_km": 22,
        "drive_min": 30,
        "distance_phrase": "approximately 22 km from our base at 44 Barwell Road, Kirby Muxloe — about a 30-minute drive via the A6",
        "surcharge_note": "No — Loughborough LE11 and LE12 are within our service area and quoted at standard fixed rates. At 30 minutes from our base it is our furthest regular area, but we make scheduled visits and do not add any travel charge to quotes.",
    },
    {
        "file": "landscaping-markfield.html",
        "name": "Markfield",
        "postcodes": "LE67",
        "postcode_short": "LE67",
        "direction": "a large village in the LE67 postcode on the edge of Charnwood Forest, approximately 8 miles north-west of our Kirby Muxloe base",
        "council": "North West Leicestershire District Council",
        "distance_km": 10,
        "drive_min": 18,
        "distance_phrase": "approximately 10 km from our base at 44 Barwell Road, Kirby Muxloe — about an 18-minute drive",
        "surcharge_note": "No — Markfield LE67 is within our standard service area and all quotes are at fixed rates with no travel surcharge. The 18-minute drive from our base puts Markfield comfortably within our everyday working radius.",
    },
    {
        "file": "landscaping-narborough.html",
        "name": "Narborough",
        "postcodes": "LE19",
        "postcode_short": "LE19",
        "direction": "south-west of Leicester in the LE19 postcode, in the Soar valley approximately 6 miles from our Kirby Muxloe base",
        "council": "Blaby District Council",
        "distance_km": 5,
        "drive_min": 12,
        "distance_phrase": "approximately 5 km from our base at 44 Barwell Road, Kirby Muxloe — about a 12-minute drive",
        "surcharge_note": "No — Narborough LE19 is well within our standard service area, and no travel surcharge is added. At 12 minutes from our base, it is one of our regular close-in work areas and is priced at the same fixed rates as everywhere else we cover.",
    },
    {
        "file": "landscaping-ratby.html",
        "name": "Ratby",
        "postcodes": "LE6",
        "postcode_short": "LE6",
        "direction": "north-west of Leicester in the LE6 postcode, barely 3 miles from our Kirby Muxloe base",
        "council": "Hinckley & Bosworth Borough Council",
        "distance_km": 5,
        "drive_min": 10,
        "distance_phrase": "approximately 5 km from our base at 44 Barwell Road, Kirby Muxloe — about a 10-minute drive",
        "surcharge_note": "No — Ratby LE6 is one of our nearest areas; there is no travel surcharge and never will be. We can often schedule Ratby visits at very short notice, and all work is priced at our standard fixed rates.",
    },
    {
        "file": "landscaping-syston.html",
        "name": "Syston",
        "postcodes": "LE7",
        "postcode_short": "LE7",
        "direction": "a substantial market town in the LE7 postcode, 6 miles north of Leicester along the A607",
        "council": "Charnwood Borough Council",
        "distance_km": 14,
        "drive_min": 22,
        "distance_phrase": "approximately 14 km from our base at 44 Barwell Road, Kirby Muxloe — about a 22-minute drive",
        "surcharge_note": "No — Syston LE7 is within our standard service area with no travel surcharge. The 22-minute drive from our base is within our regular working radius and all Syston quotes are priced at the same fixed rates as any other area.",
    },
    {
        "file": "landscaping-thurmaston.html",
        "name": "Thurmaston",
        "postcodes": "LE4",
        "postcode_short": "LE4",
        "direction": "north of Leicester in the LE4 postcode, bordering Birstall to the north and Leicester's Hamilton district to the south",
        "council": "Charnwood Borough Council",
        "distance_km": 12,
        "drive_min": 20,
        "distance_phrase": "approximately 12 km from our base at 44 Barwell Road, Kirby Muxloe — about a 20-minute drive",
        "surcharge_note": "No — Thurmaston LE4 is a core part of our service area and carries no travel surcharge. At 20 minutes from our base we work here frequently, and all quotes are at our standard fixed rates.",
    },
]

# ---------------------------------------------------------------------------
# FAQ pair generator
# ---------------------------------------------------------------------------

def make_new_faqs(a: dict) -> str:
    """Return two JSON FAQ objects (as a string) ready to append inside mainEntity."""

    # Q1 — geographic / postcode context
    if a["distance_km"] == 0:
        distance_context = (
            f"{a['name']} is our home: Premium Landscapes is based here at 44 Barwell Road, "
            f"Kirby Muxloe, LE9 2AA. The village sits in the {a['postcodes']} postcode and falls "
            f"within {a['council']}."
        )
    else:
        distance_context = (
            f"{a['name']} is {a['direction']}, covered by the {a['postcodes']} postcode district "
            f"and falling under {a['council']} for planning purposes. "
            f"For us, that is {a['distance_phrase']}, which means we can usually schedule a site "
            f"visit within a few days of enquiry."
        )

    q1 = (
        f'{{\n'
        f'      "@type": "Question",\n'
        f'      "name": "What part of Leicestershire is {a["name"]} in, and which postcode does it cover?",\n'
        f'      "acceptedAnswer": {{\n'
        f'        "@type": "Answer",\n'
        f'        "text": "{distance_context}"\n'
        f'      }}\n'
        f'    }}'
    )

    # Q2 — travel surcharge clarification
    q2 = (
        f'{{\n'
        f'      "@type": "Question",\n'
        f'      "name": "Is there a travel surcharge for projects in {a["name"]}?",\n'
        f'      "acceptedAnswer": {{\n'
        f'        "@type": "Answer",\n'
        f'        "text": "{a["surcharge_note"]}"\n'
        f'      }}\n'
        f'    }}'
    )

    return q1, q2


# ---------------------------------------------------------------------------
# Pattern: find the closing  ]  }  of the FAQPage JSON-LD block.
# The last question always ends with  }  then newline then  ]  then newline then }
# We look for the pattern inside a <script type="application/ld+json"> that
# contains "@type": "FAQPage".
# ---------------------------------------------------------------------------

# Matches the final closing `    }\n  ]\n}` of the FAQPage block
FAQPAGE_CLOSE = re.compile(
    r'("@type":\s*"FAQPage".*?)(    \}\n  \]\n\})',
    re.DOTALL,
)


def process_page(a: dict) -> str:
    filepath = ROOT / a["file"]
    if not filepath.exists():
        print(f"  SKIP  {a['file']} — file not found")
        return "skip"

    html = filepath.read_text(encoding="utf-8")

    # Locate the FAQPage block — we need to insert before its closing `  ]`
    m = FAQPAGE_CLOSE.search(html)
    if not m:
        print(f"  WARN  {a['file']} — FAQPage closing pattern not found")
        return "warn"

    q1_str, q2_str = make_new_faqs(a)

    # Guard: skip if these questions are already present (idempotency)
    guard = f"What part of Leicestershire is {a['name']} in"
    if guard in html:
        print(f"  SKIP  {a['file']} — already has new FAQ pairs")
        return "skip"

    # Build replacement: last existing question closes with `    }`, then we
    # insert a comma + the two new questions, then the original closing `  ]\n}`
    old_close = m.group(2)           # '    }\n  ]\n}'
    new_close = (
        f"    }},\n"
        f"    {q1_str},\n"
        f"    {q2_str}\n"
        f"  ]\n"
        f"}}"
    )

    html_new = html[:m.start(2)] + new_close + html[m.end(2):]

    if html_new == html:
        print(f"  WARN  {a['file']} — substitution produced no change")
        return "warn"

    filepath.write_text(html_new, encoding="utf-8")
    print(f"  OK    {a['file']}")
    return "ok"


def main():
    ok = warn = skip = 0
    for area in AREAS:
        result = process_page(area)
        if result == "ok":
            ok += 1
        elif result == "warn":
            warn += 1
        else:
            skip += 1

    print(f"\nDone — {ok} updated, {warn} warnings, {skip} skipped")
    if warn:
        sys.exit(1)


if __name__ == "__main__":
    main()
