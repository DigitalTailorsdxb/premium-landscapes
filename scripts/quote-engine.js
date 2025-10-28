// Premium Landscapes - Instant Quote Engine
// Multi-step conversational quote system

let currentStep = 1;
const totalSteps = 5;
let quoteData = {
    features: [],
    productDetails: {}, // Stores details for each product
    additionalNotes: '',
    area: 40,
    budget: '',
    postcode: '',
    email: '',
    phone: '',
    aiDesign: false,
    files: []
};

// Product examples for suggestions
const productExamples = {
    'patio': 'Indian sandstone patio 40 sqm',
    'decking': 'Composite decking 30 sqm',
    'turf': 'Artificial turf 25 sqm with drainage',
    'driveway': 'Block paving driveway 50 sqm',
    'fencing': '20 meters close-board fencing 1.8m high',
    'lighting': 'LED garden lighting system with 10 uplights',
    'full-redesign': 'Complete garden transformation',
    'other': 'Additional features'
};

// Initialize quote engine
document.addEventListener('DOMContentLoaded', function() {
    initializeFeatureCards();
    initializeAreaSlider();
    initializeBudgetOptions();
    initializeFileUpload();
    initializeFileUploadStep5();
    initializeAddProductButtons();
    updateSummary();
});

// Feature card selection
function initializeFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('click', function() {
            const feature = this.dataset.feature;
            this.classList.toggle('selected');
            
            if (this.classList.contains('selected')) {
                if (!quoteData.features.includes(feature)) {
                    quoteData.features.push(feature);
                    quoteData.productDetails[feature] = ''; // Initialize with empty details
                }
            } else {
                quoteData.features = quoteData.features.filter(f => f !== feature);
                delete quoteData.productDetails[feature];
            }
            
            updateSummary();
        });
    });
}

// Build product detail fields for Step 2
function buildProductDetailFields() {
    const container = document.getElementById('productDetailFields');
    container.innerHTML = '';
    
    quoteData.features.forEach((feature, index) => {
        const featureName = feature.charAt(0).toUpperCase() + feature.slice(1).replace('-', ' ');
        const fieldHtml = `
            <div class="bg-stone p-5 rounded-xl border-2 border-gray-200 product-detail-field" data-feature="${feature}">
                <div class="flex justify-between items-center mb-3">
                    <h4 class="font-semibold text-gray-900 flex items-center">
                        <i class="fas fa-th-large text-primary mr-2"></i>
                        ${featureName}
                    </h4>
                    <button type="button" onclick="removeProduct('${feature}')" class="text-red-500 hover:text-red-700 text-sm">
                        <i class="fas fa-times mr-1"></i> Remove
                    </button>
                </div>
                <textarea 
                    id="detail-${feature}" 
                    rows="2"
                    class="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:outline-none focus:border-accent transition-colors text-base"
                    placeholder="e.g., ${productExamples[feature] || 'Add details...'}"
                ></textarea>
            </div>
        `;
        container.innerHTML += fieldHtml;
    });
    
    // Restore previously entered details
    quoteData.features.forEach(feature => {
        const textarea = document.getElementById(`detail-${feature}`);
        if (textarea && quoteData.productDetails[feature]) {
            textarea.value = quoteData.productDetails[feature];
        }
        
        // Add event listener to save details
        if (textarea) {
            textarea.addEventListener('input', function() {
                quoteData.productDetails[feature] = this.value;
                updateSummary();
            });
        }
    });
    
    // Also listen to additional notes
    const additionalNotes = document.getElementById('additionalNotes');
    if (additionalNotes) {
        additionalNotes.value = quoteData.additionalNotes;
        additionalNotes.addEventListener('input', function() {
            quoteData.additionalNotes = this.value;
        });
    }
}

// Remove product
function removeProduct(feature) {
    quoteData.features = quoteData.features.filter(f => f !== feature);
    delete quoteData.productDetails[feature];
    
    // Update Step 1 visual
    const featureCard = document.querySelector(`.feature-card[data-feature="${feature}"]`);
    if (featureCard) {
        featureCard.classList.remove('selected');
    }
    
    buildProductDetailFields();
    updateSummary();
}

