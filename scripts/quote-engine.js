// Premium Landscapes - Instant Quote Engine
// Multi-step conversational quote system

let currentStep = 1;
const totalSteps = 5;
let quoteData = {
    features: [],
    description: '',
    area: 40,
    budget: '',
    postcode: '',
    email: '',
    phone: '',
    aiDesign: false,
    files: []
};

// Initialize quote engine
document.addEventListener('DOMContentLoaded', function() {
    initializeFeatureCards();
    initializeExampleChips();
    initializeAreaSlider();
    initializeBudgetOptions();
    initializeFileUpload();
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
                }
            } else {
                quoteData.features = quoteData.features.filter(f => f !== feature);
            }
            
            updateSummary();
        });
    });
}

// Example chip functionality
function initializeExampleChips() {
    const exampleChips = document.querySelectorAll('.example-chip');
    const descriptionField = document.getElementById('projectDescription');
    
    exampleChips.forEach(chip => {
        chip.addEventListener('click', function(e) {
            e.preventDefault();
            const text = this.dataset.text;
            const currentValue = descriptionField.value.trim();
            
            if (currentValue) {
                descriptionField.value = currentValue + '\n• ' + text;
            } else {
                descriptionField.value = '• ' + text;
            }
            
            quoteData.description = descriptionField.value;
            updateSummary();
        });
    });
    
    // Update on manual typing
    descriptionField.addEventListener('input', function() {
        quoteData.description = this.value;
        updateSummary();
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

// File upload with drag & drop
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
        displayFilePreview(files);
        updateSummary();
    }
    
    function displayFilePreview(files) {
        filePreview.innerHTML = '';
        Array.from(files).forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const preview = document.createElement('div');
                preview.className = 'relative';
                preview.innerHTML = `
                    <img src="${e.target.result}" class="w-full h-24 object-cover rounded-lg" alt="Preview ${index + 1}">
                    <button type="button" onclick="removeFile(${index})" class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full text-xs">×</button>
                `;
                filePreview.appendChild(preview);
            };
            reader.readAsDataURL(file);
        });
    }
}

function removeFile(index) {
    quoteData.files.splice(index, 1);
    const fileInput = document.getElementById('fileInput');
    const dt = new DataTransfer();
    quoteData.files.forEach(file => dt.items.add(file));
    fileInput.files = dt.files;
    
    // Re-display preview
    const filePreview = document.getElementById('filePreview');
    filePreview.innerHTML = '';
    quoteData.files.forEach((file, i) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.createElement('div');
            preview.className = 'relative';
            preview.innerHTML = `
                <img src="${e.target.result}" class="w-full h-24 object-cover rounded-lg" alt="Preview ${i + 1}">
                <button type="button" onclick="removeFile(${i})" class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full text-xs">×</button>
            `;
            filePreview.appendChild(preview);
        };
        reader.readAsDataURL(file);
    });
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
            html += `
                <div class="summary-item flex items-center space-x-2 bg-stone px-3 py-2 rounded-lg">
                    <i class="fas fa-check-circle text-accent"></i>
                    <span class="text-sm font-semibold">${featureName}</span>
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
    if (aiDesignCheckbox) {
        quoteData.aiDesign = aiDesignCheckbox.checked;
    }
    
    // Hide form, show loading
    document.getElementById('step5').classList.add('hidden');
    document.getElementById('loadingState').classList.remove('hidden');
    
    // Simulate API call (replace with actual webhook)
    console.log('Quote Data:', quoteData);
    
    // Demo: Show quote after 2 seconds
    setTimeout(() => {
        showQuoteResult();
    }, 2000);
    
    // Real implementation:
    // const webhookUrl = window.CONFIG?.quoteWebhookUrl || 'https://your-make-webhook-url.com';
    // const formData = new FormData();
    // formData.append('features', JSON.stringify(quoteData.features));
    // formData.append('description', quoteData.description);
    // formData.append('area', quoteData.area);
    // formData.append('budget', quoteData.budget);
    // formData.append('postcode', quoteData.postcode);
    // formData.append('email', quoteData.email);
    // formData.append('phone', quoteData.phone);
    // formData.append('aiDesign', quoteData.aiDesign);
    // quoteData.files.forEach((file, index) => {
    //     formData.append(`file${index}`, file);
    // });
    
    // try {
    //     const response = await fetch(webhookUrl, {
    //         method: 'POST',
    //         body: formData
    //     });
    //     const result = await response.json();
    //     showQuoteResult(result);
    // } catch (error) {
    //     console.error('Error submitting quote:', error);
    //     alert('There was an error processing your quote. Please try again.');
    //     document.getElementById('loadingState').classList.add('hidden');
    //     document.getElementById('step5').classList.remove('hidden');
    // }
}

function showQuoteResult(data) {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('quoteResult').classList.remove('hidden');
    
    // Demo breakdown
    const breakdown = document.getElementById('quoteBreakdown');
    breakdown.innerHTML = `
        <div class="flex justify-between items-center py-2 border-b">
            <span class="text-gray-700">Patio (Porcelain 40m²)</span>
            <span class="font-semibold">£3,200 - £4,800</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b">
            <span class="text-gray-700">Artificial Turf (25m²)</span>
            <span class="font-semibold">£1,200 - £2,400</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b">
            <span class="text-gray-700">Labour & Installation</span>
            <span class="font-semibold">£3,100 - £4,300</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b">
            <span class="text-gray-700">Materials Delivery</span>
            <span class="font-semibold">£500 - £700</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b">
            <span class="text-gray-700">Waste Removal</span>
            <span class="font-semibold">£300 - £500</span>
        </div>
        <div class="flex justify-between items-center py-3 font-bold text-lg">
            <span class="text-primary">Total (inc. VAT)</span>
            <span class="text-primary">£8,500 - £12,500</span>
        </div>
    `;
    
    // Scroll to result
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function emailQuote() {
    alert(`Quote will be emailed to: ${quoteData.email}\n\nIn production, this will trigger an automated email with PDF attachment.`);
    console.log('Email quote to:', quoteData.email);
    
    // Real implementation would call Make.com webhook to send email
}
