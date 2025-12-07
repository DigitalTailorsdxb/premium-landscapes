// AI Design Generator Engine
// Handles multi-step form, feature selection, and design generation

let currentStep = 1;
const totalSteps = 4;

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
    updateProgress();
});

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
    
    // Budget
    if (designData.budget) {
        let budgetText = '';
        switch(designData.budget) {
            case '<5000': budgetText = 'Under £5k'; break;
            case '5000-10000': budgetText = '£5k - £10k'; break;
            case '10000-20000': budgetText = '£10k - £20k'; break;
            case '20000-30000': budgetText = '£20k - £30k'; break;
            case '>30000': budgetText = '£30k+'; break;
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
    
    // Hide form, show loading
    document.getElementById('step4').classList.add('hidden');
    document.getElementById('loadingState').classList.remove('hidden');
    
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
    
    const webhookUrl = brandConfig?.webhooks?.design || 'https://your-n8n-webhook-url.com';
    
    console.log('🔗 Webhook URL:', webhookUrl);
    
    if (!webhookUrl || webhookUrl.includes('your-n8n-webhook-url')) {
        console.warn('⚠️ Webhook URL not configured. Using demo mode.');
        setTimeout(() => {
            showSuccess();
        }, 2000);
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
        
        const result = await response.json();
        console.log('📬 Workflow response:', result);
        
        showSuccess();
        
    } catch (error) {
        console.error('❌ Error submitting design request:', error);
        alert('There was an error processing your request. Please try again or contact us at 07444887813');
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('step4').classList.remove('hidden');
    }
}

function showSuccess() {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('successResult').classList.remove('hidden');
    document.getElementById('confirmEmail').textContent = designData.email;
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
