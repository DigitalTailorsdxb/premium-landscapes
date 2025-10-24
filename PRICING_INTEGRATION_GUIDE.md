# 🧱 Pricing System Integration Guide

## Overview
This guide explains how to connect the Premium Landscapes instant quote system to your Make.com or n8n pricing workflow. The frontend is **fully built and ready** - you just need to connect the backend.

---

## 📊 How The Pricing System Works

### Formula
```
Total = (Material Cost + Labour Cost + Excavation + Waste Removal) × Area × Regional Factor × Overhead Markup
```

### Components
| Component | Description | Source |
|-----------|-------------|--------|
| **Material Costs** | Price per m² (porcelain, decking, turf, etc.) | Your supplier price sheet |
| **Labour Costs** | Installation cost per m² or per hour | Based on crew daily rates |
| **Excavation / Base Prep** | Cost per m³ of soil removal + hardcore, MOT, sand | Added to all hard surfaces |
| **Waste & Skip** | Price per skip or tonne | Postcode-based modifier |
| **Overhead + Margin** | Admin, transport, project management, profit | 25-30% markup |

---

## 🔌 Quick Start: 3-Step Connection

### Step 1: Create Your Pricing Sheet
Create a Google Sheet with this structure:

| Material | Unit | MatCost | LabourCost | Excavation | Waste | RegionFactor |
|----------|------|---------|------------|------------|-------|--------------|
| Porcelain Paving | m² | 65 | 45 | 12 | 8 | 1.05 |
| Artificial Turf | m² | 30 | 20 | 6 | 4 | 1.00 |
| Composite Decking | m² | 80 | 55 | 12 | 6 | 1.10 |
| Fence Panel | metre | 20 | 15 | 0 | 2 | 1.00 |
| Block Paving Driveway | m² | 70 | 50 | 15 | 10 | 1.05 |
| Garden Lighting (per light) | unit | 50 | 30 | 0 | 0 | 1.00 |

**Share the sheet** with your Make.com service account or make it public (read-only).

### Step 2: Create Make.com Workflow
Create a new scenario with these modules:

1. **Webhook (Trigger)** - Receives quote data from website
2. **OpenAI / GPT-4** - Parse free-text descriptions into structured data (optional but recommended)
3. **Google Sheets - Search Rows** - Lookup pricing for each product
4. **Iterator** - Loop through each product
5. **Math Operations** - Calculate totals with formula above
6. **Aggregator** - Combine all line items
7. **Router** - Split workflow:
   - **Branch A:** Generate PDF quote
   - **Branch B:** Send email with quote
   - **Branch C:** Log to Airtable/CRM
   - **Branch D:** Send WhatsApp message (optional)
8. **Webhook Response** - Return pricing data to website

### Step 3: Connect to Website
Open `scripts/config.js` and add your webhook URLs:

```javascript
webhooks: {
    quote: "https://hook.eu2.make.com/YOUR-ACTUAL-WEBHOOK-ID",
    email: "https://hook.eu2.make.com/YOUR-EMAIL-WEBHOOK-ID"
}
```

Then in `scripts/quote-engine.js`, uncomment lines 509-541 to enable live webhook calls.

---

## 📤 Data Sent FROM Website

When a user submits the quote form, the website sends this JSON structure:

```json
{
  "customer": {
    "email": "customer@example.com",
    "phone": "07444887813",
    "postcode": "LE1 2AB"
  },
  "project": {
    "products": [
      {
        "type": "patio",
        "name": "Patio",
        "description": "Porcelain paving, 55sqm, grey contemporary style",
        "area": 75
      },
      {
        "type": "turf",
        "name": "Lawn/Turf",
        "description": "Premium artificial turf for family use, 25sqm",
        "area": 75
      }
    ],
    "additionalNotes": "Need work completed before summer",
    "totalArea": 75,
    "budget": "£10,000-£15,000"
  },
  "files": [
    {
      "name": "garden-photo.jpg",
      "type": "image/jpeg",
      "size": 245678,
      "data": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
    }
  ],
  "options": {
    "aiDesign": true,
    "requestedAIDesign": true
  },
  "metadata": {
    "timestamp": "2025-10-24T14:30:00.000Z",
    "source": "website",
    "formVersion": "2.0",
    "confidence": 85
  }
}
```

---

## 📥 Data Expected BACK to Website

Your Make.com workflow should return this structure:

```json
{
  "success": true,
  "quoteId": "Q-2025-001",
  "breakdown": [
    {
      "description": "Porcelain Patio (55m²)",
      "low": 6600,
      "high": 7500
    },
    {
      "description": "Artificial Turf (25m²)",
      "low": 1750,
      "high": 2100
    },
    {
      "description": "Base Preparation & Excavation",
      "low": 1200,
      "high": 1800
    },
    {
      "description": "Waste Removal (3 skips)",
      "low": 600,
      "high": 900
    }
  ],
  "totalLow": 10150,
  "totalHigh": 12300,
  "confidence": 85,
  "pdfUrl": "https://your-storage.com/quotes/Q-2025-001.pdf",
  "estimatedDays": 5
}
```

---

## 🤖 OpenAI Integration (Recommended)

Use GPT-4 to parse natural language into structured data:

### Input to GPT:
```
User wrote: "Porcelain patio 55 sqm, artificial turf 25 sqm, fencing 25 m"
```

### Prompt Template:
```
Parse this landscaping quote request into structured JSON:

{user_input}

Return JSON with this structure:
{
  "items": [
    {
      "material": "Porcelain Paving",
      "quantity": 55,
      "unit": "m²"
    }
  ]
}
```

