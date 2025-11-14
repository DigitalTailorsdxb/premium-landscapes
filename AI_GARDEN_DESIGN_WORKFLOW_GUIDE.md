# AI Garden Design Workflow - Complete Implementation Guide

## Overview
This document explains how the **AI Garden Design** feature works from customer submission to AI-generated design delivery via email.

---

## 🎯 **Workflow Summary**

**Customer Journey:**
1. Customer fills out design form on `design.html` (features, style, budget, optional garden photo)
2. Form data + photo sent to n8n/Make.com webhook as JSON payload
3. Workflow receives data, processes customer photo (if provided)
4. AI generates 3-4 garden design concepts using DALL·E 3 or Midjourney
5. Designs emailed back to customer with branded PDF/images

---

## 📤 **Step 1: How Website Sends Data to Workflow**

### Frontend Implementation (Already Built)

**File:** `scripts/design-engine.js`

The website captures customer inputs through a 4-step form:
- **Step 1:** Garden features (patio, decking, lawn, water feature, etc.)
- **Step 2:** Style preference (modern, traditional, cottage, zen, etc.) + optional garden photo upload
- **Step 3:** Garden size + budget range
- **Step 4:** Contact details (email, phone)

### Photo Upload System

The form supports drag-and-drop or click-to-upload:
```javascript
// Photo stored in designData.photo as File object
designData.photo = file; // e.g., "my-garden.jpg"
```

When submitted, the photo is **converted to Base64** automatically:
```javascript
const reader = new FileReader();
reader.onload = function(e) {
    webhookPayload.photo = {
        name: designData.photo.name,       // "garden.jpg"
        type: designData.photo.type,       // "image/jpeg"
        size: designData.photo.size,       // 245678 (bytes)
        data: e.target.result              // "data:image/jpeg;base64,/9j/4AAQ..."
    };
    await sendToWebhook(webhookPayload);
};
reader.readAsDataURL(designData.photo);
```

---

## 📦 **Step 2: Webhook Payload Structure**

### Webhook Endpoint
```
POST https://your-n8n-instance.com/webhook/premium-landscapes-ai-design
Content-Type: application/json
```

### Complete Payload Example

```json
{
  "customer": {
    "email": "john.smith@example.com",
    "phone": "07444887813"
  },
  "design": {
    "features": [
      "patio",
      "lawn",
      "planting",
      "lighting",
      "water-feature"
    ],
    "styleDescription": "modern minimalist",
    "gardenSize": "50",
    "budget": "£10k-£20k"
  },
  "photo": {
    "name": "my-garden.jpg",
    "type": "image/jpeg",
    "size": 245678,
    "data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBD..."
  },
  "metadata": {
    "timestamp": "2025-11-14T10:30:45.123Z",
    "source": "website",
    "formVersion": "2.0"
  }
}
```

### Payload Without Photo (Budget-Based Design)
```json
{
  "customer": {
    "email": "jane.doe@example.com",
    "phone": "07555123456"
  },
  "design": {
    "features": ["decking", "fencing", "turf"],
    "styleDescription": "family-friendly cottage garden",
    "gardenSize": "80",
    "budget": "£5k-£10k"
  },
  "photo": null,
  "metadata": {
    "timestamp": "2025-11-14T10:30:45.123Z",
    "source": "website",
    "formVersion": "2.0"
  }
}
```

---

## ⚙️ **Step 3: n8n/Make.com Workflow Processing**

### Workflow Structure (6 Main Nodes)

#### **Node 1: Webhook Trigger**
- **Type:** Webhook (POST)
- **URL Path:** `/webhook/premium-landscapes-ai-design`
- **Authentication:** Optional (add secret token header for security)
- **Output:** Raw JSON payload

---

#### **Node 2: Data Validation & Enrichment**
- **Type:** Code/Function Node
- **Purpose:** Validate payload, normalize data, generate request ID

```javascript
// Example validation logic
const payload = $input.all()[0].json;

// Validate required fields
if (!payload.customer?.email) {
  throw new Error('Customer email is required');
}

// Generate unique request ID
const requestId = `DESIGN-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

// Normalize budget to numeric range
const budgetMap = {
  '£5k-£10k': { min: 5000, max: 10000 },
  '£10k-£20k': { min: 10000, max: 20000 },
  '£20k-£30k': { min: 20000, max: 30000 },
  '£30k+': { min: 30000, max: 50000 }
};

const budgetRange = budgetMap[payload.design.budget] || { min: 5000, max: 15000 };

return {
  requestId: requestId,
  customer: payload.customer,
  design: {
    ...payload.design,
    budgetMin: budgetRange.min,
    budgetMax: budgetRange.max
  },
  photo: payload.photo,
  timestamp: payload.metadata.timestamp
};
```

---

#### **Node 3: Process Customer Photo (If Provided)**
- **Type:** Code Node
- **Purpose:** Decode Base64 image, save to temporary storage or extract image data

**Option A: Keep Base64 for Direct API Use**
```javascript
const input = $input.all()[0].json;

