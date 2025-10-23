const brandConfig = {
    companyName: "Premium Landscapes",
    primaryColor: "#2d5016",
    phone: "+44 1234 567890",
    email: "hello@premiumlandscapes.co.uk",
    whatsapp: "441234567890",
    location: "Serving London & Home Counties",
    
    webhooks: {
        quote: "https://hook.eu2.make.com/your-quote-webhook-url",
        design: "https://hook.eu2.make.com/your-design-webhook-url",
        contact: "https://hook.eu2.make.com/your-contact-webhook-url"
    }
};

function applyBranding() {
    document.getElementById('companyName').textContent = brandConfig.companyName;
    document.getElementById('footerCompanyName').textContent = brandConfig.companyName;
    document.getElementById('copyrightCompanyName').textContent = brandConfig.companyName;
    
    document.getElementById('contactPhone').textContent = brandConfig.phone;
    document.getElementById('contactPhone').href = `tel:${brandConfig.phone}`;
    
    document.getElementById('contactEmail').textContent = brandConfig.email;
    document.getElementById('contactEmail').href = `mailto:${brandConfig.email}`;
    
    document.getElementById('contactLocation').textContent = brandConfig.location;
    
    const whatsappMessage = encodeURIComponent("Hi, I'd like a quote for my garden");
    document.getElementById('whatsappLink').href = `https://wa.me/${brandConfig.whatsapp}?text=${whatsappMessage}`;
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyBranding);
} else {
    applyBranding();
}
