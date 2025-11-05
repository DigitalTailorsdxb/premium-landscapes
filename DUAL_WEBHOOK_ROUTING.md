# Dual Webhook Routing - Separate Workflows for Quote Types

## Overview
The quote system now **automatically routes** to different n8n webhook URLs based on quote type, enabling you to build completely separate workflows with different pricing logic, PDF templates, and automation for:
- **Standard Quotes** (Individual Products)
- **Full Garden Redesign Quotes**

---

## 🔧 Configuration

### Webhook URLs in `scripts/config.js`

```javascript
webhooks: {
    // Standard quote workflow (Patio, Decking, Turf, Driveway, Fencing, Lighting, Other)
    quote: "https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-quote",
    
    // Full garden redesign workflow (comprehensive material selector)
    quoteFullRedesign: "https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-full-redesign"
}
```

---

## 🎯 Automatic Routing Logic

The system checks `project.type` in the webhook payload and routes accordingly:

### Standard Quote → `webhooks.quote`
**Triggered when:** User selects individual products (Patio, Decking, Turf, etc.)

**Payload structure:**
```json
{
  "customer": { ... },
  "project": {
    "type": "individual_products",
    "products": [
      {
        "productId": "patio",
        "displayName": "Patio Installation",
        "material": "Porcelain tiles",
        "area_m2": 30,
        "unitType": "m²"
      }
    ],
    "totalArea_m2": 30,
    "totalBudget_gbp": 8000
  }
}
```

**Console output:**
```
🎯 Quote Type: INDIVIDUAL PRODUCTS
🔗 Routing to: Standard Quote Workflow
📤 SENDING TO N8N: https://...webhook/premium-landscapes-quote
```

---

### Full Redesign → `webhooks.quoteFullRedesign`
**Triggered when:** User selects "Full Redesign" feature

**Payload structure:**
```json
{
  "customer": { ... },
  "project": {
    "type": "full_garden_redesign",
    "title": "Complete Garden Redesign Installation",
    "totalArea_m2": 100,
    "totalBudget_gbp": 25000,
    
    "gardenDesign": {
      "budgetBasedDesign": false,
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
      "designVisionNotes": "Modern minimalist, low maintenance garden...",
      "materials": [...]  // Flat list for iteration
    }
  }
}
```

#### Budget-Based Design Mode
When a customer checks **"Not sure what you want? Let us design within your budget!"**, the payload includes:
```json
{
  "project": {
    "gardenDesign": {
      "budgetBasedDesign": true,  // Customer wants you to design based on budget
      "categories": {},  // May be empty if no materials selected
      "totalMaterialCount": 0,
      "designVisionNotes": "Modern style, pet-friendly, low maintenance required..."
    }
  }
}
```

**Key difference:** When `budgetBasedDesign: true`, customers may skip material selection entirely and rely on you to create a design proposal within their stated budget. The `designVisionNotes` field becomes critical for understanding their requirements.

**Console output:**
```
🎯 Quote Type: FULL GARDEN REDESIGN
🔗 Routing to: Full Redesign Workflow
📤 SENDING TO N8N: https://...webhook/premium-landscapes-full-redesign
```

---

## 🛠️ Setting Up Your n8n Workflows

### Workflow 1: Standard Quotes
**Webhook URL:** `/webhook/premium-landscapes-quote`

**Purpose:** Handle individual product quotes with simple pricing

**Steps:**
1. **Webhook Trigger** → Receive payload
2. **Filter Node** → Check `project.type === "individual_products"`
3. **Loop Products** → Iterate through `project.products[]`
4. **Lookup Pricing** → Google Sheets lookup by `productId`
5. **Calculate Total** → Multiply `area_m2 × price_per_m2`
6. **Generate PDF** → Itemized breakdown by product
7. **Send Email** → Quote delivered to customer

---

### Workflow 2: Full Garden Redesign
**Webhook URL:** `/webhook/premium-landscapes-full-redesign`

**Purpose:** Handle complex multi-material garden designs with detailed pricing

**Steps:**
1. **Webhook Trigger** → Receive payload
2. **Filter Node** → Check `project.type === "full_garden_redesign"`
3. **Check Budget-Based Mode** → If `project.gardenDesign.budgetBasedDesign === true`:
   - **Budget-Only Path:** Customer wants you to design within budget
   - Focus on `project.totalBudget_gbp` and `designVisionNotes`
   - Create custom design proposal
   - Send consultation email offering design service
