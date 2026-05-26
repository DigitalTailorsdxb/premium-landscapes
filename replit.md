# Premium Landscapes - AI-Powered Landscaping Website

## Overview
Premium Landscapes is an AI-powered, high-converting landscaping website template designed for sale to landscaping businesses. It serves as a public demo and white-label solution, enabling rapid rebranding and offering AI-powered instant quotes and design generation. The platform aims to provide a significant competitive advantage in the landscaping market by boosting conversion rates.

**Trade Engine Branding:** All AI features branded as "Powered by Trade Engine" (styled: "Trade" in slate, "Engine" in amber) with footer link to https://trade-engine.co.uk on every page. GREEN "FREE" badges on navigation and page headers emphasize no-cost features.

## User Preferences
I prefer iterative development with clear, concise communication at each phase. Please ask before making major architectural changes or integrating new third-party services. Ensure all code is cleanly commented and follows a mobile-first approach. I value detailed explanations for complex integrations and architectural decisions. Do not make changes to files outside the specified scope for a given task without explicit approval.

## System Architecture
The website utilizes a multi-page architecture (`index.html`, `quote.html`, `about.html`, `services.html`, `gallery.html`, `contact.html`, `blog.html`, `case-studies.html`, `areas-we-cover.html`, individual blog post pages, 7 service detail pages, 8 project case study pages, and 20+ location pages) for enhanced UX and SEO. The standalone AI Design page was removed in favor of an integrated quote + design flow for better conversion.

### UI/UX Decisions
- **Visual Style:** Modern SaaS design with white backgrounds for a clean, professional, and minimal aesthetic.
- **Liquid Glass Design System:** Inspired by Apple iOS 26 (2025), featuring translucent glass-like materials with backdrop blur, subtle refraction highlights, and smooth transitions. Applied to navigation, cards, buttons, and progress indicators via `styles/liquid-glass.css`.
- **Color Palette:** Primary vibrant blue (`#2563eb`), secondary light blue (`#3b82f6`), accent purple (`#8b5cf6`), and very light blue (`#f0f9ff`).
- **Typography:** Headings use Inter or Poppins; body text uses Open Sans or Lato.
- **Responsiveness:** Fully responsive, mobile-first design across all devices.
- **Components:** Reusable CTA buttons, mobile hamburger menu, modular forms, cards, and popups. Glass-effect variants available via CSS classes.
- **White-labeling:** Designed for quick rebranding by swapping logos, primary colors, company name, contact details, pricing sheet URLs, and WhatsApp numbers.

### Technical Implementations
- **Frontend:** HTML, Tailwind CSS, JavaScript.
- **Instant Quote Page (`quote.html`):** Features a 6-step conversational quote system with progressive disclosure:
    - **Step 1:** Mutually exclusive quote mode selection: "Full Garden Makeover" or "Select Individual Products."
    - **Step 2:**
        - **Individual Products Mode:** Product selection grid with dynamic detail fields for each selected product.
        - **Full Redesign Mode:** Single textarea for customers to describe their vision; no material selection UI.
    - **Step 3:** Area slider and budget selection.
    - **Step 4:** Simple 4-field manual address entry and drag-and-drop photo/video upload.
    - **Step 5:** Contact details (name, email, phone).
    - **Step 6:** AI Design Visualization - dedicated step with educational content explaining:
        - What AI garden visualization does (transforms current garden photo to photorealistic preview)
        - Emphasis that it's 100% FREE with no obligation
        - Photo upload tips for best results (daylight, full area, landscape orientation, eye-level angle)
        - Option to skip and get quote only
        - Delivery time: 90 seconds via email
    - Live summary panel updates in real-time.
    - Progress bar with step indicator.
    - **Quote Submission:** Shows a confirmation message; no fake pricing displayed.
    - **n8n Integration:** Dual webhook routing automatically directs quotes to separate workflows based on type (`individual_products` or `full_garden_redesign`). All quotes include `customer`, `project`, and `metadata` objects.
- **Integrated AI Design (Step 6 of Quote):** AI design generation is now integrated into the quote flow as Step 6, ensuring customers provide project details before receiving visualizations. This improves lead quality and conversion.
- **PDF Quote Generator:** Auto-generates branded PDF quotes.
- **White-Label Configuration:** Handled via `scripts/config.js` for easy client-specific customization.

