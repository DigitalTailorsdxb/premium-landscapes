# n8n Workflow Activation Guide

## The Problem
You're seeing the error: **"There was an error processing your quote"**

This happens because the n8n workflows need to be **ACTIVE** to receive webhook requests. Simply executing them once doesn't keep them running.

## The Solution

### Step 1: Go to n8n
Open your n8n instance at: `https://digitaltailorsdxb.app.n8n.cloud/`

### Step 2: Activate Each Production Workflow

You need to activate all 3 production workflows. Look for these workflow names:

1. **Premium Landscapes - Individual Products Quote**
   - Webhook URL: `/webhook/premium-landscapes-quote`
   
2. **Premium Landscapes - Full Garden Redesign Quote**
   - Webhook URL: `/webhook/premium-landscapes-full-redesign`
   
3. **Premium Landscapes - AI Garden Design**
   - Webhook URL: `/webhook/premium-landscapes-ai-design`

### Step 3: Toggle to Active

For each workflow:
1. Open the workflow in n8n
2. Look for the **toggle switch** at the top (usually top-right)
3. Click it so it shows **"Active"** (green/enabled state)
4. The workflow is now listening for webhook requests

### Step 4: Test

1. Go to your website: `quote.html`
2. Fill out a quote request
3. Submit the form
4. You should receive the quote email successfully

## Important Notes

- **Active vs Executed:** 
  - ✅ **Active** = Workflow runs continuously and responds to webhooks
  - ❌ **Executed** = Workflow runs once and stops
  
- **All 3 Must Be Active:**
  - Individual products quotes → Workflow 1
  - Full redesign quotes → Workflow 2
  - AI design requests → Workflow 3

- **Check Status Regularly:**
  - Workflows can become inactive if there's an error
  - Always ensure they're active before demo/client presentations

## Testing Each Workflow

### Test Individual Products Quote:
1. Select "Select Individual Products" mode
2. Choose Patio + enter details
3. Complete steps and submit
4. Should route to `/webhook/premium-landscapes-quote`

### Test Full Redesign Quote:
1. Select "Complete Garden Redesign" mode
2. Select some materials or check "Budget-based design"
3. Complete steps and submit
4. Should route to `/webhook/premium-landscapes-full-redesign`

### Test AI Design:
1. Check "Also send me AI garden design concepts" in Step 5
2. Optionally upload 1 photo
3. Submit quote
4. Should trigger both quote workflow + AI design workflow

## Troubleshooting

If you still get errors:

1. **Check Browser Console:**
   - Right-click → Inspect → Console tab
   - Look for red error messages
   - They'll show the exact webhook URL and error

2. **Check n8n Execution Log:**
   - In n8n, click "Executions" tab
   - See if any executions failed
   - Read error messages

3. **Verify Webhook URLs:**
   - Make sure production URLs don't have `-test` in them
   - Should be `/webhook/` not `/webhook-test/`

4. **CORS Issues:**
   - Ensure n8n webhook nodes have CORS enabled
   - Allow origin: `*` or your specific domain
