document.addEventListener('DOMContentLoaded', function() {
    
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuLinks = document.querySelectorAll('.mobile-menu-link');
    
    mobileMenuBtn.addEventListener('click', function() {
        mobileMenu.classList.add('active');
    });
    
    closeMobileMenu.addEventListener('click', function() {
        mobileMenu.classList.remove('active');
    });
    
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileMenu.classList.remove('active');
        });
    });
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    const carousel = document.getElementById('carousel');
    const carouselPrev = document.getElementById('carouselPrev');
    const carouselNext = document.getElementById('carouselNext');
    
    carouselNext.addEventListener('click', function() {
        carousel.scrollBy({
            left: carousel.offsetWidth / 2 + 24,
            behavior: 'smooth'
        });
    });
    
    carouselPrev.addEventListener('click', function() {
        carousel.scrollBy({
            left: -(carousel.offsetWidth / 2 + 24),
            behavior: 'smooth'
        });
    });
    
    const quoteForm = document.getElementById('quoteForm');
    quoteForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(quoteForm);
        
        const quoteData = {
            projectDescription: formData.get('projectDescription'),
            postcode: formData.get('postcode'),
            email: formData.get('email'),
            timestamp: new Date().toISOString()
        };
        
        console.log('Quote Request:', quoteData);
        console.log('Project Description:', quoteData.projectDescription);
        
        try {
            const response = await fetch(brandConfig.webhooks.quote, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(quoteData)
            });
            
            if (response.ok) {
                const result = await response.json();
                displayQuoteResult(result);
            } else {
                displayQuoteResult({
                    estimate: '£3,800 - £6,200',
                    breakdown: [
                        { feature: 'Project Analysis', price: 'Processing...' }
                    ],
                    message: 'Demo mode: Your quote will be calculated by AI based on materials and labour costs. Connect GPT workflow for live pricing.'
                });
            }
        } catch (error) {
            console.log('Using demo mode - webhook not connected yet');
            displayQuoteResult({
                estimate: '£3,800 - £6,200',
                breakdown: [
                    { feature: 'Project Analysis', price: 'Processing...' }
                ],
                message: 'Demo mode: Your quote will be calculated by AI based on materials and labour costs. Connect GPT workflow for live pricing.'
            });
        }
    });
    
    function displayQuoteResult(result) {
        const quoteResult = document.getElementById('quoteResult');
        const quoteDetails = document.getElementById('quoteDetails');
        
        let html = `
            <div class="text-center mb-6">
                <p class="text-3xl font-bold text-primary">${result.estimate}</p>
                ${result.message ? `<p class="text-sm text-gray-500 mt-2">${result.message}</p>` : ''}
            </div>
        `;
        
        if (result.breakdown && result.breakdown.length > 0) {
            html += '<div class="space-y-2 mb-6">';
            result.breakdown.forEach(item => {
                html += `
                    <div class="flex justify-between items-center py-2 border-b border-gray-200">
                        <span class="font-semibold">${item.feature}</span>
                        <span class="text-gray-600">${item.price}</span>
                    </div>
                `;
            });
            html += '</div>';
        }
        
        html += `
            <div class="flex gap-4 mt-6">
                <button onclick="window.location.href='#design'" class="flex-1 bg-primary text-white px-6 py-3 rounded-full hover:bg-primary-dark transition">
                    Generate AI Design
                </button>
                <button onclick="alert('PDF download will be available once Make.com is connected')" class="flex-1 bg-white border-2 border-primary text-primary px-6 py-3 rounded-full hover:bg-stone transition">
                    Download PDF
                </button>
            </div>
        `;
        
        quoteDetails.innerHTML = html;
        quoteResult.classList.remove('hidden');
        
        quoteResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    const designForm = document.getElementById('designForm');
    designForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(designForm);
        const designData = {
            style: formData.get('designStyle'),
            email: formData.get('designEmail'),
            timestamp: new Date().toISOString()
        };
        
        console.log('Design Request:', designData);
        
        try {
            const response = await fetch(brandConfig.webhooks.design, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(designData)
            });
            
            if (response.ok) {
                const result = await response.json();
                displayDesignResult(result);
            } else {
                displayDesignResult({
                    message: 'Your AI design is being generated and will be emailed to you shortly.',
                    demo: true
                });
            }
        } catch (error) {
            console.log('Using demo mode - webhook not connected yet');
            displayDesignResult({
                message: 'Your AI design is being generated and will be emailed to you shortly.',
                demo: true
            });
        }
    });
    
    function displayDesignResult(result) {
        const designResult = document.getElementById('designResult');
        const designDetails = document.getElementById('designDetails');
        
        let html = `
            <div class="text-center">
                <i class="fas fa-check-circle text-primary text-5xl mb-4"></i>
                <p class="text-lg mb-4">${result.message}</p>
                ${result.demo ? '<p class="text-sm text-gray-500">Demo mode: Connect Make.com + DALL·E for live AI generation.</p>' : ''}
            </div>
        `;
        
        if (result.imageUrl) {
            html = `
                <div class="text-center mb-4">
                    <img src="${result.imageUrl}" alt="AI Generated Design" class="w-full rounded-xl mb-4">
                    <a href="${result.imageUrl}" download class="inline-block bg-primary text-white px-6 py-3 rounded-full hover:bg-primary-dark transition">
                        Download Design
                    </a>
                </div>
            `;
        }
        
        designDetails.innerHTML = html;
        designResult.classList.remove('hidden');
        
        designResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    const contactForm = document.getElementById('contactForm');
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(contactForm);
        const contactData = {
            name: formData.get('contactName'),
            email: formData.get('contactEmailForm'),
            message: formData.get('contactMessage'),
            timestamp: new Date().toISOString()
        };
        
        console.log('Contact Form:', contactData);
        
        const resultDiv = document.getElementById('contactFormResult');
        
        try {
            const response = await fetch(brandConfig.webhooks.contact, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(contactData)
            });
            
            if (response.ok) {
                resultDiv.className = 'mt-4 p-4 rounded-lg bg-green-100 text-green-800';
                resultDiv.textContent = 'Thank you! Your message has been sent successfully.';
                resultDiv.classList.remove('hidden');
                contactForm.reset();
            } else {
                resultDiv.className = 'mt-4 p-4 rounded-lg bg-blue-100 text-blue-800';
                resultDiv.textContent = 'Demo mode: Message logged to console. Connect Make.com webhook for live submissions.';
                resultDiv.classList.remove('hidden');
            }
        } catch (error) {
            console.log('Using demo mode - webhook not connected yet');
            resultDiv.className = 'mt-4 p-4 rounded-lg bg-blue-100 text-blue-800';
            resultDiv.textContent = 'Demo mode: Message logged to console. Connect Make.com webhook for live submissions.';
            resultDiv.classList.remove('hidden');
        }
        
        setTimeout(() => {
            resultDiv.classList.add('hidden');
        }, 5000);
    });
});
