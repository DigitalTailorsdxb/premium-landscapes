# Google Maps Autocomplete Implementation - Nov 5, 2025

## ✅ Implementation Complete

Google Maps Places Autocomplete has been successfully re-implemented as an **optional helper** above the manual address entry fields. This provides the best of both worlds: smart autocomplete for convenience + reliable manual entry as backup.

---

## 🎯 Design Approach

### **Key Principle: Autocomplete as Helper, Not Requirement**

```
┌─────────────────────────────────────────┐
│ 🔍 Quick Address Search (Optional)      │ ← Autocomplete search box
│   "Start typing your address..."       │   Shows Google dropdown
└─────────────────────────────────────────┘
             ↓ Auto-fills ↓
┌─────────────────────────────────────────┐
│ House Number: 42                        │ ← Always visible & editable
│ Street: University Road                 │ ← Users can override
│ City: Leicester                         │ ← Manual fallback works
│ Postcode: LE3 5RT                       │
└─────────────────────────────────────────┘
```

**Benefits:**
- ✅ Autocomplete helps users find addresses quickly
- ✅ Manual fields always work (no dependencies)
- ✅ Users can edit/override autocomplete data
- ✅ No DOM manipulation = crash-proof
- ✅ Graceful degradation if API fails

---

## 🔧 Technical Implementation

### **1. HTML Structure (quote.html)**

Added separate autocomplete search box in Step 4:

```html
<!-- Google Maps Autocomplete Search (Optional Helper) -->
<div class="mb-6 bg-blue-50 border-2 border-blue-200 rounded-xl p-4">
    <label class="block text-gray-700 font-semibold mb-2">
        <i class="fas fa-search-location text-blue-600 mr-2"></i>Quick Address Search (Optional)
    </label>
    <input 
        type="text" 
        id="addressAutocomplete" 
        class="w-full px-5 py-4 rounded-xl border-2 border-blue-300 focus:outline-none focus:border-accent transition-colors text-base bg-white"
        placeholder="Start typing your address... e.g., 42 University Road"
    >
    <p class="text-xs text-gray-600 mt-2">
        <i class="fas fa-info-circle"></i> Start typing to search, or fill in the fields below manually
    </p>
</div>

<!-- Manual Address Entry (Always Visible & Editable) -->
<div class="mb-6">
    <label>House Number / Name</label>
    <input type="text" id="houseNumber" ... >
</div>
<div class="mb-6">
    <label>Street Name *</label>
    <input type="text" id="street" required ... >
</div>
<div class="mb-6">
    <label>City / Town *</label>
    <input type="text" id="city" required ... >
</div>
<div class="mb-6">
    <label>Postcode *</label>
    <input type="text" id="postcode" required ... >
</div>
```

### **2. API Loading (quote.html)**

Dynamic Google Maps API loader with retry mechanism:

```javascript
// Load Google Maps API dynamically with API key from config
// Wait for config.js to load first
const loadGoogleMaps = () => {
    if (window.ENV_GOOGLE_MAPS_API_KEY) {
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${window.ENV_GOOGLE_MAPS_API_KEY}&libraries=places&loading=async`;
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
        console.log('🗺️ Google Maps API script added with key');
    } else {
        console.warn('⚠️ Google Maps API key not configured - autocomplete disabled');
    }
};

// Retry mechanism to wait for config.js to load
let retryCount = 0;
const checkAndLoad = () => {
    if (window.ENV_GOOGLE_MAPS_API_KEY) {
        loadGoogleMaps();
    } else if (retryCount < 20) {
        retryCount++;
        setTimeout(checkAndLoad, 100);
    } else {
        console.warn('⚠️ Google Maps API key not found after retries - autocomplete disabled');
    }
};
```

**Why this approach:**
- Waits for `config.js` to load API key first
- Retries up to 20 times (2 seconds total)
- Gracefully degrades if API key unavailable
- No blocking = page loads fast

### **3. Autocomplete Initialization (quote-engine.js)**

Safe lazy-loading initialization:

```javascript
let autocompleteInitialized = false;
let autocomplete = null;

