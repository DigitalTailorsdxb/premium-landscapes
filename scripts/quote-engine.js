// Premium Landscapes - Instant Quote Engine
// Multi-step conversational quote system

// ============================================================================
// SUBMISSION OVERLAY CONTROLLER - Simple, bulletproof UI transitions
// ============================================================================

const SubmissionOverlay = {
    isRedesign: false,
    hasImage: false,
    currentStep: 0,
    totalSteps: 6,
    stepTimers: [],
    
    // Progress steps WITH AI design (90 seconds total - 8 steps @ 11.25s each)
    stepsWithDesign: [
        { icon: 'fa-clipboard-list', label: 'Reading your requirements...' },
        { icon: 'fa-image', label: 'Analysing your garden photo...' },
        { icon: 'fa-brain', label: 'Understanding your space...' },
        { icon: 'fa-wand-magic-sparkles', label: 'AI creating your design...' },
        { icon: 'fa-palette', label: 'Rendering visualisation...' },
        { icon: 'fa-sparkles', label: 'Adding finishing touches...' },
        { icon: 'fa-file-pdf', label: 'Preparing your quote...' },
        { icon: 'fa-envelope', label: 'Sending to your email...' }
    ],
    // Progress steps WITHOUT AI design (30 seconds total)
    stepsQuoteOnly: [
        { icon: 'fa-clipboard-check', label: 'Reading your selections...' },
        { icon: 'fa-calculator', label: 'Calculating quantities...' },
        { icon: 'fa-sterling-sign', label: 'Getting local prices...' },
        { icon: 'fa-file-invoice', label: 'Building your quote...' },
        { icon: 'fa-envelope', label: 'Sending to your email...' },
        { icon: 'fa-check-circle', label: 'Complete!' }
    ],
    
    // Show the overlay immediately
    show(isRedesign, hasImage = false) {
        console.log('🎯 OVERLAY: Showing submission overlay, isRedesign:', isRedesign, 'hasImage:', hasImage);
        this.isRedesign = isRedesign;
        this.hasImage = hasImage;
        this.currentStep = 0;
        
        const overlay = document.getElementById('submissionOverlay');
        if (!overlay) {
            console.error('❌ OVERLAY: submissionOverlay element not found!');
            return;
        }
        
        // Force show overlay
        overlay.classList.remove('hidden');
        overlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // Set title based on mode
        const title = document.getElementById('overlayTitle');
        const subtitle = document.getElementById('overlaySubtitle');
        if (hasImage) {
            title.textContent = 'Creating Your AI Garden Design';
            subtitle.textContent = 'Our AI is generating a bespoke visualisation of your garden';
        } else {
            title.textContent = 'Processing Your Quote';
            subtitle.textContent = 'Calculating prices and preparing your quote';
        }
        
        // Build progress steps
        this.buildProgressSteps();
        
        // Start animation
        this.animateSteps();
        
        console.log('✅ OVERLAY: Overlay is now visible');
    },
    
    buildProgressSteps() {
        const container = document.getElementById('overlayProgress');
        const steps = this.hasImage ? this.stepsWithDesign : this.stepsQuoteOnly;
        
        container.innerHTML = steps.map((step, i) => `
            <div class="overlay-step flex items-center py-2" data-step="${i}">
                <div class="step-icon w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center mr-4 transition-all duration-300">
                    <i class="fas ${step.icon} text-gray-400 text-lg"></i>
                </div>
                <div class="flex-1">
                    <p class="step-label font-medium text-gray-400 transition-all duration-300">${step.label}</p>
                </div>
                <div class="step-status w-8 h-8 flex items-center justify-center">
                    <i class="fas fa-circle text-gray-200 text-sm"></i>
                </div>
            </div>
        `).join('');
    },
    
    animateSteps() {
        const steps = this.hasImage ? this.stepsWithDesign : this.stepsQuoteOnly;
        // 100 seconds with image (8 steps @ 12.5s each), 15 seconds for quote only (6 steps @ 2.5s each)
        const stepDuration = this.hasImage ? 12500 : 2500;
        
        console.log(`⏱️ OVERLAY: Animation duration - ${this.hasImage ? '90s (with design)' : '30s (quote only)'}`);
        
        steps.forEach((_, i) => {
            const timer = setTimeout(() => {
                this.activateStep(i);
                
                // If last step, show success after a delay
                if (i === steps.length - 1) {
                    setTimeout(() => this.showSuccess(), 2000);
                }
            }, i * stepDuration);
            this.stepTimers.push(timer);
        });
    },
    
    activateStep(stepIndex) {
        const container = document.getElementById('overlayProgress');
        const stepEl = container.querySelector(`[data-step="${stepIndex}"]`);
        
        if (stepEl) {
            const icon = stepEl.querySelector('.step-icon');
            const label = stepEl.querySelector('.step-label');
            const statusContainer = stepEl.querySelector('.step-status');
            
            // Activate this step
            icon.classList.remove('bg-gray-100');
            icon.classList.add('bg-primary', 'shadow-lg');
            icon.querySelector('i').classList.remove('text-gray-400');
            icon.querySelector('i').classList.add('text-white');
            
            label.classList.remove('text-gray-400');
            label.classList.add('text-gray-800', 'font-semibold');
            
            // Replace with bigger green tick
            statusContainer.innerHTML = '<i class="fas fa-check-circle text-green-500 text-2xl"></i>';
        }
        
        console.log(`🔄 OVERLAY: Step ${stepIndex + 1} activated`);
    },
    
    showSuccess() {
        console.log('🎉 OVERLAY: Showing success state, hasImage:', this.hasImage);
        
        // Hide processing, show appropriate success
        document.getElementById('overlayProcessing').classList.add('hidden');
        
        if (this.hasImage) {
            document.getElementById('overlaySuccessRedesign').classList.remove('hidden');
        } else {
            document.getElementById('overlaySuccessProducts').classList.remove('hidden');
        }
    },
    
    // Force complete animation (called when webhook returns)
    forceComplete() {
        // Clear pending timers
        this.stepTimers.forEach(t => clearTimeout(t));
        this.stepTimers = [];
        
        // Activate all steps
        const steps = this.hasImage ? this.stepsWithDesign : this.stepsQuoteOnly;
        steps.forEach((_, i) => this.activateStep(i));
        
        // Show success
        setTimeout(() => this.showSuccess(), 500);
    },
    
    // Hide overlay (for errors or reset)
    hide() {
        const overlay = document.getElementById('submissionOverlay');
        if (overlay) {
            overlay.classList.add('hidden');
            overlay.style.display = 'none';
        }
        document.body.style.overflow = '';
        
        // Clear timers
        this.stepTimers.forEach(t => clearTimeout(t));
        this.stepTimers = [];
    }
};

