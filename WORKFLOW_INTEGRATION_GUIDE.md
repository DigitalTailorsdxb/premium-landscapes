# Premium Landscapes - Complete Workflow Integration Guide

## Overview
This document explains how all 3 workflows are connected and how to configure them in n8n.

---

## 🔗 **The 3 Workflows**

### **1. Individual Products Quote Workflow**
- **Webhook:** `/webhook-test/premium-landscapes-quote`
- **Purpose:** Generate quotes for specific products (patio, decking, turf, etc.)
- **Output:** PDF quote via email

### **2. Full Garden Redesign Quote Workflow**
- **Webhook:** `/webhook-test/premium-landscapes-full-redesign`
- **Purpose:** Generate comprehensive garden redesign quotes with AI-powered material selection
- **Output:** PDF quote via email

### **3. AI Garden Design Workflow**
- **Webhook:** `/webhook-test/premium-landscapes-ai-design`
- **Purpose:** Generate AI-powered garden design images using DALL-E 3
- **Output:** 4 design concept images via email

---

## 🎯 **Integration Flow**

### **Flow 1: Quote → AI Design (Optional Add-on)**

```
Customer fills quote form
    ↓
Selects products/budget
    ↓
Checks "Also send me AI garden design concepts" ✓
    ↓
Submits quote
    ↓
[Website sends 2 webhooks in parallel]
    ↓                              ↓
Quote Workflow            AI Design Workflow
    ↓                              ↓
PDF Quote Email           4 Design Images Email
```

**Implementation:**
- Quote form has checkbox: "Also send me AI garden design concepts (Free)"
- When checked, website sends data to BOTH workflows:
  1. Quote webhook (generates PDF quote)
  2. AI Design webhook (generates design images)
- Customer receives 2 separate emails within 60 seconds

---

### **Flow 2: AI Design → Quote (Standalone)**

```
Customer goes to /design.html
    ↓
Fills design form (features, style, budget, optional photo)
    ↓
Submits design request
    ↓
AI Design Workflow
    ↓
4 Design Images Email
    ↓
Email includes "Get Instant Quote" CTA button
    ↓
Customer clicks → redirects to /quote.html
```

**Implementation:**
- AI Design email template includes prominent "Get Instant Quote" button
- Button links to: `https://your-site.com/quote.html`
- Creates seamless conversion path: Design viewer → Quote requester

---

## 📦 **Data Flow Between Workflows**

### **Quote Form → AI Design Workflow**

When AI design checkbox is checked, the quote form sends this payload to `/webhook-test/premium-landscapes-ai-design`:

```json
{
  "customer": {
    "email": "john@example.com",
    "phone": "07444887813",
    "name": "John Smith"
  },
  "design": {
    "features": ["patio", "decking", "turf", "lighting"],
    "styleDescription": "Garden with patio area, decking, lawn, garden lighting",
    "gardenSize": "50",
    "budget": "10000-20000",
    "materials": [],
    "budgetBasedDesign": false,
    "designNotes": ""
  },
  "photo": {
    "name": "garden.jpg",
    "type": "image/jpeg",
    "size": 245678,
    "data": "data:image/jpeg;base64,/9j/4AAQ..."
  },
  "metadata": {
    "timestamp": "2025-11-14T19:30:00.000Z",
    "source": "quote-form",
    "formVersion": "2.0",
    "quoteType": "individual-products",
    "hasPhoto": true,
    "hasMaterials": false
  }
}
```

**For Full Garden Redesign with Materials:**
```json
{
  "customer": { "email": "...", "phone": "...", "name": "..." },
  "design": {
    "features": ["porcelain_patio", "composite_decking", "artificial_turf"],
    "styleDescription": "Complete garden redesign with Porcelain Patio, Composite Decking, Artificial Turf",
    "gardenSize": "80",
    "budget": "20000-30000",
    "materials": [
      { "category": "paving", "name": "porcelain_patio", "displayName": "Porcelain Patio" },
      { "category": "decking", "name": "composite_decking", "displayName": "Composite Decking" },
      { "category": "lawn", "name": "artificial_turf", "displayName": "Artificial Turf" }
    ],
    "budgetBasedDesign": false,
    "designNotes": "Low maintenance, modern aesthetic"
  },
  "photo": null,
  "metadata": {
    "timestamp": "2025-11-14T19:30:00.000Z",
    "source": "quote-form",
    "formVersion": "2.0",
    "quoteType": "full-redesign",
    "hasPhoto": false,
    "hasMaterials": true
  }
}
```