### GPT Response:
```json
{
  "items": [
    {
      "material": "Porcelain Paving",
      "quantity": 55,
      "unit": "m²"
    },
    {
      "material": "Artificial Turf",
      "quantity": 25,
      "unit": "m²"
    },
    {
      "material": "Fence Panel",
      "quantity": 25,
      "unit": "metre"
    }
  ]
}
```

---

## 💡 Smart Enhancements

### 1. **AI Area Estimation from Photos**
Use GPT-4 Vision to estimate garden size from uploaded images:

```javascript
// In Make.com: GPT-4 Vision module
prompt: "Estimate the total area of this garden in square metres. Consider visible boundaries, patio areas, and lawn space. Provide a single number."
```

### 2. **Regional Pricing Adjustment**
The config already includes regional modifiers:
- **London/SE:** +15% (`regionalModifiers.SW = 1.15`)
- **Home Counties:** +10% (`regionalModifiers.AL = 1.10`)
- **Midlands:** Baseline (`regionalModifiers.LE = 1.00`)

Extract postcode prefix and apply modifier:
```javascript
// Example: "LE1 2AB" → "LE" → 1.00
// Example: "SW1A 1AA" → "SW" → 1.15
const postcodePrefix = postcode.match(/^[A-Z]+/)[0];
const modifier = brandConfig.pricing.regionalModifiers[postcodePrefix] || 1.00;
```

### 3. **Material Swap Simulation**
Offer alternatives to reduce cost:
```
"Switch from Porcelain (£110/m²) to Indian Sandstone (£85/m²) and save £1,375"
```

### 4. **Confidence Meter**
Already calculated! The `metadata.confidence` score is based on:
- Base: 50%
- +10% for features selected
- +15% for area provided
- +10% for postcode
- +15% for photos uploaded
- +10% for detailed descriptions

---

## 📄 PDF Quote Generation

Use **jsPDF** or Make.com's **PDF module** to generate branded quotes:

### Required Elements:
- ✅ Company logo and branding
- ✅ Quote ID and date
- ✅ Customer details (name, postcode)
- ✅ Itemized breakdown table
- ✅ Total price range (low-high)
- ✅ Confidence score visual indicator
- ✅ Estimated project duration
- ✅ Terms & conditions
- ✅ Call-to-action (WhatsApp, phone)

---

## 📧 Email & WhatsApp Integration

### Email Template:
```
Subject: Your Instant Garden Quote - £{totalLow}-£{totalHigh}

Hi {customerName},

Thank you for using our instant quote system! Based on your requirements, here's your personalized estimate:

🏡 Project Summary:
{products_list}

💰 Price Range: £{totalLow} - £{totalHigh} (inc. VAT)
📊 Confidence Score: {confidence}%
⏱️ Estimated Duration: {estimatedDays} days

📎 Your detailed PDF quote is attached.

Ready to get started? Reply to this email or WhatsApp us at 07444 887813.

Best regards,
Premium Landscapes Team
```

### WhatsApp Template (via 360dialog/Twilio):
```
Hi! Your garden quote is ready 🏡

💰 Estimated Cost: £{totalLow}-£{totalHigh}
📊 Confidence: {confidence}%

View your detailed quote: {pdfUrl}

Questions? Just reply here!
```

---

## 🗄️ CRM Integration (Airtable/Zoho)

Store every quote in your CRM with these fields:

| Field | Type | Source |
|-------|------|--------|
| Quote ID | Text | Auto-generated |
| Customer Email | Email | Form input |
| Customer Phone | Phone | Form input |
| Postcode | Text | Form input |
| Products | Multi-select | Parsed from form |
| Total Low | Currency | Calculated |
| Total High | Currency | Calculated |
| Confidence | Number | Calculated |
| Images | Attachments | Uploaded files |
| PDF Quote | Attachment | Generated PDF |
| Status | Select | New/Contacted/Won/Lost |
| Created | DateTime | Timestamp |

---

## 🧪 Testing Checklist

Before going live, test these scenarios:

- [ ] Submit quote with 1 product (e.g., just patio)
- [ ] Submit quote with multiple products (patio + turf + decking)
- [ ] Test with London postcode (SW1A) - should see +15% price increase
- [ ] Test with Midlands postcode (LE1) - baseline pricing
- [ ] Upload 3 images - should increase confidence score
- [ ] Request AI design - should trigger design workflow
- [ ] Check email delivery with PDF attachment
- [ ] Verify CRM entry created with all fields
- [ ] Test WhatsApp message delivery (optional)
- [ ] Confirm webhook response displays correctly on site

---

## 🚀 Going Live

1. ✅ Set up Google Sheet with pricing data
2. ✅ Build Make.com workflow (or n8n)
3. ✅ Test webhook with sample data
4. ✅ Update `scripts/config.js` with real webhook URLs
5. ✅ Uncomment production code in `scripts/quote-engine.js` (lines 509-541)
6. ✅ Test end-to-end with real quote submission
7. ✅ Monitor first 10 quotes for accuracy
8. ✅ Adjust pricing data based on actual margins

---

## 📞 Support

Questions about the integration? Check the code comments in:
- `scripts/quote-engine.js` - Quote submission logic
- `scripts/config.js` - Configuration and webhook URLs
- `quote.html` - Quote form structure

**Everything is ready to connect - just plug in your webhook URLs!**
