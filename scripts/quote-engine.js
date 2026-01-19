// Premium Landscapes - Instant Quote Engine
// Multi-step conversational quote system

let currentStep = 1;
const totalSteps = 6;
let quoteData = {
    quoteMode: '', // 'full-redesign' or 'individual-products'
    features: [],
    productDetails: {}, // Stores details for each product
    productAreas: {}, // Stores area/size for each product
    additionalNotes: '',
    designVisionNotes: '', // Design vision & requirements for full redesign
    area: 40,
    budget: '',
    postcode: '',
    email: '',
    phone: '',
    name: '',
    aiDesign: false,
    files: []
};

// Prevent double submission
let isSubmittingQuote = false;

// Progress animation state for full redesign quotes
let progressState = {
    currentStep: 0,
    totalSteps: 7,
    isAnimating: false,
    webhookComplete: false,
    webhookSuccess: false,
    webhookResult: null,
    aiDesignEnabled: false,
    aiDesignWebhookComplete: false,
    timeouts: []
};

// ============================================================================
// PROGRESS ANIMATION TIMING - UI runs independently of webhook
// Total: 60 seconds (quote only) or 120 seconds (with AI Design)
// ============================================================================

// Base step timings - Total: ~30s
const baseStepDurations = [
    5000,  // 0: Reading requirements (5s)
    5000,  // 1: Planning structure (5s)
    8000,  // 2: Building design (8s)
    6000,  // 3: Mapping products (6s)
    6000   // 4: Building PDF (6s)
];

// AI Design step timings - Total: ~60s (adds 60s to reach 120s total)
const aiDesignStepDurations = [
    18000, // Analyzing garden photo... (18s)
    22000, // Creating photorealistic designs... (22s)
    18000  // AI designs ready! (18s)
];

// Final steps - Total: ~30s for quote only, ~2s for AI mode
const finalStepDurations = [
    28000, // Sending email (28s - adjusted dynamically for AI mode)
    2000   // Done! (2s)
];

// Reset progress timeline to initial state
function resetProgressTimeline() {
    const aiDesignEnabled = quoteData.aiDesign === true;
    
    progressState = {
        currentStep: 0,
        totalSteps: aiDesignEnabled ? 10 : 7,
        isAnimating: false,
        webhookComplete: false,
        webhookSuccess: false,
        webhookResult: null,
        aiDesignEnabled: aiDesignEnabled,
        aiDesignWebhookComplete: false,
        timeouts: []
    };
    
    // Reset all step states
    const steps = document.querySelectorAll('#progressTimeline .progress-step');
    steps.forEach(step => {
        step.classList.remove('active', 'completed', 'error');
    });
    
    // Show/hide AI design steps based on checkbox
    const aiDesignSteps = document.querySelectorAll('#progressTimeline .ai-design-step');
    aiDesignSteps.forEach(step => {
        if (aiDesignEnabled) {
            step.classList.remove('hidden');
        } else {
            step.classList.add('hidden');
        }
    });
    
    console.log(`🎨 Progress timeline reset - AI Design: ${aiDesignEnabled ? 'ENABLED (+45s)' : 'DISABLED'}, Total steps: ${progressState.totalSteps}`);
}

// Start the progress animation
function startProgressAnimation() {
    progressState.isAnimating = true;
    advanceProgressStep(0);
}

// Get step duration for any step based on AI design mode
function getStepDuration(stepIndex) {
    const aiEnabled = progressState.aiDesignEnabled;
    
    // Base steps (0-4): Reading, Planning, Building design, Mapping, Building PDF
    if (stepIndex < baseStepDurations.length) {
        return baseStepDurations[stepIndex];
    }
    
    if (aiEnabled) {
        // With AI Design: steps 5-7 are AI steps, 8-9 are final steps
        const aiStepOffset = stepIndex - baseStepDurations.length;
        if (aiStepOffset < aiDesignStepDurations.length) {
            return aiDesignStepDurations[aiStepOffset];
        }
        const finalStepOffset = aiStepOffset - aiDesignStepDurations.length;
        if (finalStepOffset < finalStepDurations.length) {
            return finalStepDurations[finalStepOffset];
        }
    } else {
        // Without AI Design: steps 5-6 are final steps
        const finalStepOffset = stepIndex - baseStepDurations.length;
        if (finalStepOffset < finalStepDurations.length) {
            return finalStepDurations[finalStepOffset];
        }
    }
    
    return 0;
}

// Get the index of the "Sending email" step (varies based on AI mode)
function getSendingEmailStepIndex() {
    return progressState.aiDesignEnabled ? 8 : 5;
}

// Get the index of the "Done" step (varies based on AI mode)
function getDoneStepIndex() {
    return progressState.aiDesignEnabled ? 9 : 6;
}

// Advance to the next progress step
// Animation runs on fixed timer - independent of webhook response
function advanceProgressStep(stepIndex) {
    if (!progressState.isAnimating) return;
    
    const steps = document.querySelectorAll('#progressTimeline .progress-step:not(.hidden)');
    const totalVisibleSteps = steps.length;
    const doneStep = getDoneStepIndex();
    
    // Mark previous step as completed
    if (stepIndex > 0 && stepIndex <= totalVisibleSteps) {
        steps[stepIndex - 1].classList.remove('active');
        steps[stepIndex - 1].classList.add('completed');
    }
    
    // Mark current step as active
    if (stepIndex < totalVisibleSteps) {
        steps[stepIndex].classList.add('active');
        progressState.currentStep = stepIndex;
        
        const stepDuration = getStepDuration(stepIndex);
        
        // If this is the final "Done" step, complete animation
        if (stepIndex === doneStep) {
            const timeout = setTimeout(() => {
                steps[stepIndex].classList.remove('active');
                steps[stepIndex].classList.add('completed');
                completeProgressAnimation();
            }, stepDuration);
            progressState.timeouts.push(timeout);
            return;
        }
        
        // Schedule next step
        if (stepDuration > 0) {
            const timeout = setTimeout(() => {
                advanceProgressStep(stepIndex + 1);
            }, stepDuration);
            progressState.timeouts.push(timeout);
        }
    }
}

// Called when webhook completes (logged for debugging, UI doesn't wait)
function onWebhookComplete(success, result) {
    progressState.webhookComplete = true;
    progressState.webhookSuccess = success;
    progressState.webhookResult = result;
    
    if (success) {
        console.log('✅ Webhook completed successfully (UI running independently)');
    } else {
        console.warn('⚠️ Webhook returned error (UI continues independently):', result?.error || result?.message);
    }
}