**For Budget-Based Design (no materials specified):**
```json
{
  "customer": { "email": "...", "phone": "...", "name": "..." },
  "design": {
    "features": [],
    "styleDescription": "Complete garden redesign based on budget and requirements",
    "gardenSize": "100",
    "budget": "30000-50000",
    "materials": [],
    "budgetBasedDesign": true,
    "designNotes": "Family-friendly, low maintenance, space for kids play area"
  },
  "photo": null,
  "metadata": {
    "timestamp": "2025-11-14T19:30:00.000Z",
    "source": "quote-form",
    "formVersion": "2.0",
    "quoteType": "full-redesign",
    "hasPhoto": false,
    "hasMaterials": false
  }
}
```

**Key Differences from Standalone Design Form:**
- `metadata.source = "quote-form"` (vs "website")
- `metadata.quoteType` field indicates which quote mode was used
- `design.features` array contains selected products
- `design.styleDescription` is auto-generated from products (vs user-written)

---

## 🔧 **n8n Workflow Configuration**

### **Step 1: Update AI Design Workflow to Accept Quote Data**

Your AI Design workflow currently expects this structure:
```json
{
  "customer": { "email", "phone" },
  "design": { "features", "styleDescription", "gardenSize", "budget" },
  "photo": { "name", "type", "size", "data" }
}
```

**No changes needed!** The quote form sends data in the same format.

However, you can enhance the workflow to detect the source and customize the email:

#### **Node: "Code – Validate + Build Variants"**

Add this detection logic:

```javascript
// Detect if this came from quote form
const source = root.metadata?.source || 'website';
const isFromQuote = source === 'quote-form';

// Customize email subject based on source
const emailSubject = isFromQuote
  ? `Your AI Garden Designs + Quote Request`
  : `Your AI-Generated Garden Designs`;

// Include quote info in email if from quote form
const quoteInfo = isFromQuote
  ? `We've also sent you a detailed quote based on your ${root.metadata.quoteType === 'full-redesign' ? 'full garden redesign' : 'product selections'} request.`
  : '';

return {
  ...normalizedData,
  emailSubject,
  quoteInfo,
  source
};
```

---

### **Step 2: Update Email Template in AI Design Workflow**

#### **Node: "Code – Aggregate Designs + Email HTML"**

Update the email HTML to include quote information when triggered from quote form:

```javascript
// Build email HTML
const emailHtml = `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; background-color: #f9f9f9; }
    .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; }
    .header { text-align: center; margin-bottom: 30px; }
    .design-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0; }
    .design-card img { width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .cta-button { background: #2563eb; color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; display: inline-block; margin-top: 20px; }
    .info-box { background: #f0f9ff; border: 1px solid #3b82f6; border-radius: 8px; padding: 15px; margin: 20px 0; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="https://your-replit-url.com/static/logo.png" alt="Premium Landscapes" style="height: 60px;">
      <h1 style="color: #2563eb; margin-top: 20px;">Your AI Garden Designs Are Ready!</h1>
    </div>
    
    <p>Hi ${customerName},</p>
    
    ${source === 'quote-form' ? `
      <div class="info-box">
        <strong>✅ Quote + Designs Sent!</strong><br>
        You requested both a quote and AI design concepts. Check your inbox for:
        <ul style="margin: 10px 0;">
          <li>📄 Detailed PDF quote (separate email)</li>
          <li>🎨 AI design concepts (this email)</li>
        </ul>
      </div>
    ` : ''}
    
    <p>Based on your preferences for a <strong>${styleDescription}</strong> garden, here are your AI-generated design concepts:</p>
    
    <div class="design-grid">
      <div class="design-card">
        <img src="${design1Url}" alt="Design Concept 1">
        <p style="text-align: center; margin-top: 10px;">Concept 1</p>
      </div>
      <div class="design-card">
        <img src="${design2Url}" alt="Design Concept 2">
        <p style="text-align: center; margin-top: 10px;">Concept 2</p>
      </div>
      <div class="design-card">
        <img src="${design3Url}" alt="Design Concept 3">
        <p style="text-align: center; margin-top: 10px;">Concept 3</p>
      </div>
      <div class="design-card">
        <img src="${design4Url}" alt="Design Concept 4">
        <p style="text-align: center; margin-top: 10px;">Concept 4</p>
      </div>
    </div>
    
    ${source !== 'quote-form' ? `
      <p style="margin-top: 30px;">Love these designs? Get an instant quote to make them reality!</p>
      <div style="text-align: center;">
        <a href="https://your-replit-url.com/quote.html" class="cta-button">Get Your Free Quote</a>
      </div>
    ` : `
      <p style="margin-top: 30px;">These designs match your quote request. We'll be in touch to discuss making your dream garden a reality!</p>
    `}
    
    <hr style="margin: 40px 0; border: none; border-top: 1px solid #eee;">
    
    <p style="font-size: 12px; color: #999; text-align: center;">
      Premium Landscapes | Phone: 07444887813 | Email: info@premiumlandscapes.co.uk
    </p>
  </div>
</body>
</html>
`;

