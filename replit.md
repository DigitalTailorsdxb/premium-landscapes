# Premium Landscapes - AI-Powered Landscaping Website

## Overview
**Premium Landscapes** is an AI-powered, high-converting landscaping website template designed for sale to landscaping businesses at £3,500 setup + £200/month retainer. Its core purpose is to serve as a public demo and white-label solution, enabling rapid rebranding (< 2 hours per client). The platform offers AI-powered instant quotes (via n8n workflow) and design generation, aiming to provide a significant competitive advantage in the landscaping market by boosting conversion rates.

## Current Status
✅ **Complete & Production-Ready** - All 19 pages built and functional across mobile/desktop
✅ **Quote System Ready** - 5-step conversational quote form with n8n webhook integration configured
✅ **Mutually Exclusive Quote Modes** - Step 1 presents two clear options: "Complete Garden Redesign" OR "Select Individual Products" - selecting one automatically deselects the other (Nov 13)
✅ **Clear Mode Differentiation** - Both quote modes include "How it works" explanations so users understand: Full Redesign = entire plan based on budget/requirements, Individual Products = strict quote based only on selected products/sizes (Nov 13)
✅ **One-Click Material Selection** - Full Redesign materials add instantly with single click, no modal/quality/area inputs needed - workflow determines sizing and quality based on budget (Nov 13)
✅ **Dedicated Area Input Fields** - Each product now has a dedicated area/size input field for more accurate quotes
✅ **Clean Quote Submission** - No fake pricing shown on site; actual quote sent via email from n8n workflow
✅ **Dual Webhook Routing** - Automatic routing to separate workflows on PRODUCTION endpoints: Standard quotes → `/webhook/premium-landscapes-quote`, Full redesigns → `/webhook/premium-landscapes-full-redesign`, AI Design → `/webhook/premium-landscapes-ai-design` (Nov 18)
✅ **Logo URL for PDFs** - https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev/static/logo.png
✅ **Fencing Data Structure Fixed** - Changed from `length_m` to `length` and `unitType: 'qty'` to `unitType: 'm'` (Nov 5)
✅ **Simple Manual Address Entry** - Clean 4-field form (house number, street, city, postcode) - 100% reliable, no API dependencies (Nov 5)
✅ **Full Garden Redesign Feature** - Enhanced Step 2 with comprehensive material selector (30+ materials across 5 categories) for accurate full garden pricing. Includes budget-based design mode for customers who want design proposals without specifying materials (Nov 5)
✅ **Custom Budget Input** - Replaced budget range cards with direct numeric input field. Mandatory for Full Garden Redesign quotes to enable precise budget-based design proposals (Nov 5)
✅ **Clean gardenDesign Output** - Simplified data structure to only `budgetBasedDesign` (boolean) and `categories` (object) for optimal n8n workflow processing (Nov 5)
✅ **Mock Data Created** - Budget-based design example with £25,000 budget, 100m² area, "low maintenance & pet friendly" requirements (Nov 5)
✅ **Clean Material Selector Design** - Uniform gray/white category headers instead of multicolored options for professional appearance (Nov 11)
✅ **Dynamic Extras Detection** - Pergola, Fire Pit, and Water Feature automatically populate `extras` object when selected as materials (Nov 11)
✅ **Complete n8n Payload Structure** - Added `metadata` object with source, timestamp, quoteType, and webhookDestination matching n8n workflow expectations (Nov 11)
✅ **Workflow Integration Complete** - All 3 workflows (Individual Quote, Full Redesign Quote, AI Garden Design) now fully connected with bidirectional flow (Nov 14):
  - Quote forms include optional "Also send me AI garden design concepts" checkbox - triggers both quote + design workflows simultaneously
  - AI Design workflow accepts data from both standalone design form AND quote forms
  - Design emails include "Get Instant Quote" CTA for seamless conversion path
  - Source detection (`metadata.source`) enables customized messaging based on entry point