// Show add product menu
function showAddProductMenu() {
    document.getElementById('addProductModal').classList.remove('hidden');
}

// Close add product menu
function closeAddProductMenu() {
    document.getElementById('addProductModal').classList.add('hidden');
}

// Initialize add product buttons in modal
function initializeAddProductButtons() {
    const addProductBtns = document.querySelectorAll('.add-product-btn');
    addProductBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const feature = this.dataset.feature;
            
            if (!quoteData.features.includes(feature)) {
                quoteData.features.push(feature);
                quoteData.productDetails[feature] = '';
                
                // Update Step 1 visual
                const featureCard = document.querySelector(`.feature-card[data-feature="${feature}"]`);
                if (featureCard) {
                    featureCard.classList.add('selected');
                }
                
                buildProductDetailFields();
                updateSummary();
            }
            
            closeAddProductMenu();
        });
    });
}

// Area slider
function initializeAreaSlider() {
    const slider = document.getElementById('areaSlider');
    const valueDisplay = document.getElementById('areaValue');
    
    if (slider) {
        slider.addEventListener('input', function() {
            quoteData.area = this.value;
            valueDisplay.textContent = this.value;
            updateSummary();
        });
    }
}

// Budget options
function initializeBudgetOptions() {
    const budgetOptions = document.querySelectorAll('.budget-option');
    
    budgetOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove selected from all
            budgetOptions.forEach(opt => opt.classList.remove('selected', 'border-accent', 'bg-stone'));
            
            // Add selected to this one
            this.classList.add('selected', 'border-accent', 'bg-stone');
            quoteData.budget = this.dataset.budget;
            updateSummary();
        });
    });
}

// File upload with drag & drop (Step 4)
function initializeFileUpload() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    
    if (!dropZone || !fileInput) return;
    
    // Click to upload
    dropZone.addEventListener('click', () => fileInput.click());
    
    // Drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-accent', 'bg-stone');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('border-accent', 'bg-stone');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-accent', 'bg-stone');
        handleFiles(e.dataTransfer.files);
    });
    
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
    
    function handleFiles(files) {
        quoteData.files = Array.from(files);
        displayFilePreview(files, filePreview);
        updateSummary();
        updateAIDesignVisibility();
    }
}

// File upload for Step 5
function initializeFileUploadStep5() {
    const dropZone = document.getElementById('dropZoneStep5');
    const fileInput = document.getElementById('fileInputStep5');
    const filePreview = document.getElementById('filePreviewStep5');
    
    if (!dropZone || !fileInput) return;
    
    // Click to upload
    dropZone.addEventListener('click', () => fileInput.click());
    
    // Drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('bg-white');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('bg-white');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('bg-white');
        handleFilesStep5(e.dataTransfer.files);
    });
    
    fileInput.addEventListener('change', (e) => {
        handleFilesStep5(e.target.files);
    });
    
    function handleFilesStep5(files) {
        quoteData.files = Array.from(files);
        displayFilePreview(files, filePreview);
        updateSummary();
        updateAIDesignVisibility();
    }
}

function displayFilePreview(files, previewContainer) {
    previewContainer.innerHTML = '';
    Array.from(files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.createElement('div');
            preview.className = 'relative';
            preview.innerHTML = `
                <img src="${e.target.result}" class="w-full h-24 object-cover rounded-lg border-2 border-accent" alt="Preview ${index + 1}">
                <button type="button" onclick="removeFile(${index})" class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full text-xs hover:bg-red-600">×</button>
            `;
            previewContainer.appendChild(preview);
        };
        reader.readAsDataURL(file);
    });
}

function removeFile(index) {
    quoteData.files.splice(index, 1);
    
    // Update both file previews
    const filePreview = document.getElementById('filePreview');
    const filePreviewStep5 = document.getElementById('filePreviewStep5');
    
    if (quoteData.files.length > 0) {
        displayFilePreview(quoteData.files, filePreview);
        displayFilePreview(quoteData.files, filePreviewStep5);
    } else {
        filePreview.innerHTML = '';
        filePreviewStep5.innerHTML = '';
    }
    
    updateAIDesignVisibility();
    updateSummary();
}

