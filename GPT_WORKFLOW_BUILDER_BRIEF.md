# Premium Landscapes - Workflow Integration Brief

## 🎯 Overview
We have a dual-mode landscaping quote system with AI garden design integration. The frontend sends data to **3 separate n8n webhook endpoints** based on user selections. All workflows need to be aligned on the payload structures and integration flow.

---

## 🔗 Webhook Endpoints

### **1. Individual Products Quote**
**Endpoint:** `/webhook-test/premium-landscapes-quote`  
**Triggered when:** User selects individual products (patio, decking, turf, etc.) and requests a quote

**Payload Structure:**
```json
{
  "customer": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "07444887813",
    "address": "123 Oak Street, Birmingham, B1 2AB"
  },
  "project": {
    "type": "individual_products",
    "totalArea_m2": 50,
    "totalBudget_gbp": 15000,
    "products": [
      {
        "name": "patio",
        "material": "Porcelain",
        "area_m2": 20
      },
      {
        "name": "turf",
        "material": "Artificial grass",
        "area_m2": 30
      }
    ]
  },
  "metadata": {
    "source": "website_quote_form",
    "timestamp": "2025-11-17T15:30:00.000Z",
    "quoteType": "individual_products",
    "webhookDestination": "/webhook-test/premium-landscapes-quote"
  }
}
```

**What this workflow should do:**
- Calculate itemized pricing for each selected product
- Generate branded PDF quote with line items
- Email PDF quote to customer
- Store lead in CRM

---

### **2. Full Garden Redesign Quote**
**Endpoint:** `/webhook-test/premium-landscapes-full-redesign`  
**Triggered when:** User selects "Complete Garden Redesign" mode

**Payload Structure (with materials selected):**
```json
{
  "customer": {
    "name": "Sarah Johnson",
    "email": "sarah@example.com",
    "phone": "07555123456",
    "address": "45 Maple Drive, Oxford, OX1 3QR"
  },
  "project": {
    "type": "full_garden_redesign",
    "totalArea_m2": 80,
    "totalBudget_gbp": 25000,
    "gardenDesign": {
      "budgetBasedDesign": false,
      "categories": {
        "paving": [
          { "material": "Porcelain Patio" }
        ],
        "lawn": [
          { "material": "Artificial Turf" }
        ],
        "structures": [
          { "material": "Pergola" }
        ]
      }
    },
    "notes": "Low maintenance, modern aesthetic, pet-friendly"
  },
  "metadata": {
    "source": "website_quote_form",
    "timestamp": "2025-11-17T15:30:00.000Z",
    "quoteType": "full_garden_redesign",
    "webhookDestination": "/webhook-test/premium-landscapes-full-redesign"
  }
}
```

**Payload Structure (budget-based, no materials):**
```json
{
  "customer": { "name": "...", "email": "...", "phone": "...", "address": "..." },
  "project": {
    "type": "full_garden_redesign",
    "totalArea_m2": 100,
    "totalBudget_gbp": 35000,
    "gardenDesign": {
      "budgetBasedDesign": true,
      "categories": {}
    },
    "notes": "Family-friendly garden, space for kids play area, low maintenance"
  },
  "metadata": { "quoteType": "full_garden_redesign", ... }
}
```

**What this workflow should do:**
- If `budgetBasedDesign: true` → Design entire garden within budget constraints
- If `budgetBasedDesign: false` → Price out specifically selected materials + suggest complementary items
- Calculate comprehensive project pricing
- Generate detailed PDF proposal (not just a quote - more like a design proposal)
- Email PDF to customer
- Store lead in CRM

---

### **3. AI Garden Design Generator**
**Endpoint:** `/webhook-test/premium-landscapes-ai-design`  
**Triggered when:**
- User submits standalone design form (`design.html`), **OR**
- User checks "Also send me AI garden design concepts" checkbox in quote form

**Payload from Quote Form:**
```json
{
  "customer": {
    "email": "john@example.com",
    "phone": "07444887813",
    "name": "John Smith"
  },
  "design": {
    "features": ["patio", "decking", "turf"],
    "styleDescription": "Garden with patio area, decking, lawn",
    "gardenSize": "50",
    "budget": "10000-20000",
    "materials": [],
    "budgetBasedDesign": false,
    "designNotes": ""
  },
  "photo": {
    "name": "my-garden.jpg",
    "type": "image/jpeg",
    "size": 245678,
    "data": "data:image/jpeg;base64,/9j/4AAQ..."
  },
  "metadata": {
    "timestamp": "2025-11-17T15:30:00.000Z",
    "source": "quote-form",
    "formVersion": "2.0",
    "quoteType": "individual-products",
    "hasPhoto": true,
    "hasMaterials": false
  }
}
```