function initializePostcodeLookup() {
    console.log('✅ Address form ready - manual + autocomplete mode');
    
    const autocompleteInput = document.getElementById('addressAutocomplete');
    if (!autocompleteInput) return;
    
    // Only load Google Maps when user focuses on autocomplete
    autocompleteInput.addEventListener('focus', function() {
        if (!autocompleteInitialized) {
            loadGoogleMapsAutocomplete();
        }
    });
}

async function loadGoogleMapsAutocomplete() {
    if (autocompleteInitialized) return;
    
    try {
        const { Autocomplete } = await google.maps.importLibrary('places');
        
        const autocompleteInput = document.getElementById('addressAutocomplete');
        
        autocomplete = new Autocomplete(autocompleteInput, {
            componentRestrictions: { country: 'gb' },
            fields: ['address_components', 'formatted_address'],
            types: ['address']
        });
        
        autocomplete.addListener('place_changed', handlePlaceSelection);
        
        autocompleteInitialized = true;
        console.log('✅ Google Maps Autocomplete initialized');
        
    } catch (error) {
        console.error('❌ Failed to load Google Maps:', error);
    }
}
```

**Safety features:**
- ✅ Lazy loading (only when user focuses)
- ✅ Initialization guard flag prevents duplicates
- ✅ Modern `importLibrary()` API (not deprecated)
- ✅ Try/catch error handling
- ✅ No DOM replacement

### **4. Place Selection Handler (quote-engine.js)**

Parses Google address and fills manual fields:

```javascript
function handlePlaceSelection() {
    const place = autocomplete.getPlace();
    
    if (!place.address_components) return;
    
    let streetNumber = '';
    let route = '';
    let locality = '';
    let postalTown = '';
    let postalCode = '';
    
    // Parse address components
    place.address_components.forEach(component => {
        const types = component.types;
        
        if (types.includes('street_number')) {
            streetNumber = component.long_name;
        }
        if (types.includes('route')) {
            route = component.long_name;
        }
        if (types.includes('postal_town')) {
            postalTown = component.long_name;
        }
        if (types.includes('locality') && !postalTown) {
            locality = component.long_name;
        }
        if (types.includes('postal_code')) {
            postalCode = component.long_name;
        }
    });
    
    // Fill manual fields (but keep them editable)
    const houseNumberInput = document.getElementById('houseNumber');
    const streetInput = document.getElementById('street');
    const cityInput = document.getElementById('city');
    const postcodeInput = document.getElementById('postcode');
    
    if (houseNumberInput && streetNumber) {
        houseNumberInput.value = streetNumber;
    }
    
    if (streetInput && route) {
        streetInput.value = route;
    }
    
    if (cityInput) {
        cityInput.value = postalTown || locality || '';
    }
    
    if (postcodeInput && postalCode) {
        postcodeInput.value = postalCode;
    }
    
    // Clear autocomplete search box
    const autocompleteInput = document.getElementById('addressAutocomplete');
    if (autocompleteInput) {
        autocompleteInput.value = '';
    }
}
```

**What it does:**
1. Parses Google's `address_components` array
2. Extracts: street_number, route, postal_town, postcode
3. Sets `.value` on manual input fields
4. Fields stay editable (users can override)
5. Clears autocomplete search box

---

## 🚫 Why Previous Implementation Crashed

### **Root Causes Identified:**

1. **DOM Replacement**
   - Code was destroying and recreating input elements
   - Event listeners became dangling references
   - Multiple initializations on same element

2. **Hidden Fields Toggle**
   - Script tried to write to removed/hidden elements
   - DOM nodes didn't exist when code ran
   - Conflicting visibility logic

3. **Deprecated API**
   - Used old `google.maps.places.Autocomplete` constructor
   - Mixed with new `PlaceAutocompleteElement`
   - Double-binding and deprecation warnings

4. **No Initialization Guard**
   - Autocomplete re-initialized on every event
   - Multiple listeners on same element
   - Memory leaks and conflicts

### **How New Implementation Avoids Crashes:**

✅ **Stable DOM** - Manual fields never replaced/removed  
✅ **Autocomplete is separate** - Different input element  
✅ **Single initialization** - Guard flag prevents duplicates  
✅ **Modern API** - Uses `google.maps.importLibrary()`  
✅ **Lazy loading** - Only loads when user focuses  
✅ **No hidden fields** - All fields always visible  

---

## 📤 n8n Payload Structure (Unchanged)

**The autocomplete fills manual fields, and the form still sends the same data structure to n8n:**

```javascript
customer: {
    name: "John Smith",
    email: "john@example.com",
    phone: "07444887813",
    houseNumber: "42",          // From manual field (or autocomplete)
    street: "University Road",  // From manual field (or autocomplete)
    city: "Leicester",          // From manual field (or autocomplete)
    postcode: "LE3 5RT",        // From manual field (or autocomplete)
    address: "42, University Road, Leicester, LE3 5RT, UK"  // Combined
}
```

**No changes to:**
- Field names
- Data structure
- n8n workflow expectations
- PDF generation logic

---

## 🧪 Testing Instructions

### **Test 1: Autocomplete Happy Path**

1. Open quote form: `/quote.html`
2. Complete Steps 1-3 (select products, area, budget)
3. Step 4: Click "Quick Address Search" input
4. Type: `42 Univer...`
5. Google dropdown appears with suggestions
6. Select: "42 University Road, Leicester"
7. **Verify:** All 4 manual fields auto-fill
8. **Verify:** Fields are still editable (try changing house number)
9. Complete Step 5 and submit
10. **Check console:** Payload should show correct address

### **Test 2: Manual Entry (Autocomplete Disabled)**

1. Open quote form
2. Navigate to Step 4
3. **Skip** the autocomplete search box
4. Manually type into fields:
   - House Number: `15`
   - Street: `High Street`
   - City: `Birmingham`
   - Postcode: `B1 1AA`
5. Complete and submit
6. **Check console:** Payload should show manual address

### **Test 3: Override Autocomplete**

1. Use autocomplete to fill address
2. Change house number from `42` to `42A`
3. Change city from `Leicester` to `Leicestershire`
4. Submit form
5. **Check console:** Payload should use edited values (not original autocomplete)

### **Test 4: API Key Missing**

1. Remove `GOOGLE_MAPS_API_KEY` from environment
2. Restart server
3. Open quote form
4. **Verify:** Console shows warning about missing API key
5. **Verify:** Autocomplete search box still visible
6. **Verify:** Manual entry still works perfectly
7. **Expected:** No crashes, form still functional

---

## 🔐 API Key Management

**Environment Variable:**
```bash
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

**Server Injection (server.py):**
```python
api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
config_js = f"""
window.ENV_GOOGLE_MAPS_API_KEY = '{api_key}';
console.log('✅ Environment config loaded');
"""
```

**Frontend Access:**
```javascript
if (window.ENV_GOOGLE_MAPS_API_KEY) {
    // Load Google Maps
}
```

**Pricing:**
- Free tier: $200/month credit
- ~11,700 autocomplete requests/month
- Should be sufficient for demo site

---

## ✅ Status

- ✅ Autocomplete search box added to Step 4
- ✅ Safe initialization with lazy loading
- ✅ Place selection handler fills manual fields
- ✅ Manual fields always editable (users can override)
- ✅ Graceful degradation if API unavailable
- ✅ n8n payload structure unchanged
- ✅ No DOM manipulation = crash-proof
- ✅ Server running with updated code

**Expected behavior:** Smart autocomplete for convenience + reliable manual entry as backup! 🚀