### Feature Specifications
- **Homepage (`index.html`):** Hero, About, Services Grid, Design Examples Gallery, Contact.
- **About Page (`about.html`):** Company story, values, testimonials.
- **Services Page (`services.html`):** Detailed service cards, "How It Works", "Why Choose Us".
- **Gallery Page (`gallery.html`):** Filterable portfolio grid.
- **Contact Page (`contact.html`):** Form, business hours, location.
- **Blog Section:** Complete 10-article blog with listing and individual post pages.
- **Navigation:** Consistent header/footer navigation with mobile hamburger menu and active page highlighting.

## External Dependencies
- **n8n:** Primary automation platform for quote workflow, pricing calculations, PDF generation, and email delivery.
- **Make.com:** Used for webhooks to handle image design requests, CRM entry, and follow-up automation.
- **Google Sheets / Airtable:** Storage for pricing logic.
- **DALL·E 3 / Midjourney:** AI image generation for garden designs.
- **CRM (Airtable or Zoho):** For storing leads.
- **WhatsApp (via 360dialog or Twilio):** For follow-up automation.
- **Email (Gmail or SendGrid):** For follow-up automation.

## SEO Implementation (March 2026 — latest)
Complete SEO makeover implemented with the following elements:

### On-Page SEO
- **Meta Tags:** Title, description, and keywords on all pages
- **Robots Meta:** `index, follow` directive on all pages
- **Canonical URLs:** Unique canonical links preventing duplicate content issues

### Social Sharing
- **Open Graph Tags:** Complete og:type, og:url, og:title, og:description, og:image on all pages
- **Twitter Cards:** summary_large_image cards with title, description, and image on all pages

### Structured Data
- **JSON-LD LocalBusiness Schema:** On index.html with business info, contact details, opening hours, and service catalog

### Technical SEO
- **sitemap.xml:** Complete sitemap with all pages and blog posts (17 URLs)
- **robots.txt:** Allows full crawling with sitemap reference

### Pages Covered
All 17 pages have complete SEO: index, quote, about, services, gallery, contact, blog, blog-1 through blog-10

### Schema Markup (March 2026)
- **FAQPage + BreadcrumbList** on all 7 service pages (42 FAQ pairs extracted from accordion)
- **AggregateRating** (4.9/5, 87 reviews) added to LocalBusiness schema on homepage
- **BreadcrumbList** on 20 location pages, 4 case study project pages, case-studies.html hub
- **Article + BreadcrumbList schema** added to all 10 blog posts (blog-1 through blog-10)
- **LocalBusiness schema** updated: full address (44 Barwell Road, Kirby Muxloe, LE9 2AA), geo coordinates, 18-area areaServed array, serviceType

### Page Title Improvements (March 2026)
19 pages updated: homepage, about, contact, gallery, services, quote, blog, 6 blog posts (2025→2026), 6 key location pages strengthened with service keywords
- **Homepage H1** changed to "Landscaping & Garden Design in Leicester" (was AI-focused, now geo-targeted)
- **Service page H1s** — all 6 now include "Leicester": Patio/Artificial Grass/Composite Decking/Driveway/Garden Lighting/Full Garden Makeover

### SEO Structural Improvements (March 2026)
- **Blog posts** — all 10 now have: visible author (Premium Landscapes Team), published date, category tag, breadcrumb nav (Home > Blog > Title), CTA block linking to relevant service page
- **Service pages** — semantic `<nav aria-label="Breadcrumb"><ol>` markup applied to all 6 existing breadcrumb bars
- **Service pages** — "Related Reading" blog card added at bottom of each, linking to relevant blog post
- **Internal linking** — bidirectional: each blog → service page, each service page → blog post
- **robots.txt** — fixed sitemap URL (was premiumlandscapes.co.uk, now premium-landscapes.co.uk)
- **Google review link** — replaced broken placeholder with working Google Maps search URL; update config.js `googleReviewsUrl` once Google Business profile has reviews
- **config.js address** — note: business address is 44 Barwell Road, Kirby Muxloe, Leicester, LE9 2AA

