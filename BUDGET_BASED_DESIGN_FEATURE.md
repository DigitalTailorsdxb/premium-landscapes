# Budget-Based Design Feature

## Overview
This feature allows customers to request custom garden design proposals based solely on their budget, without needing to specify exact materials. It gives you the creative freedom to design within their price constraints.

---

## 🎯 User Experience

When a customer selects **"Full Garden Redesign"** in Step 1, they now see a prominent option in Step 2:

### The Checkbox
```
┌─────────────────────────────────────────────────────────────┐
│ 💡 Not sure what you want? Let us design within your budget!│
│                                                               │
│ If you know your budget but aren't certain about specific    │
│ materials or features, check this box. We'll create a custom │
│ design proposal tailored to your budget and vision. Just     │
│ tell us your style preferences and requirements below, and   │
│ we'll handle the rest!                                       │
└─────────────────────────────────────────────────────────────┘
```

### What Happens When Checked:
1. ✅ Material selection section dims (becomes optional)
2. ✅ "Design Vision & Requirements" field becomes **required** (asterisk shown)
3. ✅ Description emphasizes importance of vision notes
4. ✅ Customer can skip material selection entirely or add a few preferences

---

## 📦 Data Sent to n8n

### Budget-Only Mode (No Materials Selected)
```json
{
  "customer": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "07444887813",
    "postcode": "LE19 1WA"
  },
  "project": {
    "type": "full_garden_redesign",
    "title": "Complete Garden Redesign Installation",
    "totalArea_m2": 80,
    "totalBudget_gbp": 15000,
    
    "gardenDesign": {
      "budgetBasedDesign": true,  // ← KEY FLAG
      "categories": {},           // Empty - no materials selected
      "totalMaterialCount": 0,
      "designVisionNotes": "Modern minimalist style, low maintenance, pet-friendly, south-facing garden with existing oak tree to preserve",
      "materials": []             // Empty array
    }
  }
}
```

### Budget-Based With Some Materials
Customer can check the box AND add a few material preferences:
```json
{
  "gardenDesign": {
    "budgetBasedDesign": true,  // Still budget-based
    "categories": {
      "paving": [
        {
          "material": "porcelain_tiles",
          "displayName": "Porcelain Tiles",
          "quality": "premium",
          "area_m2": 30,
          "style": "Wood-effect",
          "notes": "Must be non-slip"
        }
      ]
    },
    "totalMaterialCount": 1,
    "designVisionNotes": "Modern style, low maintenance, rest of garden to be designed within budget",
    "materials": [...]
  }
}
```

---

## 🔧 How to Handle in n8n Workflow

### Detection Logic
```javascript
// Check if budget-based design requested
const isBudgetBased = payload.project.gardenDesign.budgetBasedDesign === true;

if (isBudgetBased) {
  // BUDGET-BASED PATH
  // Focus on:
  // - payload.project.totalBudget_gbp
  // - payload.project.gardenDesign.designVisionNotes
  // - Any optional materials they specified
  
  // Response strategy:
  // 1. Send consultation email
  // 2. Offer design service within budget
  // 3. Request site visit or photos
  // 4. Provide 2-3 design concept options
  
} else {
  // MATERIALS-SPECIFIED PATH (existing logic)
  // Calculate based on selected materials
}
```

### Workflow Path Comparison

| Aspect | Budget-Based | Materials-Specified |
|--------|-------------|---------------------|
| **Flag** | `budgetBasedDesign: true` | `budgetBasedDesign: false` |
| **Materials** | 0 or few preferences | Detailed material list |
| **Vision Notes** | **Critical** (customer's only input) | Helpful context |
| **Budget** | **Primary constraint** | Ballpark estimate |
| **Response** | Design consultation offer | Itemized quote |
| **Email Type** | "Let's create your dream garden within £X" | "Here's your detailed quote" |

---

## 💡 Business Value

### For Customers:
- ✅ No need to research materials
- ✅ Reduces decision paralysis
- ✅ Trust you to maximize their budget
- ✅ Simpler, faster quote process

### For Your Business:
- ✅ **More creative freedom** - design optimal solution
- ✅ **Higher margins** - choose materials that fit budget AND profit
- ✅ **Differentiation** - competitors don't offer this
- ✅ **Warmer leads** - customers who trust you to design

---

## 🧪 Testing

### Test Budget-Only Quote:
1. Go to `/quote.html`
2. Select **"Full Garden Redesign"**
3. Click Continue
4. **Check** "Not sure what you want? Let us design within your budget!"
5. **Skip** all material selection (don't click any material cards)
6. Fill **"Design Vision & Requirements"** (required):
   ```
   Modern minimalist style, low maintenance, 
   pet-friendly, existing oak tree to preserve, 
   south-facing garden
   ```
7. Step 3: Select budget **£15,000 - £25,000**
8. Complete Steps 4-5
9. Submit → Open browser console (F12)
10. **Verify payload:**
    ```
    budgetBasedDesign: true
    totalMaterialCount: 0
    designVisionNotes: "Modern minimalist..."
    ```

### Test Budget-Based With Some Materials:
1. Same as above, but:
2. After checking the checkbox, add 1-2 materials (e.g., Porcelain Tiles)
3. Submit → Verify:
   ```
   budgetBasedDesign: true
   totalMaterialCount: 1
   materials: [...]
   ```

---

## 📧 Suggested Email Responses

### Budget-Based Email Template:
```
Subject: Let's Design Your Dream Garden Within £15,000!

Hi John,

Thanks for your garden redesign request! We love your vision of a 
modern, low-maintenance, pet-friendly space.

Rather than a standard quote, we'd like to offer you something better: 
a custom design consultation where we'll create 2-3 tailored design 
concepts optimized for your £15,000 budget.

Here's what happens next:
1. Quick site visit (30 mins) - we'll photograph and measure
2. We'll create design concepts within your budget
3. Review designs together - make tweaks
4. Finalize quote based on chosen design

Book your free consultation: [CALENDAR LINK]

This approach ensures you get the absolute best garden possible 
within your budget!

Best regards,
Premium Landscapes Team
```

### Materials-Specified Email Template:
```
Subject: Your Garden Redesign Quote - £12,000-£15,000

Hi John,

Thanks for your detailed garden redesign request! 

Attached is your comprehensive quote based on:
- Premium porcelain tiles (45m²)
- Artificial turf (30m²)
- Composite decking (20m²)

Total: £12,000 - £15,000
Timeline: 10-12 working days

Ready to proceed? Reply to this email or call 07444 887813.

Best regards,
Premium Landscapes Team
```

---

## ✅ Production Ready

- ✅ Budget-based flag always delivered to n8n
- ✅ Works with zero materials or partial material selection
- ✅ Clear UI feedback (dimmed materials, required vision notes)
- ✅ Null-safe error handling
- ✅ Console logging for debugging
- ✅ Documented in DUAL_WEBHOOK_ROUTING.md
- ✅ Architect-reviewed and approved

---

## 🎨 UI States

| State | Material Section | Vision Notes | Asterisk |
|-------|-----------------|--------------|----------|
| **Checkbox Unchecked** | Full opacity | Optional | Hidden |
| **Checkbox Checked** | Dimmed (0.6 opacity) | **Required** | Visible |

Console output when toggling:
```
💡 Budget-based design mode: ON
💡 Budget-based design mode: OFF
```

---

**Next Step:** Configure your n8n workflow to detect `budgetBasedDesign: true` and send appropriate consultation emails!