let currentStep = 1;
const totalSteps = 6;
let quoteData = {
    quoteMode: '', // 'full-redesign' or 'individual-products'
    features: [],
    productDetails: {}, // Stores details for each product
    productAreas: {}, // Stores area/size for each product
    productMaterials: {}, // Stores selected sub-product/material for each product
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

// ============================================================================
// INDIVIDUAL PRODUCTS PROGRESS ANIMATION - 10 seconds total
// ============================================================================
let progressStateIndividual = {
    currentStep: 0,
    totalSteps: 6,
    isAnimating: false,
    webhookComplete: false,
    webhookSuccess: false,
    webhookResult: null,
    timeouts: []
};

// Step timings for individual products - Total: 10 seconds
const individualStepDurations = [
    1500,  // 0: Reading your selections (1.5s)
    1500,  // 1: Calculating quantities (1.5s)
    2000,  // 2: Getting local prices (2s)
    2000,  // 3: Preparing your quote (2s)
    2000,  // 4: Sending email (2s)
    1000   // 5: Done! (1s)
];

// Reset individual products progress timeline
function resetIndividualProgressTimeline() {
    progressStateIndividual = {
        currentStep: 0,
        totalSteps: 6,
        isAnimating: false,
        webhookComplete: false,
        webhookSuccess: false,
        webhookResult: null,
        timeouts: []
    };
    
    const steps = document.querySelectorAll('#progressTimelineIndividual .progress-step-ind');
    steps.forEach(step => {
        step.classList.remove('active', 'completed');
    });
    
    console.log('🎨 Individual products progress timeline reset');
}

// Start individual products progress animation
function startIndividualProgressAnimation() {
    progressStateIndividual.isAnimating = true;
    advanceIndividualProgressStep(0);
}

// Advance individual products progress step
function advanceIndividualProgressStep(stepIndex) {
    if (!progressStateIndividual.isAnimating) return;
    
    const steps = document.querySelectorAll('#progressTimelineIndividual .progress-step-ind');
    const totalSteps = steps.length;
    
    // Mark previous step as completed
    if (stepIndex > 0 && stepIndex <= totalSteps) {
        steps[stepIndex - 1].classList.remove('active');
        steps[stepIndex - 1].classList.add('completed');
    }
    
    // Mark current step as active
    if (stepIndex < totalSteps) {
        steps[stepIndex].classList.add('active');
        progressStateIndividual.currentStep = stepIndex;
        
        const stepDuration = individualStepDurations[stepIndex];
        
        // If this is the final step, complete animation after brief pause
        if (stepIndex === totalSteps - 1) {
            const timeout = setTimeout(() => {
                completeIndividualProgressAnimation();
            }, stepDuration);
            progressStateIndividual.timeouts.push(timeout);
            return;
        }
        
        // Schedule next step
        const timeout = setTimeout(() => {
            advanceIndividualProgressStep(stepIndex + 1);
        }, stepDuration);
        progressStateIndividual.timeouts.push(timeout);
    }
}

// Called when webhook completes for individual products
function onIndividualWebhookComplete(success, result) {
    progressStateIndividual.webhookComplete = true;
    progressStateIndividual.webhookSuccess = success;
    progressStateIndividual.webhookResult = result;
    
    if (success) {
        console.log('✅ Individual products webhook completed successfully');
    } else {
        console.warn('⚠️ Individual products webhook returned error:', result?.error || result?.message);
    }
}

// Complete the individual products progress animation
function completeIndividualProgressAnimation() {
    progressStateIndividual.isAnimating = false;
    
    // Clear any remaining timeouts
    progressStateIndividual.timeouts.forEach(t => clearTimeout(t));
    progressStateIndividual.timeouts = [];
    
    // Mark final step as completed
    const steps = document.querySelectorAll('#progressTimelineIndividual .progress-step-ind');
    if (steps.length > 0) {
        steps[steps.length - 1].classList.remove('active');
        steps[steps.length - 1].classList.add('completed');
    }
    
    // Hide loading state
    document.getElementById('loadingState').classList.add('hidden');
    
    // Show result based on webhook response
    const result = progressStateIndividual.webhookResult || { success: true };
    if (progressStateIndividual.webhookSuccess === false && result.success === false) {
        showQuoteError(result);
    } else {
        showQuoteResult(result);
    }
}

// Stop individual products progress animation (for errors)
function stopIndividualProgressAnimation() {
    progressStateIndividual.isAnimating = false;
    progressStateIndividual.timeouts.forEach(t => clearTimeout(t));
    progressStateIndividual.timeouts = [];
}

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
    
    // Scroll to top for visibility
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Always show success - the quote was submitted, email is on the way
    showQuoteResultRedesign(progressState.webhookResult || { success: true });
}

// Show redesign-specific success result
function showQuoteResultRedesign(data) {
    console.log('🎨 showQuoteResultRedesign called - showing success UI');
    
    console.log('🎨 showQuoteResultRedesign - Starting success UI transition');
    
    // Hide loading animation
    const loadingState = document.getElementById('loadingStateRedesign');
    if (loadingState) {
        loadingState.classList.add('hidden');
        loadingState.style.display = 'none';
    }
    
    // Show success UI with force display
    const resultElement = document.getElementById('quoteResultRedesign');
    if (resultElement) {
        resultElement.classList.remove('hidden');
        resultElement.style.display = 'block';
        console.log('✅ SUCCESS UI DISPLAYED: quoteResultRedesign');
    } else {
        console.error('❌ quoteResultRedesign element NOT FOUND!');
    }
    
    console.log('✅ Full Garden Redesign request submitted successfully!');
    console.log('Customer will receive design proposal via email from n8n workflow');
    
    // If webhook returned a quote reference, display it
    if (data?.quoteRef && data.quoteRef !== 'processing') {
        const resultDiv = document.getElementById('quoteResultRedesign');
        const refDisplay = document.createElement('div');
        refDisplay.className = 'bg-purple-50 border border-purple-200 rounded-xl p-4 mb-6 text-center';
        refDisplay.innerHTML = `
            <p class="text-sm text-gray-600 mb-1">Your Quote Reference</p>
            <p class="font-bold text-xl text-purple-600">${data.quoteRef}</p>
        `;
        resultDiv.insertBefore(refDisplay, resultDiv.children[1]);
    }
}

// Stop progress animation (for errors)
function stopProgressAnimation() {
    progressState.isAnimating = false;
    progressState.timeouts.forEach(t => clearTimeout(t));
    progressState.timeouts = [];
}

