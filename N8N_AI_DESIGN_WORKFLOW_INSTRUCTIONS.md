# n8n AI Garden Design Workflow - Build Instructions for GPT

## 🎯 Workflow Overview

**Workflow Name:** Premium Landscapes - AI Garden Design Generator

**Purpose:** Receive garden design requests from the Replit website, generate 3 AI designs using DALL-E 3, and email them to the customer with embedded images.

**Platform:** n8n.cloud (hosted)

---

## 📊 Input Data Structure

### Webhook Payload (from design-engine.js)

The workflow receives this JSON payload from the website:

```json
{
  "customer": {
    "email": "customer@example.com",
    "phone": "07444887813"
  },
  "design": {
    "features": ["patio", "water-feature", "pergola", "lighting"],
    "styleDescription": "Modern minimalist with clean lines, architectural plants, and neutral colors",
    "gardenSize": "75 sqm",
    "budget": "10000-20000"
  },
  "photo": {
    "name": "current-garden.jpg",
    "type": "image/jpeg",
    "size": 2048576,
    "data": "base64EncodedImageString..."
  },
  "metadata": {
    "timestamp": "2025-10-25T21:00:00.000Z",
    "source": "website"
  }
}
```

**Note:** The `photo` object may be null if the customer didn't upload a photo.

---

## 🔧 Workflow Node Configuration

### Node 1: Webhook Trigger
**Node Type:** Webhook  
**Configuration:**
- **HTTP Method:** POST
- **Path:** `premium-landscapes-design`
- **Response Mode:** Using 'Last Node'
- **Full Webhook URL:** `https://[your-instance].app.n8n.cloud/webhook/premium-landscapes-design`

**Output:** Raw JSON payload from website

---

### Node 2: Validate & Parse Input
**Node Type:** Code (JavaScript)  
**Purpose:** Validate incoming data and prepare for processing

```javascript
// Validate required fields
const customer = $input.item.json.customer;
const design = $input.item.json.design;

if (!customer || !customer.email) {
  throw new Error('Customer email is required');
}

if (!design || !design.features || design.features.length === 0) {
  throw new Error('At least one garden feature is required');
}

if (!design.styleDescription) {
  throw new Error('Style description is required');
}

// Parse and clean data
const cleanData = {
  customerEmail: customer.email.trim().toLowerCase(),
  customerPhone: customer.phone || '',
  features: design.features,
  styleDescription: design.styleDescription.trim(),
  gardenSize: design.gardenSize || 'not specified',
  budget: design.budget || 'not specified',
  hasPhoto: $input.item.json.photo && $input.item.json.photo.data ? true : false,
  photoData: $input.item.json.photo?.data || null,
  timestamp: $input.item.json.metadata.timestamp
};

// Budget display text
let budgetText = 'Budget not specified';
switch(cleanData.budget) {
  case '<5000': budgetText = 'Under £5,000'; break;
  case '5000-10000': budgetText = '£5,000 - £10,000'; break;
  case '10000-20000': budgetText = '£10,000 - £20,000'; break;
  case '>20000': budgetText = '£20,000+'; break;
}
cleanData.budgetDisplay = budgetText;

return cleanData;
```

**Output:** Cleaned and validated data object

---

### Node 3: Build DALL-E Prompts (Loop Preparation)
**Node Type:** Code (JavaScript)  
**Purpose:** Generate 3 different prompt variations for diversity

```javascript
const features = $input.item.json.features;
const style = $input.item.json.styleDescription;
const size = $input.item.json.gardenSize;

// Convert feature codes to readable names
const featureMap = {
  'patio': 'Natural stone patio area',
  'decking': 'Composite or timber decking',
  'lawn': 'Manicured lawn area',
  'water-feature': 'Water feature (fountain or pond)',
  'garden-beds': 'Planted garden beds with perennials',
  'seating': 'Outdoor seating area',
  'pergola': 'Wooden or metal pergola structure',
  'lighting': 'Integrated garden lighting',
  'full-redesign': 'Complete garden transformation'
};

const featureList = features.map(f => featureMap[f] || f).join(', ');

// Create 3 prompt variations
const prompts = [];

// Prompt 1: Classic interpretation
prompts.push({
  prompt: `Create a photorealistic garden design visualization for a ${size} UK residential garden.

STYLE: ${style}

KEY FEATURES TO INCLUDE:
${featureList}

