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
    
    webhooks: {
        quote: "https://hook.eu2.make.com/your-quote-webhook-url",
        design: "https://hook.eu2.make.com/your-design-webhook-url",
        contact: "https://hook.eu2.make.com/your-contact-webhook-url"
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
