# Build n8n Workflow: Premium Landscapes - Full Garden Redesign

## Context
I need to build an n8n workflow that handles **Full Garden Redesign quotes** with a unique dual-mode system:
1. **Material-Specified Mode**: Customer selects specific materials (porcelain tiles, decking, etc.) with quality levels (standard/premium/luxury) and areas
2. **Budget-Based Design Mode**: Customer provides budget + vision notes; we design custom proposal within their price constraints

I have an existing workflow for standard individual product quotes (patio, decking, turf) that I'll use as a template, but this new workflow needs different pricing logic and email handling.

---

## Webhook Trigger Configuration

**Node:** Webhook Trigger  
**Path:** `premium-landscapes-full-redesign`  
**Method:** POST  
**Response Mode:** Response Node  

**Expected Payload Structure:**
```json
{
  "customer": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "07444887813",
    "postcode": "LE19 1WA",
    "city": "Leicester",
    "street": "High Street",
    "houseNumber": "42",
    "address": "42, High Street, Leicester, LE19 1WA, UK"
  },
  "project": {
    "type": "full_garden_redesign",
    "title": "Complete Garden Redesign Installation",
    "totalArea_m2": 100,
    "totalBudget_gbp": 25000,
    
    "gardenDesign": {
      "budgetBasedDesign": false,  // or true
      
      "categories": {
        "paving": [
          {
            "material": "porcelain_tiles",
            "displayName": "Porcelain Tiles",
            "quality": "premium",
            "area_m2": 45,
            "style": "Wood-effect oak",
            "notes": "Light color preferred"
          }
        ],
        "lawn": [...],
        "structures": [...],
        "features": [...],
        "boundaries": [...]
      },
      
      "totalMaterialCount": 3,
      "designVisionNotes": "Modern minimalist style, low maintenance, pet-friendly, south-facing garden with existing oak tree to preserve",
      "materials": [...]  // Flat array of all materials
    }
  },
  "files": [],
  "options": { "aiDesign": false },
  "metadata": {
    "timestamp": "2025-01-05T10:30:00Z",
    "source": "website_quote_form",
    "formVersion": "2.0",
    "confidence": 75
  }
}
```

---

## Workflow Node Structure

### 1. Validate Input (Function Node)
**Purpose:** Extract and validate webhook payload

**Code Requirements:**
- Handle both `$json.body` and `$json` structures
- Extract: `customer`, `project`, `metadata`
- Validate required fields:
  - `customer.name`, `customer.email`
  - `project.gardenDesign` exists
  - `project.totalBudget_gbp` is present
- Check `project.gardenDesign.budgetBasedDesign` flag
- Return clean object with all data

---

### 2. Switch: Budget-Based vs Materials (IF Node)
**Purpose:** Route to different paths based on design mode

**Condition:**
```javascript
{{ $json.project.gardenDesign.budgetBasedDesign === true }}
```

**Two Paths:**
- **TRUE** → Budget-Based Design Path (consultation email)
- **FALSE** → Material Pricing Path (detailed quote)

---

## PATH A: Material-Specified Pricing

### 3a. Calculate Material Pricing (Function Node)
**Purpose:** Price each material based on quality level

**Pricing Logic:**

#### Base Rates (per m² unless stated):
```javascript
const BASE_RATES = {
  // Paving & Hard Landscaping
  porcelain_tiles: 75,
  natural_stone: 85,
  resin_bound: 65,
  gravel: 35,
  block_paving: 60,
  concrete: 50,
  
  // Lawn & Planting
  artificial_turf: 50,
  natural_lawn: 25,
  raised_beds: 180,  // per linear meter
  feature_trees: 450,  // each (avg)
  flower_beds: 120,  // per m²
  
  // Structures
  decking: 95,
  pergola: 2500,  // each (avg)
  gazebo: 3500,  // each
  garden_room: 8500,  // each
  storage_shed: 1200,  // each
  summer_house: 4500,  // each
  
  // Features
  outdoor_lighting: 120,  // per fitting (assume 1 per 10m²)
  water_feature: 1800,  // each (avg)
  fire_pit: 950,  // each
  outdoor_kitchen: 5500,  // each
  seating_area: 800,  // per unit
  bbq_area: 1200,  // each
  
  // Boundaries
  fencing: 85,  // per linear meter
  walls: 140,  // per linear meter
  hedging: 45,  // per linear meter
  gates: 650   // each
};

const QUALITY_MULTIPLIERS = {
  standard: 1.0,
  premium: 1.3,
  luxury: 1.6
};
```

