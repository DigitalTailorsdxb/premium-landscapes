# n8n Workflow Setup Guide for Premium Landscapes

## System Overview
Premium Landscapes has two main automation workflows:
1. **Instant Quote System** - AI-powered pricing calculator with PDF generation
2. **AI Garden Design** - DALL·E 3 design generation with email delivery

---

## ✅ Recommended Answers to Setup Questions

### 1️⃣ Setup Type: **n8n.cloud (Hosted)**
**Recommendation:** Use n8n.cloud for reliability and zero maintenance

**Reason:** 
- White-label template will be sold to multiple landscaping companies
- Each client needs a stable, always-on automation
- n8n.cloud provides persistent webhook URLs
- No server management required for clients

**Webhook URLs Format:**
```
Quote: https://your-instance.app.n8n.cloud/webhook/premium-landscapes-quote
Design: https://your-instance.app.n8n.cloud/webhook/premium-landscapes-design
```

---

### 2️⃣ Email Sending: **Gmail (OAuth2) + SMTP Fallback**
**Recommendation:** Primary = Gmail OAuth2, Fallback = Custom SMTP

**Setup:**
- **For Demo/Template:** Use Gmail OAuth2 (easy to set up, reliable)
- **For White-Label Clients:** Provide SMTP option for branded emails like `quotes@premiumlandscapes.co.uk`

**Why Gmail First:**
- Easy credential setup in n8n
- Reliable delivery
- Can be swapped to client's Gmail when selling template

**Email Templates Needed:**
1. **Quote Email:**
   - Subject: "Your Instant Garden Quote from [Company Name]"
   - Body: Greeting, quote summary, attached PDF, CTA to book consultation
   - Attachment: PDF quote with itemized breakdown

2. **Design Email:**
   - Subject: "Your AI Garden Designs from [Company Name]"
   - Body: Greeting, 3 AI-generated design images, description of each style
   - CTA: "Get an instant quote to bring these to life"

---

### 3️⃣ Storage: **Cloudflare R2 (Recommended) or Google Drive**
**Recommendation:** Cloudflare R2 for production, Google Drive for quick setup

**For AI Design Images:**
- **Option A (Best):** Cloudflare R2
  - Fast CDN delivery
  - Low cost (free tier: 10GB storage)
  - Professional URLs for images in emails
  - Easy n8n integration
  
- **Option B (Quick Start):** Google Drive
  - Free
  - Easy n8n node available
  - Can share images via public links
  - Good for demo/testing

**For Quote PDFs:**
- Generate inline using n8n's built-in functions
- Attach directly to email (no storage needed)
- Optionally archive in Google Drive for records

**Storage Structure:**
```
cloudflare-r2/
├── designs/
│   ├── customer-email-timestamp/
│   │   ├── design-1.png
│   │   ├── design-2.png
│   │   └── design-3.png
└── quotes/
    └── quote-customer-timestamp.pdf
```

---

### 4️⃣ Workflow Structure: **Two Separate Workflows**
**Recommendation:** Create TWO separate workflows

**Why Separate:**
- Different webhook endpoints (quote.html vs design.html)
- Different data structures and processing logic
- Easier to debug and maintain
- Can deploy one without affecting the other
- Easier for white-label clients to understand

**Workflow 1: Quote System**
```
Webhook → Validate Data → Parse Product Details 
→ Calculate Pricing (with regional modifiers) 
→ Generate PDF Quote → Send Email → Store in CRM
```

**Workflow 2: AI Design System**
```
Webhook → Validate Data → Build DALL·E Prompt 
→ Generate 3 Designs (loop) → Upload to Storage 
→ Send Email with Images → Store in CRM
```

---

## 📊 Data Flow Architecture

### Quote System Webhook Payload (from quote-engine.js)
```json
{
  "customer": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "07444887813",
    "postcode": "NN1 4PB"
  },
  "project": {
    "products": ["patio", "decking", "turf"],
    "productDetails": {
      "patio": "30 sqm natural stone",
      "decking": "20 sqm composite",
      "turf": "50 sqm artificial grass"
    },
    "area": 85,
    "budget": "10000-20000",
    "notes": "Existing oak tree to work around",
    "photos": ["base64Image1", "base64Image2"]
  },
  "pricing": {
    "region": "Midlands",
    "regionalModifier": 1.0,
    "confidence": 75
  },
  "metadata": {
    "timestamp": "2025-10-25T01:00:00Z",
    "source": "website"
  }
}
```

### Design System Webhook Payload (from design-engine.js)
```json
{
  "customer": {
    "email": "laura@example.com",
    "phone": "07444887813"
  },
  "design": {
    "features": ["patio", "water-feature", "pergola", "lighting"],
    "styleDescription": "Modern minimalist with clean lines and architectural plants",
    "gardenSize": "75 sqm",
    "budget": "10000-20000"
  },
  "photo": {
    "name": "current-garden.jpg",
    "type": "image/jpeg",
    "size": 2048576,
    "data": "base64ImageString"
  },
  "metadata": {
    "timestamp": "2025-10-25T01:00:00Z",
    "source": "website"
  }
}
```