4. **Materials-Specified Path** → If materials are selected:
   - Extract Materials → Access `project.gardenDesign.materials[]`
   - Loop Materials → For each material:
     - Lookup base price (e.g., porcelain_tiles = £65/m²)
     - Apply quality multiplier:
       - Standard: × 1.0
       - Premium: × 1.3
       - Luxury: × 1.6
     - Calculate: `base_price × quality × area_m2`
   - Group by Category → Use `project.gardenDesign.categories`
5. **Add Design Consultation** → Fixed fee for full redesign
6. **Generate PDF** → Grouped by category with design vision notes
7. **Send Email** → Comprehensive design quote or consultation proposal

---

## 📊 Comparison

| Feature | Standard Quote | Full Redesign |
|---------|----------------|---------------|
| **Webhook** | `webhooks.quote` | `webhooks.quoteFullRedesign` |
| **Data Structure** | `products[]` array | `gardenDesign.categories{}` object |
| **Pricing Logic** | Simple product × area | Material × quality × area + design fee |
| **PDF Template** | Itemized list | Grouped by category + vision notes |
| **Typical Projects** | Single feature installs | Complete garden transformations |

---

## 🧪 Testing Your Setup

### Test Standard Quote:
1. Go to `/quote.html`
2. Select "Patio Installation"
3. Click Continue
4. Fill material: "Porcelain tiles", area: 30 m²
5. Complete Steps 3-5
6. Submit → Check console for:
   ```
   🎯 Quote Type: INDIVIDUAL PRODUCTS
   📤 SENDING TO N8N: .../premium-landscapes-quote
   ```

### Test Full Redesign Quote:
1. Go to `/quote.html`
2. Select "Full Garden Redesign"
3. Click Continue
4. Add materials (e.g., Porcelain Tiles, Artificial Turf, Decking)
5. Set quality levels and areas
6. Complete Steps 3-5
7. Submit → Check console for:
   ```
   🎯 Quote Type: FULL GARDEN REDESIGN
   📤 SENDING TO N8N: .../premium-landscapes-full-redesign
   ```

---

## 🔍 Debugging

### Check Routing:
Open browser console (F12) and look for routing messages:
```javascript
🎯 Quote Type: FULL GARDEN REDESIGN
🔗 Routing to: Full Redesign Workflow
📤 SENDING TO N8N: https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-full-redesign
```

### Verify Payload:
The console logs the complete payload structure:
```javascript
📦 FULL PAYLOAD: { customer: {...}, project: {...} }
```

### Demo Mode:
If webhook URLs contain placeholders (`your-`), the system enters demo mode:
```
⚠️ Webhook URL not configured. Using demo mode.
```

---

## 🎨 Customization

### Change Webhook URLs:
Edit `scripts/config.js`:
```javascript
webhooks: {
    quote: "https://YOUR-N8N-INSTANCE/webhook/standard-quotes",
    quoteFullRedesign: "https://YOUR-N8N-INSTANCE/webhook/full-redesign"
}
```

### Use Same Workflow (Not Recommended):
If you want both quote types to go to the same workflow, set them to the same URL:
```javascript
webhooks: {
    quote: "https://your-n8n.app/webhook/all-quotes",
    quoteFullRedesign: "https://your-n8n.app/webhook/all-quotes"  // Same URL
}
```
Then use a **Switch node** in n8n to route by `project.type`.

---

## ✅ Benefits of Separate Workflows

1. **Different Pricing Logic** - Full redesigns can use complex material-based calculations
2. **Different PDF Templates** - Full redesigns can show grouped categories, standard shows simple list
3. **Different Email Copy** - Customize messaging per quote type
4. **Easier Debugging** - Isolate issues to specific quote types
5. **Independent Scaling** - Adjust workflows without affecting the other
6. **Better Analytics** - Track conversion rates separately

---

## 📝 Summary

✅ Frontend automatically detects quote type  
✅ Routes to correct webhook URL  
✅ Clear console logging for debugging  
✅ Enables completely separate n8n workflows  
✅ Production-ready with null-safe error handling  

**Next Step:** Build your two n8n workflows using the payload structures above!