**Calculation Steps:**
1. Loop through `project.gardenDesign.materials` array
2. For each material:
   ```javascript
   basePrice = BASE_RATES[material.material]
   qualityMultiplier = QUALITY_MULTIPLIERS[material.quality]
   area = material.area_m2
   
   itemTotal = basePrice × qualityMultiplier × area
   ```
3. Sum all item totals
4. Add design consultation fee: **£850 (fixed)**
5. Add contingency: **5%**
6. Calculate subtotal
7. Add VAT: **20%**
8. Return breakdown + grand total

**Output Structure:**
```json
{
  "pricing": {
    "items": [
      {
        "category": "paving",
        "material": "Porcelain Tiles",
        "quality": "Premium",
        "area": "45 m²",
        "baseRate": 75,
        "multiplier": 1.3,
        "lineTotal": 4387.50
      }
    ],
    "materialsSubtotal": 12500,
    "designConsultation": 850,
    "contingency": 667.50,
    "subtotal": 14017.50,
    "vat": 2803.50,
    "total": 16821.00
  }
}
```

---

### 4a. Generate AI Summary (Basic LLM Chain)
**Purpose:** Create professional quote summary

**Model:** GPT-4o-mini or similar  
**Prompt Template:**
```
You are a professional landscaping quote writer for Premium Landscapes.

Create a warm, professional 3-paragraph summary for this full garden redesign quote:

Customer: {{$json.customer.name}}
Budget: £{{$json.project.totalBudget_gbp}}
Selected Materials: {{$json.project.gardenDesign.totalMaterialCount}} items
Quote Total: £{{$json.pricing.total}}

Materials:
{{#each $json.project.gardenDesign.materials}}
- {{this.displayName}} ({{this.quality}}) - {{this.area_m2}} m²
{{/each}}

Design Vision: {{$json.project.gardenDesign.designVisionNotes}}

Write 3 paragraphs:
1. Acknowledge their vision and selected materials
2. Highlight key features and quality choices
3. Invite them to schedule a consultation to refine the design

Keep it personal, enthusiastic, and professional. Max 150 words.
```

---

### 5a. Build Materials PDF (Function Node)
**Purpose:** Generate detailed quote PDF with materials grouped by category

**HTML Template Requirements:**
- Logo: `https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev/static/logo.png`
- Quote Reference: `PL-25-XXXX` (auto-increment or timestamp)
- Customer details section
- **Materials breakdown table** grouped by category:
  - Paving & Hard Landscaping
  - Lawn & Planting
  - Structures
  - Features
  - Boundaries
- Each row: Material | Quality | Area | Unit Rate | Line Total
- Subtotals section:
  - Materials Total
  - Design Consultation: £850
  - Contingency (5%)
  - Subtotal
  - VAT (20%)
  - **Grand Total**
- Terms & conditions footer
- Contact details