// Complete the progress animation and show result
// Always shows success - UI runs independently of webhook
function completeProgressAnimation() {
    progressState.isAnimating = false;
    
    // Clear any remaining timeouts
    progressState.timeouts.forEach(t => clearTimeout(t));
    progressState.timeouts = [];
    
    // Hide loading state and show success result
    document.getElementById('loadingStateRedesign').classList.add('hidden');
    
    // Always show success - the quote was submitted, email is on the way
    showQuoteResult(progressState.webhookResult || { success: true });
}

// Stop progress animation (for errors)
function stopProgressAnimation() {
    progressState.isAnimating = false;
    progressState.timeouts.forEach(t => clearTimeout(t));
    progressState.timeouts = [];
}

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
    initializeQuoteModeCards();
    initializeFeatureCards();
    initializeAreaSlider();
    initializeBudgetOptions();
    initializeFileUpload();
    initializeFileUploadStep5();
    initializeAddProductButtons();
    initializePostcodeLookup();
    initializeDesignVisionNotes();
    updateSummary();
});

// Initialize design vision notes field (for full redesign mode)
function initializeDesignVisionNotes() {
    const designVisionNotes = document.getElementById('designVisionNotes');
    if (designVisionNotes) {
        designVisionNotes.addEventListener('input', function() {
            quoteData.designVisionNotes = this.value;
            updateSummary();
        });
    }
}

// Quote mode card selection (Step 1 - mutually exclusive)
function initializeQuoteModeCards() {
    const modeCards = document.querySelectorAll('.quote-mode-card');
    modeCards.forEach(card => {
        card.addEventListener('click', function() {
            const mode = this.dataset.mode;
            
            // Remove selected class from all mode cards
            modeCards.forEach(c => c.classList.remove('selected'));
            
            // Add selected to clicked card
            this.classList.add('selected');
            
            // Set quote mode
            quoteData.quoteMode = mode;
            
            // Clear features and set mode
            quoteData.features = [];
            quoteData.productDetails = {};
            quoteData.productAreas = {};
            
            if (mode === 'full-redesign') {
                quoteData.features.push('full-redesign');
            } else if (mode === 'individual-products') {
                // Individual products mode - user will select products in Step 2
                quoteData.features = [];
            }
            
            console.log('✅ Quote mode selected:', mode);
            updateSummary();
        });
    });
}

