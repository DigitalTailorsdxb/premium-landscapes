# Premium Landscapes - AI-Powered Landscaping Website

## Overview
**Premium Landscapes** is an AI-powered, high-converting landscaping website template designed for sale to landscaping businesses at £3,500 setup + £200/month retainer. Its core purpose is to serve as a public demo and white-label solution, enabling rapid rebranding (< 2 hours per client). The platform offers AI-powered instant quotes (via n8n workflow) and design generation, aiming to provide a significant competitive advantage in the landscaping market by boosting conversion rates.

## Current Status
✅ **Complete & Production-Ready** - All 19 pages built and functional across mobile/desktop
✅ **Quote System Ready** - 5-step conversational quote form with n8n webhook integration configured
✅ **Dedicated Area Input Fields** - Each product now has a dedicated area/size input field for more accurate quotes
✅ **Enhanced Confidence Score** - Dynamic scoring (30-95%) based on completeness of information provided
✅ **Clean Quote Submission** - No fake pricing shown on site; actual quote sent via email from n8n workflow
✅ **n8n Integration Active** - Webhook URL: https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-quote (FIXED Nov 3)
✅ **Logo URL for PDFs** - https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev/static/logo.png
✅ **Fencing Data Structure Fixed** - Changed from `length_m` to `length` and `unitType: 'qty'` to `unitType: 'm'` (Nov 5)
✅ **Google Maps Autocomplete Re-implemented** - Smart optional helper above manual fields, crash-proof with lazy loading (Nov 5)
✅ **Hybrid Address Entry** - Google autocomplete for convenience + reliable manual entry fallback (see GOOGLE_MAPS_AUTOCOMPLETE.md)

## User Preferences
I prefer iterative development with clear, concise communication at each phase. Please ask before making major architectural changes or integrating new third-party services. Ensure all code is cleanly commented and follows a mobile-first approach. I value detailed explanations for complex integrations and architectural decisions. Do not make changes to files outside the specified scope for a given task without explicit approval.

## System Architecture
The website utilizes a multi-page architecture (`index.html`, `quote.html`, `design.html`, `about.html`, `services.html`, `gallery.html`, `contact.html`, `blog.html`, and individual blog post pages) for enhanced UX and SEO.

### UI/UX Decisions
- **Visual Style:** Modern SaaS design with white backgrounds throughout for a clean, professional, and minimal aesthetic.
- **Color Palette:** Primary vibrant blue (#2563eb), secondary light blue (#3b82f6), accent purple (#8b5cf6), and very light blue (#f0f9ff) for subtle backgrounds. No colorful gradients, only subtle fades on CTAs.
- **Typography:** Headings use Inter or Poppins; body text uses Open Sans or Lato.
- **Responsiveness:** Fully responsive, mobile-first design across all devices.
- **Components:** Reusable CTA buttons, mobile hamburger menu, modular forms, cards, and popups.
- **White-labeling:** Designed for quick rebranding by swapping logos, primary colors (via Tailwind config/CSS variables), company name (JSON config), contact details, pricing sheet URLs, and WhatsApp numbers.

### Technical Implementations
- **Frontend:** HTML, Tailwind CSS, JavaScript.
- **Instant Quote Page (`quote.html`):** Revolutionary 5-step conversational quote system with progressive disclosure:
  - **Step 1:** Visual feature selection (Patio, Decking, Turf, Driveway, Fencing, Lighting, Full Redesign, Other)
  - **Step 2:** Dynamic product detail fields - each selected product from Step 1 automatically gets its own detail textarea. Users can add/remove products via modal popup. Additional notes field for general project information not related to specific products.
  - **Step 3:** Area slider (10-150 m²) and budget selection cards
  - **Step 4:** Hybrid address entry with optional Google Maps autocomplete search box above 4 manual input fields (house number, street, city, postcode). Autocomplete fills manual fields when selected, but users can type/edit manually. Lazy loading prevents crashes. Includes drag-and-drop photo/video upload.
  - **Step 5:** Contact details with conditional AI design preview option (only visible if images uploaded; otherwise shows upload prompt)
  - Live summary panel updates in real-time showing selected products, area, budget, location, and photo count
  - Progress bar with step indicator and percentage
  - **Quote Submission:** After submission, shows confirmation message explaining quote will be emailed. No fake pricing displayed on site.
  - **n8n Integration:** Webhook sends all data to n8n workflow which handles pricing calculation, PDF generation, and email delivery
  - **Material/Details First:** Product detail cards show material/description field first, followed by area/size input below
- **AI Design Generator Page (`design.html`):** Allows users to select preferred garden styles, upload an optional image of their current garden, and provide an email for receiving AI-generated designs. The workflow sends data to a Make.com webhook, which then uses GPT-4o to generate prompts for DALL·E or Midjourney.
- **PDF Quote Generator:** Auto-generates branded PDF quotes with client details, itemized breakdown, total price range, and company branding.
- **White-Label Configuration:** Handled via `scripts/config.js` with defensive null checks for easy client-specific customization.
- **Demo Mode:** Includes console logging for all forms to facilitate development and testing.

### Feature Specifications
- **Homepage (`index.html`):** Hero, About, Services Grid, Design Examples Gallery, Contact.
- **About Page (`about.html`):** Company story, values, testimonials.
- **Services Page (`services.html`):** Detailed service cards, "How It Works", "Why Choose Us".
- **Gallery Page (`gallery.html`):** Filterable portfolio grid.
- **Contact Page (`contact.html`):** Form, business hours, location.
- **Blog Section:** Complete 10-article blog with listing and individual post pages.
- **Navigation:** Consistent header/footer navigation with mobile hamburger menu and active page highlighting.

## External Dependencies
- **n8n:** Primary automation platform for quote workflow - handles pricing calculations, PDF generation, and email delivery.
- **Make.com:** Used for webhooks to handle image design requests, CRM entry, and follow-up automation.
- **Google Maps Places API:** Optional address autocomplete helper for UK addresses - fills manual fields when user searches. Gracefully degrades if API unavailable (manual entry always works). Free tier: $200/month credit (~11,700 lookups/month). API key stored in GOOGLE_MAPS_API_KEY environment variable.
- **Google Sheets / Airtable:** Storage for pricing logic, connected via n8n for estimate calculations.
- **DALL·E 3 / Midjourney:** AI image generation based on user inputs for garden designs.
- **CRM (Airtable or Zoho):** For storing leads (name, email, postcode, features, quote, images) with optional push to Google Sheets or ReTool dashboard.
- **WhatsApp (via 360dialog or Twilio):** For follow-up automation, integrated via Make.com.
- **Email (Gmail or SendGrid):** For follow-up automation.
- **Vapi + ElevenLabs (Optional):** For AI voice agent integration.
- **jsPDF:** For in-browser PDF generation.