**Styling:** Clean, modern, blue theme (#2563eb), professional layout

---

### 6a. Convert to PDF (HTTP Request → CloudConvert or PDF.co)
**Purpose:** Convert HTML to PDF binary

**Service:** CloudConvert API  
**Endpoint:** `/v2/convert`  
**Input:** HTML from previous node  
**Output:** Binary PDF file

---

### 7a. Send Materials Quote Email (Email Send Node)
**From:** premiumlandscapesuk@gmail.com  
**To:** `{{$json.customer.email}}`  
**Subject:** `Your Complete Garden Redesign Quote – {{$json.customer.name}} 🌿`

**HTML Body:**
```html
<div style="font-family:Inter,Arial,sans-serif;line-height:1.6;color:#0b2e4c;">
  <p>Hi {{$json.customer.name}},</p>
  
  <p>Thank you for requesting a quote for your complete garden redesign! We're excited about your vision for a {{$json.project.gardenDesign.designVisionNotes}}.</p>
  
  <p><strong>Your tailored quote is attached as a PDF.</strong></p>
  
  <h3 style="color:#2563eb;">Quote Summary</h3>
  <ul>
    <li><strong>Total Investment:</strong> £{{$json.pricing.total}}</li>
    <li><strong>Materials Selected:</strong> {{$json.project.gardenDesign.totalMaterialCount}} premium items</li>
    <li><strong>Estimated Timeline:</strong> 12-15 working days</li>
  </ul>
  
  {{$json.aiSummary}}
  
  <h3 style="color:#2563eb;">Next Steps</h3>
  <p>Ready to transform your garden? We'd love to schedule a free site visit to:</p>
  <ul>
    <li>Review your material selections in person</li>
    <li>Refine the design to perfection</li>
    <li>Discuss your timeline and preferences</li>
  </ul>
  
  <p><a href="tel:07444887813" style="display:inline-block;background:#2563eb;color:white;padding:12px 24px;text-decoration:none;border-radius:8px;margin-top:10px;">📞 Call 07444 887813</a></p>
  
  <p>Or reply to this email with your preferred times!</p>
  
  <p>Looking forward to creating your dream garden,<br>
  <strong>The Premium Landscapes Team</strong></p>
  
  <hr style="margin:30px 0;border:none;border-top:1px solid #e5e7eb;">
  <p style="font-size:12px;color:#6b7280;">
    Premium Landscapes | 07444 887813 | info@premium-landscapes.co.uk<br>
    Serving Midlands & Home Counties
  </p>
</div>
```

**Attachments:** PDF from previous node

---

## PATH B: Budget-Based Design

### 3b. Calculate Budget Range (Function Node)
**Purpose:** Determine realistic design scope

**Logic:**
```javascript
const budget = $json.project.totalBudget_gbp;
const area = $json.project.totalArea_m2;

// Estimate per-m² range
const lowPerM2 = budget * 0.7 / area;  // Conservative
const highPerM2 = budget * 0.95 / area; // Optimistic (leave 5% buffer)

return {
  budgetAnalysis: {
    totalBudget: budget,
    area: area,
    estimatedRangeLow: Math.round(budget * 0.7),
    estimatedRangeHigh: Math.round(budget * 0.95),
    perM2Low: Math.round(lowPerM2),
    perM2High: Math.round(highPerM2),
    designVision: $json.project.gardenDesign.designVisionNotes
  }
};
```

---

### 4b. Generate Consultation AI Response (Basic LLM Chain)
**Purpose:** Create personalized consultation invitation

**Prompt:**
```
You are a senior landscape designer at Premium Landscapes.

A customer has requested a custom garden design within their budget rather than specifying materials upfront. Write a warm, consultative email response.

Customer: {{$json.customer.name}}
Budget: £{{$json.project.totalBudget_gbp}}
Garden Size: {{$json.project.totalArea_m2}} m²
Vision: {{$json.project.gardenDesign.designVisionNotes}}

Write 3-4 paragraphs that:
1. Acknowledge their smart approach to budget-based design
2. Explain how you'll create 2-3 custom design concepts within their budget
3. Highlight what's possible at their budget level (be specific and exciting)
4. Invite them to book a free consultation + site visit

Tone: Professional, enthusiastic, consultative. Make them feel excited and confident. Max 200 words.
```

---

### 5b. Send Budget-Based Consultation Email (Email Send Node)
**From:** premiumlandscapesuk@gmail.com  
**To:** `{{$json.customer.email}}`  
**Subject:** `Let's Design Your Dream Garden Within £{{$json.project.totalBudget_gbp}}! 🌿`

**HTML Body:**
```html
<div style="font-family:Inter,Arial,sans-serif;line-height:1.6;color:#0b2e4c;">
  <p>Hi {{$json.customer.name}},</p>
  
  <p>Thank you for your garden redesign request! We love that you're giving us the creative freedom to design within your <strong>£{{$json.project.totalBudget_gbp}} budget</strong> – this is often the best way to maximize value and create something truly special.</p>
  
  {{$json.aiResponse}}
  
  <h3 style="color:#2563eb;">Your Custom Design Process</h3>
  <ol>
    <li><strong>Free Site Visit (30 mins)</strong> – We'll photograph, measure, and discuss your vision</li>
    <li><strong>Design Concepts</strong> – We'll create 2-3 tailored designs within your budget</li>
    <li><strong>Review Together</strong> – Refine your favorite design to perfection</li>
    <li><strong>Detailed Quote</strong> – Final pricing based on your chosen design</li>
  </ol>
  
  <h3 style="color:#2563eb;">What's Possible at Your Budget?</h3>
  <p>With £{{$json.project.totalBudget_gbp}} for {{$json.project.totalArea_m2}} m², we can realistically include:</p>
  <ul>
    <li>Premium patio or decking area (20-30 m²)</li>
    <li>Quality artificial turf or natural lawn</li>
    <li>Feature lighting package</li>
    <li>Raised beds or planting borders</li>
    <li>Professional finish throughout</li>
  </ul>
  
  <p><strong>Ready to see your options?</strong></p>
  
  <p><a href="https://calendly.com/premium-landscapes/consultation" style="display:inline-block;background:#2563eb;color:white;padding:14px 28px;text-decoration:none;border-radius:8px;margin-top:10px;font-weight:600;">📅 Book Free Consultation</a></p>
  
  <p>Or call/text us: <a href="tel:07444887813" style="color:#2563eb;font-weight:600;">07444 887813</a></p>
  
  <p>We typically respond within 4 hours and can often schedule visits within 48 hours.</p>
  
  <p>Excited to create your dream garden!<br>
  <strong>The Premium Landscapes Team</strong></p>
  
  <hr style="margin:30px 0;border:none;border-top:1px solid #e5e7eb;">
  <p style="font-size:12px;color:#6b7280;">
    Premium Landscapes | 07444 887813 | info@premium-landscapes.co.uk<br>
    Serving Midlands & Home Counties
  </p>
</div>
```

**No PDF attached** for budget-based mode – this is a consultation invitation

---

## Merge Paths (Both Routes Continue Here)

### 8. Log to Google Sheets (Google Sheets Node)
**Operation:** Append Row  
**Sheet:** "Full Redesign Quotes Log"  
**Document ID:** `1GIlzFrvqkdYGYQotkKaOox4m6x2qrqvLk0X6xMYJg7s` (or create new)

**Columns:**
```javascript
{
  "Timestamp": "{{$now}}",
  "Customer Name": "{{$json.customer.name}}",
  "Email": "{{$json.customer.email}}",
  "Phone": "{{$json.customer.phone}}",
  "Postcode": "{{$json.customer.postcode}}",
  "Budget": "{{$json.project.totalBudget_gbp}}",
  "Area (m²)": "{{$json.project.totalArea_m2}}",
  "Mode": "{{$json.project.gardenDesign.budgetBasedDesign ? 'Budget-Based' : 'Materials Specified'}}",
  "Material Count": "{{$json.project.gardenDesign.totalMaterialCount}}",
  "Quote Total": "{{$json.pricing.total || 'Consultation'}}",
  "Design Vision": "{{$json.project.gardenDesign.designVisionNotes}}",
  "Status": "Sent"
}
```

---

### 9. Respond to Webhook (Respond to Webhook Node)
**Purpose:** Send success response back to website

**Response:**
```javascript
{
  "success": true,
  "message": "Quote processed successfully",
  "customer": "{{$json.customer.name}}",
  "email": "{{$json.customer.email}}",
  "mode": "{{$json.project.gardenDesign.budgetBasedDesign ? 'budget-based' : 'materials'}}",
  "total": "{{$json.pricing.total || 'Consultation requested'}}"
}
```

---

## Error Handling

### Error Trigger Node
**Purpose:** Catch all workflow errors

### Send Error Alert (Email Send Node)
**To:** premiumlandscapesuk@gmail.com  
**Subject:** `⚠️ Full Redesign Workflow Error – {{$json.error.lastNodeExecuted}}`  
**Body:** Include execution ID, error message, node name, timestamp

---

## Key Differences from Standard Workflow

| Aspect | Standard Quote | Full Redesign |
|--------|---------------|---------------|
| **Webhook Path** | `/premium-landscapes-quote` | `/premium-landscapes-full-redesign` |
| **Pricing** | Simple per-product rates | Material × Quality × Area |
| **Products** | Array of individual products | Categorized materials object |
| **Dual Mode** | No | Yes (budget vs materials) |
| **Email** | Single template | Two templates (quote vs consultation) |
| **PDF** | Always attached | Only for materials mode |
| **Design Fee** | N/A | £850 fixed |

---

## Testing Payloads

### Test 1: Material-Specified Mode
```json
{
  "customer": {"name": "Test User", "email": "test@example.com", "phone": "07444887813", "postcode": "LE19 1WA"},
  "project": {
    "type": "full_garden_redesign",
    "totalArea_m2": 80,
    "totalBudget_gbp": 18000,
    "gardenDesign": {
      "budgetBasedDesign": false,
      "categories": {
        "paving": [{"material": "porcelain_tiles", "displayName": "Porcelain Tiles", "quality": "premium", "area_m2": 30}],
        "lawn": [{"material": "artificial_turf", "displayName": "Artificial Turf", "quality": "standard", "area_m2": 40}]
      },
      "totalMaterialCount": 2,
      "designVisionNotes": "Modern, low maintenance",
      "materials": [...]
    }
  }
}
```

### Test 2: Budget-Based Mode
```json
{
  "customer": {"name": "Budget Test", "email": "budget@example.com", "phone": "07444887813", "postcode": "LE19 1WA"},
  "project": {
    "type": "full_garden_redesign",
    "totalArea_m2": 100,
    "totalBudget_gbp": 25000,
    "gardenDesign": {
      "budgetBasedDesign": true,
      "categories": {},
      "totalMaterialCount": 0,
      "designVisionNotes": "Modern minimalist, low maintenance, pet-friendly",
      "materials": []
    }
  }
}
```

---

## Required Credentials
- SMTP (Gmail): `premiumlandscapesuk@gmail.com`
- Google Sheets API: Access to quotes log spreadsheet
- CloudConvert API: For PDF generation
- OpenAI API: For AI summaries (GPT-4o-mini)

---

## Implementation Instructions for n8n

1. Import my existing "Premium Landscapes - Instant Quote" workflow as reference
2. Duplicate it and rename to "Premium Landscapes - Full Garden Redesign"
3. Change webhook path to `premium-landscapes-full-redesign`
4. Replace "Validate Input" function with new structure for `gardenDesign` object
5. Add IF node after validation to check `budgetBasedDesign` flag
6. Create TWO parallel branches:
   - **Branch A:** Material pricing → PDF → Quote email
   - **Branch B:** Budget analysis → Consultation email (no PDF)
7. Both branches merge at Google Sheets logging
8. Update pricing function with material rates + quality multipliers
9. Update PDF template to show categorized materials
10. Create two email templates
11. Test with both payload types

**Build this workflow following the exact node structure above, using my existing workflow's styling and error handling patterns.**