// Sub-products configuration - matches n8n pricing workflow allocation keys EXACTLY
const subProducts = {
    'patio': {
        label: 'Paving Material',
        options: [
            // Natural Stone Paving
            { value: 'indian_sandstone', label: 'Indian Sandstone', price: '££' },
            { value: 'limestone_paving', label: 'Limestone', price: '£££' },
            { value: 'granite_paving', label: 'Granite', price: '£££' },
            { value: 'slate_paving', label: 'Slate', price: '£££' },
            { value: 'york_stone', label: 'York Stone', price: '££££' },
            { value: 'travertine', label: 'Travertine', price: '£££' },
            { value: 'quartzite', label: 'Quartzite', price: '£££' },
            // Natural Stone Setts
            { value: 'granite_setts', label: 'Granite Setts', price: '££' },
            { value: 'sandstone_setts', label: 'Sandstone Setts', price: '££' },
            { value: 'cobblestones', label: 'Cobblestones', price: '££' },
            // Manufactured Paving
            { value: 'porcelain_patio', label: 'Porcelain Tiles', price: '£££' },
            { value: 'concrete_paving', label: 'Concrete Paving', price: '££' },
            { value: 'block_paving', label: 'Block Paving', price: '££' },
            { value: 'resin_bound', label: 'Resin Bound', price: '££££' }
        ]
    },
    'decking': {
        label: 'Decking Type',
        options: [
            { value: 'composite_deck', label: 'Composite Decking', price: '£££' },
            { value: 'softwood_deck', label: 'Softwood (Treated)', price: '££' },
            { value: 'hardwood_deck', label: 'Hardwood', price: '££££' }
        ]
    },
    'turf': {
        label: 'Lawn Type',
        options: [
            { value: 'natural_turf', label: 'Natural Rolled Turf', price: '£' },
            { value: 'artificial_turf', label: 'Artificial Turf (35-40mm)', price: '££' }
        ]
    },
    'fencing': {
        label: 'Fencing Type',
        options: [
            { value: 'panel_fencing', label: 'Panel Fencing', price: '££' },
            { value: 'closeboard_fencing', label: 'Closeboard Fencing', price: '££' },
            { value: 'composite_fencing', label: 'Composite Fencing', price: '£££' },
            { value: 'trellis_panels', label: 'Trellis Panels', price: '££' }
        ]
    },
    'lighting': {
        label: 'Lighting Type',
        options: [
            { value: 'lighting_fitting', label: 'Lighting Fitting', price: '££' },
            { value: 'lighting_transformer', label: 'Lighting Transformer', price: '££' },
            { value: 'lighting_cable', label: 'Lighting Cable', price: '£' },
            { value: 'lighting_kit_10', label: 'Lighting Kit (10 fittings)', price: '££££' }
        ]
    },
    'steps': {
        label: 'Step Material',
        options: [
            { value: 'sandstone_step', label: 'Sandstone Steps', price: '£££' },
            { value: 'granite_step', label: 'Granite Steps', price: '££££' },
            { value: 'limestone_step', label: 'Limestone Steps', price: '£££' },
            { value: 'brick_step', label: 'Brick Steps', price: '£££' },
            { value: 'sleeper_step', label: 'Sleeper Steps', price: '££' }
        ]
    },
    'walls': {
        label: 'Wall Type',
        options: [
            { value: 'brick_wall', label: 'Brick Wall', price: '£££' },
            { value: 'stone_wall', label: 'Stone Wall', price: '££££' },
            { value: 'rendered_wall', label: 'Rendered Block Wall', price: '£££' },
            { value: 'sleeper_wall_single', label: 'Sleeper Wall (Single)', price: '££' },
            { value: 'sleeper_wall_double', label: 'Sleeper Wall (Double)', price: '£££' },
            { value: 'sleeper_wall_triple', label: 'Sleeper Wall (Triple)', price: '£££' }
        ]
    },
    'water-features': {
        label: 'Water Feature Type',
        options: [
            { value: 'water_feature', label: 'Water Feature', price: '££££' },
            { value: 'wall_mounted_feature', label: 'Wall-Mounted Feature', price: '£££' },
            { value: 'fountain_small', label: 'Small Fountain', price: '£££' },
            { value: 'fountain_large', label: 'Large Fountain', price: '££££' },
            { value: 'water_rill', label: 'Water Rill', price: '£££' },
            { value: 'cascade_waterfall', label: 'Cascade/Waterfall', price: '££££' },
            { value: 'water_bowl_contemporary', label: 'Contemporary Water Bowl', price: '££££' },
            { value: 'corten_steel_feature', label: 'Corten Steel Feature', price: '££££' }
        ]
    },
    'ponds': {
        label: 'Pond Type',
        options: [
            { value: 'small_pond', label: 'Small Garden Pond', price: '£££' },
            { value: 'medium_pond', label: 'Medium Garden Pond', price: '££££' },
            { value: 'large_pond', label: 'Large Garden Pond', price: '££££' },
            { value: 'wildlife_pond', label: 'Wildlife Pond', price: '££££' },
            { value: 'koi_pond', label: 'Koi Pond', price: '££££' },
            { value: 'pond_liner', label: 'Pond Liner', price: '£' },
            { value: 'pond_pump', label: 'Pond Pump', price: '££' },
            { value: 'pond_filter', label: 'Pond Filter', price: '£££' },
            { value: 'uv_clarifier', label: 'UV Clarifier', price: '££' }
        ]
    },
    'pergolas': {
        label: 'Pergola Type',
        options: [
            { value: 'timber_pergola_open_3x3', label: 'Timber Pergola (Open 3x3)', price: '£££' },
            { value: 'timber_pergola_roofed_3x3', label: 'Timber Pergola (Roofed 3x3)', price: '££££' },
            { value: 'aluminium_pergola_modern_3x3', label: 'Aluminium Pergola (Modern 3x3)', price: '££££' },
            { value: 'steel_pergola_flat_roof_3x3', label: 'Steel Pergola (Flat Roof 3x3)', price: '££££' },
            { value: 'pergola_attached', label: 'Attached Pergola', price: '£££' },
            { value: 'gazebo', label: 'Gazebo', price: '££££' }
        ]
    },
    'planting': {
        label: 'Planting Type',
        options: [
            { value: 'planting_beds', label: 'Planting Beds', price: '£' },
            { value: 'rendered_planter', label: 'Rendered Planter', price: '£££' },
            { value: 'raised_bed', label: 'Raised Bed', price: '£££' },
            { value: 'raised_bed_sleepers', label: 'Raised Bed (Sleepers)', price: '££' },
            { value: 'feature_tree', label: 'Feature Tree', price: '£££' },
            { value: 'shrub_large', label: 'Large Shrubs', price: '££' },
            { value: 'shrub_medium', label: 'Medium Shrubs', price: '£' },
            { value: 'topsoil', label: 'Topsoil', price: '££' },
            { value: 'mulch_bark', label: 'Mulch/Bark', price: '£' }
        ]
    },
    'hedging': {
        label: 'Hedging Type',
        options: [
            { value: 'native_hedging', label: 'Native Hedging', price: '££' },
            { value: 'instant_screening', label: 'Instant Screening', price: '£££' }
        ]
    },
    'aggregates': {
        label: 'Aggregate Type',
        options: [
            { value: 'gravel_path', label: 'Gravel Path', price: '££' },
            { value: 'decorative_gravel', label: 'Decorative Gravel', price: '££' },
            { value: 'bark_path', label: 'Bark Path', price: '£' },
            { value: 'slate_chippings', label: 'Slate Chippings', price: '££' },
            { value: 'pebbles_decorative', label: 'Decorative Pebbles', price: '££' },
            { value: 'stepping_stones', label: 'Stepping Stones', price: '££' }
        ]
    },
    'drainage': {
        label: 'Drainage Type',
        options: [
            { value: 'channel_drain', label: 'Channel Drain', price: '££' },
            { value: 'french_drain', label: 'French Drain', price: '££' },
            { value: 'soakaway', label: 'Soakaway', price: '£££' }
        ]
    },
    'other': {
        label: 'Product Type',
        options: [
            { value: '', label: '-- Select a product --', price: '' },
            { group: 'Fire & Seating', options: [
                { value: 'fire_pit', label: 'Fire Pit', price: '£££' },
                { value: 'sunken_firepit', label: 'Sunken Fire Pit', price: '£££' },
                { value: 'sunken_firepit_seating_package', label: 'Fire Pit & Seating Package', price: '££££' },
                { value: 'seating_area_basic', label: 'Seating Area (Basic)', price: '££££' },
                { value: 'seating_sunken', label: 'Sunken Seating Area', price: '££££' },
                { value: 'seating_rendered', label: 'Rendered Seating', price: '££££' },
                { value: 'seating_stone', label: 'Stone Seating', price: '££££' }
            ]},
            { group: 'Outdoor Kitchens', options: [
                { value: 'outdoor_kitchen_starter', label: 'Outdoor Kitchen (Starter)', price: '££££' },
                { value: 'outdoor_kitchen_standard', label: 'Outdoor Kitchen (Standard)', price: '££££' },
                { value: 'outdoor_kitchen_premium', label: 'Outdoor Kitchen (Premium)', price: '££££' },
                { value: 'bbq_area', label: 'BBQ Area', price: '£££' },
                { value: 'built_in_bbq', label: 'Built-in BBQ', price: '£££' }
            ]},
            { group: 'Garden Rooms & Storage', options: [
                { value: 'shed', label: 'Shed', price: '£££' },
                { value: 'shed_large', label: 'Shed (Large)', price: '£££' },
                { value: 'summer_house', label: 'Summer House', price: '££££' },
                { value: 'greenhouse_small', label: 'Greenhouse (Small)', price: '££££' },
                { value: 'greenhouse_medium', label: 'Greenhouse (Medium)', price: '££££' },
                { value: 'greenhouse_large', label: 'Greenhouse (Large)', price: '££££' },
                { value: 'garden_room', label: 'Garden Room', price: '££££' }
            ]},
            { group: 'Edging', options: [
                { value: 'edging_concrete', label: 'Concrete Edging', price: '£' },
                { value: 'edging_steel', label: 'Steel Edging', price: '££' },
                { value: 'edging_aluminium', label: 'Aluminium Edging', price: '££' },
                { value: 'edging_plastic', label: 'Plastic Edging', price: '£' }
            ]},
            { group: 'Decorative', options: [
                { value: 'decorative_screen', label: 'Decorative Screen', price: '£££' },
                { value: 'boulders_feature', label: 'Feature Boulders', price: '££' },
                { value: 'non_slip_ramp', label: 'Non-Slip Ramp', price: '£££' }
            ]}
        ]
    }
};

// Product examples for suggestions (legacy - kept for textarea placeholders)
const productExamples = {
    'patio': 'Any specific requirements...',
    'decking': 'Any specific requirements...',
    'turf': 'Any specific requirements...',
    'fencing': 'Height requirements, gate needed, etc...',
    'lighting': 'Specific areas to light, ambience preferences...',
    'full-redesign': 'Complete garden transformation',
    'other': 'Additional details...'
};

// Initialize quote engine
document.addEventListener('DOMContentLoaded', function() {
    initializeQuoteModeCards();
    initializeFeatureCards();
    initializeProductSearch();
    initializeAreaSlider();
    initializeBudgetOptions();
    initializeFileUpload();
    initializeFileUploadStep5();
    initializeAddProductButtons();
    initializePostcodeLookup();
    initializeDesignVisionNotes();
    initializeProductDetailsToggle();
    updateSummary();
});

function initializeProductDetailsToggle() {
    const toggleBtn = document.getElementById('toggleProductDetails');
    const collapsible = document.getElementById('productDetailsCollapsible');
    const toggleText = document.getElementById('toggleProductDetailsText');
    const toggleIcon = document.getElementById('toggleProductDetailsIcon');
    
    if (toggleBtn && collapsible) {
        toggleBtn.addEventListener('click', function() {
            const isHidden = collapsible.classList.contains('hidden');
            collapsible.classList.toggle('hidden');
            if (toggleText) toggleText.textContent = isHidden ? 'Hide' : 'Show';
            if (toggleIcon) toggleIcon.style.transform = isHidden ? 'rotate(180deg)' : '';
        });
    }
}

function updateSelectedProductsCount() {
    const countEl = document.getElementById('selectedProductsCount');
    if (countEl && quoteData.selectedProducts) {
        countEl.textContent = quoteData.selectedProducts.length;
    }
}

