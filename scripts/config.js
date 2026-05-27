const brandConfig = {
    companyName: "Premium Landscapes",
    primaryColor: "#2563eb",
    secondaryColor: "#3b82f6",
    accentColor: "#8b5cf6",
    phone: "07877 934782",
    email: "premiumlandscapesuk@gmail.com",
    whatsapp: "447877934782",
    location: "Serving Midlands & Home Counties",
    address: "",

    // ============================================================================
    // SOCIAL PROOF CONFIGURATION
    // ============================================================================
    social: {
        // Facebook Business Page URL — used in reviews embed and CTA buttons
        facebookPageUrl: "https://www.facebook.com/Premiumlandscapesuk/reviews",

        // Google Business Profile URL — update this once your Google profile is established
        // To find your link: Google Business Profile dashboard → "Get more reviews" → copy the link
        googleReviewsUrl: "https://www.google.com/maps/search/Premium+Landscapes+Kirby+Muxloe+Leicester",

        // Aggregate rating — update with real figures once Google Business reviews are live
        ratingValue: null,
        reviewCount: null,

        // Reviews — add real verified customer reviews here once collected
        // Format: { name, location, rating, date, text, initials, avatarColor, source }
        reviews: []
    },
    
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
        quote: "https://n8n.trade-engine.co.uk/webhook/premium-landscapes-quote",
        quoteFullRedesign: "https://n8n.trade-engine.co.uk/webhook/premium-landscapes-full-redesign",
        email: "https://hook.eu2.make.com/your-email-webhook-url",
        contact: "https://hook.eu2.make.com/your-contact-webhook-url",
        securityToken: "8f3c9a7e41b24d0ab6e5c9f0a2d7e18b9c6a4f7e23d15b9c0e4a6d8f2b1c97e"
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
    
    const locationLink = `${brandConfig.location} — <a href="areas-we-cover.html" class="hover:text-primary transition">Areas We Cover</a>`;
    const contactLocationEl = document.getElementById('contactLocation');
    if (contactLocationEl) contactLocationEl.innerHTML = locationLink;
    const footerLocationEl = document.getElementById('footerLocation');
    if (footerLocationEl) footerLocationEl.innerHTML = locationLink;
    setElement('addressLine1', 'Your Business Address');
    setElement('addressLine2', 'Your City, County');
    setElement('addressPostcode', 'Postcode');
    setElement('serviceArea', 'Your Region');
    
    const whatsappMessage = encodeURIComponent("Hi, I'd like a quote for my garden");
    const whatsappUrl = `https://wa.me/${brandConfig.whatsapp}?text=${whatsappMessage}`;
    setElement('whatsappLink', null, 'href', whatsappUrl);

    // Wire up social / review links
    document.querySelectorAll('[data-fb-page]').forEach(el => {
        el.href = brandConfig.social.facebookPageUrl;
    });
    document.querySelectorAll('[data-google-reviews]').forEach(el => {
        el.href = brandConfig.social.googleReviewsUrl;
    });

    // Update aggregate rating display
    document.querySelectorAll('[data-review-count]').forEach(el => {
        el.textContent = brandConfig.social.reviewCount;
    });
    document.querySelectorAll('[data-rating-value]').forEach(el => {
        el.textContent = brandConfig.social.ratingValue;
    });

    // Render review cards if the container exists
    renderReviews();

    // Load Facebook Page Plugin if container exists
    loadFacebookPlugin();
}

function renderReviews() {
    const container = document.getElementById('reviewCardsContainer');
    if (!container || !brandConfig.social.reviews) return;

    const sourceIcon = (source) => source === 'facebook'
        ? `<svg class="w-4 h-4" fill="#1877F2" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>`
        : `<svg class="w-4 h-4" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>`;

    const stars = (n) => Array(n).fill(`<svg class="w-4 h-4 text-amber-400 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>`).join('');

    container.innerHTML = brandConfig.social.reviews.map(r => `
        <div class="review-card bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex flex-col">
            <div class="flex items-start justify-between mb-3">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0"
                         style="background-color:${r.avatarColor}">${r.initials}</div>
                    <div>
                        <p class="font-semibold text-gray-900 text-sm leading-tight">${r.name}</p>
                        <p class="text-gray-400 text-xs">${r.location}</p>
                    </div>
                </div>
                <div class="flex-shrink-0 opacity-80">${sourceIcon(r.source)}</div>
            </div>
            <div class="flex items-center gap-0.5 mb-3">${stars(r.rating)}</div>
            <p class="text-gray-600 text-sm leading-relaxed flex-grow">"${r.text}"</p>
            <p class="text-gray-300 text-xs mt-3">${r.date}</p>
        </div>
    `).join('');
}

function loadFacebookPlugin() {
    const fbContainer = document.getElementById('facebookPagePlugin');
    if (!fbContainer) return;

    // Strip any sub-path (e.g. /reviews) — the Page Plugin needs the base page URL
    const basePageUrl = brandConfig.social.facebookPageUrl.replace(/\/(reviews|posts|about|photos).*$/, '');
    const pageUrl = encodeURIComponent(basePageUrl);
    fbContainer.innerHTML = `
        <iframe
            src="https://www.facebook.com/plugins/page.php?href=${pageUrl}&tabs=timeline&width=340&height=500&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=true"
            width="340" height="500"
            style="border:none;overflow:hidden;border-radius:12px;width:100%;max-width:340px"
            scrolling="no" frameborder="0" allowfullscreen="true"
            allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"
            loading="lazy">
        </iframe>`;
}

// Export brandConfig to window so other scripts can access it
window.brandConfig = brandConfig;

// Debug logging to verify config is loaded
console.log('✅ Config loaded! Webhook URL:', brandConfig?.webhooks?.quote);

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyBranding);
} else {
    applyBranding();
}
