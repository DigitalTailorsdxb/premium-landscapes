// AI Design Generator Engine
// Handles multi-step form, feature selection, and design generation

let currentStep = 1;
const totalSteps = 4;

// Progress animation state for AI design generation
let designProgressState = {
    currentStep: 0,
    totalSteps: 7,
    isAnimating: false,
    webhookComplete: false,
    webhookSuccess: false,
    webhookResult: null,
    timeouts: []
};

// Progress step timings (milliseconds) - ~45 seconds total to match AI generation
const designProgressDurations = [
    7000,  // Analysing your photo
    7500,  // Understanding your style
    9000,  // Generating AI concepts
    8500,  // Rendering design visuals
    8000,  // Applying finishing touches
    5000,  // Sending to your inbox
    1500   // Done
];

// Reset progress timeline to initial state
function resetDesignProgress() {
    designProgressState = {
        currentStep: 0,
        totalSteps: 7,
        isAnimating: false,
        webhookComplete: false,
        webhookSuccess: false,
        webhookResult: null,
        timeouts: []
    };
    
    const steps = document.querySelectorAll('#designProgressTimeline .progress-step');
    steps.forEach(step => {
        step.classList.remove('active', 'completed', 'error');
    });
}

// Start the progress animation
function startDesignProgress() {
    designProgressState.isAnimating = true;
    advanceDesignStep(0);
}

// Advance to the next progress step
function advanceDesignStep(stepIndex) {
    if (!designProgressState.isAnimating) return;
    
    const steps = document.querySelectorAll('#designProgressTimeline .progress-step');
    
    // Mark previous step as completed
    if (stepIndex > 0) {
        steps[stepIndex - 1].classList.remove('active');
        steps[stepIndex - 1].classList.add('completed');
    }
    
    // If we've reached the last two steps (Sending, Done), wait for webhook
    if (stepIndex >= 5 && !designProgressState.webhookComplete) {
        // Keep "Sending to your inbox" as active until webhook completes
        steps[5].classList.add('active');
        designProgressState.currentStep = 5;
        return; // Will be resumed by webhook callback
    }
    
    // If webhook is complete and failed, show error
    if (designProgressState.webhookComplete && !designProgressState.webhookSuccess) {
        steps[stepIndex].classList.add('error');
        designProgressState.isAnimating = false;
        return;
    }
    
    // Mark current step as active
    if (stepIndex < steps.length) {
        steps[stepIndex].classList.add('active');
        designProgressState.currentStep = stepIndex;
        
        // Schedule next step
        if (stepIndex < steps.length - 1) {
            const timeout = setTimeout(() => {
                advanceDesignStep(stepIndex + 1);
            }, designProgressDurations[stepIndex]);
            designProgressState.timeouts.push(timeout);
        } else {
            // Final step (Done) - wait a moment then show result
            const timeout = setTimeout(() => {
                completeDesignProgress();
            }, 1500);
            designProgressState.timeouts.push(timeout);
        }
    }
}

// Called when webhook completes - resume animation
function onDesignWebhookComplete(success, result) {
    designProgressState.webhookComplete = true;
    designProgressState.webhookSuccess = success;
    designProgressState.webhookResult = result;
    
    if (!designProgressState.isAnimating) return;
    
    const steps = document.querySelectorAll('#designProgressTimeline .progress-step');
    
    if (success) {
        // Complete the "Sending" step and move to "Done"
        steps[5].classList.remove('active');
        steps[5].classList.add('completed');
        
        // Activate and complete "Done" step
        steps[6].classList.add('active');
        designProgressState.currentStep = 6;
        
        setTimeout(() => {
            steps[6].classList.remove('active');
            steps[6].classList.add('completed');
            completeDesignProgress();
        }, 1500);
    } else {
        // Show error on current step
        const currentIdx = designProgressState.currentStep;
        steps[currentIdx].classList.remove('active');
        steps[currentIdx].classList.add('error');
        designProgressState.isAnimating = false;
        
        // Show error UI after a brief moment
        setTimeout(() => {
            document.getElementById('loadingState').classList.add('hidden');
            const errorMessage = result?.error || result?.message || 'The AI design workflow encountered an error.';
            showError(errorMessage);
        }, 1500);
    }
}

// Complete the progress animation and show result
function completeDesignProgress() {
    designProgressState.isAnimating = false;
    
    // Clear any remaining timeouts
    designProgressState.timeouts.forEach(t => clearTimeout(t));
    designProgressState.timeouts = [];
    
    // Hide loading state and show result
    document.getElementById('loadingState').classList.add('hidden');
    
    if (designProgressState.webhookSuccess) {
        showSuccess();
    }
}

