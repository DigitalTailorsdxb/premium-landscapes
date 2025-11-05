# Full Garden Redesign Feature - Implementation Guide

## Overview
The Enhanced Step 2 provides a comprehensive material selector when "Full Redesign" is selected in Step 1, allowing users to select multiple materials with detailed specifications for accurate pricing.

---

## User Flow

### Step 1: Select "Full Redesign"
User clicks the "Full Redesign" card in Step 1 → Proceeds to Step 2

### Step 2: Material Selection (Full Redesign Mode)
Instead of standard product detail fields, users see **5 collapsible categories**:

#### 1. 🏗️ Paving & Hard Landscaping (Blue)
- Porcelain Tiles
- Natural Stone  
- Resin Bound
- Gravel
- Block Paving
- Concrete

#### 2. 🌱 Lawn & Planting (Green)
- Artificial Turf
- Natural Lawn
- Raised Beds
- Feature Trees
- Flower Beds

#### 3. 🏠 Structures (Amber)
- Decking
- Pergola
- Gazebo
- Garden Room
- Storage Shed
- Summer House

#### 4. ✨ Features (Purple)
- Outdoor Lighting
- Water Feature
- Fire Pit
- Outdoor Kitchen
- Seating Area
- BBQ Area

#### 5. 🚧 Boundaries (Slate)
- Fencing
- Walls
- Hedging
- Gates

---

## Material Detail Modal

When a user clicks any material card, a modal opens collecting:

**Quality Level** (Required):
- ○ Standard (Budget-friendly)
- ○ Premium (High quality)
- ○ Luxury (Top-tier)

**Area/Quantity** (Required):
- Number input (m²)
- Example: 25

**Style/Pattern** (Optional):
- Text input
- Example: "Wood-effect", "Contemporary grey"

**Additional Notes** (Optional):
- Textarea
- Example: "Prefer light colors to match existing patio"

---

## Selected Materials Summary

After saving materials, a summary panel appears showing:

```
✅ Selected Materials

Porcelain Tiles
premium quality • 45m²
[Remove ×]

Artificial Turf  
luxury quality • 60m²
[Remove ×]

Composite Decking
premium quality • 20m²
[Remove ×]
```

**Design Vision & Special Requirements** textarea at bottom for overall notes.

---

## Data Structure Sent to n8n Webhook

When "Full Redesign" is selected with materials, the payload includes:

```json
{
  "customer": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "07444887813",
    "postcode": "LE3 5RT",
    "city": "Leicester",
    "street": "University Road",
    "houseNumber": "42",
    "address": "42, University Road, Leicester, LE3 5RT, UK"
  },
  "project": {
    "title": "Complete Garden Redesign Installation",
    "type": "full_garden_redesign",
    "totalArea_m2": 100,
    "totalBudget_gbp": 25000,
    "layoutType": "standard",
    "sunlight": "partial sun",
    "stylePreference": "contemporary",
    "maintenanceLevel": "low maintenance",
    "siteConditions": {
      "access": "standard access",
      "soilType": "loam",
      "drainage": "good"
    },
    "products": [...],
    "extras": {...},
    "notes": "Website quote request",
    
    "gardenDesign": {
      "categories": {
        "paving": [
          {
            "material": "porcelain_tiles",
            "displayName": "Porcelain Tiles",
            "quality": "premium",
            "area_m2": 45,
            "style": "Wood-effect oak",
            "notes": "Light color to match house"
          }
        ],
        "lawn": [
          {
            "material": "artificial_turf",
            "displayName": "Artificial Turf",
            "quality": "luxury",
            "area_m2": 60,
            "style": "35mm pile height",
            "notes": "Pet-friendly, natural look"
          }
        ],
        "structures": [
          {
            "material": "decking",
            "displayName": "Decking",
            "quality": "premium",
            "area_m2": 20,
            "style": "Composite grey",
            "notes": "Low maintenance preferred"
          }
        ]
      },
      "totalMaterialCount": 3,
      "designVisionNotes": "Modern minimalist garden, low maintenance, south-facing, existing oak tree to preserve",
      "materials": [
        // Flat list of all materials for easy iteration
        {...},
        {...},
        {...}
      ]
    }
  }
}
```

---

## n8n Workflow Processing

Your n8n workflow can now:

1. **Detect Full Redesign** via `project.type === 'full_garden_redesign'`
2. **Access Materials** via `project.gardenDesign.materials[]`
3. **Loop Through Categories** via `project.gardenDesign.categories.paving`, `.lawn`, etc.
4. **Calculate Pricing** using:
   - `material` → Look up base price from pricing sheet
   - `quality` → Apply multiplier (standard: 1.0, premium: 1.3, luxury: 1.6)
   - `area_m2` → Multiply by price per m²
5. **Generate Quote PDF** with itemized breakdown by category
6. **Include Design Notes** from `designVisionNotes` in customer communication

---

## Testing Checklist

- [ ] Select "Full Redesign" in Step 1
- [ ] Verify Step 2 shows material categories (not standard product fields)
- [ ] Click category header → Expands/collapses with chevron rotation
- [ ] Click material card → Modal opens with title "Porcelain Tiles"
- [ ] Select quality level → Button highlights with blue border
- [ ] Enter area (e.g., 25) → Required field validation
- [ ] Enter style (optional) → Accepts text
- [ ] Click Save → Modal closes, card highlights blue
- [ ] Verify summary panel shows selected material with details
- [ ] Click Remove (×) → Material disappears, card unhighlights
- [ ] Enter Design Vision notes → Saves to payload
- [ ] Complete Steps 3-5 → Submit quote
- [ ] Check browser console → See `project.gardenDesign` object logged
- [ ] Verify n8n webhook receives full payload with material data

---

## Key Benefits

✅ **Structured Data Collection** - Each material captured with quality, area, style, notes  
✅ **Accurate Pricing** - Quality levels allow tiered pricing (standard/premium/luxury)  
✅ **Category Organization** - Groups materials for easy processing and PDF generation  
✅ **Design Context** - Vision notes provide overall design intent  
✅ **Flexible** - Users can mix materials from different categories  
✅ **Reusable** - Build pricing sheets in Google Sheets/Airtable by material + quality  

---

## Next Steps

1. **Build n8n Workflow** to process `project.gardenDesign` data
2. **Create Pricing Sheet** with columns: material, quality, price_per_m2, installation_cost
3. **Design PDF Template** showing materials grouped by category with subtotals
4. **Test End-to-End** from form submission → email delivery

---

## Console Logging

When testing, watch for these console messages:

```
🔄 updateStep2Mode called - isFullRedesign: true
🔧 Initializing material cards...
✅ Material cards initialized
🎨 Full Redesign mode activated
✅ Material saved: {category: "paving", material: "porcelain_tiles", ...}
🎨 Full Garden Design data included: {categories: {...}, totalMaterialCount: 3, ...}
```

---

**Status:** ✅ Feature complete and ready for testing  
**Date:** November 5, 2025  
**Version:** 1.0