// Feature card selection (for individual products in Step 2)
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
    
    // Listen to design vision notes (for full redesign mode)
    const designVisionNotes = document.getElementById('designVisionNotes');
    if (designVisionNotes) {
        designVisionNotes.value = quoteData.designVisionNotes;
        designVisionNotes.addEventListener('input', function() {
            quoteData.designVisionNotes = this.value;
            updateSummary();
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

// Custom budget input (mandatory for full redesign)
function initializeBudgetOptions() {
    const budgetInput = document.getElementById('customBudgetInput');
    
    if (budgetInput) {
        budgetInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value && value > 0) {
                quoteData.budget = value;
                updateSummary();
            } else {
                quoteData.budget = null;
            }
        });
    }
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

function initializePostcodeLookup() {
    console.log('✅ Address form ready - manual entry mode');
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

// Update AI design description based on whether photos are uploaded
function updateAIDesignVisibility() {
    const aiDesignDescription = document.getElementById('aiDesignDescription');
    
    if (!aiDesignDescription) return;
    
    if (quoteData.files.length > 0) {
        // With photos - image-based design
        aiDesignDescription.textContent = 'Based on your uploaded photos, we\'ll transform your current garden into stunning AI-generated design concepts and email them within 90 seconds';
    } else {
        // Without photos - budget-based design
        aiDesignDescription.textContent = 'Based on your budget and preferences, we\'ll generate photorealistic design concepts and email them to you within 90 seconds';
    }
}

// Navigation functions
function nextStep() {
    // Step 1: Validate quote mode selection
    if (currentStep === 1 && !quoteData.quoteMode) {
        alert('Please select a quote option: Complete Garden Redesign or Select Individual Products');
        return;
    }
    
    // Step 2: Validate products selected for individual-products mode
    if (currentStep === 2 && quoteData.quoteMode === 'individual-products' && quoteData.features.length === 0) {
        alert('Please select at least one product');
        return;
    }
    
    // Step 3: Garden size (m²) is mandatory for Full Garden Redesign
    if (currentStep === 3 && quoteData.quoteMode === 'full-redesign') {
        const areaValue = parseInt(document.getElementById('areaSlider')?.value) || 0;
        if (areaValue < 10) {
            alert('Please set your garden size using the slider');
            return;
        }
        // Store the area value
        quoteData.area = areaValue;
    }
    
    if (currentStep === 4) {
        const postcodeInput = document.getElementById('postcode');
        if (!postcodeInput.value.trim()) {
            alert('Please enter your postcode');
            postcodeInput.focus();
            return;
        }
        quoteData.postcode = postcodeInput.value.trim().toUpperCase();
        
        // Capture all address fields from manual entry
        const cityInput = document.getElementById('city');
        const streetInput = document.getElementById('street');
        const houseNumberInput = document.getElementById('houseNumber');
        
        if (cityInput) quoteData.city = cityInput.value.trim();
        if (streetInput) quoteData.street = streetInput.value.trim();
        if (houseNumberInput) quoteData.houseNumber = houseNumberInput.value.trim();
    }
    
    // Step 5: Validate contact details
    if (currentStep === 5) {
        const nameInput = document.getElementById('name');
        const emailInput = document.getElementById('email');
        const phoneInput = document.getElementById('phone');
        
        if (!nameInput.value.trim()) {
            alert('Please enter your name');
            nameInput.focus();
            return;
        }
        if (!emailInput.value.trim() || !emailInput.value.includes('@')) {
            alert('Please enter a valid email address');
            emailInput.focus();
            return;
        }
        if (!phoneInput.value.trim()) {
            alert('Please enter your phone number');
            phoneInput.focus();
            return;
        }
        
        // Store contact details
        quoteData.name = nameInput.value.trim();
        quoteData.email = emailInput.value.trim();
        quoteData.phone = phoneInput.value.trim();
    }
    
    // Hide current step
    document.getElementById(`step${currentStep}`).classList.add('hidden');
    
    // Show next step
    currentStep++;
    
    // Special handling for Step 2: detect Full Redesign mode
    if (currentStep === 2) {
        updateStep2Mode();
    }
    document.getElementById(`step${currentStep}`).classList.remove('hidden');
    
    // Build product detail fields when entering step 2
    if (currentStep === 2) {
        buildProductDetailFields();
    }
    
    // Update AI design visibility when entering step 5
    if (currentStep === 5) {
        updateAIDesignVisibility();
    }
    
    // Initialize AI upload handlers when entering step 6
    if (currentStep === 6) {
        setTimeout(initAIUploadHandlers, 100);
        // Set aiDesign to true by default in step 6
        const aiDesignCheckbox = document.getElementById('aiDesign');
        if (aiDesignCheckbox) {
            aiDesignCheckbox.checked = true;
        }
    }
    
    // Update progress
    updateProgress();
    updateSummary();
    
    // Hide hero on mobile when past step 1 for cleaner UX
    updateHeroVisibility();
    
    // Scroll to form container with offset for sticky header
    scrollToFormTop();
}

// Scroll to show step content below sticky header and progress bar
function scrollToFormTop() {
    setTimeout(() => {
        // Find the active step's gradient header and scroll it into view
        const activeStep = document.getElementById(`step${currentStep}`);
        if (activeStep) {
            // Use scrollIntoView which respects CSS scroll-padding-top
            activeStep.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }, 150);
}

// Hide/show hero section based on current step (mobile only)
function updateHeroVisibility() {
    const heroSection = document.getElementById('quoteHero');
    console.log('updateHeroVisibility called - step:', currentStep, 'width:', window.innerWidth, 'heroFound:', !!heroSection);
    if (!heroSection) return;
    
    // Hide on mobile (< 768px) when past step 1
    if (window.innerWidth < 768 && currentStep > 1) {
        heroSection.style.display = 'none';
        console.log('Hero hidden');
    } else {
        heroSection.style.display = '';
        console.log('Hero shown');
    }
}

function prevStep() {
    // Hide current step
    document.getElementById(`step${currentStep}`).classList.add('hidden');
    
    // Show previous step
    currentStep--;
    document.getElementById(`step${currentStep}`).classList.remove('hidden');
    
    // Update progress
    updateProgress();
    
    // Update hero visibility when going back
    updateHeroVisibility();
    
    // Scroll to form container with offset for sticky header
    scrollToFormTop();
}

function skipAIDesign() {
    // Uncheck AI design and submit without it
    const aiDesignCheckbox = document.getElementById('aiDesign');
    if (aiDesignCheckbox) {
        aiDesignCheckbox.checked = false;
    }
    quoteData.aiDesign = false;
    quoteData.aiDesignFiles = [];
    submitQuote();
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
    
    // Show quote type at the top
    if (quoteData.quoteMode) {
        const modeLabel = quoteData.quoteMode === 'full-redesign' ? 'Full redesign' : 'Individual products';
        const modeIcon = quoteData.quoteMode === 'full-redesign' ? 'fa-magic' : 'fa-th';
        html += `
            <div class="summary-item flex items-center space-x-2 bg-gradient-to-r from-blue-50 to-purple-50 px-3 py-2 rounded-lg border border-accent">
                <i class="fas ${modeIcon} text-accent"></i>
                <span class="text-sm font-bold text-primary">${modeLabel}</span>
            </div>
        `;
    }
    
    // Show selected products for individual mode
    if (quoteData.quoteMode === 'individual-products' && quoteData.features.length > 0) {
        html += '<div class="space-y-2 mt-2">';
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
    
    // Show selected materials count for full redesign mode
    if (quoteData.quoteMode === 'full-redesign' && typeof gardenDesignMaterials !== 'undefined') {
        const materialCount = Object.keys(gardenDesignMaterials).length;
        if (materialCount > 0) {
            const materialNames = Object.values(gardenDesignMaterials)
                .map(m => m.name || m.material)
                .slice(0, 3)
                .join(', ');
            const moreText = materialCount > 3 ? ` +${materialCount - 3} more` : '';
            html += `
                <div class="summary-item bg-stone px-3 py-2 rounded-lg mt-2">
                    <p class="text-sm"><i class="fas fa-layer-group text-accent mr-2"></i>Materials: <strong>${materialNames}${moreText}</strong></p>
                </div>
            `;
        }
    }
    
    // Show design vision notes if provided
    if (quoteData.designVisionNotes && quoteData.designVisionNotes.trim()) {
        const visionPreview = quoteData.designVisionNotes.substring(0, 50) + (quoteData.designVisionNotes.length > 50 ? '...' : '');
        html += `
            <div class="summary-item bg-stone px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-lightbulb text-accent mr-2"></i>Vision: <strong>${visionPreview}</strong></p>
            </div>
        `;
    }
    
    // Only show area after step 3 (where it's set)
    if (quoteData.area && currentStep >= 3) {
        html += `
            <div class="summary-item bg-stone px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-ruler-combined text-accent mr-2"></i>Garden size: <strong>${quoteData.area} m²</strong></p>
            </div>
        `;
    }
    
    if (quoteData.budget) {
        const formattedBudget = typeof quoteData.budget === 'number' 
            ? `£${quoteData.budget.toLocaleString('en-GB')}` 
            : quoteData.budget;
        html += `
            <div class="summary-item bg-stone px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-pound-sign text-accent mr-2"></i>Budget: <strong>${formattedBudget}</strong></p>
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
    
    // Show if AI design is selected (only show on step 6)
    if (currentStep >= 6) {
        const aiDesignCheckbox = document.getElementById('aiDesign');
        if (aiDesignCheckbox && aiDesignCheckbox.checked) {
            html += `
                <div class="summary-item bg-gradient-to-r from-purple-50 to-blue-50 px-3 py-2 rounded-lg mt-2 border border-purple-200">
                    <p class="text-sm"><i class="fas fa-sparkles text-accent mr-2"></i><strong>+ Free AI Design</strong></p>
                </div>
            `;
        }
    }
    
    if (html === '') {
        html = '<p class="text-gray-500 text-sm italic">Select features to see your summary...</p>';
    }
    
    summaryContent.innerHTML = html;
}

// Submit quote
async function submitQuote() {
    // Prevent double submission
    if (isSubmittingQuote) {
        console.log('⚠️ Quote submission already in progress, ignoring duplicate click');
        return;
    }
    isSubmittingQuote = true;
    
    console.log('🚀 SUBMIT QUOTE FUNCTION CALLED - Version: 20251028-FINAL');
    console.log('Current quoteData:', quoteData);
    
    // Validation
    const nameInput = document.getElementById('name');
    if (!nameInput.value.trim()) {
        alert('Please enter your name');
        nameInput.focus();
        isSubmittingQuote = false;
        return;
    }
    
    const emailInput = document.getElementById('email');
    if (!emailInput.value.trim() || !emailInput.value.includes('@')) {
        alert('Please enter a valid email address');
        emailInput.focus();
        isSubmittingQuote = false;
        return;
    }
    
    quoteData.name = nameInput.value.trim();
    quoteData.email = emailInput.value.trim();
    
    const phoneInput = document.getElementById('phone');
    if (!phoneInput.value.trim()) {
        alert('Please enter your phone number');
        phoneInput.focus();
        isSubmittingQuote = false;
        return;
    }
    quoteData.phone = phoneInput.value.trim();
    
    const aiDesignCheckbox = document.getElementById('aiDesign');
    if (aiDesignCheckbox && !aiDesignCheckbox.disabled) {
        quoteData.aiDesign = aiDesignCheckbox.checked;
    }
    
    // Validate: AI Design requires a photo upload
    if (quoteData.aiDesign) {
        const hasAIPhoto = aiDesignFiles.length > 0;
        const hasQuotePhoto = quoteData.files.length > 0;
        
        if (!hasAIPhoto && !hasQuotePhoto) {
            alert('Please upload a photo of your garden to get your free AI design visualization.');
            isSubmittingQuote = false;
            return;
        }
    }
    
    // Hide form - step6 is the AI Design step
    document.getElementById('step6').classList.add('hidden');
    
    // Check if this is a full redesign to determine which loading state to show
    const isFullRedesignMode = quoteData.quoteMode === 'full-redesign';
    
    if (isFullRedesignMode) {
        // Show animated progress for full redesign
        document.getElementById('loadingStateRedesign').classList.remove('hidden');
        resetProgressTimeline();
        startProgressAnimation();
    } else {
        // Show standard loading spinner for individual products
        document.getElementById('loadingState').classList.remove('hidden');
    }
    
    // ============================================================================
    // WEBHOOK INTEGRATION POINT - Ready for Make.com/n8n Connection
    // ============================================================================
    
    // Structure data for n8n workflow
    const webhookPayloadPromise = prepareWebhookPayload();
    
    try {
        const webhookPayload = await webhookPayloadPromise;
        console.log('Quote Data for n8n Webhook:', webhookPayload);
        
        // ========================================================================
        // SMART ROUTING: Different webhooks for different quote types
        // ========================================================================
        // Check if this is a full garden redesign quote
        const isFullRedesign = webhookPayload.project.type === 'full_garden_redesign';
        
        // Route to appropriate webhook
        const webhookUrl = isFullRedesign 
            ? window.brandConfig?.webhooks?.quoteFullRedesign 
            : window.brandConfig?.webhooks?.quote;
        
        const quoteType = isFullRedesign ? 'FULL GARDEN REDESIGN' : 'INDIVIDUAL PRODUCTS';
        console.log(`🎯 Quote Type: ${quoteType}`);
        console.log(`🔗 Routing to: ${isFullRedesign ? 'Full Redesign Workflow' : 'Standard Quote Workflow'}`);
        
        // Check if webhook URL is configured
        if (!webhookUrl || webhookUrl.includes('your-') || webhookUrl.includes('-webhook-url')) {
            console.warn('⚠️ Webhook URL not configured. Using demo mode.');
            console.log('To enable live quotes, update the webhook URLs in scripts/config.js');
            console.log('Standard quotes: /webhook/premium-landscapes-quote');
            console.log('Full redesign: /webhook/premium-landscapes-full-redesign');
            
            // Demo mode: Simulate webhook completion after delay
            if (isFullRedesignMode) {
                // Let animation run then complete
                setTimeout(() => {
                    onWebhookComplete(true, { demo: true });
                }, 8000); // Allow time for animation
            } else {
                setTimeout(() => {
                    showQuoteResult();
                }, 2000);
            }
            return;
        }
        
        // ========================================================================
        // SEND WEBHOOK - Fire and forget for Full Redesign (UI runs independently)
        // ========================================================================
        console.log('========================================');
        console.log('🚀 SENDING WEBHOOK - UI RUNS INDEPENDENTLY');
        console.log('========================================');
        console.log('📤 SENDING TO N8N:', webhookUrl);
        console.log('⏰ Timestamp:', new Date().toISOString());
        console.log('📦 Quote Type:', isFullRedesign ? 'FULL REDESIGN' : 'INDIVIDUAL PRODUCTS');
        console.log('📧 AI Design Requested:', webhookPayload.metadata?.aiDesignRequested || false);
        
        if (isFullRedesignMode) {
            // FULL REDESIGN: Fire-and-forget - UI runs on fixed timer
            // Animation: 60s (quote only) or 120s (with AI design)
            fetch(webhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(webhookPayload)
            }).then(response => {
                console.log('✅ Webhook sent successfully, status:', response.status);
                onWebhookComplete(true, { success: true });
            }).catch(error => {
                console.warn('⚠️ Webhook error (UI continues):', error.message);
                onWebhookComplete(false, { error: error.message });
            });
            
            // UI animation runs independently - don't wait for webhook
            console.log('🎬 UI animation started - runs for', quoteData.aiDesign ? '120s' : '60s');
            
        } else {
            // INDIVIDUAL PRODUCTS: Wait for response to show results
            try {
                const response = await fetch(webhookUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(webhookPayload)
                });
                
                console.log('✅ n8n Response Status:', response.status);
                
                if (!response.ok) {
                    throw new Error(`Webhook returned status ${response.status}`);
                }
                
                let result = {};
                try {
                    result = await response.json();
                    console.log('n8n Response:', result);
                } catch (e) {
                    console.log('n8n returned non-JSON response');
                }
                
                const hasError = result.success === false || result.error;
                if (hasError) {
                    showQuoteError(result.error || result.message || 'Error processing quote');
                } else {
                    showQuoteResult(result);
                }
                
            } catch (error) {
                console.error('❌ Error:', error);
                document.getElementById('loadingState').classList.add('hidden');
                showQuoteError('There was an error processing your quote. Please try again.');
            }
        }
        
    } catch (error) {
        console.error('❌ Error preparing quote:', error);
        
        if (isFullRedesignMode) {
            // For full redesign, let animation continue - email will arrive
            console.warn('Payload preparation error, webhook may not have sent');
        } else {
            document.getElementById('loadingState').classList.add('hidden');
            showQuoteError('There was an error processing your quote.');
        }
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
    
    return Promise.all(filePromises).then(async (filesData) => {
        // Parse budget - handles both numeric input and legacy string format
        const parseBudget = (budget) => {
            if (!budget) return null;
            
            // If already a number, return it
            if (typeof budget === 'number') return budget;
            
            // Legacy string format (e.g., "£5k-£10k" or "<5000")
            const match = String(budget).match(/(\d+)k/i);
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
                    material: material
                };
                
                // Add type-specific fields using dedicated area input
                if (feature === 'patio' || feature === 'driveway') {
                    product.unitType = 'm2';
                    product.area_m2 = dedicatedArea ? parseInt(dedicatedArea) : defaultArea;
                    product.edging = description.toLowerCase().includes('edging') ? 'standard edging' : 'none';
                    product.includeDrainage = true;
                } else if (feature === 'decking') {
                    product.unitType = 'm2';
                    product.area_m2 = dedicatedArea ? parseInt(dedicatedArea) : defaultArea;
                    product.raised = description.toLowerCase().includes('raised');
                    product.steps = description.toLowerCase().includes('step') ? 3 : 0;
                    product.balustrade = description.toLowerCase().includes('glass') ? 'glass panels' : 'none';
                } else if (feature === 'turf') {
                    product.unitType = 'm2';
                    product.area_m2 = dedicatedArea ? parseInt(dedicatedArea) : defaultArea;
                    product.includeEdging = true;
                } else if (feature === 'fencing') {
                    product.unitType = 'm';
                    product.length = dedicatedArea ? parseInt(dedicatedArea) : 20;
                    product.height_m = 1.8;
                } else if (feature === 'lighting') {
                    product.unitType = 'qty';
                    product.fittings = dedicatedArea ? parseInt(dedicatedArea) : 8;
                    product.wattagePerFitting = 6;
                    product.control = 'standard switch';
                } else {
                    product.unitType = 'm2';
                    product.area_m2 = dedicatedArea ? parseInt(dedicatedArea) : defaultArea;
                }
                
                return product;
            });
        };
        
        // Build n8n-compatible payload
        const buildFullAddress = () => {
            const parts = [];
            if (quoteData.houseNumber) parts.push(quoteData.houseNumber);
            if (quoteData.street) parts.push(quoteData.street);
            if (quoteData.city) parts.push(quoteData.city);
            if (quoteData.postcode) parts.push(quoteData.postcode);
            parts.push('UK');
            return parts.join(', ');
        };
        
        // Check if Full Redesign mode with materials
        const isFullRedesign = quoteData.features.includes('full-redesign');
        const hasGardenDesignMaterials = isFullRedesign && Object.keys(gardenDesignMaterials).length > 0;
        
        // Format garden design materials for n8n
        const formatGardenDesignMaterials = () => {
            // Full redesign mode always uses budget-based design now (simplified UI)
            // The designVisionNotes textarea contains all requirements
            
            // Return clean structure for n8n - always budget-based for full redesign
            return {
                budgetBasedDesign: true,
                categories: {},
                designVision: quoteData.designVisionNotes || ''
            };
        };
        
        // Detect extras from selected materials
        const detectExtras = () => {
            const hasPergola = !!gardenDesignMaterials['pergola'];
            const hasFirePit = !!gardenDesignMaterials['fire_pit'];
            const hasWaterFeature = !!gardenDesignMaterials['water_feature'];
            
            return {
                pergola: { include: hasPergola },
                firePit: { include: hasFirePit },
                waterFeature: { include: hasWaterFeature }
            };
        };
        
        const payload = {
            customer: {
                name: quoteData.name || 'Unknown',
                email: quoteData.email || '',
                phone: quoteData.phone || '',
                postcode: quoteData.postcode || '',
                city: quoteData.city || '',
                street: quoteData.street || '',
                houseNumber: quoteData.houseNumber || '',
                address: buildFullAddress()
            },
            project: {
                title: generateProjectTitle(),
                type: isFullRedesign ? 'full_garden_redesign' : 'individual_products',
                totalArea_m2: totalArea,
                totalBudget_gbp: totalBudget,
                layoutType: 'standard',
                sunlight: 'partial sun',
                stylePreference: 'contemporary',
                maintenanceLevel: 'low maintenance',
                siteConditions: {
                    access: 'standard access',
                    soilType: 'loam',
                    drainage: 'good'
                },
                products: transformProducts(),
                extras: detectExtras(),
                notes: isFullRedesign 
                    ? (quoteData.designVisionNotes || quoteData.additionalNotes || 'Website quote request')
                    : (quoteData.additionalNotes || 'Website quote request'),
                designPreferences: quoteData.designVisionNotes || ''
            }
        };
        
        // Add full garden design data if full redesign is selected
        // Include even if no materials (for budget-based design mode)
        if (isFullRedesign) {
            payload.project.gardenDesign = formatGardenDesignMaterials();
            console.log('🎨 Full Garden Design data included:', payload.project.gardenDesign);
        }
        
        // Add metadata for n8n workflow tracking
        // Generate unique request ID to trace duplicates
        const requestId = 'REQ-' + Date.now() + '-' + Math.random().toString(36).substring(2, 8);
        
        payload.metadata = {
            source: 'website_quote_form',
            timestamp: new Date().toISOString(),
            requestId: requestId, // Unique ID to detect duplicate webhook calls
            quoteType: isFullRedesign ? 'full_garden_redesign' : 'individual_products',
            webhookDestination: isFullRedesign 
                ? window.brandConfig?.webhooks?.quoteFullRedesign || 'https://n8n.example.com/webhook/premium-landscapes-full-redesign'
                : window.brandConfig?.webhooks?.quote || 'https://n8n.example.com/webhook/premium-landscapes-quote',
            aiDesignRequested: quoteData.aiDesign || false
        };
        
        console.log('🔑 REQUEST ID:', requestId);
        
        // Add photo for AI design if requested (single consolidated payload)
        if (quoteData.aiDesign) {
            // Priority: AI-specific photos (Step 5) > Step 4 photos
            const photoSource = aiDesignFiles.length > 0 ? aiDesignFiles : quoteData.files;
            
            if (photoSource.length > 0) {
                const file = photoSource[0];
                try {
                    const photoData = await convertFileToBase64(file);
                    payload.photo = {
                        name: file.name,
                        type: file.type,
                        size: file.size,
                        data: photoData
                    };
                    console.log('📸 Photo included in payload:', file.name, `(${(file.size / 1024).toFixed(0)} KB)`);
                } catch (photoError) {
                    console.error('Error converting photo:', photoError);
                }
            }
        }
        
        return payload;
    });
}


// ============================================================================
// DISPLAY QUOTE RESULT
// Shows confirmation message - actual quote sent via email from n8n
// ============================================================================
async function showQuoteResult(data) {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('quoteResult').classList.remove('hidden');
    
    console.log('✅ Quote request submitted successfully!');
    console.log('Customer will receive detailed PDF quote via email from n8n workflow');
    
    // If AI design was requested, it's now included in the main payload
    // No separate webhook call needed - n8n main workflow handles routing
    if (quoteData.aiDesign) {
        console.log('🎨 AI Design requested - photo included in main webhook payload');
        console.log('📸 n8n will route to AI design generation within the workflow');
        
        // Add AI design message to confirmation
        const nextStepsList = document.getElementById('nextStepsList');
        if (nextStepsList) {
            const aiDesignItem = document.createElement('li');
            aiDesignItem.className = 'flex items-start';
            aiDesignItem.innerHTML = `
                <i class="fas fa-check-circle text-accent mr-2 mt-1"></i>
                <span>You'll also receive your AI-generated garden design in a separate email</span>
            `;
            nextStepsList.appendChild(aiDesignItem);
        }
    }
    
    // Scroll to result
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================================================
// DISPLAY QUOTE ERROR
// Shows error message when webhook returns an error response
// ============================================================================
function showQuoteError(errorMessage) {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('quoteResult').classList.add('hidden');
    
    // Check if error result element exists, create if not
    let errorResult = document.getElementById('quoteError');
    if (!errorResult) {
        // Create error element dynamically
        const loadingState = document.getElementById('loadingState');
        errorResult = document.createElement('div');
        errorResult.id = 'quoteError';
        errorResult.className = 'text-center py-8';
        loadingState.parentNode.insertBefore(errorResult, loadingState.nextSibling);
    }
    
    errorResult.innerHTML = `
        <div class="text-center mb-6">
            <div class="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="fas fa-exclamation-triangle text-4xl text-red-600"></i>
            </div>
            <h2 class="font-heading font-bold text-3xl text-red-600 mb-3">Quote Request Failed</h2>
            <p class="text-gray-600 text-lg mb-6">${errorMessage}</p>
        </div>
        
        <div class="bg-red-50 p-8 rounded-2xl mb-6 border-2 border-red-200">
            <div class="flex items-start mb-4">
                <i class="fas fa-info-circle text-2xl text-red-500 mr-3 mt-1"></i>
                <div>
                    <h3 class="font-semibold text-lg text-gray-900 mb-2">What You Can Do</h3>
                    <ul class="space-y-2 text-gray-700">
                        <li class="flex items-start">
                            <i class="fas fa-redo text-red-500 mr-2 mt-1"></i>
                            <span>Try submitting your quote again in a few moments</span>
                        </li>
                        <li class="flex items-start">
                            <i class="fas fa-phone text-red-500 mr-2 mt-1"></i>
                            <span>Call us directly at <strong>07444 887813</strong> for immediate assistance</span>
                        </li>
                        <li class="flex items-start">
                            <i class="fas fa-envelope text-red-500 mr-2 mt-1"></i>
                            <span>Email us at <strong>info@premiumlandscapes.co.uk</strong></span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        
        <button onclick="location.reload()" class="bg-primary text-white px-8 py-3 rounded-full font-semibold hover:bg-primary-dark transition">
            <i class="fas fa-redo mr-2"></i>Try Again
        </button>
    `;
    
    errorResult.classList.remove('hidden');
    
    console.error('❌ Quote request failed:', errorMessage);
    
    // Scroll to result
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// NOTE: AI Design is now handled via the main quote webhook
// When aiDesignRequested: true, n8n routes to AI generation within the same workflow
// No separate webhook call needed - photo is included in main payload

// Helper: Extract design features from quote data
function extractDesignFeatures() {
    const isFullRedesign = quoteData.quoteMode === 'full-redesign';
    
    if (isFullRedesign && gardenDesignMaterials && Object.keys(gardenDesignMaterials).length > 0) {
        // Extract material names from Full Redesign mode
        return Object.values(gardenDesignMaterials).map(m => m.material || m.name || 'feature');
    }
    
    // For individual products mode, return selected products (excluding 'full-redesign')
    return quoteData.features.filter(f => f !== 'full-redesign');
}

// Helper: Build style description from quote data
function buildStyleDescription() {
    const isFullRedesign = quoteData.quoteMode === 'full-redesign';
    
    if (isFullRedesign) {
        if (quoteData.designVisionNotes) {
            return quoteData.designVisionNotes;
        }
        
        // Build from selected materials
        if (gardenDesignMaterials && Object.keys(gardenDesignMaterials).length > 0) {
            const materials = Object.values(gardenDesignMaterials)
                .map(m => m.material || m.name || '')
                .filter(Boolean)
                .join(', ');
            return `Complete garden redesign with ${materials}`;
        }
        
        return 'Complete garden redesign based on budget and requirements';
    }
    
    // Build description from selected products
    const productNames = {
        'patio': 'patio area',
        'decking': 'decking',
        'turf': 'lawn',
        'driveway': 'driveway',
        'fencing': 'fencing',
        'lighting': 'garden lighting',
        'other': 'custom features'
    };
    
    const features = quoteData.features.map(f => productNames[f] || f).join(', ');
    return `Garden with ${features}`;
}

// Helper: Format budget for design workflow
function formatBudgetForDesign(budget) {
    if (!budget) return '<5000';
    
    // If numeric, convert to range
    if (typeof budget === 'number') {
        if (budget < 5000) return '<5000';
        if (budget < 10000) return '5000-10000';
        if (budget < 20000) return '10000-20000';
        return '>20000';
    }
    
    return String(budget);
}

// Helper: Convert file to base64 string
async function convertFileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(file);
    });
}

// ============================================================================
// AI DESIGN PHOTO UPLOAD (Step 5)
// ============================================================================
let aiDesignFiles = [];
let aiUploadHandlersInitialized = false;

// Initialize AI design file upload handlers
function initAIUploadHandlers() {
    if (aiUploadHandlersInitialized) return;
    
    const aiDropZone = document.getElementById('aiDropZone');
    const aiFileInput = document.getElementById('aiFileInput');
    
    if (!aiDropZone || !aiFileInput) return;
    
    // Click to browse
    aiDropZone.addEventListener('click', () => aiFileInput.click());
    
    // File selection
    aiFileInput.addEventListener('change', (e) => {
        handleAIFiles(Array.from(e.target.files));
    });
    
    // Drag and drop
    aiDropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        aiDropZone.classList.add('border-accent');
    });
    
    aiDropZone.addEventListener('dragleave', () => {
        aiDropZone.classList.remove('border-accent');
    });
    
    aiDropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        aiDropZone.classList.remove('border-accent');
        const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
        handleAIFiles(files);
    });
    
    aiUploadHandlersInitialized = true;
}

// Toggle AI upload section visibility
function toggleAIUploadSection() {
    const checkbox = document.getElementById('aiDesign');
    const uploadSection = document.getElementById('aiDesignUploadSection');
    
    if (checkbox.checked) {
        uploadSection.classList.remove('hidden');
        // Initialize handlers when section becomes visible
        setTimeout(initAIUploadHandlers, 100);
    } else {
        uploadSection.classList.add('hidden');
        // Clear AI-specific files when unchecked
        aiDesignFiles = [];
        const preview = document.getElementById('aiFilePreview');
        if (preview) preview.innerHTML = '';
    }
    
    // Update summary to show AI design selection
    updateSummary();
}

// Handle AI design file uploads (limit: 1 image only)
function handleAIFiles(files) {
    if (files.length === 0) return;
    
    // Only accept the first image (replace existing if any)
    aiDesignFiles = [files[0]];
    
    displayAIFilePreview();
}

// Display AI file preview
function displayAIFilePreview() {
    const preview = document.getElementById('aiFilePreview');
    preview.innerHTML = '';
    
    aiDesignFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const div = document.createElement('div');
            div.className = 'relative';
            div.innerHTML = `
                <img src="${e.target.result}" class="w-full h-24 object-cover rounded-lg">
                <button 
                    onclick="removeAIFile(${index})" 
                    class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600"
                >
                    <i class="fas fa-times text-xs"></i>
                </button>
            `;
            preview.appendChild(div);
        };
        reader.readAsDataURL(file);
    });
}

// Remove AI file
function removeAIFile(index) {
    aiDesignFiles.splice(index, 1);
    displayAIFilePreview();
}

// ============================================================================
// FULL GARDEN REDESIGN MODE
// Enhanced Step 2 with comprehensive material selector
// ============================================================================

// Store selected materials for full redesign
let gardenDesignMaterials = {};
let currentMaterialSelection = null;

// Toggle material category sections
function toggleCategory(categoryName) {
    const content = document.getElementById(`${categoryName}Content`);
    const chevron = document.getElementById(`${categoryName}Chevron`);
    
    if (content && chevron) {
        content.classList.toggle('hidden');
        chevron.classList.toggle('rotate-180');
    }
}

// Toggle budget-based design mode
function toggleBudgetBasedDesign() {
    const checkbox = document.getElementById('budgetBasedDesign');
    const materialSection = document.getElementById('materialSelectionSection');
    const visionLabel = document.getElementById('designVisionLabel');
    const visionDescription = document.getElementById('designVisionDescription');
    const requiredLabel = document.getElementById('budgetBasedRequiredLabel');
    
    if (!checkbox) return;
    
    const isBudgetBased = checkbox.checked;
    
    console.log('💡 Budget-based design mode:', isBudgetBased ? 'ON' : 'OFF');
    
    if (isBudgetBased) {
        // Make material selection less prominent (optional mode)
        if (materialSection) {
            materialSection.style.opacity = '0.6';
        }
        
        // Update design vision notes to be required and emphasize importance
        // Find the label text span (not the required indicator span)
        const labelTextSpan = document.getElementById('designVisionLabel');
        if (labelTextSpan) {
            labelTextSpan.textContent = 'Your Design Vision & Requirements';
        }
        if (visionDescription) {
            visionDescription.innerHTML = '<strong class="text-primary">Required:</strong> Tell us your style preferences, must-haves, and any specific requirements. We\'ll create a custom design proposal tailored to your budget!';
        }
        if (requiredLabel) {
            requiredLabel.classList.remove('hidden');
        }
    } else {
        // Reset to normal mode
        if (materialSection) {
            materialSection.style.opacity = '1';
        }
        
        const labelTextSpan = document.getElementById('designVisionLabel');
        if (labelTextSpan) {
            labelTextSpan.textContent = 'Design Vision & Special Requirements';
        }
        if (visionDescription) {
            visionDescription.textContent = 'Tell us about your dream garden - style preferences, must-haves, any constraints';
        }
        if (requiredLabel) {
            requiredLabel.classList.add('hidden');
        }
    }
}

// Initialize material card click handlers
function initializeMaterialCards() {
    const materialCards = document.querySelectorAll('.material-card');
    materialCards.forEach(card => {
        card.addEventListener('click', function() {
            const category = this.dataset.category;
            const material = this.dataset.material;
            
            // Check if already selected
            if (gardenDesignMaterials[material]) {
                // Remove material
                removeMaterial(material);
            } else {
                // Add material directly (no modal needed)
                addMaterialDirectly(category, material);
            }
        });
    });
}

// Open material detail modal
function openMaterialDetailModal(category, material) {
    currentMaterialSelection = { category, material };
    
    // Format material name for display
    const materialName = material.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    // Update modal title
    document.getElementById('materialModalTitle').textContent = materialName;
    
    // Check if this material was already selected and populate fields
    const existingData = gardenDesignMaterials[material];
    if (existingData) {
        // Select quality option
        document.querySelectorAll('.quality-option').forEach(btn => {
            btn.classList.remove('selected');
            if (btn.dataset.quality === existingData.quality) {
                btn.classList.add('selected');
            }
        });
    } else {
        // Clear form
        document.querySelectorAll('.quality-option').forEach(btn => btn.classList.remove('selected'));
    }
    
    // Set up quality button handlers
    document.querySelectorAll('.quality-option').forEach(btn => {
        btn.onclick = function() {
            document.querySelectorAll('.quality-option').forEach(b => b.classList.remove('selected'));
            this.classList.add('selected');
        };
    });
    
    // Show modal
    document.getElementById('materialDetailModal').classList.remove('hidden');
}

// Close material detail modal
function closeMaterialDetailModal() {
    document.getElementById('materialDetailModal').classList.add('hidden');
    currentMaterialSelection = null;
}

// Save material details
function saveMaterialDetails() {
    if (!currentMaterialSelection) return;
    
    const { category, material } = currentMaterialSelection;
    
    // Get selected quality
    const selectedQuality = document.querySelector('.quality-option.selected');
    if (!selectedQuality) {
        alert('Please select a quality level');
        return;
    }
    
    const quality = selectedQuality.dataset.quality;
    
    // Save to data structure (area determined by workflow logic)
    gardenDesignMaterials[material] = {
        category,
        material,
        quality,
        area: 0,
        style: '',
        notes: '',
        displayName: material.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    };
    
    console.log('✅ Material saved:', gardenDesignMaterials[material]);
    
    // Update selected materials summary
    updateSelectedMaterialsSummary();
    
    // Close modal
    closeMaterialDetailModal();
    
    // Highlight the card that was just saved
    highlightSelectedMaterialCard(material);
}

// Add material directly without modal
function addMaterialDirectly(category, material) {
    const displayName = material.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    // Save to data structure (area and quality determined by workflow)
    gardenDesignMaterials[material] = {
        category,
        material,
        quality: 'standard',
        area: 0,
        style: '',
        notes: '',
        displayName
    };
    
    console.log('✅ Material added:', displayName);
    
    // Update selected materials summary
    updateSelectedMaterialsSummary();
    
    // Highlight the card
    highlightSelectedMaterialCard(material);
}

// Highlight material card when selected
function highlightSelectedMaterialCard(material) {
    document.querySelectorAll('.material-card').forEach(card => {
        if (card.dataset.material === material) {
            card.classList.add('!bg-primary', '!border-primary', 'shadow-lg');
            card.classList.remove('border-gray-200', 'bg-white');
            
            // Make text and icon white when selected
            const icon = card.querySelector('i');
            const text = card.querySelector('p');
            if (icon) {
                icon.classList.remove('text-primary');
                icon.classList.add('!text-white');
            }
            if (text) {
                text.classList.add('!text-white');
            }
        }
    });
}

// Update selected materials summary panel
function updateSelectedMaterialsSummary() {
    const summaryContainer = document.getElementById('selectedMaterialsSummary');
    const listContainer = document.getElementById('selectedMaterialsList');
    
    const materialCount = Object.keys(gardenDesignMaterials).length;
    
    if (materialCount === 0) {
        summaryContainer.classList.add('hidden');
        return;
    }
    
    summaryContainer.classList.remove('hidden');
    listContainer.innerHTML = '';
    
    Object.values(gardenDesignMaterials).forEach(mat => {
        const itemHtml = `
            <div class="flex justify-between items-center p-2 bg-white rounded-lg">
                <div>
                    <p class="font-semibold text-sm">${mat.displayName}</p>
                </div>
                <button onclick="removeMaterial('${mat.material}')" class="text-red-500 hover:text-red-700">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        listContainer.innerHTML += itemHtml;
    });
}

// Remove a material from selection
function removeMaterial(material) {
    delete gardenDesignMaterials[material];
    updateSelectedMaterialsSummary();
    
    // Remove highlight from card
    document.querySelectorAll('.material-card').forEach(card => {
        if (card.dataset.material === material) {
            card.classList.remove('!bg-primary', '!border-primary', 'shadow-lg');
            card.classList.add('border-gray-200', 'bg-white');
            
            // Restore original colors
            const icon = card.querySelector('i');
            const text = card.querySelector('p');
            if (icon) {
                icon.classList.add('text-primary');
                icon.classList.remove('!text-white');
            }
            if (text) {
                text.classList.remove('!text-white');
            }
        }
    });
    
    console.log('🗑️ Material removed:', material);
}

// Detect if Full Redesign is selected and toggle Step 2 mode
function updateStep2Mode() {
    console.log('🔄 updateStep2Mode called');
    console.log('Current quoteMode:', quoteData.quoteMode);
    console.log('Current features:', quoteData.features);
    
    // Check if Full Redesign mode is selected
    const isFullRedesign = quoteData.quoteMode === 'full-redesign';
    
    const step2Standard = document.getElementById('step2Standard');
    const step2FullRedesign = document.getElementById('step2FullRedesign');
    
    if (!step2Standard || !step2FullRedesign) {
        console.error('❌ Step 2 containers not found!');
        console.error('step2Standard:', step2Standard);
        console.error('step2FullRedesign:', step2FullRedesign);
        return;
    }
    
    if (isFullRedesign) {
        // Show full redesign mode
        console.log('🎨 Showing Full Redesign mode...');
        step2Standard.classList.add('hidden');
        step2FullRedesign.classList.remove('hidden');
        
        // Initialize material cards (only once)
        setTimeout(() => {
            const materialCards = document.querySelectorAll('.material-card');
            console.log('Found material cards:', materialCards.length);
            
            if (materialCards.length > 0) {
                const firstCard = materialCards[0];
                if (!firstCard.hasAttribute('data-initialized')) {
                    console.log('🔧 Initializing material cards...');
                    initializeMaterialCards();
                    materialCards.forEach(card => {
                        card.setAttribute('data-initialized', 'true');
                    });
                    console.log('✅ Material cards initialized');
                } else {
                    console.log('ℹ️ Material cards already initialized');
                }
            } else {
                console.warn('⚠️ No material cards found in DOM');
            }
        }, 100);
        
        console.log('🎨 Full Redesign mode activated');
    } else {
        // Show standard mode
        console.log('📝 Showing Standard mode...');
        step2Standard.classList.remove('hidden');
        step2FullRedesign.classList.add('hidden');
        
        // Build standard product detail fields
        buildProductDetailFields();
        
        console.log('📝 Standard mode activated');
    }
}
