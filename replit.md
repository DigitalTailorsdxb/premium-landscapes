# Premium Landscapes - AI-Powered Landscaping Website

## Overview
Premium Landscapes is an AI-powered, high-converting landscaping website template designed for sale to landscaping businesses. It serves as a public demo and white-label solution, enabling rapid rebranding and offering AI-powered instant quotes and design generation. The platform aims to provide a significant competitive advantage in the landscaping market by boosting conversion rates.

**Trade Engine Branding:** All AI features branded as "Powered by Trade Engine" with footer link to https://tradeengine.io on every page. GREEN "FREE" badges on navigation and page headers emphasize no-cost features.

## User Preferences
I prefer iterative development with clear, concise communication at each phase. Please ask before making major architectural changes or integrating new third-party services. Ensure all code is cleanly commented and follows a mobile-first approach. I value detailed explanations for complex integrations and architectural decisions. Do not make changes to files outside the specified scope for a given task without explicit approval.

## System Architecture
The website utilizes a multi-page architecture (`index.html`, `quote.html`, `design.html`, `about.html`, `services.html`, `gallery.html`, `contact.html`, `blog.html`, and individual blog post pages) for enhanced UX and SEO.

### UI/UX Decisions
- **Visual Style:** Modern SaaS design with white backgrounds for a clean, professional, and minimal aesthetic.
- **Color Palette:** Primary vibrant blue (`#2563eb`), secondary light blue (`#3b82f6`), accent purple (`#8b5cf6`), and very light blue (`#f0f9ff`).
- **Typography:** Headings use Inter or Poppins; body text uses Open Sans or Lato.
- **Responsiveness:** Fully responsive, mobile-first design across all devices.
- **Components:** Reusable CTA buttons, mobile hamburger menu, modular forms, cards, and popups.
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
- **AI Design Generator Page (`design.html`):** Allows users to select garden styles, upload an optional image, and provide an email for AI-generated designs. The workflow sends data to a Make.com webhook.
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