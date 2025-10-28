# Quick Start Guide - Premium Landscapes

## What You Have ✅

A **complete, production-ready** AI-powered landscaping website with:
- 19 pages (homepage, 7 main pages, 10 blog posts)
- 5-step instant quote system with AI integration
- AI garden design generator
- Fully responsive mobile/desktop design
- White-label ready for quick client rebranding

## Current Status

🟢 **Fully Functional** - All pages working perfectly  
🟡 **Demo Mode** - Quote form shows mock data (no n8n connected yet)

## To Go Live with Real Quotes (Optional)

The quote system currently shows demo data. To enable **real AI-powered quotes with automated email delivery:**

### 1. Get Your n8n Webhook URL
- Import the n8n workflow (JSON file provided)
- Click the "Webhook Trigger1" node
- Copy the Production webhook URL

### 2. Update Config File
Open `scripts/config.js` and update line 35:

```javascript
webhooks: {
    quote: "https://your-n8n-url.app.n8n.cloud/webhook/premium-landscapes-quote",
    // ... other webhooks
}
```

### 3. Test It
- Fill out the Instant Quote form
- Check n8n executions tab for success
- Customer receives PDF quote via email within 2 minutes

**Detailed setup:** See `N8N_QUOTE_WEBHOOK_SETUP.md`

## White-Label Customization

To rebrand for a client (< 2 hours):

### 1. Update `scripts/config.js`
```javascript
const brandConfig = {
    companyName: "Client Company Name",
    primaryColor: "#2563eb",      // Client's brand color
    phone: "07444 887813",         // Client's phone
    email: "info@client.com",      // Client's email
    whatsapp: "447444887813",      // Client's WhatsApp
    location: "Serving Your Area",
    address: "Client Address",
}
```

### 2. Replace Logo
Replace `static/logo.png` with client's logo

### 3. Update Images (Optional)
Replace portfolio images in `images/` folder

### 4. Update Pricing (If using n8n)
Update Google Sheets pricing table connected to n8n workflow

## What Happens Without n8n?

The site works perfectly without n8n, but:
- ✅ Quote form still collects all customer data
- ✅ Beautiful 5-step user experience
- ⚠️ Shows demo quote (£11,100) to everyone
- ⚠️ No automated email delivery
- ⚠️ No PDF generation
- ⚠️ No lead tracking

**For a £3,500 white-label product, n8n is recommended** to provide:
- Dynamic pricing calculations
- Automated PDF quote generation
- Instant email delivery
- Lead tracking in Google Sheets
- Regional pricing adjustments

## File Structure

```
Premium-Landscapes/
├── index.html              # Homepage
├── quote.html              # 5-step instant quote (main USP)
├── design.html             # AI garden design generator
├── gallery.html            # Portfolio with featured project
├── services.html           # Service details
├── about.html              # Company story
├── contact.html            # Contact form
├── blog.html               # Blog listing
├── blog-1.html to blog-10.html  # Individual blog posts
├── scripts/
│   ├── config.js           # White-label configuration (EDIT THIS)
│   ├── quote-engine.js     # Quote form logic + n8n integration
│   └── main.js             # Navigation and global scripts
├── styles/
│   └── main.css            # Custom styles
└── static/
    └── logo.png            # Logo (replace for white-label)
```

## Support Documentation

- `N8N_QUOTE_WEBHOOK_SETUP.md` - Complete n8n setup instructions
- `N8N_AI_DESIGN_WORKFLOW_INSTRUCTIONS.md` - AI design generator setup
- `PRICING_INTEGRATION_GUIDE.md` - Pricing logic explained

## Demo vs Production

**Demo Mode (Current):**
- All pages functional ✅
- Quote form works beautifully ✅
- Shows £11,100 mock quote to everyone
- No email delivery
- Perfect for showcasing to potential clients

**Production Mode (With n8n):**
- All demo features ✅
- Real dynamic pricing from Google Sheets ✅
- Automated PDF generation ✅
- Instant email to customers ✅
- Lead tracking in Google Sheets ✅
- Regional price adjustments (London vs Midlands) ✅

## Next Steps

1. **Test the demo** - Navigate through all pages, try the quote form
2. **Customize for first client** - Update config.js and logo
3. **Decide on n8n** - Optional but recommended for full automation
4. **Deploy to custom domain** - Use Replit's publish feature

---

**Questions?** Check the documentation files or review the code comments in `scripts/quote-engine.js`