if (input.photo && input.photo.data) {
  // Extract base64 string (remove data URL prefix)
  const base64Data = input.photo.data.split(',')[1];
  
  return {
    ...input,
    photoBase64: base64Data,
    hasPhoto: true
  };
} else {
  return {
    ...input,
    photoBase64: null,
    hasPhoto: false
  };
}
```

**Option B: Upload to Cloud Storage (S3/Cloudinary)**
- Use n8n's HTTP Request node to upload to S3/Cloudinary
- Store the public URL for later use in AI prompts

---

#### **Node 4: AI Image Generation**

This is the **core node** where AI magic happens.

##### **Option A: OpenAI DALL·E 3 (Recommended)**

**Method 1: Generate New Designs (No Photo)**
```javascript
// n8n HTTP Request Node
// Endpoint: https://api.openai.com/v1/images/generations
// Method: POST
// Authentication: Bearer Token (OpenAI API Key)

const input = $input.all()[0].json;

// Build AI prompt from customer preferences
const features = input.design.features.join(', ');
const style = input.design.styleDescription;
const budget = `£${input.design.budgetMin/1000}k-£${input.design.budgetMax/1000}k`;

const prompt = `Professional garden design rendering: ${style} style garden featuring ${features}. 
Garden size: ${input.design.gardenSize}m². Budget range: ${budget}. 
High-quality landscape architecture visualization, aerial view, photorealistic, 
professional photography, well-lit, modern landscaping, UK garden design.`;

// Request body
{
  "model": "dall-e-3",
  "prompt": prompt,
  "n": 1,
  "size": "1024x1024",
  "quality": "hd",
  "style": "natural"
}

// Response: { "data": [{ "url": "https://..." }] }
```

**Method 2: Image-to-Image Transformation (With Photo)**

⚠️ **Important:** DALL·E 3 does **NOT** support image variations or edits. You have two options:

1. **Use GPT-4 Vision to analyze the photo first**, then generate new designs based on analysis
2. **Use Midjourney** for true image-to-image transformation

**GPT-4 Vision Approach:**
```javascript
// Step 1: Analyze customer's garden photo
// HTTP Request to https://api.openai.com/v1/chat/completions

{
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Analyze this garden image. Describe: current layout, size estimate, existing features, sun exposure, soil type, opportunities for improvement."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,${photoBase64}"
          }
        }
      ]
    }
  ],
  "max_tokens": 500
}

// Step 2: Use analysis to create better DALL·E prompt
const analysis = gptVisionResponse.choices[0].message.content;

const enhancedPrompt = `Garden design transformation based on this analysis: ${analysis}. 
Create a ${style} style redesign featuring ${features}. 
Budget: ${budget}. Professional landscape rendering, photorealistic, before-and-after style.`;

// Step 3: Generate with DALL·E 3
```

---

##### **Option B: Midjourney (via Discord Bot)**

Midjourney supports true image-to-image transformation using `/imagine` with image URLs.

**Implementation:**
1. Upload customer photo to publicly accessible URL (S3/Cloudinary)
2. Use Midjourney Discord bot API (via third-party service like [Midjourney API](https://www.midjourneyapi.io/))
3. Send prompt with image reference

```javascript
// Example Midjourney API request
{
  "prompt": "transform this garden into modern minimalist design with patio, water feature, lighting --ar 16:9 --v 6",
  "image_url": "https://your-s3-bucket.com/customer-photos/garden-123.jpg",
  "aspect_ratio": "16:9",
  "version": "6"
}
```

---

#### **Node 5: Generate Multiple Design Variations**

**Loop Node:** Generate 3-4 design concepts

```javascript
// n8n Split In Batches or Loop node
const numberOfDesigns = 4;
const designPrompts = [];

const basePrompt = `${style} garden design featuring ${features}, ${gardenSize}m², budget ${budget}`;

// Create variations
designPrompts.push(`${basePrompt}, aerial view, daytime, professional photography`);
designPrompts.push(`${basePrompt}, ground level perspective, evening lighting`);
designPrompts.push(`${basePrompt}, close-up of patio area, family gathering`);
designPrompts.push(`${basePrompt}, seasonal variation with flowers in bloom`);

