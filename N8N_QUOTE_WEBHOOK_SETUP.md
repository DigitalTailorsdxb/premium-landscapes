# n8n Instant Quote Webhook Setup Guide

## Overview
This guide explains how to connect your Premium Landscapes website to the n8n instant quote workflow.

## Prerequisites
1. ✅ n8n workflow imported and activated
2. ✅ OpenAI API credentials configured in n8n
3. ✅ Gmail/SMTP credentials configured in n8n
4. ✅ Google Sheets & Google Drive credentials configured in n8n

## Step 1: Get Your n8n Webhook URL

1. **Open your n8n workflow** called "Premium Landscapes - Instant Quote (Final)"
2. **Click on the "Webhook Trigger1" node** (first node in the workflow)
3. **Find the Webhook URL** - it will look like:
   ```
   https://your-n8n-instance.app.n8n.cloud/webhook/premium-landscapes-quote
   ```
   Or if self-hosted:
   ```
   https://your-domain.com/webhook/premium-landscapes-quote
   ```
4. **Copy this URL** - you'll need it in the next step

## Step 2: Update Website Configuration

1. **Open** `scripts/config.js` in your website files
2. **Find the webhooks section** (around line 34)
3. **Replace the placeholder URL** with your actual n8n webhook URL:

```javascript
webhooks: {
    quote: "https://your-n8n-instance.app.n8n.cloud/webhook/premium-landscapes-quote",
    email: "https://hook.eu2.make.com/your-email-webhook-url",
    design: "https://hook.eu2.make.com/your-design-webhook-url",
    contact: "https://hook.eu2.make.com/your-contact-webhook-url"
},
```

4. **Save the file**

## Step 3: Test the Connection

1. **Go to your website** and navigate to the Instant Quote page
2. **Fill out the quote form:**
   - Select at least one feature (e.g., Patio, Decking)
   - Add product details
   - Set area and budget
   - Enter postcode
   - Provide email and phone

3. **Submit the form**

4. **Check your n8n workflow execution:**
   - Go to n8n → Executions tab
   - You should see a new execution with status "Success"
   - Click it to see the data flow

5. **Check your email:**
   - You should receive a PDF quote within 1-2 minutes
   - The PDF should be uploaded to your Google Drive

## Expected Data Format

The website sends this JSON payload to n8n:

```json
{
  "customer": {
    "name": "johndoe",
    "email": "johndoe@example.com",
    "phone": "07444887813",
    "postcode": "LE3 3GH"
  },
  "project": {
    "products": ["patio", "decking", "turf"],
    "productDetails": {
      "patio": "Indian sandstone 30sqm",
      "decking": "Composite decking 20sqm", 
      "turf": "Artificial grass 25sqm"
    },
    "additionalNotes": "Would like raised beds as well",
    "area": 75,
    "budget": "£10k-£15k"
  },
  "files": [],
  "aiDesign": false,
  "timestamp": "2025-10-28T00:00:00.000Z",
  "source": "website",
  "confidence": 85
}
```

## n8n Workflow Data Processing

Your n8n workflow processes the data as follows:

1. **Validate Input** - Ensures customer email and products are provided
2. **Calculate Pricing** - Uses product types to calculate costs:
   - Checks `project.products` array for: patio, decking, turf, driveway, fencing, lighting, firepit, planters
   - Applies pricing from the pricing table in the workflow
3. **AI Enhancement** - GPT-4 Turbo writes a professional quote summary
4. **Generate PDF** - Creates branded PDF with itemized breakdown
5. **Send Email** - Emails PDF to customer
6. **Log to Sheets** - Records quote in Google Sheets
7. **Upload to Drive** - Archives PDF in Google Drive folder
8. **Error Handling** - Sends alert email if anything fails

## Webhook Response Format

The n8n workflow should respond with:

```json
{
  "success": true,
  "message": "Quote received successfully"
}
```

The website doesn't currently process the response (it just shows a success message), but you can extend this later to show dynamic pricing if needed.

## Troubleshooting

### Website shows "Demo Mode" message
- **Cause:** Webhook URL not configured or still contains placeholder text
- **Fix:** Update `scripts/config.js` with your actual n8n webhook URL

### n8n execution shows "Missing customer email" error
- **Cause:** Form validation failed or data structure incorrect
- **Fix:** Ensure email field is filled out on the website form

### No email received
- **Check:** n8n execution logs - did the Email node execute?
- **Check:** Gmail/SMTP credentials in n8n
- **Check:** Email not in spam folder

### PDF not generated
- **Check:** HTML to PDF node in n8n - any errors?
- **Check:** All data fields are present (customer name, products, etc.)

### Google Sheets/Drive errors
- **Check:** Google OAuth credentials are valid
- **Check:** Sheet ID and folder ID are correct in the workflow nodes
- **Check:** Service account has write permissions

## Production Checklist

Before going live:
- [ ] n8n workflow tested end-to-end
- [ ] Webhook URL updated in config.js
- [ ] Test quote sent successfully
- [ ] PDF generated and looks professional
- [ ] Email sent to correct address
- [ ] Google Sheets logging working
- [ ] Google Drive upload working
- [ ] Error alerting working (test by breaking something intentionally)
- [ ] Workflow is activated in n8n
- [ ] CORS/security settings configured if using custom domain

## Support

If you need help:
1. Check n8n execution logs for specific errors
2. Check browser console for JavaScript errors
3. Verify all API credentials in n8n
4. Test webhook URL directly with Postman/curl

---

**Ready to go live?** Once tested, your instant quote system will automatically:
- Generate professional PDF quotes
- Email them to customers within 2 minutes
- Log all quotes in Google Sheets
- Archive PDFs in Google Drive
- Handle errors gracefully with email alerts
