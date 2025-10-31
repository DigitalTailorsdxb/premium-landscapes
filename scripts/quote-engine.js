// Premium Landscapes - Instant Quote Engine
// Multi-step conversational quote system

let currentStep = 1;
const totalSteps = 5;
let quoteData = {
    features: [],
    productDetails: {}, // Stores details for each product
    productAreas: {}, // Stores area/size for each product
    additionalNotes: '',
    area: 40,
    budget: '',
    postcode: '',
    email: '',
    phone: '',
    name: '',
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
        
        // Determine the area label and placeholder based on product type
        const areaConfig = {
            'fencing': { label: 'Length (meters)', placeholder: '25', unit: 'm' },
            'lighting': { label: 'Number of Fittings', placeholder: '8', unit: 'fittings' },
            'full-redesign': { label: 'Total Area (m²)', placeholder: '100', unit: 'm²' },
            'default': { label: 'Area (m²)', placeholder: '40', unit: 'm²' }
        };
        
        const config = areaConfig[feature] || areaConfig['default'];
        
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
                
                <!-- Material/Description Field -->
                <div class="mb-3">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Material & Details (optional)</label>
                    <textarea 
                        id="detail-${feature}" 
                        rows="2"
                        class="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:outline-none focus:border-accent transition-colors text-base"
                        placeholder="e.g., ${productExamples[feature] || 'Add details...'}"
                    ></textarea>
                </div>
                
                <!-- Area/Size Input Field -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">${config.label}</label>
                    <div class="flex gap-2">
                        <input 
                            type="number" 
                            id="area-${feature}"
                            min="1"
                            class="flex-1 px-4 py-3 rounded-lg border-2 border-gray-200 focus:outline-none focus:border-accent transition-colors text-base"
                            placeholder="${config.placeholder}"
                        />
                        <span class="flex items-center px-3 text-gray-600 bg-gray-100 rounded-lg">${config.unit}</span>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += fieldHtml;
    });
    
    // Restore previously entered details and add event listeners
    quoteData.features.forEach(feature => {
        const textarea = document.getElementById(`detail-${feature}`);
        const areaInput = document.getElementById(`area-${feature}`);
        
        // Restore values
        if (textarea && quoteData.productDetails[feature]) {
            textarea.value = quoteData.productDetails[feature];
        }
        if (areaInput && quoteData.productAreas[feature]) {
            areaInput.value = quoteData.productAreas[feature];
        }
        
        // Add event listeners
        if (textarea) {
            textarea.addEventListener('input', function() {
                quoteData.productDetails[feature] = this.value;
                updateSummary();
            });
        }
        if (areaInput) {
            areaInput.addEventListener('input', function() {
                quoteData.productAreas[feature] = this.value;
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
    delete quoteData.productAreas[feature];
    
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
    console.log('🚀 SUBMIT QUOTE FUNCTION CALLED - Version: 20251028-FINAL');
    console.log('Current quoteData:', quoteData);
    
    // Validation
    const nameInput = document.getElementById('name');
    if (!nameInput.value.trim()) {
        alert('Please enter your name');
        nameInput.focus();
        return;
    }
    
    const emailInput = document.getElementById('email');
    if (!emailInput.value.trim() || !emailInput.value.includes('@')) {
        alert('Please enter a valid email address');
        emailInput.focus();
        return;
    }
    
    quoteData.name = nameInput.value.trim();
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
        console.log('📤 SENDING TO N8N:', webhookUrl);
        console.log('📦 PAYLOAD BEING SENT:', JSON.stringify(webhookPayload, null, 2));
        
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(webhookPayload)
        });
        
        console.log('✅ n8n Response Status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('n8n Error Response:', errorText);
            throw new Error(`Webhook returned status ${response.status}: ${errorText}`);
        }
        
        // Get response text first to handle empty responses
        const responseText = await response.text();
        console.log('n8n Raw Response:', responseText);
        
        // Try to parse JSON, or use empty object if response is empty
        let result = {};
        if (responseText && responseText.trim()) {
            try {
                result = JSON.parse(responseText);
                console.log('n8n Parsed Response:', result);
            } catch (e) {
                console.warn('n8n returned non-JSON response, using demo mode');
            }
        } else {
            console.log('n8n returned empty response, using demo mode');
        }
        
        // Show success message
        showQuoteResult(result);
        
    } catch (error) {
        console.error('❌ Error submitting quote:', error);
        console.error('Error type:', error.constructor.name);
        console.error('Error message:', error.message);
        console.error('Error stack:', error.stack);
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
        // Parse budget from string like "£5k-£10k" to number
        const parseBudget = (budgetStr) => {
            if (!budgetStr) return null;
            const match = budgetStr.match(/(\d+)k/i);
            return match ? parseInt(match[1]) * 1000 : null;
        };
        
        const totalBudget = parseBudget(quoteData.budget);
        const totalArea = parseInt(quoteData.area) || 40;
        
        // Generate project title based on selected products
        const generateProjectTitle = () => {
            const productNames = {
                'patio': 'Patio',
                'decking': 'Decking',
                'turf': 'Lawn',
                'driveway': 'Driveway',
                'fencing': 'Fencing',
                'lighting': 'Lighting',
                'full-redesign': 'Complete Garden Redesign',
                'other': 'Custom Garden'
            };
            
            const features = quoteData.features.map(f => productNames[f] || f).join(' & ');
            return features ? `${features} Installation` : 'Garden Transformation';
        };
        
        // Transform simple products array into detailed objects for n8n
        const transformProducts = () => {
            return quoteData.features.map(feature => {
                const description = quoteData.productDetails[feature] || '';
                
                // Use dedicated area field if provided, otherwise parse from description or use default
                const dedicatedArea = quoteData.productAreas[feature];
                const defaultArea = Math.round(totalArea / quoteData.features.length);
                
                // Parse material from description
                const extractMaterial = (text) => {
                    const lowerText = text.toLowerCase();
                    
                    if (lowerText.includes('porcelain')) return 'porcelain';
                    if (lowerText.includes('sandstone') || lowerText.includes('indian')) return 'indian sandstone';
                    if (lowerText.includes('composite')) return 'composite';
                    if (lowerText.includes('artificial')) return 'artificial grass';
                    if (lowerText.includes('block')) return 'block paving';
                    if (lowerText.includes('close board') || lowerText.includes('close-board')) return 'close board';
                    
                    return 'standard';
                };
                
                const material = extractMaterial(description);
                
                // Base product structure
                const product = {
                    type: feature,
                    description: description || `${feature} installation`,
                    material: material,
                    unitType: (feature === 'fencing' || feature === 'lighting') ? 'qty' : 'm2'
                };
                
                // Add type-specific fields using dedicated area input
                if (feature === 'patio' || feature === 'driveway') {
                    product.area_m2 = dedicatedArea ? parseInt(dedicatedArea) : defaultArea;
                    product.edging = description.toLowerCase().includes('edging') ? 'standard edging' : 'none';
                    product.includeDrainage = true;
                } else if (feature === 'decking') {
                    product.area_m2 = dedicatedArea ? parseInt(dedicatedArea) : defaultArea;
                    product.raised = description.toLowerCase().includes('raised');
                    product.steps = description.toLowerCase().includes('step') ? 3 : 0;
                    product.balustrade = description.toLowerCase().includes('glass') ? 'glass panels' : 'none';
                } else if (feature === 'turf') {
                    product.area_m2 = dedicatedArea ? parseInt(dedicatedArea) : defaultArea;
                    product.includeEdging = true;
                } else if (feature === 'fencing') {
                    product.length_m = dedicatedArea ? parseInt(dedicatedArea) : 20;
                    product.height_m = 1.8;
                } else if (feature === 'lighting') {
                    product.fittings = dedicatedArea ? parseInt(dedicatedArea) : 8;
                    product.wattagePerFitting = 6;
                    product.control = 'standard switch';
                } else {
                    product.area_m2 = dedicatedArea ? parseInt(dedicatedArea) : defaultArea;
                }
                
                return product;
            });
        };
        
        // Build n8n-compatible payload
        return {
            customer: {
                name: quoteData.name || 'Unknown',
                email: quoteData.email,
                phone: quoteData.phone || '',
                postcode: quoteData.postcode,
                address: `${quoteData.postcode}, UK` // Generate basic address from postcode
            },
            project: {
                title: generateProjectTitle(),
                totalArea_m2: totalArea,
                totalBudget_gbp: totalBudget,
                layoutType: 'standard', // Default value
                sunlight: 'partial sun', // Default value
                stylePreference: 'contemporary', // Default value
                maintenanceLevel: 'low maintenance', // Default value
                siteConditions: {
                    access: 'standard access',
                    soilType: 'loam',
                    drainage: 'good'
                },
                products: transformProducts(),
                extras: {
                    pergola: { include: false },
                    firePit: { include: false },
                    waterFeature: { include: false }
                },
                notes: quoteData.additionalNotes || 'Website quote request'
            }
        };
    });
}

