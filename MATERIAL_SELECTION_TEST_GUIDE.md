# Material Selection Test Guide
**Last Updated:** Nov 12, 2025

## ✅ Current Status: ALL WORKING
Your test with 27 materials was successful! All data captured correctly and sent to n8n.

---

## 🧪 Test Scenarios to Verify

### **Scenario 1: Single Material from Each Category**
**Goal:** Verify each category is captured independently

**Steps:**
1. Select "Full redesign" in Step 1
2. In Step 2, select ONE material from each category:
   - Paving: Porcelain Tiles (10m², Standard)
   - Lawn: Artificial Turf (15m², Premium)
   - Structures: Decking (20m², Luxury)
   - Features: Outdoor Lighting (5m², Standard)
   - Boundaries: Fencing (10m², Premium)
3. Complete the form and submit

**Expected Output in Console:**
```javascript
project.gardenDesign.categories: {
  paving: [1 material],
  lawn: [1 material],
  structures: [1 material],
  features: [1 material],
  boundaries: [1 material]
}
```

---

### **Scenario 2: Multiple Materials from Same Category**
**Goal:** Verify multiple selections within one category

**Steps:**
1. Select ONLY paving materials:
   - Porcelain Tiles (20m², Standard)
   - Natural Stone (15m², Premium)
   - Resin Bound (10m², Luxury)
2. Complete the form

**Expected Output:**
```javascript
project.gardenDesign.categories: {
  paving: [3 materials]
}
```

---

### **Scenario 3: Extras Auto-Detection**
**Goal:** Verify pergola, fire pit, water feature auto-populate extras object

**Steps:**
1. Select these specific materials:
   - Pergola (from Structures)
   - Fire Pit (from Features)
   - Water Feature (from Features)
2. Complete the form

**Expected Output:**
```javascript
project.extras: {
  pergola: { include: true },
  firePit: { include: true },
  waterFeature: { include: true }
}
```

---

### **Scenario 4: Budget-Based Design Mode**
**Goal:** Verify budget-based mode sends empty categories

**Steps:**
1. Select "Full redesign"
2. Check "I'm not sure - design within my budget"
3. Enter budget and design vision notes
4. **Do NOT select any materials**
5. Complete the form

**Expected Output:**
```javascript
project.gardenDesign: {
  budgetBasedDesign: true,
  categories: {}
}
```

---

### **Scenario 5: Quality Level Variations**
**Goal:** Verify all quality levels (Standard, Premium, Luxury) are captured

**Steps:**
1. Select 3 different materials with different qualities:
   - Natural Stone (Standard)
   - Decking (Premium)
   - Fire Pit (Luxury)
2. Submit

**Expected Output in n8n:**
Each material should show its quality level correctly in the PDF pricing.

---

## 🔍 How to Verify Results

### **In Browser Console (F12):**
1. Open Developer Tools → Console tab
2. Submit a quote
3. Look for these log entries:
   - `✅ Material saved:` - Shows each material as you add it
   - `📦 FULL PAYLOAD:` - Shows complete webhook payload before sending
   - `✅ n8n Response Status: 200` - Confirms successful delivery

### **In n8n Workflow:**
1. Check the "Executions" tab
2. Click the latest execution
3. Click "Webhook Trigger" node to see received data
4. Verify:
   - ✅ `customer` object has all fields
   - ✅ `project.gardenDesign.categories` contains your selections
   - ✅ `project.extras` shows pergola/firePit/waterFeature if selected
   - ✅ `metadata.quoteType` = "full_garden_redesign"

### **In Generated PDF:**
1. Check the email or download the PDF
2. Verify:
   - ✅ All selected materials appear in itemized list
   - ✅ Quantities match what you entered
   - ✅ Quality levels reflected in pricing
   - ✅ Extras (pergola, fire pit, water feature) listed separately

---

## 📊 Material Reference

### **Paving & Hard Landscaping (6 options)**
- Porcelain Tiles, Natural Stone, Resin Bound, Gravel, Block Paving, Concrete

### **Lawn & Planting (5 options)**
- Artificial Turf, Natural Lawn, Raised Beds, Feature Trees, Flower Beds

### **Structures (6 options)**
- Decking, Pergola*, Gazebo, Garden Room, Storage Shed, Summer House

### **Features (6 options)**
- Outdoor Lighting, Water Feature*, Fire Pit*, Outdoor Kitchen, Seating Area, BBQ Area

### **Boundaries (4 options)**
- Fencing, Walls, Hedging, Gates

**Total: 27 materials**
*Auto-populates `extras` object when selected

---

## ✅ Success Criteria

**All tests pass when:**
1. ✅ Browser console shows `✅ n8n Response Status: 200`
2. ✅ n8n execution shows your selections in Webhook Trigger node
3. ✅ PDF email arrives with correct itemization
4. ✅ No JavaScript errors in browser console
5. ✅ All selected materials appear in PDF pricing breakdown

---

## 🐛 Common Issues & Fixes

### **Issue: Material not appearing in PDF**
- **Check:** Console logs show material was saved? (`✅ Material saved:`)
- **Fix:** Make sure area/quantity > 0 and quality level selected

### **Issue: Extras not auto-detecting**
- **Check:** Did you select "pergola", "fire_pit", or "water_feature"?
- **Fix:** Material names must match exactly (with underscores)

### **Issue: Category not in webhook payload**
- **Check:** Did you save the material (not just open the modal)?
- **Fix:** Click "Add Material" button after entering details

---

## 🎯 Your Test Results

From your Nov 12 test at 20:06:
- ✅ **27 materials selected** - ALL captured correctly
- ✅ **5 categories** - All grouped properly
- ✅ **3 extras** - Pergola, Fire Pit, Water Feature detected
- ✅ **Quality levels** - Mix of Standard, Premium, Luxury
- ✅ **PDF generated** - £19,472.68 with itemized breakdown
- ✅ **Budget** - £100,000 captured
- ✅ **Customer details** - All fields populated

**Status: 🎉 FULLY FUNCTIONAL**