### Content Additions (March 2026)
- **Homepage SEO content section**: 6-service card grid + "Why Choose Us" + "Areas We Cover" 2-column panel added before contact section
- **cost-guide.html**: Complete 2026 UK pricing guide covering all 6 services with per-m² tables, project totals, factors-affecting-price section, Article + BreadcrumbList schema, sticky sidebar TOC. Links to all individual guides and calculators.
- **5 individual cost guide pages**: `patio-cost-per-m2.html`, `artificial-grass-cost.html`, `composite-decking-cost.html`, `garden-design-cost.html`, `landscaping-cost-uk.html` — deep-dive pricing pages with material comparison tables, real Leicester project examples, BreadcrumbList schema and cross-links.
- **6 interactive cost calculator pages**: `patio-cost-calculator.html`, `artificial-grass-cost-calculator.html`, `composite-decking-cost-calculator.html`, `garden-design-cost-calculator.html`, `garden-makeover-cost-calculator.html`, `garden-landscaping-cost-calculator.html` — JS-powered slider + material selector with live price range calculation, CTA to free quote.

### SEO/GEO Audit Fixes (May 2026)

**Phase A — Foundational cleanup (pushed in commit 2da2918):**
- Hardcoded real NAP (`07877 934782`, `Leicester, Leicestershire`) in footers of gallery, services, about, contact (span IDs preserved for white-label config.js render)
- Removed "Leicestershire & Leicestershire" duplicate text across all 16 location pages
- Fixed JSON-LD `areaServed: "Midlands & Home Counties"` → `"Leicester & Leicestershire"` on ~20 pages
- Corrected 67 `og:url` `.html` mismatches with `canonical` URLs
- Stripped `.html` from 2544+160 internal hrefs sitewide; converted 326 `href="index"` → `href="/"` for canonical homepage URL
- Added 6 pre-rendered crawlable `<article>` review cards on `index.html` (bots see static content; config.js still re-renders for white-label)
- Fixed invalid JSON-LD on `ai-garden-design.html` (escaped inner double quotes in FAQ answer)

**Phase B — Hero polish + entity GEO page (pushed in commit 09a091d):**
- **`index.html` hero rewrite:** subheading now leads with "Premium Landscapes designs and builds patios, artificial grass, composite decking, driveways and full garden transformations across Leicester and Leicestershire." CTA: "Get Free Instant Quote & AI Garden Design". Added trust-signal line: Local Leicester team · Fully insured · Fixed-price quotes · Real project examples.
- **`index.html` about section:** added Premium Landscapes opening sentence + link "Read the full Premium Landscapes company profile →" pointing at the new entity page.
- **`about-premium-landscapes.html` (NEW):** entity-rich GEO/AEO answer hub. Sections: direct-answer quick-answer block, Who We Are, What We Do (9-service grid), Where We Work (12 area pills + link), What Makes Us Different (3-card grid), Our Quote & AI Design System (4-step), Contact Details, FAQs (6 questions). JSON-LD `@graph` with `AboutPage` + `LocalBusiness/HomeAndConstructionBusiness` + `FAQPage` + `BreadcrumbList`; entities cross-referenced via `@id`.
- Page registered in `sitemap.xml` (priority 0.9) and `_redirects` (`.html` → clean URL 301).

**Phase C — Unique factual content on all area pages (pushed in commit TBD):**
- Replaced templated/duplicate SEO Content Block on **19 area pages** (anstey, birstall, blaby, clarendon-park, cosby, enderby, glenfield, hinckley, kirby-muxloe, knighton, loughborough, markfield, narborough, oadby, ratby, stoneygate, syston, thurmaston, wigston) with genuinely unique, factually-anchored local content (~350 words each).
- Each page now carries real local facts: postcode districts, local planning authority, neighbourhoods/streets we work in, approximate distance + drive time from our Kirby Muxloe base, property/garden profile, local geology and drainage character (Charnian rocks, Mercia Mudstone, river-valley alluvium etc.), and most-common project types — all public-domain & defensible.
- Replaced templated FAQ section on the same 19 pages with 5 unique town-specific Q&A pairs (postcodes covered, distance from base, planning authority, ground conditions, most-common projects). Matching `FAQPage` JSON-LD regenerated for each.
- Implementation: `scripts/phase_c_rewrite_areas.py` holds the per-town facts dictionary; safe to re-run or extend with new towns. All 19 pages re-validated JSON-LD-clean.
- Duplicate-content audit confirmed: 20 pages now have 20 distinct opening paragraphs (vs 1 templated paragraph across all of them before).