**Payload from Quote Form (Full Redesign with materials):**
```json
{
  "customer": { "email": "...", "phone": "...", "name": "..." },
  "design": {
    "features": ["porcelain_patio", "composite_decking", "artificial_turf"],
    "styleDescription": "Complete garden redesign with Porcelain Patio, Composite Decking, Artificial Turf",
    "gardenSize": "80",
    "budget": "20000-30000",
    "materials": [
      { "category": "paving", "name": "porcelain_patio", "displayName": "Porcelain Patio" },
      { "category": "decking", "name": "composite_decking", "displayName": "Composite Decking" },
      { "category": "lawn", "name": "artificial_turf", "displayName": "Artificial Turf" }
    ],
    "budgetBasedDesign": false,
    "designNotes": "Low maintenance, modern aesthetic"
  },
  "photo": null,
  "metadata": {
    "source": "quote-form",
    "quoteType": "full-redesign",
    "hasPhoto": false,
    "hasMaterials": true
  }
}
```

**Payload from Standalone Design Form:**
```json
{
  "customer": { "email": "...", "name": "..." },
  "design": {
    "features": ["modern", "low-maintenance"],
    "styleDescription": "Modern low-maintenance garden",
    "gardenSize": "60",
    "budget": "15000-25000",
    "materials": [],
    "budgetBasedDesign": false,
    "designNotes": ""
  },
  "photo": { "name": "...", "type": "...", "size": ..., "data": "..." },
  "metadata": {
    "source": "website",
    "formVersion": "1.0"
  }
}
```

**What this workflow should do:**
- Use GPT-4o Vision (if photo provided) or GPT-4o (no photo) to analyze requirements
- Generate DALL·E 3 prompts based on:
  - Customer's photo (if provided)
  - Selected features/materials
  - Style description
  - Budget constraints
- Create 2-4 AI-generated garden design concepts
- Email designs to customer with:
  - Visual mockups
  - Brief description of each design
  - **"Get Instant Quote" CTA button** linking back to quote form
- Store lead in CRM

---

## 🔄 Bidirectional Flow

### **Quote → Design Integration**
1. User fills out quote form (individual OR full redesign)
2. User optionally checks "Also send me AI garden design concepts"
3. Quote submitted → Triggers quote workflow (#1 or #2)
4. If AI checkbox selected → Also triggers AI design workflow (#3)
5. Customer receives:
   - Quote email (from workflow #1 or #2)
   - Design concepts email (from workflow #3, if requested)

### **Design → Quote Integration**
1. User receives AI design concepts email
2. Email includes "Get Instant Quote" CTA
3. User clicks → Redirects to quote form
4. User fills out quote form
5. Conversion complete!

---

## 🎯 Key Implementation Notes

### **Source Detection**
Use `metadata.source` to detect entry point:
- `"website"` = Standalone design form
- `"quote-form"` = From quote form
- `"website_quote_form"` = Quote payload (for quote webhooks)

### **Photo Handling**
- `photo` can be **object with full metadata** OR **null**
- If `photo !== null`:
  - Contains `name`, `type`, `size`, `data` (base64)
  - Use GPT-4o Vision for image-based design
- If `photo === null`:
  - Use text-based GPT-4o for budget/requirements-based design

### **Full Redesign Material Detection**
- Check `metadata.hasMaterials` flag
- If `true` → Customer selected specific materials (in `design.materials` array)
- If `false` → Budget-based design mode (use `design.budgetBasedDesign` flag)

### **Error Handling**
- If AI design workflow fails, quote still succeeds
- User sees: "AI design generation unavailable at the moment. Your quote has been sent successfully."

---

## ✅ What We Need from You (GPT)

1. **Build all 3 n8n workflows** matching the endpoints and payload structures above
2. **Implement proper routing logic** based on `metadata.source` and `metadata.quoteType`
3. **Handle both photo and no-photo scenarios** in AI design workflow
4. **Generate branded PDFs** for quotes and proposals
5. **Send professional emails** with appropriate CTAs
6. **Store all leads in CRM** (Airtable or equivalent)

---

## 📋 Questions to Consider

- Do we need to handle multiple photos, or just the first one?
- What CRM are we integrating with? (Airtable, Zoho, etc.)
- What's the email service? (Gmail, SendGrid, etc.)
- Should we implement follow-up automation sequences?
- What's the pricing logic/source? (Google Sheets, hardcoded, etc.)

Let me know if you need clarification on any payload fields or integration flows!