// Build flat searchable product list from subProducts
function buildSearchableProductList() {
    const products = [];
    
    // Category icons for display
    const categoryIcons = {
        'patio': 'fa-th-large',
        'decking': 'fa-border-all',
        'turf': 'fa-seedling',
        'fencing': 'fa-border-style',
        'lighting': 'fa-lightbulb',
        'steps': 'fa-stairs',
        'walls': 'fa-layer-group',
        'water-features': 'fa-water',
        'ponds': 'fa-fish',
        'pergolas': 'fa-archway',
        'planting': 'fa-leaf',
        'hedging': 'fa-tree',
        'aggregates': 'fa-circle',
        'drainage': 'fa-tint',
        'other': 'fa-plus-circle'
    };
    
    // Category display names
    const categoryNames = {
        'patio': 'Patio/Paving',
        'decking': 'Decking',
        'turf': 'Lawn/Turf',
        'fencing': 'Fencing',
        'lighting': 'Lighting',
        'steps': 'Steps',
        'walls': 'Walls',
        'water-features': 'Water Features',
        'ponds': 'Ponds',
        'pergolas': 'Pergolas',
        'planting': 'Planting',
        'hedging': 'Hedging',
        'aggregates': 'Aggregates/Gravel',
        'drainage': 'Drainage',
        'other': 'Other'
    };
    
    // Keyword synonyms for better search results
    const keywordSynonyms = {
        'composite_deck': 'composite timber wood plastic',
        'softwood_deck': 'timber wood treated pine',
        'hardwood_deck': 'timber wood oak teak',
        'natural_turf': 'grass lawn natural real',
        'artificial_turf': 'astro fake synthetic grass lawn turf',
        'indian_sandstone': 'stone paving natural',
        'porcelain_patio': 'porcelain tiles paving modern',
        'block_paving': 'brick blocks paving',
        'resin_bound': 'resin gravel smooth',
        'decorative_gravel': 'gravel stones pebbles aggregate',
        'gravel_path': 'pathway walkway gravel',
        'panel_fencing': 'fence panels wooden timber',
        'closeboard_fencing': 'featheredge wooden timber privacy fence',
        'composite_fencing': 'modern plastic fence',
        'lighting_fitting': 'led lights outdoor garden fitting',
        'lighting_kit_10': 'led lights outdoor garden kit',
        'timber_pergola_open_3x3': 'wooden timber shade cover pergola',
        'aluminium_pergola_modern_3x3': 'metal modern shade pergola',
        'gazebo': 'shelter cover outdoor structure',
        'fire_pit': 'fire firepit pit outdoor fire',
        'sunken_firepit': 'fire pit firepit sunken',
        'outdoor_kitchen_starter': 'bbq barbecue cooking kitchen',
        'outdoor_kitchen_standard': 'bbq barbecue cooking grill kitchen',
        'outdoor_kitchen_premium': 'bbq barbecue kitchen cooking premium',
        'bbq_area': 'barbecue grill cooking bbq',
        'built_in_bbq': 'barbecue grill built-in',
        'garden_room': 'office studio building room',
        'summer_house': 'building cabin summerhouse',
        'shed': 'storage shed wooden',
        'shed_large': 'storage shed wooden large',
        'feature_tree': 'tree specimen plant',
        'native_hedging': 'hedge privacy screening hedging',
        'instant_screening': 'privacy hedge screening instant',
        'raised_bed_sleepers': 'raised bed sleeper timber',
        'channel_drain': 'drainage channel linear',
        'french_drain': 'drainage french land',
        'soakaway': 'drainage soak away water',
        'small_pond': 'pond water fish garden',
        'koi_pond': 'pond koi fish japanese',
        'wildlife_pond': 'pond wildlife natural',
        'instant_screening': 'privacy hedge bamboo',
        'seating_area': 'bench seat outdoor'
    };
    
    Object.keys(subProducts).forEach(category => {
        const config = subProducts[category];
        config.options.forEach(opt => {
            if (opt.group) {
                // Handle grouped options (like in 'other')
                opt.options.forEach(subOpt => {
                    if (subOpt.value) {
                        const synonyms = keywordSynonyms[subOpt.value] || '';
                        products.push({
                            id: `${category}_${subOpt.value}`,
                            category: category,
                            categoryName: categoryNames[category] || category,
                            categoryIcon: categoryIcons[category] || 'fa-cube',
                            value: subOpt.value,
                            label: subOpt.label,
                            group: opt.group,
                            searchText: `${subOpt.label} ${opt.group} ${categoryNames[category]} ${synonyms}`.toLowerCase()
                        });
                    }
                });
            } else if (opt.value) {
                const synonyms = keywordSynonyms[opt.value] || '';
                products.push({
                    id: `${category}_${opt.value}`,
                    category: category,
                    categoryName: categoryNames[category] || category,
                    categoryIcon: categoryIcons[category] || 'fa-cube',
                    value: opt.value,
                    label: opt.label,
                    group: null,
                    searchText: `${opt.label} ${categoryNames[category]} ${synonyms}`.toLowerCase()
                });
            }
        });
    });
    
    return products;
}

// Searchable product list (built once on load)
const searchableProducts = buildSearchableProductList();

// Initialize product search functionality with autocomplete
function initializeProductSearch() {
    const searchInput = document.getElementById('productSearch');
    const dropdown = document.getElementById('searchResultsDropdown');
    const toggleBtn = document.getElementById('browseCategoriesToggle');
    const toggleContent = document.getElementById('browseCategoriesContent');
    const toggleIcon = document.getElementById('browseCategoriesIcon');
    
    if (!searchInput || !dropdown) return;
    
    // Browse categories toggle
    if (toggleBtn && toggleContent && toggleIcon) {
        toggleBtn.addEventListener('click', function() {
            const isHidden = toggleContent.classList.contains('hidden');
            toggleContent.classList.toggle('hidden');
            toggleIcon.style.transform = isHidden ? 'rotate(180deg)' : '';
        });
    }
    
    // Search input handler
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        
        if (searchTerm.length < 2) {
            dropdown.classList.add('hidden');
            dropdown.innerHTML = '';
            return;
        }
        
        // Filter products
        const matches = searchableProducts.filter(product => 
            product.searchText.includes(searchTerm) || 
            product.label.toLowerCase().includes(searchTerm)
        ).slice(0, 15); // Limit to 15 results
        
        if (matches.length === 0) {
            dropdown.innerHTML = `
                <div class="px-6 py-8 text-center">
                    <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                        <i class="fas fa-search text-2xl text-gray-400"></i>
                    </div>
                    <p class="text-gray-600 font-medium">No products found for "${this.value}"</p>
                    <p class="text-sm text-gray-400 mt-2">Try searching for "patio", "decking", or "bbq"</p>
                </div>
            `;
            dropdown.classList.remove('hidden');
            return;
        }
        
        // Build results HTML with modern styling
        let resultsHtml = '<div class="py-2">';
        let currentCategory = '';
        let itemIndex = 0;
        
        matches.forEach(product => {
            // Add category header if changed
            if (product.categoryName !== currentCategory) {
                if (currentCategory !== '') {
                    resultsHtml += '</div>';
                }
                currentCategory = product.categoryName;
                resultsHtml += `
                    <div class="sticky top-0 px-4 py-3 bg-gradient-to-r from-gray-50 to-white border-b border-gray-100 flex items-center gap-3 z-10">
                        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary/10 to-accent/10 flex items-center justify-center">
                            <i class="fas ${product.categoryIcon} text-primary text-sm"></i>
                        </div>
                        <span class="font-bold text-gray-700 text-sm uppercase tracking-wide">${product.categoryName}</span>
                    </div>
                    <div class="divide-y divide-gray-50">
                `;
            }
            
            // Check if already selected
            const isSelected = quoteData.selectedProducts && quoteData.selectedProducts.some(p => p.id === product.id);
            itemIndex++;
            
            resultsHtml += `
                <div class="search-result-item group px-4 py-3.5 cursor-pointer flex items-center justify-between transition-all duration-200 ${isSelected ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-500' : 'hover:bg-gradient-to-r hover:from-primary/5 hover:to-accent/5 border-l-4 border-transparent hover:border-primary'}"
                     data-product-id="${product.id}"
                     data-category="${product.category}"
                     data-value="${product.value}"
                     data-label="${product.label}">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl ${isSelected ? 'bg-gradient-to-br from-green-400 to-emerald-500' : 'bg-gradient-to-br from-gray-100 to-gray-200 group-hover:from-primary/20 group-hover:to-accent/20'} flex items-center justify-center transition-all duration-200">
                            <i class="fas ${isSelected ? 'fa-check text-white' : product.categoryIcon + ' text-gray-500 group-hover:text-primary'} text-sm"></i>
                        </div>
                        <div>
                            <span class="font-semibold text-gray-800 block">${product.label}</span>
                            ${product.group ? `<span class="text-xs text-gray-400">${product.group}</span>` : ''}
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        ${isSelected 
                            ? '<span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-green-500 text-white text-xs font-bold shadow-sm"><i class="fas fa-check"></i> Added</span>' 
                            : '<span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-bold opacity-0 group-hover:opacity-100 transition-opacity"><i class="fas fa-plus"></i> Add</span>'}
                    </div>
                </div>
            `;
        });
        
        if (currentCategory !== '') {
            resultsHtml += '</div>';
        }
        resultsHtml += '</div>';
        
        dropdown.innerHTML = resultsHtml;
        dropdown.classList.remove('hidden');
        
        // Add click handlers to results
        dropdown.querySelectorAll('.search-result-item').forEach(item => {
            item.addEventListener('click', function() {
                const productId = this.dataset.productId;
                const category = this.dataset.category;
                const value = this.dataset.value;
                const label = this.dataset.label;
                
                addProductFromSearch(productId, category, value, label);
                
                // Clear search and close dropdown
                searchInput.value = '';
                dropdown.classList.add('hidden');
                dropdown.innerHTML = '';
            });
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });
    
    // Focus shows dropdown if there's text
    searchInput.addEventListener('focus', function() {
        if (this.value.length >= 2) {
            this.dispatchEvent(new Event('input'));
        }
    });
}

