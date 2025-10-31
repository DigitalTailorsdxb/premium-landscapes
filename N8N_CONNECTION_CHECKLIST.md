# n8n Workflow Connection Checklist

## ✅ Website → n8n Payload Structure (VERIFIED)

### Current Website Setup
The website sends the following structure to n8n:

```javascript
{
  customer: {
    name: string,           // ✅ REQUIRED
    email: string,          // ✅ REQUIRED  
    phone: string,          // ✅ Optional
    postcode: string,       // ✅ REQUIRED
    address: string         // ✅ Generated from postcode
  },
  project: {
    title: string,                    // e.g. "Patio & Decking Installation"
    totalArea_m2: number,            // Total project area
    totalBudget_gbp: number,         // Parsed from "£5k-£10k" → 5000-10000
    layoutType: string,              // Default: "standard"
    sunlight: string,                // Default: "partial sun"
    stylePreference: string,         // Default: "contemporary"
    maintenanceLevel: string,        // Default: "low maintenance"
    siteConditions: {
      access: string,                // Default: "standard access"
      soilType: string,              // Default: "loam"
      drainage: string               // Default: "good"
    },
    products: [                      // ✅ CRITICAL - Used by pricing calculator
      {
        type: string,                // "patio", "decking", "turf", etc.
        description: string,         // User's material/detail input
        material: string,            // Extracted: "indian sandstone", "porcelain", etc.
        unitType: string,            // "m2" or "qty"
        // Type-specific fields:
        area_m2: number,            // For patio/decking/turf (from dedicated input)
        length_m: number,           // For fencing (from dedicated input)
        fittings: number,           // For lighting (from dedicated input)
        edging: string,             // Extracted from description
        includeDrainage: boolean,   // Auto-set for patios/driveways
        raised: boolean,            // Extracted for decking
        steps: number,              // Extracted for decking
        height_m: number            // For fencing (default 1.8m)
      }
    ],
    extras: {
      pergola: { include: boolean },
      firePit: { include: boolean },
      waterFeature: { include: boolean }
    },
    notes: string                    // Additional notes or "Website quote request"
  },
  files: [                           // ✅ Optional - Images/videos
    {
      name: string,
      type: string,
      size: number,
      data: string                   // base64 data URL
    }
  ]
}
```

---

## 📋 n8n Workflow Configuration Checklist

### 1. **Webhook Trigger** 
- [ ] Path: `/premium-landscapes-quote`
- [ ] Method: POST
- [ ] Response Mode: "responseNode"
- [ ] Current URL: `https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-quote`

### 2. **Validate Input Node**
✅ Already configured to expect:
- `customer.name` (required)
- `customer.email` (required)
- `customer.postcode` (required)
- `project.products` array (required)

### 3. **Calculate Pricing1 Node**
✅ Processes products array with:
- Material-based pricing (indian sandstone, porcelain, composite, etc.)
- Area calculations (m² or linear meters)
- Lighting multiplier (1.5x)
- Contingency (5%) + VAT (20%)

**Verify:** Products structure matches:
```javascript
{
  type: "patio",
  material: "indian sandstone", 
  area_m2: 40
}
```

### 4. **Build AI Prompt Node**
✅ Uses:
- `customer.name`
- `project.stylePreference`
- `project.maintenanceLevel`
- `project.products` → builds product list
- `pricing.total`

### 5. **OpenAI Chat Model**
- [ ] Model: `chatgpt-4o-latest`
- [ ] Max Tokens: 1800
- [ ] Temperature: 0.6
- [ ] Credentials: OpenAI API configured

### 6. **Merge AI Summary Node**
✅ Combines:
- Validated customer data
- Pricing breakdown
- AI-generated summary

### 7. **Build PDF HTML Node**
- [ ] **CRITICAL:** Update logo URL to:
  ```
  https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev/static/logo.png
  ```
- [ ] Verify company branding variables
- [ ] Check footer contact details

### 8. **Convert HTML to PDF**
- [ ] PDF Generator API credentials configured
- [ ] Paper size: A4
- [ ] Orientation: Portrait

### 9. **Send Email Node**
- [ ] **TO:** Customer email from `{{$json.customer.email}}`
- [ ] **FROM:** premiumlandscapesuk@gmail.com
- [ ] **SUBJECT:** Verify template
- [ ] **ATTACHMENTS:** PDF attached as "data"
- [ ] SMTP credentials configured

### 10. **Upload PDF to Google Drive**
- [ ] Parent folder ID: `1RO45FjuBGbvFYRp8VXIxMWtuwrDHTDN7`
- [ ] Folder name: "Premium Landscapes/Quotes Archive"
- [ ] Google Drive credentials configured

### 11. **Log Quote to Google Sheets**
- [ ] Sheet ID: `1GIlzFrvqkdYGYQotkKaOox4m6x2qrqvLk0X6xMYJg7s`
- [ ] Sheet name: "Quotes Log"
- [ ] Columns mapped:
  - Timestamp
  - Customer Name → `{{$json.customerName}}`
  - Email → `{{$json.email}}`
  - Phone → `{{$json.phone}}`
  - Postcode → `{{$json.postcode}}`
  - Products → `{{$json.products}}`
  - AI Summary → `{{$json.aiSummary}}`
  - Quote Total (£) → `{{$json.total}}`
  - Drive File URL
  - Status → "Sent"