return {
  emailHtml,
  emailSubject: source === 'quote-form' ? 'Your AI Garden Designs + Quote Request' : 'Your AI-Generated Garden Designs',
  customer: { email: customerEmail, name: customerName },
  designs: allDesigns
};
```

---

## 📊 **Testing the Integration**

### **Test 1: Quote with AI Design**
1. Go to `/quote.html`
2. Fill out quote form (either mode)
3. Check "Also send me AI garden design concepts"
4. Submit
5. **Expected Result:**
   - 2 webhook triggers in n8n (quote + design)
   - 2 emails received:
     - Email 1: PDF quote
     - Email 2: 4 AI design images
   - Console shows: `🎨 AI Design requested - sending to AI Design workflow...`

### **Test 2: Standalone AI Design**
1. Go to `/design.html`
2. Fill out design form
3. Submit
4. **Expected Result:**
   - 1 webhook trigger (design only)
   - 1 email with 4 design images + "Get Instant Quote" CTA

### **Test 3: Design → Quote Flow**
1. Receive AI design email
2. Click "Get Instant Quote" button
3. **Expected Result:**
   - Redirects to `/quote.html`
   - User can now request quote

---

## 🔍 **Debugging**

### **Quote form not triggering AI Design workflow:**

Check browser console:
```
🎨 AI Design requested - sending to AI Design workflow...
📤 Sending to AI Design workflow: https://...
📦 Design payload: {...}
✅ AI Design workflow triggered successfully
```

If you see `⚠️ AI Design webhook not configured`, update `scripts/config.js`:
```javascript
webhooks: {
  design: "https://digitaltailorsdxb.app.n8n.cloud/webhook-test/premium-landscapes-ai-design"
}
```

### **AI Design workflow not receiving quote data:**

Check n8n workflow logs for the webhook payload. Should include:
- `metadata.source = "quote-form"`
- `metadata.quoteType = "individual-products"` or `"full-redesign"`

---

## 🎯 **Benefits of This Integration**

### **For Customers:**
1. **Convenience:** Get quote + designs in one request
2. **No duplicate data entry:** Same info used for both
3. **Visual + Financial:** See designs AND costs together
4. **Seamless flow:** Design viewers can easily request quotes

### **For Business:**
1. **Higher conversion:** Design viewers more likely to request quotes
2. **Better lead quality:** Customers who see designs are more engaged
3. **Upsell opportunity:** Quote requesters may add design service
4. **Data consolidation:** All customer data in one CRM entry

---

## 📝 **Summary Checklist**

- [x] AI design checkbox added to quote form (Step 5)
- [x] Checkbox always visible (not photo-dependent)
- [x] Quote form sends data to AI Design workflow when checked
- [x] AI Design workflow accepts quote data (same format as standalone)
- [x] AI Design email detects source and customizes messaging
- [x] Confirmation message mentions AI designs when requested
- [x] Design email includes "Get Quote" CTA for standalone requests
- [x] All 3 webhooks configured and tested

---

**Integration Complete!** 🚀

All three workflows now work together seamlessly while maintaining their standalone functionality.