// Add product from search selection
function addProductFromSearch(productId, category, value, label) {
    // Initialize selectedProducts array if needed
    if (!quoteData.selectedProducts) {
        quoteData.selectedProducts = [];
    }
    
    // Check if already added
    if (quoteData.selectedProducts.some(p => p.id === productId)) {
        return; // Already added
    }
    
    // Add to selected products
    quoteData.selectedProducts.push({
        id: productId,
        category: category,
        value: value,
        label: label
    });
    
    // Also add to features for compatibility
    if (!quoteData.features.includes(category)) {
        quoteData.features.push(category);
    }
    
    // Set the material for this category
    quoteData.productMaterials[category] = value;
    
    // Build the product detail fields
    buildProductDetailFieldsNew();
    updateSummary();
    updateSelectedProductsCount();
    
    // Show the selected products section
    const section = document.getElementById('selectedProductsSection');
    if (section) {
        section.classList.remove('hidden');
    }
}

// New product detail fields builder for search-based selection
function buildProductDetailFieldsNew() {
    const container = document.getElementById('productDetailFields');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!quoteData.selectedProducts || quoteData.selectedProducts.length === 0) {
        const section = document.getElementById('selectedProductsSection');
        if (section) {
            section.classList.add('hidden');
        }
        updateSelectedProductsCount();
        return;
    }
    
    updateSelectedProductsCount();
    
    quoteData.selectedProducts.forEach((product, index) => {
        const config = getUnitConfig(product.category, product.value);
        
        // Auto-populate quantity to 1 for singular products (water features, pergolas, etc.)
        let defaultValue = quoteData.productAreas[product.id] || '';
        if (!defaultValue && isSingularProduct(product.value)) {
            defaultValue = '1';
            quoteData.productAreas[product.id] = '1';
        }
        
        const fieldHtml = `
            <div class="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow product-detail-field" data-product-id="${product.id}">
                <div class="flex justify-between items-center mb-4 pb-3 border-b border-gray-100">
                    <h4 class="font-bold text-gray-900 text-base flex items-center">
                        <span class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                            <i class="fas fa-check text-green-600 text-sm"></i>
                        </span>
                        ${product.label}
                    </h4>
                    <button type="button" onclick="removeProductFromSearch('${product.id}')" class="text-gray-400 hover:text-red-500 transition-colors text-sm flex items-center gap-1 px-2 py-1 rounded-lg hover:bg-red-50">
                        <i class="fas fa-times"></i>
                        <span class="hidden sm:inline">Remove</span>
                    </button>
                </div>
                
                <!-- Size/Quantity Input -->
                <div id="area-container-${product.id}">
                    <label class="block text-sm font-semibold text-gray-700 mb-2" id="area-label-${product.id}">${config.label}</label>
                    <div class="flex gap-2">
                        <input 
                            type="number" 
                            id="area-${product.id}"
                            min="1"
                            class="flex-1 px-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-base"
                            placeholder="${config.placeholder}"
                            value="${defaultValue}"
                        />
                        <span class="flex items-center px-4 text-gray-600 bg-gray-100 rounded-xl font-medium" id="area-unit-${product.id}">${config.unit}</span>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += fieldHtml;
    });
    
    // Add event listeners for area inputs
    quoteData.selectedProducts.forEach(product => {
        const areaInput = document.getElementById(`area-${product.id}`);
        if (areaInput) {
            areaInput.addEventListener('input', function() {
                quoteData.productAreas[product.id] = this.value;
                updateSummary();
            });
        }
    });
}

// Remove product from search selection
function removeProductFromSearch(productId) {
    if (!quoteData.selectedProducts) return;
    
    // Find and remove the product
    const index = quoteData.selectedProducts.findIndex(p => p.id === productId);
    if (index > -1) {
        const removedProduct = quoteData.selectedProducts[index];
        quoteData.selectedProducts.splice(index, 1);
        
        // Remove from areas (keyed by product.id)
        delete quoteData.productAreas[productId];
        
        // Check if category still has products
        const categoryStillHasProducts = quoteData.selectedProducts.some(p => p.category === removedProduct.category);
        
        if (!categoryStillHasProducts) {
            // No more products in this category - remove from features
            quoteData.features = quoteData.features.filter(f => f !== removedProduct.category);
            delete quoteData.productMaterials[removedProduct.category];
        } else {
            // Update productMaterials to reflect remaining products in this category
            const remainingInCategory = quoteData.selectedProducts.filter(p => p.category === removedProduct.category);
            if (remainingInCategory.length > 0) {
                // Use the first remaining product's value as the category material
                quoteData.productMaterials[removedProduct.category] = remainingInCategory[0].value;
            }
        }
    }
    
    buildProductDetailFieldsNew();
    updateSummary();
}

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
    const searchInput = document.getElementById('productSearch');
    
    featureCards.forEach(card => {
        card.addEventListener('click', function() {
            const feature = this.dataset.feature;
            
            // Get the category display name
            const categoryNames = {
                'patio': 'Patio',
                'decking': 'Decking',
                'turf': 'Turf',
                'driveway': 'Driveway',
                'fencing': 'Fencing',
                'lighting': 'Lighting',
                'steps': 'Steps',
                'walls': 'Walls',
                'water-features': 'Water',
                'pergolas': 'Pergola',
                'planting': 'Planting',
                'other': ''
            };
            
            // Pre-fill search with category name to show all products in that category
            if (searchInput) {
                const searchTerm = categoryNames[feature] || feature;
                searchInput.value = searchTerm;
                searchInput.focus();
                searchInput.dispatchEvent(new Event('input'));
                
                // Scroll to search
                searchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });
}

// Build material select options HTML
function buildMaterialSelectOptions(feature) {
    const config = subProducts[feature];
    if (!config) return '';
    
    let optionsHtml = '<option value="">-- Select ' + config.label + ' --</option>';
    
    config.options.forEach(opt => {
        if (opt.group) {
            optionsHtml += `<optgroup label="${opt.group}">`;
            opt.options.forEach(subOpt => {
                optionsHtml += `<option value="${subOpt.value}">${subOpt.label}</option>`;
            });
            optionsHtml += '</optgroup>';
        } else {
            optionsHtml += `<option value="${opt.value}">${opt.label}</option>`;
        }
    });
    
    return optionsHtml;
}

// LM Products - these always use linear metres (from n8n pricing)
const LM_PRODUCTS = [
    'panel_fencing', 'closeboard_fencing', 'composite_fencing', 'trellis_panels',
    'edging_concrete', 'edging_steel', 'edging_aluminium', 'edging_plastic',
    'sleeper_wall_single', 'sleeper_wall_double', 'sleeper_wall_triple', 'raised_bed_sleepers',
    'native_hedging', 'instant_screening',
    'channel_drain', 'french_drain', 'water_rill'
];

// Products that typically only have 1 (auto-populate quantity)
const SINGULAR_PRODUCTS = [
    'water_feature', 'wall_mounted_feature', 'fountain', 'cascade_waterfall', 'water_bowl', 'corten_steel',
    'pond', 'small_pond', 'medium_pond', 'large_pond', 'koi_pond', 'wildlife_pond',
    'pergola', 'timber_pergola', 'aluminium_pergola', 'steel_pergola', 'pergola_attached', 'gazebo',
    'fire_pit', 'sunken_firepit', 'sunken_firepit_seating',
    'seating_area', 'seating_sunken', 'seating_rendered', 'seating_stone',
    'outdoor_kitchen', 'bbq_area', 'built_in_bbq',
    'garden_room', 'summer_house', 'shed', 'greenhouse', 'soakaway', 'non_slip_ramp'
];

// Check if a product should auto-populate with 1
function isSingularProduct(material) {
    if (!material) return false;
    return SINGULAR_PRODUCTS.some(singular => material.includes(singular));
}

// Get unit configuration for a product based on its material selection
function getUnitConfig(feature, material) {
    // Check if this specific product requires linear metres
    if (material && LM_PRODUCTS.includes(material)) {
        return { label: 'Length (metres)', placeholder: '', unit: 'lm' };
    }
    
    const baseConfig = {
        'fencing': { label: 'Length (metres)', placeholder: '', unit: 'lm' },
        'hedging': { label: 'Length (metres)', placeholder: '', unit: 'lm' },
        'lighting': { label: 'Number of Fittings', placeholder: '', unit: 'fittings' },
        'steps': { label: 'Number of Steps', placeholder: '', unit: 'steps' },
        'walls': { label: 'Length (metres)', placeholder: '', unit: 'lm' },
        'drainage': { label: 'Length (metres)', placeholder: '', unit: 'lm' },
        'water-features': { label: 'Quantity', placeholder: '', unit: 'qty' },
        'ponds': { label: 'Quantity', placeholder: '', unit: 'qty' },
        'pergolas': { label: 'Quantity', placeholder: '', unit: 'qty' },
        'aggregates': { label: 'Area (m²)', placeholder: '', unit: 'm²' },
        'planting': { label: 'Quantity / Area', placeholder: '', unit: 'qty' },
        'full-redesign': { label: 'Total Area (m²)', placeholder: '', unit: 'm²' },
        'default': { label: 'Area (m²)', placeholder: '', unit: 'm²' }
    };
    
    // Special unit handling for "other" products based on material type
    if (feature === 'other' && material) {
        // Edging - linear metres
        if (material.includes('edging')) {
            return { label: 'Length (metres)', placeholder: '', unit: 'lm' };
        }
        // Individual items (pergolas, sheds, fire pits, etc.)
        if (material.includes('pergola') || material.includes('gazebo') || material.includes('shed') || 
            material.includes('greenhouse') || material.includes('summer_house') || material.includes('garden_room') ||
            material.includes('firepit') || material.includes('seating') || 
            material.includes('kitchen') || material.includes('bbq') || material.includes('screen') || 
            material.includes('soakaway') || material.includes('boulder') || material.includes('ramp')) {
            return { label: 'Quantity', placeholder: '', unit: 'qty' };
        }
    }
    
    return baseConfig[feature] || baseConfig['default'];
}

// Build product detail fields for Step 2
function buildProductDetailFields() {
    const container = document.getElementById('productDetailFields');
    container.innerHTML = '';
    
    quoteData.features.forEach((feature, index) => {
        const featureName = feature.charAt(0).toUpperCase() + feature.slice(1).replace('-', ' ');
        const subProductConfig = subProducts[feature];
        const savedMaterial = quoteData.productMaterials[feature] || '';
        const config = getUnitConfig(feature, savedMaterial);
        
        // Build material select HTML
        let materialSelectHtml = '';
        if (subProductConfig) {
            materialSelectHtml = `
                <div class="mb-4">
                    <label class="block text-sm font-semibold text-gray-700 mb-2">${subProductConfig.label} <span class="text-red-500">*</span></label>
                    <select 
                        id="material-${feature}" 
                        class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-base bg-white cursor-pointer appearance-none"
                        style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27 fill=%27none%27 stroke=%27%236b7280%27 stroke-width=%272%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpolyline points=%276 9 12 15 18 9%27%3e%3c/polyline%3e%3c/svg%3e'); background-repeat: no-repeat; background-position: right 1rem center; background-size: 1em;"
                    >
                        ${buildMaterialSelectOptions(feature)}
                    </select>
                </div>
            `;
        }
        
        const fieldHtml = `
            <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow product-detail-field" data-feature="${feature}">
                <div class="flex justify-between items-center mb-4 pb-3 border-b border-gray-100">
                    <h4 class="font-bold text-gray-900 text-lg flex items-center">
                        <span class="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center mr-3">
                            <i class="fas fa-th-large text-primary text-sm"></i>
                        </span>
                        ${featureName}
                    </h4>
                    <button type="button" onclick="removeProduct('${feature}')" class="text-gray-400 hover:text-red-500 transition-colors text-sm flex items-center gap-1 px-2 py-1 rounded-lg hover:bg-red-50">
                        <i class="fas fa-times"></i>
                        <span class="hidden sm:inline">Remove</span>
                    </button>
                </div>
                
                <!-- Material Selection Dropdown -->
                ${materialSelectHtml}
                
                <!-- Area/Size Input Field -->
                <div class="mb-4" id="area-container-${feature}">
                    <label class="block text-sm font-semibold text-gray-700 mb-2" id="area-label-${feature}">${config.label}</label>
                    <div class="flex gap-2">
                        <input 
                            type="number" 
                            id="area-${feature}"
                            min="1"
                            class="flex-1 px-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-base"
                            placeholder="${config.placeholder}"
                        />
                        <span class="flex items-center px-4 text-gray-600 bg-gray-100 rounded-xl font-medium" id="area-unit-${feature}">${config.unit}</span>
                    </div>
                </div>
                
                            </div>
        `;
        container.innerHTML += fieldHtml;
    });
    
    // Restore previously entered values and add event listeners
    quoteData.features.forEach(feature => {
        const areaInput = document.getElementById(`area-${feature}`);
        const materialSelect = document.getElementById(`material-${feature}`);
        
        // Restore values
        if (areaInput && quoteData.productAreas[feature]) {
            areaInput.value = quoteData.productAreas[feature];
        }
        if (materialSelect && quoteData.productMaterials[feature]) {
            materialSelect.value = quoteData.productMaterials[feature];
        }
        
        // Add event listeners
        if (areaInput) {
            areaInput.addEventListener('input', function() {
                quoteData.productAreas[feature] = this.value;
                updateSummary();
            });
        }
        if (materialSelect) {
            materialSelect.addEventListener('change', function() {
                quoteData.productMaterials[feature] = this.value;
                
                // Update the unit label/placeholder dynamically based on material selection
                const newConfig = getUnitConfig(feature, this.value);
                const areaLabel = document.getElementById(`area-label-${feature}`);
                const areaUnit = document.getElementById(`area-unit-${feature}`);
                const areaInputField = document.getElementById(`area-${feature}`);
                
                if (areaLabel) areaLabel.textContent = newConfig.label;
                if (areaUnit) areaUnit.textContent = newConfig.unit;
                if (areaInputField) areaInputField.placeholder = newConfig.placeholder;
                
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
    delete quoteData.productMaterials[feature];
    
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
    if (currentStep === 2 && quoteData.quoteMode === 'individual-products') {
        // Check at least one product selected
        if (!quoteData.selectedProducts || quoteData.selectedProducts.length === 0) {
            alert('Please select at least one product');
            return;
        }
        
        // Validate all products have quantities/areas filled in
        const missingQuantities = [];
        quoteData.selectedProducts.forEach(product => {
            const areaInput = document.getElementById(`area-${product.id}`);
            const value = areaInput ? parseInt(areaInput.value) : 0;
            if (!value || value <= 0) {
                missingQuantities.push(product.label);
            }
        });
        
        if (missingQuantities.length > 0) {
            alert(`Please enter quantities for: ${missingQuantities.join(', ')}`);
            return;
        }
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
    
    // Skip step 3 (Project Size & Budget) for individual products mode
    // since users already specify quantities for each product
    if (currentStep === 3 && quoteData.quoteMode === 'individual-products') {
        currentStep++;
    }
    
    // Skip step 6 (AI Design) for individual products mode - no images needed
    if (currentStep === 6 && quoteData.quoteMode === 'individual-products') {
        // Submit the quote directly instead of showing step 6
        submitQuote();
        return;
    }
    
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
        
        // Update button text - "Submit Quote" for individual products, "Continue" for full redesign
        const step5Btn = document.getElementById('step5ContinueBtn');
        if (step5Btn) {
            if (quoteData.quoteMode === 'individual-products') {
                step5Btn.innerHTML = '<i class="fas fa-paper-plane mr-2"></i> Get My Quote';
            } else {
                step5Btn.innerHTML = 'Continue <i class="fas fa-arrow-right ml-2"></i>';
            }
        }
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

// Scroll to show step content - scroll to top on mobile to show spacer above header
function scrollToFormTop() {
    setTimeout(() => {
        // Always scroll to top - simple and reliable
        window.scrollTo({ top: 0, behavior: 'instant' });
    }, 50);
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
    
    // Skip step 3 (Project Size & Budget) for individual products mode when going back
    if (currentStep === 3 && quoteData.quoteMode === 'individual-products') {
        currentStep--;
    }
    
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
    // Individual products mode has fewer steps (skips step 3 and 6)
    const isIndividualProducts = quoteData.quoteMode === 'individual-products';
    const effectiveTotalSteps = isIndividualProducts ? 4 : totalSteps;
    
    // Map current step to effective step number for individual products
    let effectiveCurrentStep = currentStep;
    if (isIndividualProducts) {
        // Steps are: 1, 2, 4, 5 (mapped to display as 1, 2, 3, 4)
        if (currentStep === 1) effectiveCurrentStep = 1;
        else if (currentStep === 2) effectiveCurrentStep = 2;
        else if (currentStep === 4) effectiveCurrentStep = 3;
        else if (currentStep === 5) effectiveCurrentStep = 4;
    }
    
    const percentage = (effectiveCurrentStep / effectiveTotalSteps) * 100;
    document.getElementById('progressBar').style.width = `${percentage}%`;
    document.getElementById('progressText').textContent = `Step ${effectiveCurrentStep} of ${effectiveTotalSteps}`;
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
    
    // Show selected products for individual mode (new search-based selection)
    if (quoteData.quoteMode === 'individual-products' && quoteData.selectedProducts && quoteData.selectedProducts.length > 0) {
        html += '<div class="space-y-2 mt-2">';
        quoteData.selectedProducts.forEach(product => {
            const area = quoteData.productAreas[product.id] || '';
            const unitConfig = getUnitConfig(product.category, product.value);
            
            // Build display text
            let displayText = product.label;
            if (area) {
                displayText += ` (${area}${unitConfig.unit})`;
            }
            
            html += `
                <div class="summary-item flex items-center space-x-2 bg-stone px-3 py-2 rounded-lg">
                    <i class="fas fa-check-circle text-green-500"></i>
                    <span class="text-sm font-semibold">${displayText}</span>
                </div>
            `;
        });
        html += '</div>';
    }
    // Fallback: Show selected products for legacy category-based selection
    else if (quoteData.quoteMode === 'individual-products' && quoteData.features.length > 0) {
        html += '<div class="space-y-2 mt-2">';
        quoteData.features.forEach(feature => {
            const featureName = feature.charAt(0).toUpperCase() + feature.slice(1).replace('-', ' ');
            const selectedMaterial = quoteData.productMaterials[feature] || '';
            const area = quoteData.productAreas[feature] || '';
            
            // Get material label for display
            let materialLabel = '';
            if (selectedMaterial && subProducts[feature]) {
                const config = subProducts[feature];
                for (const opt of config.options) {
                    if (opt.group) {
                        const found = opt.options.find(o => o.value === selectedMaterial);
                        if (found) { materialLabel = found.label; break; }
                    } else if (opt.value === selectedMaterial) {
                        materialLabel = opt.label; break;
                    }
                }
            }
            
            // Build display text
            let displayText = featureName;
            if (materialLabel) {
                displayText = materialLabel;
            }
            if (area) {
                const unitConfig = getUnitConfig(feature, selectedMaterial);
                displayText += ` (${area}${unitConfig.unit})`;
            }
            
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
            alert('Please upload a photo of your garden to get your free AI design visualisation.');
            isSubmittingQuote = false;
            return;
        }
    }
    
    // Determine quote mode and if image is attached
    const isFullRedesignMode = quoteData.quoteMode === 'full-redesign';
    const hasImageAttached = quoteData.aiDesign && (aiDesignFiles.length > 0 || quoteData.files.length > 0);
    console.log('🚀 SUBMIT QUOTE - Mode:', isFullRedesignMode ? 'FULL REDESIGN' : 'INDIVIDUAL PRODUCTS');
    console.log('🖼️ SUBMIT QUOTE - Has image for AI design:', hasImageAttached);
    
    // SHOW THE SUBMISSION OVERLAY IMMEDIATELY
    // 90 seconds with image, 30 seconds without
    SubmissionOverlay.show(isFullRedesignMode, hasImageAttached);
    
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
            
            // Demo mode: Simulate webhook completion - animation will run its full duration
            if (isFullRedesignMode) {
                // Let animation run then complete
                setTimeout(() => {
                    onWebhookComplete(true, { demo: true });
                }, 8000); // Allow time for animation
            } else {
                // For individual products, store demo result - animation will handle completion
                onIndividualWebhookComplete(true, { demo: true });
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
                
                // Check response based on success flag
                if (result.success === false) {
                    // Error response from n8n - store result for when animation completes
                    if (isFullRedesignMode) {
                        onWebhookComplete(false, result);
                    } else {
                        // For individual products, store result and let animation finish
                        onIndividualWebhookComplete(false, result);
                    }
                } else {
                    // Success - store result for when animation completes
                    if (isFullRedesignMode) {
                        onWebhookComplete(true, result);
                    } else {
                        // For individual products, store result and let animation finish
                        onIndividualWebhookComplete(true, result);
                    }
                }
                
            } catch (error) {
                console.error('❌ Network Error:', error);
                stopIndividualProgressAnimation();
                document.getElementById('loadingState').classList.add('hidden');
                // Network/timeout error - show with default contact info
                showNetworkError();
            }
        }
        
    } catch (error) {
        console.error('❌ Error preparing quote:', error);
        
        if (isFullRedesignMode) {
            // For full redesign, let animation continue - email will arrive
            console.warn('Payload preparation error, webhook may not have sent');
        } else {
            stopIndividualProgressAnimation();
            document.getElementById('loadingState').classList.add('hidden');
            showNetworkError();
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
                const selectedMaterial = quoteData.productMaterials[feature] || '';
                
                // Use dedicated area field if provided, otherwise parse from description or use default
                const dedicatedArea = quoteData.productAreas[feature];
                const defaultArea = Math.round(totalArea / quoteData.features.length);
                
                // Get material label from subProducts config
                const getMaterialLabel = (feature, materialKey) => {
                    const config = subProducts[feature];
                    if (!config) return materialKey;
                    
                    for (const opt of config.options) {
                        if (opt.group) {
                            const found = opt.options.find(o => o.value === materialKey);
                            if (found) return found.label;
                        } else if (opt.value === materialKey) {
                            return opt.label;
                        }
                    }
                    return materialKey;
                };
                
                const materialLabel = selectedMaterial ? getMaterialLabel(feature, selectedMaterial) : 'standard';
                
                // Base product structure with allocation key for n8n pricing
                const product = {
                    type: feature,
                    description: description || `${feature} installation`,
                    material: materialLabel,
                    allocationKey: selectedMaterial // This is the key n8n pricing uses!
                };
                
                // Add type-specific fields using dedicated area input
                if (feature === 'patio' || feature === 'aggregates') {
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
                } else if (feature === 'other') {
                    // For "other" category, determine unit type based on selected material
                    const config = getUnitConfig(feature, selectedMaterial);
                    if (config.unit === 'steps' || config.unit === 'qty' || config.unit === 'fittings') {
                        product.unitType = 'qty';
                        product.qty = dedicatedArea ? parseInt(dedicatedArea) : 1;
                    } else if (config.unit === 'm') {
                        product.unitType = 'm';
                        product.length = dedicatedArea ? parseInt(dedicatedArea) : 10;
                    } else {
                        product.unitType = 'm2';
                        product.area_m2 = dedicatedArea ? parseInt(dedicatedArea) : defaultArea;
                    }
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
                stylePreference: detectStylePreference(),
                maintenanceLevel: detectMaintenanceLevel(),
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
        
        // Add items array for individual products (n8n expected format)
        if (!isFullRedesign && quoteData.selectedProducts && quoteData.selectedProducts.length > 0) {
            payload.items = quoteData.selectedProducts.map(product => {
                const quantity = parseInt(quoteData.productAreas[product.id]) || 1;
                const unitConfig = getUnitConfig(product.category, product.value);
                
                return {
                    category: product.category,
                    product: product.value,
                    productLabel: product.label,
                    quantity: quantity,
                    unit: unitConfig?.unit || 'm²'
                };
            });
            console.log('📦 Individual products items array:', payload.items);
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
        
        // Add photo for AI design if requested (Full Redesign mode only)
        if (isFullRedesign && quoteData.aiDesign) {
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
    console.log('🎨 showQuoteResult - Starting success UI transition');
    stopIndividualProgressAnimation();
    
    // Hide loading animation
    const loadingEl = document.getElementById('loadingState');
    if (loadingEl) {
        loadingEl.classList.add('hidden');
        loadingEl.style.display = 'none';
    }
    
    // Show success UI with force display
    const resultEl = document.getElementById('quoteResult');
    if (resultEl) {
        resultEl.classList.remove('hidden');
        resultEl.style.display = 'block';
        console.log('✅ SUCCESS UI DISPLAYED: quoteResult');
    } else {
        console.error('❌ quoteResult element NOT FOUND!');
    }
    
    console.log('✅ Quote request submitted successfully!');
    console.log('Customer will receive detailed PDF quote via email from n8n workflow');
    
    // If webhook returned a quote reference, display it
    if (data?.quoteRef && data.quoteRef !== 'processing') {
        const quoteResultDiv = document.getElementById('quoteResult');
        const refDisplay = document.createElement('div');
        refDisplay.className = 'bg-green-50 border border-green-200 rounded-xl p-4 mb-6 text-center';
        refDisplay.innerHTML = `
            <p class="text-green-800 font-medium">
                <i class="fas fa-file-invoice mr-2"></i>
                Quote Reference: <strong>${data.quoteRef}</strong>
            </p>
        `;
        // Insert after the confirmation icon
        const confirmationBox = quoteResultDiv.querySelector('.bg-gradient-to-br');
        if (confirmationBox) {
            confirmationBox.parentNode.insertBefore(refDisplay, confirmationBox);
        }
    }
    
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
// Accepts full response object from n8n with contact info
// ============================================================================
function showQuoteError(errorResponse) {
    stopIndividualProgressAnimation();
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('loadingStateRedesign')?.classList.add('hidden');
    document.getElementById('quoteResult').classList.add('hidden');
    document.getElementById('quoteResultRedesign')?.classList.add('hidden');
    
    // Extract error details from response
    const message = errorResponse?.message || 'Sorry, there was an error processing your quote request.';
    const contact = errorResponse?.contact || {
        email: window.brandConfig?.contact?.email || 'premiumlandscapesuk@gmail.com',
        phone: window.brandConfig?.contact?.phone || '07877 934782',
        message: 'Please contact us with your details and we\'ll create your quote manually.'
    };
    const errorType = errorResponse?.error?.type || 'Unknown';
    const errorDetails = errorResponse?.error?.details || '';
    
    // Check if error result element exists, create if not
    let errorResult = document.getElementById('quoteError');
    if (!errorResult) {
        const loadingState = document.getElementById('loadingState');
        errorResult = document.createElement('div');
        errorResult.id = 'quoteError';
        errorResult.className = 'text-center py-8';
        loadingState.parentNode.insertBefore(errorResult, loadingState.nextSibling);
    }
    
    errorResult.innerHTML = `
        <div class="text-center mb-6">
            <div class="w-20 h-20 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="fas fa-exclamation-triangle text-4xl text-amber-600"></i>
            </div>
            <h2 class="font-heading font-bold text-2xl md:text-3xl text-gray-800 mb-3">Oops! Something Went Wrong</h2>
            <p class="text-gray-600 text-lg mb-6">${message}</p>
        </div>
        
        <div class="bg-white p-6 md:p-8 rounded-2xl mb-6 border-2 border-gray-200 shadow-lg">
            <h3 class="font-semibold text-lg text-primary mb-4 flex items-center justify-center">
                <i class="fas fa-headset mr-2"></i>
                Get Help Directly
            </h3>
            <div class="space-y-4 text-gray-700">
                <a href="mailto:${contact.email}" class="flex items-center justify-center p-3 bg-blue-50 rounded-xl hover:bg-blue-100 transition">
                    <i class="fas fa-envelope text-primary mr-3"></i>
                    <span class="font-medium">${contact.email}</span>
                </a>
                <a href="tel:${contact.phone.replace(/\s/g, '')}" class="flex items-center justify-center p-3 bg-green-50 rounded-xl hover:bg-green-100 transition">
                    <i class="fas fa-phone text-green-600 mr-3"></i>
                    <span class="font-medium">${contact.phone}</span>
                </a>
                <p class="text-center text-sm text-gray-500 mt-4">${contact.message}</p>
            </div>
        </div>
        
        <button onclick="location.reload()" class="bg-primary text-white px-8 py-3 rounded-full font-semibold hover:bg-primary-dark transition shadow-lg">
            <i class="fas fa-redo mr-2"></i>Try Again
        </button>
    `;
    
    errorResult.classList.remove('hidden');
    
    console.error('❌ Quote request failed:', message);
    console.error('Error type:', errorType, '| Details:', errorDetails);
    
    // Scroll to result
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================================================
// DISPLAY NETWORK ERROR
// Shows error message when network/timeout error occurs
// ============================================================================
function showNetworkError() {
    stopIndividualProgressAnimation();
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('loadingStateRedesign')?.classList.add('hidden');
    document.getElementById('quoteResult').classList.add('hidden');
    document.getElementById('quoteResultRedesign')?.classList.add('hidden');
    
    const contactEmail = window.brandConfig?.contact?.email || 'premiumlandscapesuk@gmail.com';
    const contactPhone = window.brandConfig?.contact?.phone || '07877 934782';
    
    // Check if error result element exists, create if not
    let errorResult = document.getElementById('quoteError');
    if (!errorResult) {
        const loadingState = document.getElementById('loadingState');
        errorResult = document.createElement('div');
        errorResult.id = 'quoteError';
        errorResult.className = 'text-center py-8';
        loadingState.parentNode.insertBefore(errorResult, loadingState.nextSibling);
    }
    
    errorResult.innerHTML = `
        <div class="text-center mb-6">
            <div class="w-20 h-20 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="fas fa-wifi text-4xl text-amber-600"></i>
            </div>
            <h2 class="font-heading font-bold text-2xl md:text-3xl text-gray-800 mb-3">Connection Error</h2>
            <p class="text-gray-600 text-lg mb-6">We couldn't reach our quote system. Please check your internet connection and try again.</p>
        </div>
        
        <div class="bg-white p-6 md:p-8 rounded-2xl mb-6 border-2 border-gray-200 shadow-lg">
            <h3 class="font-semibold text-lg text-primary mb-4 flex items-center justify-center">
                <i class="fas fa-headset mr-2"></i>
                If the problem persists, contact us:
            </h3>
            <div class="space-y-4 text-gray-700">
                <a href="mailto:${contactEmail}" class="flex items-center justify-center p-3 bg-blue-50 rounded-xl hover:bg-blue-100 transition">
                    <i class="fas fa-envelope text-primary mr-3"></i>
                    <span class="font-medium">${contactEmail}</span>
                </a>
                <a href="tel:${contactPhone.replace(/\s/g, '')}" class="flex items-center justify-center p-3 bg-green-50 rounded-xl hover:bg-green-100 transition">
                    <i class="fas fa-phone text-green-600 mr-3"></i>
                    <span class="font-medium">${contactPhone}</span>
                </a>
            </div>
        </div>
        
        <button onclick="location.reload()" class="bg-primary text-white px-8 py-3 rounded-full font-semibold hover:bg-primary-dark transition shadow-lg">
            <i class="fas fa-redo mr-2"></i>Try Again
        </button>
    `;
    
    errorResult.classList.remove('hidden');
    
    console.error('❌ Network error - could not reach quote system');
    
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
        'fencing': 'fencing',
        'hedging': 'hedging',
        'drainage': 'drainage',
        'aggregates': 'gravel and aggregates',
        'lighting': 'garden lighting',
        'other': 'custom features'
    };
    
    const features = quoteData.features.map(f => productNames[f] || f).join(', ');
    return `Garden with ${features}`;
}

// Helper: Detect style preference from user's design vision notes
function detectStylePreference() {
    const notes = (quoteData.designVisionNotes || quoteData.additionalNotes || '').toLowerCase();
    
    // Style keywords to detect (ordered by specificity)
    const stylePatterns = [
        { keywords: ['traditional', 'classic', 'heritage', 'period', 'victorian', 'edwardian'], style: 'traditional' },
        { keywords: ['cottage', 'country', 'rustic', 'farmhouse', 'natural', 'wildflower'], style: 'cottage' },
        { keywords: ['mediterranean', 'spanish', 'tuscan', 'italian', 'terracotta'], style: 'mediterranean' },
        { keywords: ['japanese', 'zen', 'oriental', 'asian', 'minimalist zen'], style: 'japanese' },
        { keywords: ['tropical', 'exotic', 'lush', 'jungle', 'palm'], style: 'tropical' },
        { keywords: ['formal', 'symmetrical', 'structured', 'parterre', 'geometric formal'], style: 'formal' },
        { keywords: ['modern', 'contemporary', 'sleek', 'minimalist', 'clean lines', 'architectural'], style: 'contemporary' },
        { keywords: ['low maintenance', 'easy care', 'minimal upkeep'], style: 'low-maintenance' }
    ];
    
    for (const pattern of stylePatterns) {
        for (const keyword of pattern.keywords) {
            if (notes.includes(keyword)) {
                console.log(`🎨 Style detected: "${pattern.style}" from keyword "${keyword}"`);
                return pattern.style;
            }
        }
    }
    
    // Default to 'not specified' so LLM can infer from other details
    console.log('🎨 No specific style detected - letting AI infer from description');
    return 'not specified - infer from customer description';
}

// Helper: Detect maintenance level from user's notes
function detectMaintenanceLevel() {
    const notes = (quoteData.designVisionNotes || quoteData.additionalNotes || '').toLowerCase();
    
    if (notes.includes('low maintenance') || notes.includes('easy care') || notes.includes('minimal upkeep') || notes.includes('no maintenance')) {
        return 'low maintenance';
    }
    if (notes.includes('high maintenance') || notes.includes('formal garden') || notes.includes('manicured')) {
        return 'high maintenance';
    }
    
    // Default - let AI decide based on design
    return 'moderate - as appropriate for design';
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
    
    // Update the header title, subtitle, and icon
    const step2Title = document.getElementById('step2Title');
    const step2Subtitle = document.getElementById('step2Subtitle');
    const step2Icon = document.getElementById('step2Icon');
    
    if (isFullRedesign) {
        // Update header for full redesign mode
        if (step2Title) step2Title.textContent = 'Full Garden Makeover';
        if (step2Subtitle) step2Subtitle.textContent = "We'll create a complete custom design and quote based on your vision and budget";
        if (step2Icon) step2Icon.innerHTML = '<i class="fas fa-wand-magic-sparkles text-xl text-white"></i>';
        
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
        // Update header for standard mode
        if (step2Title) step2Title.textContent = 'Select Your Products';
        if (step2Subtitle) step2Subtitle.textContent = "Choose the products you'd like quoted";
        if (step2Icon) step2Icon.innerHTML = '<i class="fas fa-boxes-stacked text-xl text-white"></i>';
        
        // Show standard mode
        console.log('📝 Showing Standard mode...');
        step2Standard.classList.remove('hidden');
        step2FullRedesign.classList.add('hidden');
        
        // Build standard product detail fields
        buildProductDetailFields();
        
        console.log('📝 Standard mode activated');
    }
}