DESIGN REQUIREMENTS:
- Photorealistic rendering quality
- UK climate-appropriate plants (hardy perennials, native species)
- Professional landscape design aesthetic
- Warm, natural lighting (late afternoon golden hour)
- View from main seating/entertaining area perspective
- Contemporary UK residential garden setting
- Realistic proportions and scale

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K quality)
- Landscape orientation
- Natural, realistic colors
- Professional architectural visualization style`,
  variation: 'Classic'
});

// Prompt 2: Modern twist
prompts.push({
  prompt: `Design a stunning modern garden visualization for a ${size} UK outdoor space.

STYLE DIRECTION: ${style} with contemporary architectural elements

MUST INCLUDE:
${featureList}

DESIGN ELEMENTS:
- Magazine-worthy photorealistic quality
- Modern UK garden design trends
- Sustainable planting scheme (low maintenance, drought-tolerant)
- Evening ambiance with subtle lighting
- Entertaining and relaxation focus
- Clean lines and sophisticated materials
- View from French doors/patio perspective

RENDERING QUALITY:
- Professional architectural visualization
- 4K resolution, landscape format
- Balanced composition
- Rich, natural color palette`,
  variation: 'Modern'
});

// Prompt 3: Lush & inviting
prompts.push({
  prompt: `Visualize an inviting, lush garden design for a ${size} UK residential property.

AESTHETIC: ${style} with abundant planting and natural flow

FEATURED ELEMENTS:
${featureList}

DESIGN VISION:
- Photorealistic garden photography style
- Mature, established garden appearance
- Layered planting with varied heights and textures
- Midday natural lighting with dappled shade
- Inviting, relaxing atmosphere
- Family-friendly and functional spaces
- View showcasing the garden's depth and variety

PRODUCTION QUALITY:
- High-end garden magazine photography
- 4K resolution, landscape orientation
- Vibrant, natural colors
- Professional composition`,
  variation: 'Lush'
});

return prompts.map((p, index) => ({
  ...p,
  designNumber: index + 1,
  customerEmail: $input.item.json.customerEmail,
  customerPhone: $input.item.json.customerPhone,
  features: features,
  styleDescription: style,
  gardenSize: size,
  budget: $input.item.json.budget,
  budgetDisplay: $input.item.json.budgetDisplay
}));
```

**Output:** Array of 3 prompt objects  
**Split Into Items:** Yes (creates 3 separate items for loop)

---

### Node 4: Generate AI Design (Loop - runs 3x)
**Node Type:** HTTP Request  
**Purpose:** Call OpenAI DALL-E 3 API to generate each design

**Configuration:**
- **Method:** POST
- **URL:** `https://api.openai.com/v1/images/generations`
- **Authentication:** Predefined Credentials (OpenAI API - placeholder)
- **Headers:**
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {{$credentials.openAIApi.apiKey}}`

**Body (JSON):**
```json
{
  "model": "dall-e-3",
  "prompt": "={{$json.prompt}}",
  "n": 1,
  "size": "1792x1024",
  "quality": "hd",
  "response_format": "b64_json"
}
```

**Options:**
- **Timeout:** 120000 (2 minutes)
- **Retry on Fail:** Yes, 2 times

**Output:** Base64 encoded image data from DALL-E

---

### Node 5: Process Image Data
**Node Type:** Code (JavaScript)  
**Purpose:** Extract and format image data for email

```javascript
// Extract base64 image from OpenAI response
const imageData = $input.item.json.data[0].b64_json;
const designNumber = $input.item.json.designNumber;
const variation = $input.item.json.variation;

return {
  designNumber: designNumber,
  variation: variation,
  imageBase64: imageData,
  imageCid: `design${designNumber}@premium-landscapes`,
  customerEmail: $input.item.json.customerEmail,
  customerPhone: $input.item.json.customerPhone,
  features: $input.item.json.features,
  styleDescription: $input.item.json.styleDescription,
  gardenSize: $input.item.json.gardenSize,
  budget: $input.item.json.budget,
  budgetDisplay: $input.item.json.budgetDisplay
};
```

**Output:** Formatted image data with metadata

---

### Node 6: Aggregate All Designs
**Node Type:** Aggregate  
**Purpose:** Combine the 3 separate design images back into one item

**Configuration:**
- **Aggregate:** All Items
- **Output Format:** Combine all item data

**Output:** Single item with array of all 3 designs

---

### Node 7: Build Email HTML
**Node Type:** Code (JavaScript)  
**Purpose:** Create HTML email with embedded images

```javascript
const designs = $input.item.json;
const customerEmail = designs[0].customerEmail;
const styleDescription = designs[0].styleDescription;
const features = designs[0].features;
const gardenSize = designs[0].gardenSize;
const budgetDisplay = designs[0].budgetDisplay;