// Call DALL·E 3 for each prompt
// Store all generated image URLs
```

---

#### **Node 6: Email Delivery to Customer**

**Email Service:** Use Gmail/SendGrid/Resend

**Email Template:**

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; background-color: #f9f9f9; }
    .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; }
    .header { text-align: center; margin-bottom: 30px; }
    .design-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .design-card img { width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .cta-button { background: #2563eb; color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; display: inline-block; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="https://your-replit-url.com/static/logo.png" alt="Premium Landscapes" style="height: 60px;">
      <h1 style="color: #2563eb; margin-top: 20px;">Your AI Garden Designs Are Ready!</h1>
    </div>
    
    <p>Hi {{customer.name}},</p>
    
    <p>Thank you for using our AI Garden Design Generator. Based on your preferences for a <strong>{{design.styleDescription}}</strong> garden featuring <strong>{{design.features}}</strong>, we've created these design concepts:</p>
    
    <div class="design-grid">
      <div class="design-card">
        <img src="{{design1Url}}" alt="Design Concept 1">
        <p style="text-align: center; margin-top: 10px;">Design Concept 1</p>
      </div>
      <div class="design-card">
        <img src="{{design2Url}}" alt="Design Concept 2">
        <p style="text-align: center; margin-top: 10px;">Design Concept 2</p>
      </div>
      <div class="design-card">
        <img src="{{design3Url}}" alt="Design Concept 3">
        <p style="text-align: center; margin-top: 10px;">Design Concept 3</p>
      </div>
      <div class="design-card">
        <img src="{{design4Url}}" alt="Design Concept 4">
        <p style="text-align: center; margin-top: 10px;">Design Concept 4</p>
      </div>
    </div>
    
    <p style="margin-top: 30px;">Love these designs? We can make them a reality!</p>
    
    <div style="text-align: center;">
      <a href="https://your-replit-url.com/quote.html" class="cta-button">Get Your Free Quote</a>
    </div>
    
    <p style="margin-top: 30px; font-size: 14px; color: #666;">
      <strong>Next Steps:</strong><br>
      1. Download your favorite designs above<br>
      2. Click the button to request a detailed quote<br>
      3. Our team will provide accurate pricing within 60 seconds
    </p>
    
    <hr style="margin: 40px 0; border: none; border-top: 1px solid #eee;">
    
    <p style="font-size: 12px; color: #999; text-align: center;">
      Premium Landscapes | Phone: 07444887813 | Email: info@premiumlandscapes.co.uk
    </p>
  </div>
</body>
</html>
```

**n8n Email Node Configuration:**
- **To:** `{{customer.email}}`
- **Subject:** `Your AI Garden Designs Are Ready! 🎨`
- **From:** `Premium Landscapes <noreply@premiumlandscapes.co.uk>`
- **Attachments:** Optional (attach design images as files)

---

## 🔐 **Security Considerations**

1. **Webhook Authentication:** Add secret token validation
2. **Rate Limiting:** Limit requests per IP/email to prevent abuse
3. **File Size Validation:** Max 10MB for uploaded photos
4. **Image Type Validation:** Only allow jpg, png, webp
5. **Email Validation:** Verify email format before sending

---

## 💰 **Cost Considerations**

**DALL·E 3 Pricing (as of Nov 2024):**
- Standard quality: $0.040 per image (1024x1024)
- HD quality: $0.080 per image (1024x1024)

**Per Customer Request:**
- 4 designs × $0.080 = **$0.32 per request (HD quality)**
- 4 designs × $0.040 = **$0.16 per request (Standard quality)**

**Recommendation:** Use Standard quality to keep costs low, reserve HD for premium customers.

---

## 📊 **Optional: CRM Integration**

After email delivery, log the request to your CRM:

```javascript
// Node 7: Log to Google Sheets/Airtable
{
  "timestamp": "2025-11-14T10:30:45Z",
  "requestId": "DESIGN-12345",
  "customerEmail": "john@example.com",
  "customerPhone": "07444887813",
  "features": "patio, lawn, lighting",
  "style": "modern minimalist",
  "budget": "£10k-£20k",
  "hasPhoto": true,
  "designUrls": [
    "https://dalle-url-1.png",
    "https://dalle-url-2.png",
    "https://dalle-url-3.png",
    "https://dalle-url-4.png"
  ],
  "emailSent": true,
  "status": "completed"
}
```

---

## 🚀 **Workflow Activation Checklist**

### Before Going Live:

- [ ] **Add OpenAI API Key** to n8n credentials
- [ ] **Configure email service** (Gmail OAuth or SendGrid API key)
- [ ] **Update webhook URL** in `scripts/config.js`:
  ```javascript
  webhooks: {
    design: 'https://your-n8n-instance.com/webhook/premium-landscapes-ai-design'
  }
  ```
- [ ] **Uncomment production code** in `scripts/design-engine.js` (lines 312-331)
- [ ] **Test end-to-end:** Submit test design request, verify email delivery
- [ ] **Set up error monitoring** (n8n workflow error notifications)
- [ ] **Configure rate limiting** (max 10 requests/hour per email)

---

## 📞 **Support & Troubleshooting**

**Common Issues:**

1. **"Photo not appearing in workflow"**
   - Check Base64 encoding in browser console
   - Verify `photo.data` field exists in webhook payload

2. **"DALL·E 3 returning errors"**
   - Check API key permissions
   - Verify prompt length (max 4000 characters)
   - Ensure budget is within OpenAI rate limits

3. **"Email not delivered"**
   - Check spam folder
   - Verify SendGrid/Gmail API credentials
   - Check n8n email node logs for errors

---

## 🎯 **Success Metrics to Track**

1. **Conversion rate:** Design requests → Quote requests
2. **Average time:** Webhook received → Email delivered
3. **Customer satisfaction:** Track email open rates
4. **Cost per request:** Monitor OpenAI API usage
5. **Error rate:** Failed workflows / Total requests

---

**End of Guide** ✅

For questions or workflow optimization, contact your technical team.
