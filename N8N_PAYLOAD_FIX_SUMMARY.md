# n8n Payload Fix Summary

## ✅ Issues Fixed (Oct 31, 2025)

### 1. **Prevented Undefined Values**
**Problem:** `email` and `postcode` could be `undefined`, breaking n8n validation

**Fix:** Added fallback to empty strings
```javascript
customer: {
    name: quoteData.name || 'Unknown',
    email: quoteData.email || '',        // ✅ Now has fallback
    phone: quoteData.phone || '',
    postcode: quoteData.postcode || '',  // ✅ Now has fallback
    city: quoteData.city || '',
    street: quoteData.street || '',
    address: buildFullAddress()
}
```

### 2. **Fixed Address Data Capture**
**Problem:** Google Maps autocomplete filled `city` and `street` inputs but values weren't saved to `quoteData`

**Fix:** Added capture when moving from Step 4 → Step 5
```javascript
// In nextStep() function - Step 4 validation:
quoteData.postcode = postcodeInput.value.trim();
quoteData.city = cityInput.value.trim();      // ✅ Now captured
quoteData.street = streetInput.value.trim();  // ✅ Now captured
```

### 3. **Enhanced Console Logging**
Added detailed payload logging for debugging:
```javascript
console.log('📦 PAYLOAD STRUCTURE:');
console.log('  customer:', { name, email, phone, postcode, city, street, address });
console.log('  project.products:', webhookPayload.project.products.length, 'items');
console.log('📦 FULL PAYLOAD:', JSON.stringify(webhookPayload, null, 2));
```

---

## 📤 Current Payload Structure

The website now sends this exact structure to n8n:

```json
{
  "customer": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "07444 887813",
    "postcode": "LE3 5RT",
    "city": "Leicester",
    "street": "42 University Road",
    "address": "42 University Road, Leicester, LE3 5RT, UK"
  },
  "project": {
    "title": "Patio & Lawn Installation",
    "totalArea_m2": 50,
    "totalBudget_gbp": 5000,
    "layoutType": "standard",
    "sunlight": "partial sun",
    "stylePreference": "contemporary",
    "maintenanceLevel": "low maintenance",
    "siteConditions": {
      "access": "standard access",
      "soilType": "loam",
      "drainage": "good"
    },
    "products": [
      {
        "type": "patio",
        "description": "Indian sandstone with edging",
        "material": "indian sandstone",
        "unitType": "m2",
        "area_m2": 30,
        "edging": "standard edging",
        "includeDrainage": true
      },
      {
        "type": "turf",
        "description": "Artificial grass",
        "material": "artificial grass",
        "unitType": "m2",
        "area_m2": 20,
        "includeEdging": true
      }
    ],
    "extras": {
      "pergola": { "include": false },
      "firePit": { "include": false },
      "waterFeature": { "include": false }
    },
    "notes": "Website quote request"
  }
}
```

---

## 🔧 n8n Workflow Updates Needed

### **Validate Input Node**
Your n8n workflow must accept these **new optional fields**:

```javascript
customer.city     // ✅ Optional (can be empty string)
customer.street   // ✅ Optional (can be empty string)
customer.address  // ✅ Enhanced (now includes street, city if available)
```

**Action Required:**
- If using "strict" validation mode → Add `city` and `street` as optional fields
- If using "loose" validation mode → No changes needed (extra fields ignored)

### **Existing Fields Still Work**
These fields are **unchanged** and work exactly as before:
- `customer.name` ✅
- `customer.email` ✅
- `customer.phone` ✅
- `customer.postcode` ✅
- `customer.address` ✅ (just enhanced with more detail)

---

## 🧪 Testing Instructions

1. **Submit a test quote** with full address autocomplete
2. **Check browser console** for detailed payload logs
3. **Check n8n execution logs** to see what was received
4. **Verify no errors** about undefined/null fields

### Expected Console Output:
```
📤 SENDING TO N8N: https://digitaltailorsdxb.app.n8n.cloud/webhook-test/premium-landscapes-quote
📦 PAYLOAD STRUCTURE:
  customer: { name: "John Smith", email: "john@example.com", ... }
  project.products: 2 items
  project.totalArea_m2: 50
  project.totalBudget_gbp: 5000
✅ n8n Response Status: 200
✅ n8n Response OK: true
```

---

## ⚠️ Common n8n Errors After This Update

### Error: "Field 'customer.city' is not defined"
**Fix:** In n8n Validate Input node → Add `city` and `street` as optional fields

### Error: "customer.address is null"
**Fix:** Check that `quoteData.postcode` is being captured in Step 4

### Error: "Cannot read property 'name' of undefined"
**Fix:** Ensure n8n nodes reference `$json.customer.name` not `$json.name`

---

## 📝 Changelog

**Oct 31, 2025:**
- ✅ Added Google Maps autocomplete for UK addresses
- ✅ Fixed city/street data capture
- ✅ Added fallback values for all customer fields
- ✅ Enhanced console logging for debugging
- ✅ Updated payload structure documentation
