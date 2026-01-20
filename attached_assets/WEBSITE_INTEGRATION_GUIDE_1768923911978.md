# WEBSITE INTEGRATION GUIDE - FOR REPLIT DEVELOPERS

## 🎯 OVERVIEW
Your n8n workflow now sends proper error responses when quotes fail. The website needs to handle these responses and show appropriate messages to users.

---

## 📡 WEBHOOK RESPONSE FORMATS

### **✅ SUCCESS RESPONSE (Quote Generated)**
```json
{
  "success": true,
  "message": "Quote generated successfully! Check your email for the full proposal.",
  "quoteRef": "PL-260120-145818",
  "status": "completed",
  "email": "customer@example.com"
}
```
**HTTP Status Code:** `200`

---

### **❌ ERROR RESPONSE (Workflow Failed)**
```json
{
  "success": false,
  "message": "Sorry, your request was too complex for our system to process. Please try with a simpler design or contact us directly.",
  "error": {
    "type": "WorkflowCrashedError",
    "details": "System ran out of memory"
  },
  "status": "failed",
  "executionId": "1333",
  "contact": {
    "email": "premiumlandscapesuk@gmail.com",
    "phone": "07877 934782",
    "message": "Please contact us with your details and we'll create your quote manually."
  }
}
```
**HTTP Status Code:** `500`

---

### **⏳ PROCESSING RESPONSE (Rare - Unclear State)**
```json
{
  "success": true,
  "message": "Quote accepted for processing",
  "quoteRef": "processing",
  "status": "processing"
}
```
**HTTP Status Code:** `202`

---

## 💻 RECOMMENDED WEBSITE CODE

### **JavaScript/React Example:**

```javascript
async function submitQuoteRequest(formData) {
  const webhookUrl = 'YOUR_N8N_WEBHOOK_URL';
  
  try {
    // Show loading state
    showLoadingMessage('Processing your quote request...');
    
    // Send request to n8n
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData)
    });
    
    // Parse response
    const result = await response.json();
    
    // Handle based on success flag
    if (result.success) {
      // ✅ SUCCESS
      showSuccessMessage(
        result.message,
        result.quoteRef,
        result.email
      );
    } else {
      // ❌ ERROR
      showErrorMessage(
        result.message,
        result.contact
      );
    }
    
  } catch (error) {
    // Network error or timeout
    showNetworkError();
  }
}

function showSuccessMessage(message, quoteRef, email) {
  // Show success UI
  const successDiv = document.getElementById('success-message');
  successDiv.innerHTML = `
    <div class="success-box">
      <h2>✅ Quote Request Received!</h2>
      <p>${message}</p>
      <p><strong>Quote Reference:</strong> ${quoteRef}</p>
      <p><strong>Sent to:</strong> ${email}</p>
      <p>Check your inbox (and spam folder) for your detailed quote.</p>
    </div>
  `;
  successDiv.style.display = 'block';
}

function showErrorMessage(message, contact) {
  // Show error UI with contact info
  const errorDiv = document.getElementById('error-message');
  errorDiv.innerHTML = `
    <div class="error-box">
      <h2>⚠️ Oops! Something Went Wrong</h2>
      <p>${message}</p>
      <div class="contact-info">
        <h3>Get Help Directly:</h3>
        <p>📧 Email: <a href="mailto:${contact.email}">${contact.email}</a></p>
        <p>📞 Phone: <a href="tel:${contact.phone}">${contact.phone}</a></p>
        <p>${contact.message}</p>
      </div>
      <button onclick="location.reload()">Try Again</button>
    </div>
  `;
  errorDiv.style.display = 'block';
}

function showNetworkError() {
  // Handle network/timeout errors
  const errorDiv = document.getElementById('error-message');
  errorDiv.innerHTML = `
    <div class="error-box">
      <h2>⚠️ Connection Error</h2>
      <p>We couldn't reach our quote system. Please check your internet connection and try again.</p>
      <p>If the problem persists, contact us at:</p>
      <p>📧 <a href="mailto:premiumlandscapesuk@gmail.com">premiumlandscapesuk@gmail.com</a></p>
      <p>📞 <a href="tel:07877934782">07877 934782</a></p>
      <button onclick="location.reload()">Try Again</button>
    </div>
  `;
  errorDiv.style.display = 'block';
}

function showLoadingMessage(message) {
  // Show loading state
  const loadingDiv = document.getElementById('loading-message');
  loadingDiv.innerHTML = `
    <div class="loading-spinner"></div>
    <p>${message}</p>
  `;
  loadingDiv.style.display = 'block';
}
```