// Stop progress animation (for errors)
function stopDesignProgress() {
    designProgressState.isAnimating = false;
    designProgressState.timeouts.forEach(t => clearTimeout(t));
    designProgressState.timeouts = [];
}

const designData = {
    features: [],
    styleDescription: '',
    photo: null,
    gardenSize: '',
    budget: '',
    email: '',
    phone: ''
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupFeatureCards();
    setupPhotoUpload();
    setupGardenSizeInput();
    updateProgress();
});

// Garden size input handler
function setupGardenSizeInput() {
    const gardenSizeInput = document.getElementById('gardenSize');
    if (gardenSizeInput) {
        gardenSizeInput.addEventListener('input', function() {
            designData.gardenSize = this.value.trim();
            updateSummary();
        });
    }
}

// Feature card selection (Step 1)
function setupFeatureCards() {
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            const feature = this.getAttribute('data-feature');
            
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
                designData.features = designData.features.filter(f => f !== feature);
            } else {
                this.classList.add('selected');
                designData.features.push(feature);
            }
            
            updateSummary();
        });
    });
}

// Style description update (Step 2)
function updateStyleDescription(value) {
    designData.styleDescription = value;
    updateSummary();
}

// Budget selection
function selectBudget(button) {
    // Remove selection from all budget options
    document.querySelectorAll('.budget-option').forEach(opt => {
        opt.classList.remove('border-accent', 'bg-blue-50');
        opt.classList.add('border-gray-200');
    });
    
    // Select this option
    button.classList.remove('border-gray-200');
    button.classList.add('border-accent', 'bg-blue-50');
    
    designData.budget = button.getAttribute('data-budget');
    updateSummary();
}

// Photo upload handling
function setupPhotoUpload() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('gardenPhoto');
    const photoPreview = document.getElementById('photoPreview');
    const photoName = document.getElementById('photoName');
    
    if (!dropZone || !fileInput) return;
    
    // Click to upload
    dropZone.addEventListener('click', function(e) {
        if (e.target.tagName !== 'BUTTON') {
            fileInput.click();
        }
    });
    
    // File selected
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            designData.photo = file;
            photoPreview.classList.remove('hidden');
            photoName.textContent = file.name;
            updateSummary();
        }
    });
    
    // Drag and drop
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('border-accent');
    });
    
    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('border-accent');
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('border-accent');
        
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const file = e.dataTransfer.files[0];
            fileInput.files = e.dataTransfer.files;
            designData.photo = file;
            photoPreview.classList.remove('hidden');
            photoName.textContent = file.name;
            updateSummary();
        }
    });
}