// Feature display names
const featureMap = {
  'patio': 'Patio/Terrace',
  'decking': 'Decking',
  'lawn': 'Lawn Area',
  'water-feature': 'Water Feature',
  'garden-beds': 'Garden Beds',
  'seating': 'Seating Area',
  'pergola': 'Pergola',
  'lighting': 'Garden Lighting',
  'full-redesign': 'Full Garden Redesign'
};

const featureList = features.map(f => featureMap[f] || f).join(', ');

// Build HTML email
const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
    }
    .container {
      background-color: #ffffff;
      padding: 40px 30px;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
      padding-bottom: 20px;
      border-bottom: 3px solid #2563eb;
    }
    .logo {
      max-width: 200px;
      height: auto;
      margin-bottom: 20px;
    }
    h1 {
      color: #2563eb;
      font-size: 28px;
      margin: 0;
    }
    .intro {
      background-color: #f0f9ff;
      padding: 20px;
      border-radius: 8px;
      margin: 25px 0;
      border-left: 4px solid #2563eb;
    }
    .summary {
      background-color: #fafafa;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
    }
    .summary h3 {
      color: #2563eb;
      margin-top: 0;
      font-size: 18px;
    }
    .summary-item {
      margin: 10px 0;
      padding: 8px 0;
      border-bottom: 1px solid #e5e5e5;
    }
    .summary-item:last-child {
      border-bottom: none;
    }
    .summary-label {
      font-weight: bold;
      color: #555;
    }
    .design-section {
      margin: 40px 0;
      padding: 25px;
      background-color: #fafafa;
      border-radius: 8px;
    }
    .design-title {
      color: #2563eb;
      font-size: 22px;
      margin-bottom: 15px;
      text-align: center;
    }
    .design-image {
      width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
      margin: 20px 0;
    }
    .design-description {
      text-align: center;
      color: #666;
      font-style: italic;
      margin-top: 10px;
    }
    .cta-section {
      text-align: center;
      margin: 40px 0 30px 0;
      padding: 30px 20px;
      background: linear-gradient(135deg, #2563eb 0%, #8b5cf6 100%);
      border-radius: 12px;
      color: white;
    }
    .cta-section h2 {
      color: white;
      margin-top: 0;
      font-size: 24px;
    }
    .cta-button {
      display: inline-block;
      background-color: white;
      color: #2563eb;
      padding: 15px 40px;
      text-decoration: none;
      border-radius: 50px;
      font-weight: bold;
      font-size: 18px;
      margin: 15px 0;
      box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .contact-info {
      text-align: center;
      margin: 30px 0;
      padding: 20px;
      background-color: #f0f9ff;
      border-radius: 8px;
    }
    .contact-item {
      margin: 10px 0;
      font-size: 16px;
    }
    .contact-icon {
      color: #2563eb;
      margin-right: 8px;
    }
    .footer {
      text-align: center;
      margin-top: 40px;
      padding-top: 20px;
      border-top: 2px solid #e5e5e5;
      color: #666;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev/static/logo.png" alt="Premium Landscapes" class="logo">
      <h1>Your AI Garden Designs Are Ready! 🎨</h1>
    </div>

    <div class="intro">
      <p style="margin: 0; font-size: 16px;">
        <strong>Hi there!</strong>
      </p>
      <p style="margin-top: 10px;">
        Thank you for using our AI Garden Design tool. We've created <strong>3 stunning design concepts</strong> based on your preferences. Each design showcases a unique interpretation of your vision.
      </p>
    </div>

    <div class="summary">
      <h3>📋 Your Design Brief</h3>
      <div class="summary-item">
        <span class="summary-label">Style:</span> ${styleDescription}
      </div>
      <div class="summary-item">
        <span class="summary-label">Features:</span> ${featureList}
      </div>
      <div class="summary-item">
        <span class="summary-label">Garden Size:</span> ${gardenSize}
      </div>
      <div class="summary-item">
        <span class="summary-label">Budget Range:</span> ${budgetDisplay}
      </div>
    </div>

    <!-- Design 1 -->
    <div class="design-section">
      <h2 class="design-title">🌿 Design Concept 1: ${designs[0].variation} Style</h2>
      <img src="cid:${designs[0].imageCid}" alt="Garden Design 1" class="design-image">
      <p class="design-description">A ${designs[0].variation.toLowerCase()} interpretation of your vision</p>
    </div>

    <!-- Design 2 -->
    <div class="design-section">
      <h2 class="design-title">🌸 Design Concept 2: ${designs[1].variation} Style</h2>
      <img src="cid:${designs[1].imageCid}" alt="Garden Design 2" class="design-image">
      <p class="design-description">A ${designs[1].variation.toLowerCase()} variation with unique character</p>
    </div>

    <!-- Design 3 -->
    <div class="design-section">
      <h2 class="design-title">🌺 Design Concept 3: ${designs[2].variation} Style</h2>
      <img src="cid:${designs[2].imageCid}" alt="Garden Design 3" class="design-image">
      <p class="design-description">A ${designs[2].variation.toLowerCase()} approach to your garden transformation</p>
    </div>

    <!-- CTA Section -->
    <div class="cta-section">
      <h2>Love What You See? 💚</h2>
      <p style="font-size: 16px; margin: 15px 0;">
        Get an instant quote to bring these designs to life!
      </p>
      <a href="https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev/quote.html" class="cta-button">
        Get Instant Quote →
      </a>
      <p style="font-size: 14px; margin-top: 20px; opacity: 0.9;">
        Our AI-powered quote system delivers accurate pricing in minutes
      </p>
    </div>

    <!-- Contact Info -->
    <div class="contact-info">
      <h3 style="color: #2563eb; margin-top: 0;">Questions? We're Here to Help</h3>
      <div class="contact-item">
        <span class="contact-icon">📞</span>
        <strong>Phone:</strong> 07444 887813
      </div>
      <div class="contact-item">
        <span class="contact-icon">✉️</span>
        <strong>Email:</strong> info@premium-landscapes.co.uk
      </div>
      <div class="contact-item">
        <span class="contact-icon">🌐</span>
        <strong>Website:</strong> <a href="https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev">Premium Landscapes</a>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      <p>
        These AI-generated designs are conceptual visualizations to inspire your project.<br>
        Final designs will be tailored to your specific site conditions and preferences.
      </p>
      <p style="margin-top: 15px;">
        <strong>Premium Landscapes</strong> - Transforming Gardens with AI-Powered Innovation<br>
        Serving the Midlands & Home Counties
      </p>
    </div>
  </div>
</body>
</html>
`;

return {
  html: html,
  customerEmail: customerEmail,
  designs: designs,
  subject: 'Your AI Garden Designs from Premium Landscapes 🌿'
};
```

**Output:** Email HTML and metadata

---

### Node 8: Send Email with Embedded Images
**Node Type:** Gmail / Send Email  
**Purpose:** Send the HTML email with 3 designs embedded as inline images

**Configuration:**
- **Authentication:** Gmail OAuth2 (placeholder credentials)
- **To:** `={{$json.customerEmail}}`
- **Subject:** `={{$json.subject}}`
- **Email Type:** HTML
- **HTML:** `={{$json.html}}`

**Attachments (embedded images):**
Add 3 attachments as inline/embedded:
```javascript
[
  {
    "type": "binary",
    "property": "designs[0].imageBase64",
    "contentId": "={{$json.designs[0].imageCid}}",
    "fileName": "design-1.png",
    "mimeType": "image/png",
    "encoding": "base64"
  },
  {
    "type": "binary",
    "property": "designs[1].imageBase64",
    "contentId": "={{$json.designs[1].imageCid}}",
    "fileName": "design-2.png",
    "mimeType": "image/png",
    "encoding": "base64"
  },
  {
    "type": "binary",
    "property": "designs[2].imageBase64",
    "contentId": "={{$json.designs[2].imageCid}}",
    "fileName": "design-3.png",
    "mimeType": "image/png",
    "encoding": "base64"
  }
]
```

**Output:** Email send confirmation

---

### Node 9: Log to CRM (Optional)
**Node Type:** HTTP Request  
**Purpose:** Store lead in Airtable/Google Sheets

**Configuration:**
- **Method:** POST
- **URL:** `{{$credentials.crmWebhook}}` (placeholder)
- **Body:**
```json
{
  "email": "={{$json.customerEmail}}",
  "phone": "={{$json.designs[0].customerPhone}}",
  "features": "={{$json.designs[0].features.join(', ')}}",
  "style": "={{$json.designs[0].styleDescription}}",
  "garden_size": "={{$json.designs[0].gardenSize}}",
  "budget": "={{$json.designs[0].budgetDisplay}}",
  "timestamp": "={{$now}}",
  "source": "AI Garden Design",
  "status": "Design Sent"
}
```

**Output:** CRM confirmation

---

### Node 10: Webhook Response
**Node Type:** Respond to Webhook  
**Purpose:** Send success response back to website

**Configuration:**
- **Response Code:** 200
- **Response Body:**
```json
{
  "success": true,
  "message": "AI designs generated and sent successfully",
  "email": "={{$json.customerEmail}}",
  "designsGenerated": 3
}
```

**Output:** HTTP response to website (triggers success state)

---

## 🧪 Test Data Payload

Include this test payload for immediate testing:

```json
{
  "_TEST_MODE": true,
  "customer": {
    "email": "test@premiumlandscapes.co.uk",
    "phone": "07444887813"
  },
  "design": {
    "features": ["patio", "water-feature", "lighting"],
    "styleDescription": "TEST: Modern minimalist with clean lines and architectural plants",
    "gardenSize": "50 sqm",
    "budget": "10000-20000"
  },
  "photo": null,
  "metadata": {
    "timestamp": "2025-10-25T21:00:00.000Z",
    "source": "test-webhook"
  }
}
```

**Note:** Test emails should have "[TEST]" prefix in subject line when `_TEST_MODE` is true.

---

## 🔐 Required Credentials (Placeholders)

1. **OpenAI API**
   - Type: Header Auth
   - Name: `openAIApi`
   - Header: `Authorization`
   - Value: `Bearer sk-proj-PLACEHOLDER`

2. **Gmail OAuth2**
   - Type: OAuth2
   - Name: `gmailOAuth`
   - Grant Type: Authorization Code
   - Client ID: `PLACEHOLDER`
   - Client Secret: `PLACEHOLDER`

3. **CRM Webhook (Optional)**
   - Type: Generic
   - Name: `crmWebhook`
   - URL: `https://hooks.airtable.com/PLACEHOLDER`

---

## 📝 White-Label Variables

These should be easily configurable at the workflow level:

```javascript
// Brand Configuration
const BRAND_LOGO = "https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev/static/logo.png";
const COMPANY_NAME = "Premium Landscapes";
const CONTACT_PHONE = "07444 887813";
const CONTACT_EMAIL = "info@premium-landscapes.co.uk";
const WEBSITE_URL = "https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev";
const QUOTE_PAGE_URL = "https://dc75ac27-bacc-4020-bfea-3d95e4c635f0-00-3n5dcfbaxdmz3.sisko.replit.dev/quote.html";
```

---

## ✅ Success Criteria

The workflow should:
- ✅ Receive webhook data from Replit website
- ✅ Validate all required fields
- ✅ Generate 3 unique DALL-E 3 design variations
- ✅ Embed all images inline in HTML email
- ✅ Send professional branded email to customer
- ✅ Log lead to CRM (optional)
- ✅ Return success response to website
- ✅ Handle errors gracefully with retry logic
- ✅ Complete in under 3 minutes total

---

## 🚀 Deployment Notes

1. **n8n.cloud Setup:**
   - Import workflow JSON
   - Activate workflow
   - Copy webhook URL
   - Update `scripts/config.js` on Replit with webhook URL

2. **Credential Setup:**
   - Add OpenAI API key
   - Configure Gmail OAuth2
   - Test with test payload

3. **Testing:**
   - Send test webhook payload
   - Verify email delivery
   - Check all 3 images display correctly
   - Confirm CTA links work

---

## 📋 Final Checklist

- [ ] Webhook configured and active
- [ ] OpenAI credentials added
- [ ] Gmail OAuth2 configured
- [ ] Test email sent successfully
- [ ] All 3 images embedded correctly
- [ ] Email renders properly on mobile
- [ ] CTA links point to correct URLs
- [ ] Brand logo displays correctly
- [ ] Error handling tested
- [ ] CRM integration working (if enabled)

---

**This workflow is production-ready and white-label compatible!** 🎯