---

## 🎨 RECOMMENDED CSS

```css
/* Success Message */
.success-box {
  background: #d4edda;
  border: 2px solid #28a745;
  border-radius: 8px;
  padding: 30px;
  margin: 20px 0;
  text-align: center;
}

.success-box h2 {
  color: #155724;
  margin-bottom: 15px;
}

/* Error Message */
.error-box {
  background: #f8d7da;
  border: 2px solid #dc3545;
  border-radius: 8px;
  padding: 30px;
  margin: 20px 0;
  text-align: center;
}

.error-box h2 {
  color: #721c24;
  margin-bottom: 15px;
}

.contact-info {
  background: white;
  padding: 20px;
  border-radius: 5px;
  margin: 20px 0;
}

.contact-info a {
  color: #0066cc;
  text-decoration: none;
  font-weight: bold;
}

.contact-info a:hover {
  text-decoration: underline;
}

/* Loading State */
.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Buttons */
button {
  background: #0066cc;
  color: white;
  border: none;
  padding: 12px 30px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 15px;
}

button:hover {
  background: #0052a3;
}
```

---

## 📱 HTML STRUCTURE

```html
<!-- Add these containers to your quote form page -->

<!-- Loading State -->
<div id="loading-message" style="display: none;"></div>

<!-- Success State -->
<div id="success-message" style="display: none;"></div>

<!-- Error State -->
<div id="error-message" style="display: none;"></div>
```

---

## 🔍 TESTING CHECKLIST

### **Test 1: Successful Quote**
1. Fill out form with valid data
2. Submit
3. Should see: ✅ Success message with quote ref
4. Should receive: Email with quote PDF

### **Test 2: Workflow Error**
1. (You'll trigger this by testing with budget=0 or complex design)
2. Should see: ⚠️ Error message with contact info
3. Should NOT see: Generic browser error

### **Test 3: Network Error**
1. Disconnect internet
2. Submit form
3. Should see: Connection error message

---

## 🚀 DEPLOYMENT STEPS FOR REPLIT

### **What to Tell Your Replit Developer:**

```
Hey! We've updated the quote webhook to send proper error responses.

CHANGES NEEDED:

1. The webhook now returns `success: true/false` in the JSON response

2. Update the form submission handler to check `result.success`:
   - If true: Show success message with quote ref
   - If false: Show error message with contact info

3. Add these UI elements:
   - Success message container
   - Error message container  
   - Loading spinner

4. See attached code examples for:
   - JavaScript handler (submitQuoteRequest function)
   - CSS styles
   - HTML containers

TESTING:
Test both success and error scenarios before deploying.

FILES ATTACHED:
- WEBSITE_INTEGRATION_GUIDE.md (this file)
- JavaScript example
- CSS example
- HTML example
```

---

## 🎯 KEY IMPROVEMENTS

**BEFORE:**
- User submits form
- Workflow crashes
- User sees: (generic timeout or nothing)
- User thinks: "Did it work? Should I try again?"

**AFTER:**
- User submits form
- Workflow crashes
- User sees: "Sorry, error occurred. Contact us at..."
- User thinks: "Okay, I'll email them directly"

---

## ⚠️ IMPORTANT NOTES

1. **Always check `result.success`** - Don't assume HTTP 200 means success
2. **Show contact info on errors** - Always give users a way to reach you
3. **Handle timeouts** - Webhooks can timeout after 30-60 seconds
4. **Test both scenarios** - Success AND error cases
5. **Mobile responsive** - Make sure error messages look good on mobile

---

## 🐛 DEBUGGING

If errors aren't showing correctly:

```javascript
// Add this to see what you're receiving:
console.log('Webhook response:', result);
console.log('Success?', result.success);
console.log('Message:', result.message);
```

---

## 📞 CONTACT

If Replit developers need clarification, they can test the webhook directly:

```bash
# Test with curl
curl -X POST YOUR_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "name": "Test User",
      "email": "test@example.com",
      "phone": "07700900000",
      "postcode": "SW1A 1AA",
      "city": "London"
    },
    "project": {
      "totalArea_m2": 50,
      "totalBudget_gbp": 10000,
      "stylePreference": "modern",
      "requirements": "simple patio"
    }
  }'
```

This will show them the exact response format! 🚀
