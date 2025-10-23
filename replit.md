# Premium Landscapes - AI-Powered Landscaping Website

**Last Updated:** October 23, 2025

## 📋 Project Overview

**Premium Landscapes** is a high-converting, AI-powered landscaping website template designed to be sold to landscaping clients for **£3,500 setup + £200/month retainer**.

### Purpose
- Public demo and white-label template
- Fast rebranding capability (< 2 hours per new client)
- Modular, mobile-first design
- AI-powered instant quotes and design generation

### Tech Stack
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Integrations:** Make.com, Google Sheets, Airtable, DALL·E/Midjourney
- **Optional:** Vapi + WhatsApp, ElevenLabs

---

## 🖥️ Page Structure

### 1. Hero Section
- **Heading:** "Instant Garden Quotes. AI-Generated Designs."
- **Subheading:** "Get a price and design concept in minutes — no pressure, no sales calls."
- **CTA Button:** "Get Instant Quote" → scrolls to form

### 2. About Section
- Two-column layout: Text + Image
- Trust-building, results-focused messaging
- Clean, minimal, earthy tones

### 3. Services Grid
- 2-3 columns on mobile
- Services include:
  - Lawn Installation
  - Decking
  - Patio
  - Fencing
  - Lighting
  - Full Redesigns
- Icons/images with Tailwind hover animations

### 4. Instant Quote Engine
**Form Fields:**
- Area size (sqm)
- Postcode
- Feature checkboxes (Lawn, Decking, Lighting, etc.)
- Optional image upload
- Email

**Workflow:**
1. User submits → Make.com webhook
2. Make.com queries Google Sheet with supplier pricing
3. Returns estimated price range + optional breakdown
4. Optional: "Download PDF Quote" button
5. Optional: "Generate AI Design" button

### 5. AI Design Generator
**Form Fields:**
- Image upload (optional)
- Preferred style dropdown (Modern, Tropical, Low-Maintenance, etc.)

**Workflow:**
1. Submit → Make webhook
2. Make → GPT-4o generates prompt → DALL·E or Midjourney
3. Display returned image in browser or email
4. Optional: carousel for multiple variants

### 6. Design Examples
- Carousel of AI-generated example images
- Optional: "Before/After" mode
- Pre-generated with multiple styles and sizes

### 7. Contact Section
- Embedded contact form
- Click-to-call phone number
- WhatsApp link (pre-filled message)
- Optional: embedded map

---

## 🎨 Design System

### Visual Style
- Minimalist and earthy (garden design meets modern SaaS)
- White background
- Muted greens, dark greys, hints of brown/stone/terracotta
- Rounded edges, clean icons
- Fully responsive across all devices

### Typography
- **Headings:** Inter or Poppins (bold, clean)
- **Body:** Open Sans or Lato (professional, neutral)

### Components
- Reusable CTA buttons (primary: green, secondary: white outline)
- Mobile hamburger menu
- Modular forms, cards, popups

---

## ⚙️ Integrations

### Make.com Webhooks
- Instant Quote Submission
- Image Design Request
- CRM Entry
- Follow-up Automation (email/WhatsApp)

### Google Sheets / Airtable
- Pricing logic storage (editable per client)
- Connected via Make for estimate calculations

### DALL·E 3 / Midjourney
- Design prompts generated from user inputs
- Returns 1-3 AI-generated garden designs

### CRM
- Airtable or Zoho
- Stores: name, email, postcode, features, quote, images
- Optional: push to Google Sheets or ReTool dashboard

### Follow-up Automation
- WhatsApp via 360dialog or Twilio (Make.com)
- Email via Gmail or SendGrid
- Optional: AI voice agent via Vapi + ElevenLabs

---

## 🧾 PDF Quote Generator

Auto-generates branded PDF with:
- Client name
- Quote breakdown
- Total price range
- Logo and company details
- Styled as modern invoice
- Built using Make's PDF tools or jsPDF in-browser

---

## 🧩 White-Label/Rebrandable Elements