---

## 🔧 n8n Workflow Components

### Quote Workflow Nodes
1. **Webhook** - Receive quote data
2. **Function** - Validate & parse product details
3. **Function** - Calculate pricing with regional modifiers
4. **Function** - Generate confidence score (50-95%)
5. **Code** - Create PDF quote (jsPDF or similar)
6. **Gmail/SMTP** - Send quote email with PDF
7. **HTTP Request** - Push to CRM (Airtable/Google Sheets)
8. **Webhook Response** - Confirm to website

### Design Workflow Nodes
1. **Webhook** - Receive design request
2. **Function** - Build DALL·E prompt from features + style
3. **HTTP Request** - Call OpenAI DALL·E 3 API (loop 3x for 3 designs)
4. **Cloudflare R2/Google Drive** - Upload generated images
5. **Function** - Build email HTML with image URLs
6. **Gmail/SMTP** - Send design email
7. **HTTP Request** - Push to CRM
8. **Webhook Response** - Confirm to website

---

## 🎨 DALL·E Prompt Construction

**Example Prompt Builder:**
```javascript
// n8n Function Node
const features = $json.design.features; // ["patio", "water-feature", "pergola"]
const style = $json.design.styleDescription; // "Modern minimalist..."
const size = $json.design.gardenSize; // "75 sqm"

const prompt = `Create a photorealistic garden design render for a ${size} UK garden. 
Style: ${style}

Features to include:
${features.map(f => `- ${f.replace('-', ' ')}`).join('\n')}

Requirements:
- Photorealistic quality
- UK climate-appropriate plants
- Professional landscape design
- Warm natural lighting
- View from garden seating area perspective
- Contemporary UK residential setting

Technical specs: 4K quality, landscape orientation, natural colors`;

return { prompt: prompt };
```

---

## 📧 Email Templates

### Quote Email (HTML)
```html
<h1>Your Instant Garden Quote</h1>
<p>Hi {{customer.name}},</p>

<p>Thank you for requesting a quote from Premium Landscapes. We've analyzed your project and prepared a detailed estimate.</p>

<h2>Project Summary</h2>
<ul>
  <li>Area: {{project.area}} m²</li>
  <li>Budget Range: {{project.budget}}</li>
  <li>Features: {{project.products}}</li>
</ul>

<p><strong>Estimated Price Range: £{{pricing.min}} - £{{pricing.max}}</strong></p>

<p>See the attached PDF for a detailed breakdown.</p>

<a href="tel:07444887813">Call us: 07444 887813</a>
```

### Design Email (HTML)
```html
<h1>Your AI Garden Designs</h1>
<p>Hi there,</p>

<p>We've created 3 stunning AI-generated design concepts based on your preferences:</p>

<h2>Design 1: {{style}} Garden</h2>
<img src="{{design1Url}}" width="600" />

<h2>Design 2: {{style}} Garden (Variation)</h2>
<img src="{{design2Url}}" width="600" />

<h2>Design 3: {{style}} Garden (Alternative)</h2>
<img src="{{design3Url}}" width="600" />

<p>Love what you see? Get an instant quote to bring these designs to life!</p>
<a href="https://premiumlandscapes.co.uk/quote.html">Get Instant Quote</a>
```

---

## 🔐 Required Credentials

### For Quote Workflow
1. Gmail/SMTP credentials (email sending)
2. CRM API key (Airtable or Google Sheets)

### For Design Workflow
1. OpenAI API key (DALL·E 3 access)
2. Cloudflare R2 credentials (or Google Drive OAuth)
3. Gmail/SMTP credentials (email sending)
4. CRM API key

---

## 🚀 Testing Strategy

1. **Quote Test:**
   - Submit quote form with sample data
   - Verify webhook receives data
   - Check pricing calculations
   - Confirm PDF generation
   - Test email delivery

2. **Design Test:**
   - Submit design form with features
   - Monitor DALL·E API calls
   - Verify 3 images generated
   - Check image upload to storage
   - Test email with image links

---

## 📝 White-Label Configuration

Each client needs to customize:
1. **Webhook URLs** - Update in `scripts/config.js`
2. **Email sender** - Change to client's branded email
3. **PDF branding** - Company logo, colors, contact details
4. **CRM integration** - Client's Airtable/Sheets
5. **Regional pricing** - Adjust for client's service area

---

## Summary Recommendation

**✅ Best Setup:**
- Platform: n8n.cloud
- Email: Gmail OAuth2 (easy swap to SMTP later)
- Storage: Cloudflare R2 (professional, scalable)
- Structure: 2 separate workflows (cleaner architecture)

This setup is production-ready, scalable, and easy for white-label clients to understand and manage.
