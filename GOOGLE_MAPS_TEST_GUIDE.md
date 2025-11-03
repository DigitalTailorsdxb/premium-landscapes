# Google Maps Address Autocomplete - Test Guide

## ✅ Status: CONNECTED & WORKING

**Console confirms:**
```
✅ Environment config loaded
✅ Google Maps Places API loaded successfully
✅ Google Maps autocomplete initialized successfully
```

---

## 🧪 How to Test the Address Finder

### **Step 1: Open the Quote Page**
Go to: `https://your-replit-url/quote.html`

### **Step 2: Navigate to Step 4**
Complete the form:
1. **Step 1:** Select features (Patio, Decking, etc.)
2. **Step 2:** Add details for each product
3. **Step 3:** Select area and budget
4. **Step 4:** 👈 **THIS IS WHERE THE AUTOCOMPLETE IS!**

### **Step 3: Test the Autocomplete**
In Step 4, you'll see a field labeled **"Postcode or address"**

**Try typing:**
- `42 University Road, Leicester`
- `LE3 5RT`
- `10 Downing Street, London`
- Any UK postcode or street address

**What should happen:**
1. As you type, Google shows a dropdown with address suggestions
2. Click a suggestion
3. **Auto-fills:**
   - City/Town field
   - Street field
   - Postcode field

---

## 🔧 Technical Details

**API Key:** ✅ Configured in environment (`GOOGLE_MAPS_API_KEY`)

**Endpoint:** `/api/config.js` - Successfully serving API key to browser

**Input Field:** `#postcode` - Replaced with autocomplete-enabled input

**Google Maps Libraries:** `places` library loaded

**Country Restriction:** UK only (`componentRestrictions: { country: 'uk' }`)

**Field Types:** `address` - Returns full street addresses

**Data Captured:**
```javascript
- Street: e.g., "42 University Road"
- City: e.g., "Leicester"
- Postcode: e.g., "LE3 5RT"
- Full Address: "42 University Road, Leicester, LE3 5RT, UK"
```

---

## ⚠️ Google Deprecation Notice

The console shows a warning about `google.maps.places.Autocomplete` being deprecated in favor of `PlaceAutocompleteElement`. 

**Current status:**
- ✅ Still works perfectly
- ✅ Will receive bug fixes for major issues
- ⏰ 12 months notice before discontinuation
- 📅 Migration recommended but not urgent

**When to migrate:**
- You have time to migrate later
- Current implementation is stable
- Google will provide 12 months notice before full deprecation

---

## 🎯 What Gets Sent to n8n

When user submits the quote, the webhook receives:

```json
{
  "customer": {
    "postcode": "LE3 5RT",
    "city": "Leicester",
    "street": "42 University Road",
    "address": "42 University Road, Leicester, LE3 5RT, UK"
  }
}
```

**All fields have fallback values** (empty string `''`) - no undefined/null errors! ✅

---

## 🐛 Troubleshooting

**If autocomplete doesn't appear:**

1. **Check browser console** (F12) - Should see:
   ```
   ✅ Google Maps Places API loaded successfully
   ✅ Google Maps autocomplete initialized successfully
   ```

2. **Make sure you're on Step 4** - The autocomplete only appears in the Location step

3. **Clear browser cache** - Sometimes old cached scripts interfere

4. **Check API key quota** - Free tier allows ~11,700 lookups/month

5. **Test with a common address** - Try "10 Downing Street, London SW1A"

---

## 💰 API Costs

**Current plan:** Google Maps free tier
- **Monthly credit:** $200/month
- **Cost per lookup:** ~$0.017
- **Lookups available:** ~11,700/month
- **Current usage:** Check Google Cloud Console

**Upgrade if needed:**
- Only charged after $200 credit is used
- Pay-as-you-go pricing applies
- Monitor usage in Google Cloud Console

---

## ✅ Next Steps

1. **Test the autocomplete** by filling out the quote form to Step 4
2. **Submit a test quote** and check n8n receives the full address data
3. **Monitor API usage** in Google Cloud Console
4. **Consider migration** to `PlaceAutocompleteElement` in future (12+ months timeline)