| Element | How to Swap |
|---------|-------------|
| Logo | `/public/images/logo.png` |
| Primary Color | Tailwind config / CSS variables |
| Company Name | JSON config or global variable |
| Contact Email | `.env` or config file |
| Pricing Sheet URL | Make / Airtable scenario input |
| WhatsApp Number | `.env` or config block |

**Goal:** New client setup in under 2 hours

---

## 📁 File Structure

```
/premium-landscapes/
│
├── index.html
├── styles/
│   └── tailwind.css
├── scripts/
│   └── main.js
├── images/
│   └── logo.png
│   └── examples/
├── components/
│   └── header.html
│   └── footer.html
├── .env
├── README.md
└── replit.nix
```

---

## 📦 Deployment Plan

- **Development:** Live site hosted on Replit
- **Production:** Cloudflare Pages + custom domain
- **Includes:** 
  - index.html, styles.css (Tailwind), scripts.js
  - All Make webhook endpoints
  - replit.nix for backend services (if needed)

---

## ✅ Success Criteria

A successful build must:
1. ✅ Load fast on mobile
2. ✅ Collect user inputs and trigger correct webhook logic
3. ✅ Display quote + image instantly or email results
4. ✅ Visually feel trustworthy, clean, and professional
5. ✅ Be fully reusable for new clients in under 2 hours

---

## 🛠️ Build Phases (Iterative)

### Phase 1: Static Site with Placeholder Forms
- HTML structure with Tailwind
- Quote form with mock inputs
- Dummy buttons with webhook placeholders
- Placeholder image carousel

### Phase 2: Make.com Quote Logic
- Connect quote form to Make webhook
- Integrate Google Sheets pricing
- Return and display quote

### Phase 3: PDF Generation
- Implement PDF quote download
- Brand with logo and styling

### Phase 4: Image Generation
- Connect AI design form to Make webhook
- Integrate DALL·E/Midjourney API
- Display generated designs

### Phase 5: CRM + Follow-up Automation
- Store leads in Airtable/Zoho
- Set up WhatsApp/email automation
- Optional: Vapi voice agent

---

## 📝 Development Notes

- Everything should be cleanly commented and modular
- Mobile-first approach
- Test each form with console output before connecting to Make
- Use environment variables for all sensitive/client-specific data
- Keep components reusable and DRY

---

## 🎯 Current Status

**Created:** October 23, 2025
**Last Updated:** October 23, 2025
**Status:** Phase 1 Complete ✅ - Fully functional static website with placeholder integrations

### ✅ Completed Features
- All 7 sections implemented (Hero, About, Services, Quote Engine, AI Design Generator, Design Examples, Contact)
- Mobile-responsive design with earthy color palette (greens, greys, stone)
- Smooth scrolling navigation
- Mobile hamburger menu
- Interactive carousel for design examples
- Three functional forms ready for Make.com webhook integration:
  - Instant Quote Form (with area size, postcode, features, email, image upload)
  - AI Design Generator Form (with style selection, image upload)
  - Contact Form
- White-label configuration system in `scripts/config.js`
- Demo mode with console logging (shows when webhooks not connected)
- Proper error handling for all forms

### 📝 Next Steps (Phase 2-5)
1. **Phase 2:** Connect Make.com webhooks for quote calculation
2. **Phase 3:** Implement PDF quote generation
3. **Phase 4:** Integrate DALL·E/Midjourney for AI design generation
4. **Phase 5:** Add CRM integration and follow-up automation

### 🔌 Ready to Connect
To connect Make.com webhooks, update the URLs in `scripts/config.js`:
```javascript
webhooks: {
    quote: "https://hook.eu2.make.com/your-quote-webhook-url",
    design: "https://hook.eu2.make.com/your-design-webhook-url",
    contact: "https://hook.eu2.make.com/your-contact-webhook-url"
}
```

---

## 💡 Business Model

- **Setup Fee:** £3,500
- **Monthly Retainer:** £200
- **Target Market:** UK landscaping businesses
- **Value Proposition:** Instant quotes + AI designs = higher conversion rates