// ============================================================================
// CONFIDENCE SCORE CALCULATION
// Based on data completeness for accurate pricing - the more info, the higher the score
// ============================================================================
function calculateConfidenceScore() {
    let score = 30; // Base score (lower starting point)
    
    // 1. Products selected (up to +15 points)
    const productCount = quoteData.features.length;
    if (productCount > 0) score += Math.min(productCount * 3, 15);
    
    // 2. Area sizes provided for products (up to +20 points)
    const areasProvided = Object.keys(quoteData.productAreas).filter(key => {
        const value = quoteData.productAreas[key];
        return value && value > 0;
    }).length;
    if (areasProvided > 0) {
        score += Math.min(areasProvided * 5, 20);
    }
    
    // 3. Product descriptions/materials (up to +15 points)
    const detailedDescriptions = Object.values(quoteData.productDetails).filter(desc => {
        return desc && desc.length > 10;
    }).length;
    if (detailedDescriptions > 0) {
        score += Math.min(detailedDescriptions * 3, 15);
    }
    
    // 4. Budget selected (+10 points)
    if (quoteData.budget && quoteData.budget.length > 0) score += 10;
    
    // 5. Total area provided (+8 points)
    if (quoteData.area && quoteData.area > 0) score += 8;
    
    // 6. Location/Postcode provided (+10 points)
    if (quoteData.postcode && quoteData.postcode.length >= 5) score += 10;
    
    // 7. Photos uploaded (+12 points - visual data is valuable)
    if (quoteData.files.length > 0) score += 12;
    if (quoteData.files.length >= 3) score += 5; // Bonus for multiple photos
    
    // 8. Contact details complete (+5 points)
    if (quoteData.name && quoteData.email) score += 5;
    if (quoteData.phone && quoteData.phone.length >= 10) score += 3;
    
    // 9. Additional notes provided (+2 points)
    if (quoteData.additionalNotes && quoteData.additionalNotes.length > 20) score += 2;
    
    return Math.min(score, 95); // Cap at 95% (never 100% without site visit)
}

// ============================================================================
// DISPLAY QUOTE RESULT
// Shows confirmation message - actual quote sent via email from n8n
// ============================================================================
function showQuoteResult(data) {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('quoteResult').classList.remove('hidden');
    
    console.log('✅ Quote request submitted successfully!');
    console.log('Customer will receive detailed PDF quote via email from n8n workflow');
    
    // Scroll to result
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
