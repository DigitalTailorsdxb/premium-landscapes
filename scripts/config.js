const brandConfig = {
    companyName: "Premium Landscapes",
    primaryColor: "#2563eb",
    secondaryColor: "#3b82f6",
    accentColor: "#8b5cf6",
    phone: "07444 887813",
    email: "info@premium-landscapes.co.uk",
    whatsapp: "447444887813",
    location: "Serving Midlands & Home Counties",
    address: "Leicester Forest East, Leicester",
    
    // ============================================================================
    // WEBHOOK CONFIGURATION - Make.com / n8n Integration Points
    // ============================================================================
    // When ready to go live, replace these URLs with your actual webhook endpoints
    // 
    // QUOTE WEBHOOK receives:
    //   - customer: {email, phone, postcode}
    //   - project: {products[], additionalNotes, totalArea, budget}
    //   - files: [{name, type, size, data (base64)}]
    //   - options: {aiDesign, requestedAIDesign}
    //   - metadata: {timestamp, source, formVersion, confidence}
    //
    // QUOTE WEBHOOK should return:
    //   - success: true/false
    //   - quoteId: "Q-2025-001"
    //   - breakdown: [{description, low, high}]
    //   - totalLow: 8500
    //   - totalHigh: 12500
    //   - confidence: 92
    //   - pdfUrl: "https://..." (optional)
    //   - estimatedDays: 5 (optional)
    //
    webhooks: {
        quote: "https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-quote",
        email: "https://hook.eu2.make.com/your-email-webhook-url",
        design: "https://hook.eu2.make.com/your-design-webhook-url",
        contact: "https://hook.eu2.make.com/your-contact-webhook-url"
    },
    
    // ============================================================================
    // PRICING SYSTEM CONFIGURATION
    // ============================================================================
    pricing: {
        // Google Sheets ID containing pricing data
        // Sheet should have columns: Material, Unit, MatCost, LabourCost, Excavation, Waste, RegionFactor
        googleSheetsId: "your-google-sheets-id-here",
        
        // Default overhead/markup percentage (25% = 1.25)
        overheadMarkup: 1.25,
        
        // Regional pricing modifiers by postcode area
        regionalModifiers: {
            // London & South East (higher costs)
            "SW": 1.15, "SE": 1.15, "NW": 1.15, "N": 1.15, "E": 1.15,
            "W": 1.15, "EC": 1.15, "WC": 1.15,
            
            // Home Counties
            "AL": 1.10, "SL": 1.10, "HP": 1.10, "WD": 1.10, "EN": 1.10,
            "HA": 1.10, "UB": 1.10, "TW": 1.10, "KT": 1.10, "SM": 1.10,
            "CR": 1.10, "BR": 1.10, "DA": 1.10, "RM": 1.10,
            
            // Midlands (baseline)
            "LE": 1.00, "CV": 1.00, "B": 1.00, "DE": 1.00, "NG": 1.00,
            "NN": 1.00, "MK": 1.00, "LU": 1.00,
            
            // Default for unlisted areas
            "DEFAULT": 1.00
        },
        
        // Confidence thresholds
        confidence: {
            excellent: 90,  // All details provided + photos
            good: 75,       // Most details provided
            fair: 60,       // Basic details only
            low: 50         // Minimal information
        }
    }
};

function applyBranding() {
    const setElement = (id, text, attr = null, attrValue = null) => {
        const el = document.getElementById(id);
        if (el) {
            if (text) el.textContent = text;
            if (attr && attrValue) el.setAttribute(attr, attrValue);
        }
    };
    
    setElement('companyName', brandConfig.companyName);
    setElement('footerCompanyName', brandConfig.companyName);
    setElement('copyrightCompanyName', brandConfig.companyName);
    setElement('footerCopyright', brandConfig.companyName);
    
    setElement('contactPhone', brandConfig.phone, 'href', `tel:${brandConfig.phone}`);
    setElement('footerPhone', brandConfig.phone);
    setElement('phoneLink', brandConfig.phone, 'href', `tel:${brandConfig.phone}`);
    
    setElement('contactEmail', brandConfig.email, 'href', `mailto:${brandConfig.email}`);
    setElement('footerEmail', brandConfig.email);
    setElement('emailLink', brandConfig.email, 'href', `mailto:${brandConfig.email}`);
    
    setElement('contactLocation', brandConfig.location);
    setElement('footerLocation', brandConfig.location);
    setElement('addressLine1', 'Your Business Address');
    setElement('addressLine2', 'Your City, County');
    setElement('addressPostcode', 'Postcode');
    setElement('serviceArea', 'Your Region');
    
    const whatsappMessage = encodeURIComponent("Hi, I'd like a quote for my garden");
    const whatsappUrl = `https://wa.me/${brandConfig.whatsapp}?text=${whatsappMessage}`;
    setElement('whatsappLink', null, 'href', whatsappUrl);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyBranding);
} else {
    applyBranding();
}