**⚠️ NOTE:** The Sheet columns reference `$json.customerName` but the merged data has `$json.customer.name`. You may need to update these mappings or add a node to flatten the structure.

### 12. **Respond to Webhook**
✅ Returns:
```javascript
{
  success: true,
  message: "Quote logged and sent successfully",
  customer: "{{$json.customer?.name}}",
  email: "{{$json.customer?.email}}",
  total: "{{$json.pricing?.total}}"
}
```

### 13. **Error Handling**
- [ ] Error Catcher configured
- [ ] Error alerts sent to: premiumlandscapesuk@gmail.com
- [ ] Email includes execution URL and stack trace

---

## 🔧 Required n8n Changes

### **CRITICAL FIXES:**

1. **Google Sheets Column Mappings** (Node: "Log Quote to Google Sheets")
   
   Change FROM → TO:
   ```
   Customer Name: {{$json.customerName}} → {{$json.customer.name}}
   Email: {{$json.email}} → {{$json.customer.email}}
   Phone: {{$json.phone}} → {{$json.customer.phone}}
   Postcode: {{$json.postcode}} → {{$json.customer.postcode}}
   Products: {{$json.products}} → {{$json.project.products | join}}
   Quote Total: {{$json.total}} → {{$json.pricing.total}}
   ```

2. **PDF Logo URL** (Node: "Build PDF HTML")
   
   Set `logoUrl` variable to:
   ```
   https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev/static/logo.png
   ```
   
   **When going live**, update to:
   ```
   https://premium-landscapes.co.uk/static/logo.png
   ```

3. **Email Template** (Node: "Send Email")
   
   Current subject uses incorrect variables. Update to:
   ```
   Subject: Your Detailed Garden Quote for {{$json.customer.name}} – {{$json.project.title}} 🌿
   ```

---

## 🧪 Testing Checklist

### Test Payload Example:
```json
{
  "customer": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "07444887813",
    "postcode": "LE36AA"
  },
  "project": {
    "title": "Patio Installation",
    "totalArea_m2": 40,
    "totalBudget_gbp": 8000,
    "stylePreference": "contemporary",
    "maintenanceLevel": "low maintenance",
    "products": [
      {
        "type": "patio",
        "description": "Indian sandstone patio with edging",
        "material": "indian sandstone",
        "unitType": "m2",
        "area_m2": 40,
        "edging": "standard edging",
        "includeDrainage": true
      }
    ],
    "notes": "Test quote from website"
  }
}
```

### Expected Results:
- ✅ Email sent to `john@example.com` with PDF attachment
- ✅ PDF uploaded to Google Drive
- ✅ Quote logged in Google Sheets
- ✅ Webhook responds with success message
- ✅ AI summary generated and included in PDF

---

## 📊 Workflow Flow Summary

```
Webhook Trigger
    ↓
Validate Input (check required fields)
    ↓
Calculate Pricing1 (process products, calculate total)
    ↓
Build AI Prompt (create personalized summary prompt)
    ↓
Basic LLM Chain (generate AI summary with OpenAI)
    ↓
Merge AI Summary (combine all data)
    ↓
Build PDF HTML (create PDF content)
    ↓
Convert HTML to PDF (generate PDF file)
    ↓
[Split into 2 parallel paths]
    ├─→ Send Email (with PDF attachment)
    │       ↓
    │   Upload PDF to Google Drive
    │       ↓
    │   Merge (wait for both paths)
    │
    └─→ Merge (wait for both paths)
            ↓
        Log Quote to Google Sheets
            ↓
        Respond to Webhook (success message)
```

---

## 🚀 Website Configuration (Already Complete)

✅ Webhook URL configured in `scripts/config.js`:
```javascript
webhooks: {
  quote: "https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-quote"
}
```

✅ Payload structure matches n8n expectations
✅ Product details with dedicated area inputs
✅ Material extraction logic working
✅ Base64 file encoding ready (if needed)

---

## 📝 Next Steps

1. **Import workflow to n8n** (if not already done)
2. **Update the 3 critical fixes** listed above
3. **Test with sample payload** 
4. **Verify email delivery**
5. **Check Google Sheets logging**
6. **Confirm PDF generation with logo**
7. **Enable webhook trigger** (currently disabled)
8. **Test from live website**

---

## 🔗 Quick Links

- **n8n Workflow:** https://digitaltailorsdxb.app.n8n.cloud/
- **Webhook URL:** https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-quote
- **Google Sheets Log:** https://docs.google.com/spreadsheets/d/1GIlzFrvqkdYGYQotkKaOox4m6x2qrqvLk0X6xMYJg7s/edit
- **Google Drive Folder:** https://drive.google.com/drive/folders/1RO45FjuBGbvFYRp8VXIxMWtuwrDHTDN7
- **Website Config:** `scripts/config.js` line 35
- **Payload Builder:** `scripts/quote-engine.js` lines 620-756

---

**Last Updated:** October 30, 2025
**Status:** Ready for n8n configuration and testing