// Update AI design section visibility based on whether photos are uploaded
function updateAIDesignVisibility() {
    const aiDesignSection = document.getElementById('aiDesignSection');
    const noPhotoPrompt = document.getElementById('noPhotoPrompt');
    
    if (quoteData.files.length > 0) {
        // Show AI design checkbox
        aiDesignSection.classList.remove('hidden');
        noPhotoPrompt.classList.add('hidden');
    } else {
        // Hide checkbox, show upload prompt
        aiDesignSection.classList.add('hidden');
        noPhotoPrompt.classList.remove('hidden');
    }
}

// Navigation functions
function nextStep() {
    // Validation
    if (currentStep === 1 && quoteData.features.length === 0) {
        alert('Please select at least one feature');
        return;
    }
    
    if (currentStep === 4) {
        const postcodeInput = document.getElementById('postcode');
        if (!postcodeInput.value.trim()) {
            alert('Please enter your postcode');
            postcodeInput.focus();
            return;
        }
        quoteData.postcode = postcodeInput.value.trim();
    }
    
    // Hide current step
    document.getElementById(`step${currentStep}`).classList.add('hidden');
    
    // Show next step
    currentStep++;
    document.getElementById(`step${currentStep}`).classList.remove('hidden');
    
    // Build product detail fields when entering step 2
    if (currentStep === 2) {
        buildProductDetailFields();
    }
    
    // Update AI design visibility when entering step 5
    if (currentStep === 5) {
        updateAIDesignVisibility();
    }
    
    // Update progress
    updateProgress();
    updateSummary();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function prevStep() {
    // Hide current step
    document.getElementById(`step${currentStep}`).classList.add('hidden');
    
    // Show previous step
    currentStep--;
    document.getElementById(`step${currentStep}`).classList.remove('hidden');
    
    // Update progress
    updateProgress();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateProgress() {
    const percentage = (currentStep / totalSteps) * 100;
    document.getElementById('progressBar').style.width = `${percentage}%`;
    document.getElementById('progressText').textContent = `Step ${currentStep} of ${totalSteps}`;
    document.getElementById('progressPercent').textContent = `${Math.round(percentage)}%`;
}

// Update live summary
function updateSummary() {
    const summaryContent = document.getElementById('summaryContent');
    let html = '';
    
    if (quoteData.features.length > 0) {
        html += '<div class="space-y-2">';
        quoteData.features.forEach(feature => {
            const featureName = feature.charAt(0).toUpperCase() + feature.slice(1).replace('-', ' ');
            const details = quoteData.productDetails[feature] || '';
            const displayText = details ? details.substring(0, 30) + (details.length > 30 ? '...' : '') : featureName;
            
            html += `
                <div class="summary-item flex items-center space-x-2 bg-stone px-3 py-2 rounded-lg">
                    <i class="fas fa-check-circle text-accent"></i>
                    <span class="text-sm font-semibold">${displayText}</span>
                </div>
            `;
        });
        html += '</div>';
    }
    
    if (quoteData.area && quoteData.area != 40) {
        html += `
            <div class="summary-item bg-stone px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-ruler-combined text-accent mr-2"></i>Area: <strong>${quoteData.area} m²</strong></p>
            </div>
        `;
    }
    
    if (quoteData.budget) {
        html += `
            <div class="summary-item bg-stone px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-pound-sign text-accent mr-2"></i>Budget: <strong>${quoteData.budget}</strong></p>
            </div>
        `;
    }
    
    if (quoteData.postcode) {
        html += `
            <div class="summary-item bg-stone px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-map-marker-alt text-accent mr-2"></i>Location: <strong>${quoteData.postcode}</strong></p>
            </div>
        `;
    }
    
    if (quoteData.files.length > 0) {
        html += `
            <div class="summary-item bg-stone px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-image text-accent mr-2"></i>Photos: <strong>${quoteData.files.length} uploaded</strong></p>
            </div>
        `;
    }
    
    if (html === '') {
        html = '<p class="text-gray-500 text-sm italic">Select features to see your summary...</p>';
    }
    
    summaryContent.innerHTML = html;
}

// Submit quote
async function submitQuote() {
    // Validation
    const emailInput = document.getElementById('email');
    if (!emailInput.value.trim() || !emailInput.value.includes('@')) {
        alert('Please enter a valid email address');
        emailInput.focus();
        return;
    }
    
    quoteData.email = emailInput.value.trim();
    
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        quoteData.phone = phoneInput.value.trim();
    }
    
    const aiDesignCheckbox = document.getElementById('aiDesign');
    if (aiDesignCheckbox && !aiDesignCheckbox.disabled) {
        quoteData.aiDesign = aiDesignCheckbox.checked;
    }
    
    // Hide form, show loading
    document.getElementById('step5').classList.add('hidden');
    document.getElementById('loadingState').classList.remove('hidden');
    
    // ============================================================================
    // WEBHOOK INTEGRATION POINT - Ready for Make.com/n8n Connection
    // ============================================================================
    
    // Structure data for n8n workflow
    const webhookPayloadPromise = prepareWebhookPayload();
    
    try {
        const webhookPayload = await webhookPayloadPromise;
        console.log('Quote Data for n8n Webhook:', webhookPayload);
        
        // Get webhook URL from config
        const webhookUrl = brandConfig?.webhooks?.quote;
        
        // Check if webhook URL is configured
        if (!webhookUrl || webhookUrl.includes('your-quote-webhook-url')) {
            console.warn('⚠️ Webhook URL not configured. Using demo mode.');
            console.log('To enable live quotes, update the webhook URL in scripts/config.js');
            console.log('Your n8n webhook path should be: /webhook/premium-landscapes-quote');
            
            // Demo mode: Show quote after 2 seconds
            setTimeout(() => {
                showQuoteResult();
            }, 2000);
            return;
        }
        
        // Send to n8n workflow
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(webhookPayload)
        });
        
        if (!response.ok) {
            throw new Error(`Webhook returned status ${response.status}`);
        }
        
        const result = await response.json();
        console.log('n8n Response:', result);
        
        // Show success message
        showQuoteResult(result);
        
    } catch (error) {
        console.error('Error submitting quote:', error);
        alert('There was an error processing your quote. Please try again or contact us at 07444 887813');
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('step5').classList.remove('hidden');
    }
}

