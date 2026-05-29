# Premium Landscapes — AI-Powered Landscaping Website

## Overview
Premium Landscapes is a high-converting, white-label landscaping website template (public demo + resale product for landscaping businesses). It offers AI-powered instant quotes and garden design visualisation, and is built for rapid rebranding. Real business: Premium Landscapes, 44 Barwell Road, Kirby Muxloe, Leicester, LE9 2AA · phone 07877 934782 · domain premium-landscapes.co.uk.

**Trade Engine branding:** All AI features are branded "Powered by Trade Engine" ("Trade" in slate, "Engine" in amber) with a footer link to https://trade-engine.co.uk on every page. GREEN "FREE" badges on nav and page headers emphasise no-cost features.

## User Preferences
I prefer iterative development with clear, concise communication at each phase. Please ask before making major architectural changes or integrating new third-party services. Ensure all code is cleanly commented and follows a mobile-first approach. I value detailed explanations for complex integrations and architectural decisions. Do not make changes to files outside the specified scope for a given task without explicit approval.

## System Architecture
- **Stack:** Static multi-page site — HTML + Tailwind CSS + vanilla JavaScript. No build step.
- **Hosting:** GitHub → Cloudflare Pages. Clean URLs via `_redirects` (`.html` → extensionless, all 301). Local preview served by `static-web-server` on **port 80** (config: `.config/static-web-server.toml`, no-cache headers). Note: the screenshot tool hits :5000 and won't work here — verify pages with `curl http://localhost:80/...`.
- **White-labelling:** `scripts/config.js` holds all client-specific values (company name, phone, address, colours, social links, reviews) and renders them into placeholder span IDs at runtime. Static fallback content is hardcoded in HTML so crawlers see real content; config.js re-renders on top for white-label swaps.
- **Page set (~107 HTML pages):** homepage, quote, about, services, gallery, contact, blog hub + 20 blog posts, case-studies hub + 10 project pages, areas-we-cover + 20+ location pages, 25 service pages, area×service combo pages, cost guide + 5 deep-dive guides + 6 interactive calculators, plus about-premium-landscapes entity page and 404.

### UI/UX
- **Visual style:** Modern SaaS — clean white backgrounds, minimal, professional.
- **Liquid Glass design system** (Apple iOS-inspired): translucent materials, backdrop blur, refraction highlights, smooth transitions, via `styles/liquid-glass.css`. Applied to nav, cards, buttons, progress indicators.
- **Colour palette:** primary blue `#2563eb`, secondary `#3b82f6`, accent purple `#8b5cf6`, light blue `#f0f9ff`.
- **Typography:** headings Inter/Poppins; body Open Sans/Lato.
- **Responsive:** fully mobile-first.

### Key features
- **Instant Quote (`quote.html`):** 6-step conversational flow with progressive disclosure — (1) mode select: Full Garden Makeover vs Select Individual Products; (2) product grid w/ dynamic fields OR free-text vision; (3) area slider + budget; (4) manual address + photo/video upload; (5) contact details; (6) AI Design Visualization (educational, 100% free, ~90s delivery by email, skippable). Live summary panel, progress bar. Submission shows a confirmation message — no fake pricing. **n8n dual-webhook routing** by quote type (`individual_products` vs `full_garden_redesign`); payloads carry `customer`, `project`, `metadata`.
- **PDF quote generator:** auto-generates branded PDF quotes.

## Hero image convention
Photo heroes use a `.hero-photo` class added right after `.hero-gradient` in the page `<style>`:
```css
.hero-photo {
    background: linear-gradient(135deg, rgba(30,58,95,0.72) 0%, rgba(37,99,235,0.55) 50%, rgba(124,58,237,0.55) 100%),
                url('images/heroes/hero-NAME.webp') center/cover no-repeat;
}
```
Then swap **only the main hero section's** class `hero-gradient` → `hero-photo` (leave any CTA blocks that also use `hero-gradient`). Images live in `images/heroes/` as paired `.webp` + `.jpg`. Convert with PIL: open → RGB → resize if width > 1920 → save WebP (quality 82, method 6) + JPEG (quality 82, optimize, progressive). `attached_assets/` is NOT web-served, so copy/convert into `images/heroes/` first; `cwebp` is not installed.

All 25 service pages and the cost guide now have photo heroes. The 10 `projects/*` case-study pages stay gradient-only by design (see content rules).

## Content & data rules
- **No invented projects, customers, testimonials, or quotes**, and **no stock imagery on case studies** — project pages get real photos of the actual completed jobs only. `projects/_template.html` is a noindex draft scaffold documenting the publish checklist.
- Educational/regulatory blog content is fact-anchored to public-domain standards (BS 7533, Part P, IP ratings, SuDS/Schedule 3, GPDO permitted development, Environment Agency guidance) — no fabricated case studies.
- Reviews in `config.js` (`social.reviews`, aggregate rating) drive the homepage/about review grids via `renderReviews()`; update `googleReviewsUrl` once the Google Business profile has live reviews.

## SEO state (current)
Comprehensive SEO/GEO implementation is in place across all pages:
- **On-page:** unique title/meta/keywords, `index,follow`, canonical URLs on every page.
- **Social:** complete Open Graph + Twitter `summary_large_image` cards.
- **Structured data (JSON-LD):** LocalBusiness + AggregateRating + Review objects (homepage); Service + FAQPage + BreadcrumbList on service pages; Article + BreadcrumbList + FAQPage on all 20 blog posts; BreadcrumbList on location/project pages; CollectionPage/ItemList on case-studies hub; AboutPage/@graph on the entity page. All validated, 0 errors.
- **Technical:** `sitemap.xml` (~104 URLs, clean slugs), `robots.txt` (full crawl + sitemap ref), `_redirects` with no redirect chains.
- **Content depth:** unique factual local content + 5 town-specific FAQs on every area page; 20 blog posts; cost guide + 5 deep-dive pricing pages + 6 calculators; 5 high-intent area×service combo pages; entity/answer hub (`about-premium-landscapes`). Bidirectional internal linking (blog ↔ service ↔ area ↔ case study).
- **Generator scripts** (idempotent, re-runnable) live in `scripts/`: `build_area_service_pages.py`, `phase_c_rewrite_areas.py`, `phase_d_blogs.py`, `blog_url_rename.py`, `phase_e_thin_content.py`.

## External dependencies
- **n8n** — quote workflow automation, pricing, PDF generation, email delivery.
- **Make.com** — webhooks for image design requests, CRM entry, follow-up.
- **Google Sheets / Airtable** — pricing logic storage.
- **DALL·E 3 / Midjourney** — AI garden design images.
- **CRM (Airtable or Zoho)** — lead storage.
- **WhatsApp (360dialog / Twilio)** and **Email (Gmail / SendGrid)** — follow-up automation.

## Open items / future work
- `commercial-astroturf-leicester` hero photo contains a rival "GREENSCAPE OUTDOOR LIVING" wall sign — decision pending (leave / paint out / swap).
- A few heavy heroes could be recompressed (granite ~470KB, turfing ~450KB, retaining ~419KB, natural-stone ~412KB).
- Case-study project pages await real job photos before going beyond gradient heroes.
