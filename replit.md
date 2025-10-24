# Premium Landscapes - AI-Powered Landscaping Website

## Overview
**Premium Landscapes** is an AI-powered, high-converting landscaping website template designed for sale to landscaping businesses. Its core purpose is to serve as a public demo and white-label solution, enabling rapid rebranding (< 2 hours per client). The platform offers AI-powered instant quotes and design generation, aiming to provide a significant competitive advantage in the landscaping market by boosting conversion rates.

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
- **Instant Quote Page (`quote.html`):** Features a natural language input for project descriptions, postcode, email, and optional image upload. The workflow involves user submission to a Make.com webhook, GPT analysis of the description against a pricing database, calculation of costs, and return of an itemized quote with options to download as PDF or generate an AI design.
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
- **Make.com:** Used for webhooks to handle instant quote submissions, image design requests, CRM entry, and follow-up automation.
- **Google Sheets / Airtable:** Storage for pricing logic, connected via Make.com for estimate calculations.
- **DALL·E 3 / Midjourney:** AI image generation based on user inputs for garden designs.
- **CRM (Airtable or Zoho):** For storing leads (name, email, postcode, features, quote, images) with optional push to Google Sheets or ReTool dashboard.
- **WhatsApp (via 360dialog or Twilio):** For follow-up automation, integrated via Make.com.
- **Email (Gmail or SendGrid):** For follow-up automation.
- **Vapi + ElevenLabs (Optional):** For AI voice agent integration.
- **jsPDF:** For in-browser PDF generation.