// Navigation
function nextStep() {
    // Validation
    if (currentStep === 1 && designData.features.length === 0) {
        alert('Please select at least one feature for your garden design');
        return;
    }
    
    if (currentStep === 2 && !designData.styleDescription.trim()) {
        alert('Please describe your desired garden style');
        return;
    }
    
    // Hide current step
    document.getElementById(`step${currentStep}`).classList.add('hidden');
    
    // Show next step
    currentStep++;
    document.getElementById(`step${currentStep}`).classList.remove('hidden');
    
    updateProgress();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function prevStep() {
    // Hide current step
    document.getElementById(`step${currentStep}`).classList.add('hidden');
    
    // Show previous step
    currentStep--;
    document.getElementById(`step${currentStep}`).classList.remove('hidden');
    
    updateProgress();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Update progress bar
function updateProgress() {
    const percent = (currentStep / totalSteps) * 100;
    document.getElementById('progressBar').style.width = percent + '%';
    document.getElementById('progressText').textContent = `Step ${currentStep} of ${totalSteps}`;
    document.getElementById('progressPercent').textContent = Math.round(percent) + '%';
}

// Update summary panel
function updateSummary() {
    const summaryContent = document.getElementById('summaryContent');
    let html = '';
    
    // Features
    if (designData.features.length > 0) {
        html += `
            <div class="mb-4">
                <h4 class="font-semibold text-sm text-gray-700 mb-2">Selected Features:</h4>
                <div class="space-y-1">
        `;
        
        designData.features.forEach(feature => {
            const featureName = feature.charAt(0).toUpperCase() + feature.slice(1).replace('-', ' ');
            html += `
                <div class="flex items-center text-sm">
                    <i class="fas fa-check text-accent mr-2"></i>
                    <span>${featureName}</span>
                </div>
            `;
        });
        
        html += `</div></div>`;
    }
    
    // Style Description
    if (designData.styleDescription) {
        const truncatedStyle = designData.styleDescription.length > 60 
            ? designData.styleDescription.substring(0, 60) + '...' 
            : designData.styleDescription;
        html += `
            <div class="summary-item bg-white px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-palette text-accent mr-2"></i>Style: <strong>${truncatedStyle}</strong></p>
            </div>
        `;
    }
    
    // Photo
    if (designData.photo) {
        html += `
            <div class="summary-item bg-white px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-image text-accent mr-2"></i>Photo: <strong>Uploaded</strong></p>
            </div>
        `;
    }
    
    // Garden Size
    if (designData.gardenSize) {
        html += `
            <div class="summary-item bg-white px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-ruler-combined text-accent mr-2"></i>Size: <strong>${designData.gardenSize}</strong></p>
            </div>
        `;
    }
    
    // Budget
    if (designData.budget) {
        let budgetText = '';
        switch(designData.budget) {
            case '5000-10000': budgetText = '£5k - £10k'; break;
            case '10000-20000': budgetText = '£10k - £20k'; break;
            case '20000-30000': budgetText = '£20k - £30k'; break;
            case '30000-50000': budgetText = '£30k - £50k'; break;
            case '>50000': budgetText = '£50k+'; break;
            default: budgetText = designData.budget; break;
        }
        html += `
            <div class="summary-item bg-white px-3 py-2 rounded-lg mt-2">
                <p class="text-sm"><i class="fas fa-pound-sign text-accent mr-2"></i>Budget: <strong>${budgetText}</strong></p>
            </div>
        `;
    }
    
    if (html === '') {
        html = '<p class="text-gray-500 text-sm italic">Select features to see your summary...</p>';
    }
    
    summaryContent.innerHTML = html;
}

// Submit design request
async function submitDesign() {
    // Validation
    const nameInput = document.getElementById('name');
    if (!nameInput.value.trim()) {
        alert('Please enter your name');
        nameInput.focus();
        return;
    }
    designData.name = nameInput.value.trim();
    
    const emailInput = document.getElementById('email');
    if (!emailInput.value.trim() || !emailInput.value.includes('@')) {
        alert('Please enter a valid email address');
        emailInput.focus();
        return;
    }
    designData.email = emailInput.value.trim();
    
    const phoneInput = document.getElementById('phone');
    if (!phoneInput.value.trim()) {
        alert('Please enter your phone number');
        phoneInput.focus();
        return;
    }
    designData.phone = phoneInput.value.trim();
    
    // Address validation
    const streetInput = document.getElementById('street');
    if (!streetInput.value.trim()) {
        alert('Please enter your street name');
        streetInput.focus();
        return;
    }
    
    const cityInput = document.getElementById('city');
    if (!cityInput.value.trim()) {
        alert('Please enter your city or town');
        cityInput.focus();
        return;
    }
    
    const postcodeInput = document.getElementById('postcode');
    if (!postcodeInput.value.trim()) {
        alert('Please enter your postcode');
        postcodeInput.focus();
        return;
    }
    
    // Budget validation
    if (!designData.budget) {
        alert('Please select a budget range');
        return;
    }
    
    // Collect address data
    const houseNumberInput = document.getElementById('houseNumber');
    designData.houseNumber = houseNumberInput ? houseNumberInput.value.trim() : '';
    designData.street = streetInput.value.trim();
    designData.city = cityInput.value.trim();
    designData.postcode = postcodeInput.value.trim();
    
    const sizeInput = document.getElementById('gardenSize');
    if (sizeInput) {
        designData.gardenSize = sizeInput.value.trim();
    }
    
    // Budget is already saved in designData via selectBudget function
    
    // Hide form, show loading with animated progress
    document.getElementById('step4').classList.add('hidden');
    document.getElementById('loadingState').classList.remove('hidden');
    resetDesignProgress();
    startDesignProgress();
    
    // Prepare webhook payload
    const webhookPayload = {
        customer: {
            name: designData.name,
            email: designData.email,
            phone: designData.phone,
            houseNumber: designData.houseNumber,
            street: designData.street,
            city: designData.city,
            postcode: designData.postcode,
            address: `${designData.houseNumber ? designData.houseNumber + ' ' : ''}${designData.street}, ${designData.city}, ${designData.postcode}`
        },
        design: {
            features: designData.features,
            styleDescription: designData.styleDescription,
            gardenSize: designData.gardenSize,
            budget: designData.budget
        },
        photo: null, // Will be populated with base64 if photo exists
        metadata: {
            timestamp: new Date().toISOString(),
            source: 'website',
            formVersion: '2.0'
        }
    };
    
    // Convert photo to base64 if exists
    if (designData.photo) {
        const reader = new FileReader();
        reader.onload = async function(e) {
            webhookPayload.photo = {
                name: designData.photo.name,
                type: designData.photo.type,
                size: designData.photo.size,
                data: e.target.result
            };
            
            await sendToWebhook(webhookPayload);
        };
        reader.readAsDataURL(designData.photo);
    } else {
        await sendToWebhook(webhookPayload);
    }
}

async function sendToWebhook(payload) {
    console.log('🎨 AI DESIGN REQUEST - Sending to n8n workflow...');
    console.log('📦 Design Data:', payload);
    
    const webhookUrl = window.brandConfig?.webhooks?.design || 'https://your-n8n-webhook-url.com';
    
    console.log('🔗 Webhook URL:', webhookUrl);
    
    if (!webhookUrl || webhookUrl.includes('your-n8n-webhook-url')) {
        console.warn('⚠️ Webhook URL not configured. Using demo mode.');
        // Demo mode: Let animation run then complete
        setTimeout(() => {
            onDesignWebhookComplete(true, { demo: true });
        }, 40000); // Allow time for animation
        return;
    }
    
    try {
        console.log('📤 Sending to n8n...');
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        console.log('✅ Response received:', response.status);
        
        if (!response.ok) {
            throw new Error(`Webhook returned status ${response.status}`);
        }
        
        // Try to parse JSON response
        let result = {};
        try {
            result = await response.json();
            console.log('📬 Workflow response:', result);
        } catch (e) {
            console.warn('Response is not JSON, treating as success');
        }
        
        // Check if webhook returned an error in the response body
        const hasError = result.success === false || 
                         result.error || 
                         result.status === 'error' ||
                         result.status === 'failed';
        
        if (hasError) {
            const errorMessage = result.error || result.message || 'The workflow encountered an error generating your design.';
            console.error('❌ Webhook returned error:', errorMessage);
            onDesignWebhookComplete(false, { error: errorMessage });
        } else {
            onDesignWebhookComplete(true, result);
        }
        
    } catch (error) {
        console.error('❌ Error submitting design request:', error);
        stopDesignProgress();
        onDesignWebhookComplete(false, { error: 'There was an error processing your request. Please try again or contact us.' });
    }
}

function showSuccess() {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('successResult').classList.remove('hidden');
    document.getElementById('confirmEmail').textContent = designData.email;
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showError(errorMessage) {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('successResult').classList.add('hidden');
    
    // Check if error result element exists, create if not
    let errorResult = document.getElementById('designError');
    if (!errorResult) {
        // Create error element dynamically
        const loadingState = document.getElementById('loadingState');
        errorResult = document.createElement('div');
        errorResult.id = 'designError';
        errorResult.className = 'step-container text-center py-8';
        loadingState.parentNode.insertBefore(errorResult, loadingState.nextSibling);
    }
    
    errorResult.innerHTML = `
        <div class="bg-red-100 rounded-full h-20 w-20 flex items-center justify-center mx-auto mb-6">
            <i class="fas fa-exclamation-triangle text-red-600 text-4xl"></i>
        </div>
        <h3 class="font-heading font-bold text-3xl text-red-600 mb-4">Design Request Failed</h3>
        <p class="text-lg text-gray-700 mb-6">${errorMessage}</p>
        <div class="bg-red-50 rounded-xl p-6 max-w-md mx-auto mb-6 border border-red-200">
            <p class="text-gray-700 mb-4">
                <i class="fas fa-phone text-red-500 mr-2"></i>
                Call us at <strong>07444 887813</strong> for help
            </p>
            <p class="text-sm text-gray-500">
                Or email us at info@premiumlandscapes.co.uk
            </p>
        </div>
        <button onclick="location.reload()" class="bg-primary text-white px-8 py-3 rounded-full font-semibold hover:bg-primary-dark transition">
            <i class="fas fa-redo mr-2"></i>Try Again
        </button>
    `;
    
    errorResult.classList.remove('hidden');
    
    console.error('❌ Design request failed:', errorMessage);
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