✅ **AI Design Always Available** - AI design checkbox now always visible in quote form (not photo-dependent) - works with photos (image-based) OR without (budget-based) (Nov 14)
✅ **Dynamic Confirmation Messaging** - Quote confirmation automatically mentions AI designs when checkbox selected (Nov 14)
✅ **AI Design Photo Upload (Step 5)** - When AI design checkbox is selected, upload section appears allowing users to upload garden photos specifically for AI design generation. Photos uploaded here take priority over Step 4 photos. Drag-and-drop interface with image preview and remove functionality (Nov 18)

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
  - **Step 1:** Mutually exclusive quote mode selection - users choose EITHER "Complete Garden Redesign" (entire plan based on budget/requirements) OR "Select Individual Products" (strict quote based on selected products/sizes only). Clear "How it works" explanations for both modes.
  - **Step 2 (Dual Mode):**
    - **Individual Products Mode:** Product selection grid (Patio, Decking, Turf, Driveway, Fencing, Lighting, Other) followed by dynamic detail fields for each selected product - material/description textarea and area/size input
    - **Full Redesign Mode:** Comprehensive material selector with 5 collapsible categories (Paving & Hard Landscaping, Lawn & Planting, Structures, Features, Boundaries) containing 30+ material options. **One-click selection** - materials add instantly with single click, no modal needed. Workflow determines sizing and quality automatically based on budget. Selected materials appear in real-time summary panel with remove functionality. **Budget-Based Design Option:** Checkbox allowing customers to request design proposals based on budget without specifying materials - enables flexibility to design within price constraints. Design vision notes field for overall project requirements.
  - **Step 3:** Area slider (10-150 m²) and budget selection cards
  - **Step 4:** Simple 4-field manual address entry (house number, street, city, postcode) - fast, reliable, no API dependencies. Includes drag-and-drop photo/video upload.
  - **Step 5:** Contact details with AI design checkbox. When checked, reveals drag-and-drop photo upload section for garden images. AI-specific photos take priority over Step 4 photos in the workflow payload
  - Live summary panel updates in real-time showing selected products, area, budget, location, and photo count
  - Progress bar with step indicator and percentage
  - **Quote Submission:** After submission, shows confirmation message explaining quote will be emailed. No fake pricing displayed on site.
  - **n8n Integration:** Dual webhook routing automatically directs quotes to separate workflows based on type
    - **Complete Payload Structure:** All quotes include `customer`, `project`, and `metadata` objects
      - `customer`: name, email, phone, postcode, city, street, houseNumber, address
      - `project`: title, type, totalArea_m2, totalBudget_gbp, layoutType, sunlight, stylePreference, maintenanceLevel, siteConditions, products, extras, notes
      - `extras`: Dynamic detection - pergola, firePit, waterFeature automatically set to `{ include: true }` when selected as materials
      - `metadata`: source, timestamp (ISO), quoteType, webhookDestination for workflow tracking
    - **Standard Quote Webhook:** `webhooks.quote` - receives `project.type: "individual_products"` with products array for simple pricing
    - **Full Redesign Webhook:** `webhooks.quoteFullRedesign` - receives `project.type: "full_garden_redesign"` with `project.gardenDesign` object containing:
      - `budgetBasedDesign` (boolean) - true when customer wants design proposal within budget
      - `categories` (object) - grouped materials when customer selects specific materials (empty {} when budget-based)
    - Smart routing logic checks `project.type` and sends to appropriate URL automatically
    - Clear console logging shows quote type and target workflow for debugging (see DUAL_WEBHOOK_ROUTING.md)
    - **Mock data available:** See `N8N_MOCK_DATA_CODE.js` for n8n Code node format or `MOCK_BUDGET_BASED_DESIGN.json` for JSON (£25k, 100m², low maintenance & pet friendly)
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
- **Google Sheets / Airtable:** Storage for pricing logic, connected via n8n for estimate calculations.
- **DALL·E 3 / Midjourney:** AI image generation based on user inputs for garden designs.
- **CRM (Airtable or Zoho):** For storing leads (name, email, postcode, features, quote, images) with optional push to Google Sheets or ReTool dashboard.
- **WhatsApp (via 360dialog or Twilio):** For follow-up automation, integrated via Make.com.
- **Email (Gmail or SendGrid):** For follow-up automation.
- **Vapi + ElevenLabs (Optional):** For AI voice agent integration.
- **jsPDF:** For in-browser PDF generation.