# Fencing Data Structure Fix - Nov 4, 2025

## ✅ Issue Fixed

**Problem:** Fencing product was sending incorrect field names to n8n workflow

**n8n Expected:**
```json
{
  "type": "Fencing",
  "material": "Feather Edge",
  "unitType": "m",
  "length": 20
}
```

**Website Was Sending:**
```json
{
  "type": "fencing",
  "material": "feather edge",
  "unitType": "qty",  ❌ Wrong
  "length_m": 20      ❌ Wrong field name
}
```

---

## 🔧 Fix Applied

Updated `scripts/quote-engine.js` to send correct fencing data structure:

```javascript
// BEFORE (incorrect):
else if (feature === 'fencing') {
    product.length_m = dedicatedArea ? parseInt(dedicatedArea) : 20;
    product.height_m = 1.8;
    product.unitType = 'qty';  // Wrong unit type
}

// AFTER (correct):
else if (feature === 'fencing') {
    product.unitType = 'm';  // ✅ Meters
    product.length = dedicatedArea ? parseInt(dedicatedArea) : 20;  // ✅ Correct field name
    product.height_m = 1.8;
}
```

---

## 📤 New Fencing Payload

When user selects fencing, n8n now receives:

```json
{
  "type": "fencing",
  "description": "20 meters close-board fencing",
  "material": "feather edge",
  "unitType": "m",
  "length": 20,
  "height_m": 1.8
}
```

**All field names match n8n expectations** ✅

---

## 📋 All Product Unit Types

For reference, here's what each product type now sends:

| Product      | unitType | Dimension Field |
|--------------|----------|-----------------|
| Patio        | `m2`     | `area_m2`       |
| Decking      | `m2`     | `area_m2`       |
| Turf/Lawn    | `m2`     | `area_m2`       |
| Driveway     | `m2`     | `area_m2`       |
| **Fencing**  | **`m`**  | **`length`**    |
| Lighting     | `qty`    | `fittings`      |
| Full Redesign| `m2`     | `area_m2`       |

---

## 🧪 Testing

To verify the fix:

1. **Create a test quote with fencing:**
   - Step 1: Select "Fencing"
   - Step 2: Enter "Close-board fencing" with 25 meters
   - Complete the rest of the form
   - Submit

2. **Check browser console:**
   ```
   📦 FULL PAYLOAD:
   {
     "project": {
       "products": [
         {
           "type": "fencing",
           "unitType": "m",
           "length": 25,
           "height_m": 1.8
         }
       ]
     }
   }
   ```

3. **Check n8n execution:**
   - Should no longer return £0 for fencing
   - Pricing calculation should work correctly
   - PDF quote should show proper fencing price

---

## ⚠️ n8n Workflow Update Required

**Your n8n "Calculate Pricing" node** may need updating:

**BEFORE (looking for wrong field):**
```javascript
const length = product.length_m;  // ❌ Won't find this anymore
```

**AFTER (correct field name):**
```javascript
const length = product.length;  // ✅ Correct
```

**Make sure your pricing function uses:**
- `product.length` (not `product.length_m`)
- `product.unitType === 'm'` (not `'qty'`)

---

## ✅ Status

- ✅ Fencing data structure fixed
- ✅ Field name changed: `length_m` → `length`
- ✅ Unit type changed: `qty` → `m`
- ✅ Server restarted with changes
- ✅ Ready for testing

**Expected result:** Fencing quotes should now calculate correctly in n8n! 🚀