// ============================================================================
// WEBHOOK PAYLOAD PREPARATION
// Structures data for n8n pricing workflow
// ============================================================================
function prepareWebhookPayload() {
    // Build product details with descriptions
    const productDetails = {};
    quoteData.features.forEach(feature => {
        productDetails[feature] = quoteData.productDetails[feature] || '';
    });
    
    // Upload files as base64 for AI analysis (optional)
    const filePromises = quoteData.files.map(file => {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve({
                name: file.name,
                type: file.type,
                size: file.size,
                data: e.target.result  // base64 data URL
            });
            reader.readAsDataURL(file);
        });
    });
    
    return Promise.all(filePromises).then(filesData => {
        return {
            // Customer Information (required by n8n workflow)
            customer: {
                name: quoteData.email.split('@')[0], // Extract name from email
                email: quoteData.email,
                phone: quoteData.phone || '',
                postcode: quoteData.postcode,
            },
            
            // Project Details - products as simple array of strings (n8n expects this format)
            project: {
                products: quoteData.features, // Simple array: ['patio', 'decking', 'turf']
                productDetails: productDetails, // Detailed descriptions for each product
                additionalNotes: quoteData.additionalNotes || '',
                area: parseInt(quoteData.area) || 40,
                budget: quoteData.budget || '',
            },
            
            // Files for AI Vision Analysis (optional)
            files: filesData,
            
            // Options
            aiDesign: quoteData.aiDesign || false,
            
            // Metadata
            timestamp: new Date().toISOString(),
            source: 'website',
            confidence: calculateConfidenceScore(),
        };
    });
}