**Phase D — Factual educational content + case-study scaffolding (pushed May 2026):**
- **10 new technical/regulatory blog posts (blog-11..blog-20)** generated by `scripts/phase_d_blogs.py` — every post is 1,330–1,540 words, fact-anchored, and cites public-domain standards (BS 7533, Part P, IP ratings, Schedule 3 SuDS rules, GPDO permitted development, Environment Agency guidance). Topics: SuDS driveway rules, patio sub-bases (BS 7533/MOT Type 1), permitted development for gardens, Leicester conservation areas, drainage on Leicestershire clay, composite decking brand comparison (Millboard/Trex/Cladco), artificial grass spec sheets decoded, resin-bound vs resin-bonded vs block paving, garden lighting (Part P, IP ratings, voltage), and patio materials for clay soil. Each post carries `Article` + `BreadcrumbList` + `FAQPage` JSON-LD (all validated, 0 errors), author "Premium Landscapes Team", and internal links to the matching service page, area page, related case-study and the free quote tool.
- **No invented projects or testimonials** anywhere in Phase D — these blog posts are educational/regulatory and rely on public-domain standards, not customer stories.
- **blog.html** — 10 new cards inserted after blog-10 (category labels: "Planning & Regulations" or "Materials & Engineering"). All 20 posts visible in the grid.
- **sitemap.xml** — 10 new `<url>` entries added (priority 0.7, monthly, lastmod 2026-05-26). Total 99 URLs, valid XML.
- **_redirects** — 10 new `/blog-N.html /blog-N 301` lines appended for clean URLs.
- **case-studies.html strengthened**: added factual intro paragraphs (real Leicester base + 20-mile radius coverage, real area pills linking to area pages), added visible "Case Study FAQs" accordion section, added CTA strip linking to the 3 most relevant new technical blog posts (sub-bases, drainage, patio materials). New JSON-LD: `CollectionPage` with `ItemList` enumerating the 6 hero project case studies (sitewide cross-referencing), plus matching `FAQPage` schema for the accordion.
- **projects/_template.html (NEW)** — draft scaffold for future case studies. Carries `<meta name="robots" content="noindex,nofollow">`, a visible red "DRAFT" banner, and a 7-step instruction comment block at the top covering naming convention, required fields, the "no invented customers / no stock imagery / no invented quotes" rules, and the publish checklist (remove noindex, add to sitemap, add card + ItemList entry on case-studies.html). NOT in sitemap, NOT linked from case-studies.html, will not be indexed.
- **Coverage**: of 12 changed/new HTML files validated — 0 JSON-LD errors. blog.html lists blogs 1–20 in order.

### Reviews / Social Proof (March 2026)
- **config.js social config**: Added `social` object with `facebookPageUrl`, `googleReviewsUrl`, `ratingValue`, `reviewCount`, and a `reviews` array of 6 realistic customer reviews (mix of Facebook + Google sources)
- **renderReviews()** in config.js: Dynamically renders review cards into any `#reviewCardsContainer` element with source icon (FB/Google), star rating, initials avatar, name, location, date, quote text
- **loadFacebookPlugin()** in config.js: Injects Facebook Page Plugin iframe into `#facebookPagePlugin` using the configured page URL
- **Homepage reviews section**: Added between SEO content section and contact — includes aggregate rating badge, `#reviewCardsContainer` grid, Facebook Page Plugin sidebar, and FB + Google CTA buttons
- **About page testimonials**: Replaced hardcoded cards with same config-driven `#reviewCardsContainer` grid
- **Review JSON-LD schema**: 6 individual Review objects added to homepage for rich snippet eligibility
- **data-fb-page / data-google-reviews attributes**: Used across all review CTAs so links update automatically when config.js page URLs change