// ============================================================================
// CONFIDENCE SCORE CALCULATION
// Based on data completeness for accurate pricing
// ============================================================================
function calculateConfidenceScore() {
    let score = 50; // Base score
    
    // Add points for data completeness
    if (quoteData.features.length > 0) score += 10;
    if (quoteData.area && quoteData.area > 0) score += 15;
    if (quoteData.postcode) score += 10;
    if (quoteData.files.length > 0) score += 15; // Photos help AI estimate
    
    // Add points for detailed descriptions
    const hasDetailedDescriptions = quoteData.features.some(feature => {
        const details = quoteData.productDetails[feature];
        return details && details.length > 20;
    });
    if (hasDetailedDescriptions) score += 10;
    
    return Math.min(score, 95); // Cap at 95% (never 100% without site visit)
}

// ============================================================================
// DISPLAY QUOTE RESULT
// Handles both demo data and real webhook responses
// ============================================================================
function showQuoteResult(data) {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('quoteResult').classList.remove('hidden');
    
    const breakdown = document.getElementById('quoteBreakdown');
    
    // If real data from webhook, use it
    if (data && data.breakdown && data.totalLow && data.totalHigh) {
        // Real webhook response - calculate single estimated figure
        const totalEstimate = Math.round((data.totalLow + data.totalHigh) / 2);
        
        let breakdownHTML = '';
        data.breakdown.forEach(item => {
            const itemEstimate = Math.round((item.low + item.high) / 2);
            breakdownHTML += `
                <div class="flex justify-between items-center py-2 border-b">
                    <span class="text-gray-700">${item.description}</span>
                    <span class="font-semibold">£${itemEstimate.toLocaleString()}</span>
                </div>
            `;
        });
        
        breakdownHTML += `
            <div class="flex justify-between items-center py-3 font-bold text-lg">
                <span class="text-primary">Total Estimate (inc. VAT)</span>
                <span class="text-primary">£${totalEstimate.toLocaleString()}</span>
            </div>
        `;
        
        breakdown.innerHTML = breakdownHTML;
        
    } else {
        // Demo mode - show example breakdown with single estimated figure
        breakdown.innerHTML = `
            <div class="flex justify-between items-center py-2 border-b">
                <span class="text-gray-700">Materials & Installation</span>
                <span class="font-semibold">£7,850</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b">
                <span class="text-gray-700">Base Preparation & Excavation</span>
                <span class="font-semibold">£1,500</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b">
                <span class="text-gray-700">Waste Removal (3 skips)</span>
                <span class="font-semibold">£750</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b">
                <span class="text-gray-700">Project Management & Overhead</span>
                <span class="font-semibold">£1,000</span>
            </div>
            <div class="flex justify-between items-center py-3 font-bold text-lg">
                <span class="text-primary">Total Estimate (inc. VAT)</span>
                <span class="text-primary">£11,100</span>
            </div>
            <p class="text-xs text-gray-500 mt-2 text-center">
                <i class="fas fa-info-circle mr-1"></i>
                Demo pricing - Connect n8n for accurate regional quotes
            </p>
        `;
    }
    
    // Scroll to result
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================================================
// EMAIL QUOTE FUNCTION
// Triggers Make.com webhook to send PDF via email
// ============================================================================
function emailQuote() {
    alert(`Quote will be emailed to: ${quoteData.email}\n\nIn production, this will trigger an automated email with PDF attachment.`);
    console.log('Email quote to:', quoteData.email);
    
    // ============================================================================
    // PRODUCTION IMPLEMENTATION - Email webhook
    // ============================================================================
    // const emailWebhookUrl = window.CONFIG?.emailWebhookUrl || 'https://hook.eu1.make.com/your-email-webhook';
    // 
    // fetch(emailWebhookUrl, {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({
    //         email: quoteData.email,
    //         quoteData: quoteData,
    //         sendPDF: true,
    //         timestamp: new Date().toISOString()
    //     })
    // });
}
