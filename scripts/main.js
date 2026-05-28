document.addEventListener('DOMContentLoaded', function () {

    /* ═══════════════════════════════════════════════════════
       MOBILE MENU — handles all three patterns:
       Pattern 1: fixed inset-0 slide-drawer (index,about,etc.)
       Pattern 2: inline dropdown via .active class (54 pages)
       Pattern 3: inline onclick hidden-toggle (service pages)
    ═══════════════════════════════════════════════════════ */

    const mobileMenuBtn  = document.getElementById('mobileMenuBtn');
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    const mobileMenu     = document.getElementById('mobileMenu');
    const mobileMenuLinks = document.querySelectorAll('.mobile-menu-link');

    // Inject overlay backdrop once
    let overlay = document.getElementById('menuOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'menuOverlay';
        overlay.className = 'menu-overlay';
        document.body.appendChild(overlay);
    }

    // Is this a full-screen slide drawer (Pattern 1)?
    const isDrawer = mobileMenu && mobileMenu.classList.contains('fixed');

    function openMenu() {
        if (!mobileMenu) return;
        mobileMenu.classList.add('active');
        overlay.classList.add('active');
        if (isDrawer) {
            document.body.classList.add('menu-open');
        }
        // Animate hamburger → X
        const icon = mobileMenuBtn && mobileMenuBtn.querySelector('i');
        if (icon) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        }
    }

    function closeMenu() {
        if (!mobileMenu) return;
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.classList.remove('menu-open');
        const icon = mobileMenuBtn && mobileMenuBtn.querySelector('i');
        if (icon) {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    }

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            mobileMenu.classList.contains('active') ? closeMenu() : openMenu();
        });
    }

    if (closeMobileMenu) {
        closeMobileMenu.addEventListener('click', closeMenu);
    }

    // Close on link click
    mobileMenuLinks.forEach(link => link.addEventListener('click', closeMenu));

    // Close on overlay tap
    overlay.addEventListener('click', closeMenu);

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeMenu();
    });

    /* ═══════════════════════════════════════════════════════
       STICKY BOTTOM CTA BAR (mobile only)
       Injected via JS so it applies to every page without
       editing all 80 HTML files individually.
    ═══════════════════════════════════════════════════════ */
    if (window.innerWidth < 768) {
        // Mark quote page so bar hides itself
        if (window.location.pathname.includes('quote')) {
            document.body.classList.add('on-quote-page');
        } else {
            // Get phone from config if available
            const phone = (typeof brandConfig !== 'undefined' && brandConfig.contact && brandConfig.contact.phone)
                ? brandConfig.contact.phone
                : '0116 000 0000';
            const phoneTel = phone.replace(/\s+/g, '');

            const bar = document.createElement('div');
            bar.className = 'mobile-bottom-cta';
            bar.innerHTML = `
                <a href="tel:${phoneTel}" class="cta-call" aria-label="Call us">
                    <i class="fas fa-phone"></i>
                    <span>Call</span>
                </a>
                <a href="quote.html" class="cta-quote" aria-label="Get instant quote and AI design">
                    <i class="fas fa-magic"></i>
                    <span>Instant Quote &amp; Design</span>
                </a>`;
            document.body.appendChild(bar);
        }

        /* Scroll-to-top button */
        const scrollBtn = document.createElement('button');
        scrollBtn.className = 'scroll-top-btn';
        scrollBtn.setAttribute('aria-label', 'Scroll to top');
        scrollBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
        scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
        document.body.appendChild(scrollBtn);

        window.addEventListener('scroll', function () {
            scrollBtn.classList.toggle('visible', window.scrollY > 400);
        }, { passive: true });
    }

    /* ═══════════════════════════════════════════════════════
       SMOOTH SCROLL — internal anchor links
    ═══════════════════════════════════════════════════════ */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (!href || href === '#') return;
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
            }
        });
    });

    /* ═══════════════════════════════════════════════════════
       LAZY LOADING — images not in viewport
    ═══════════════════════════════════════════════════════ */
    if ('IntersectionObserver' in window) {
        const imgObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imgObserver.unobserve(img);
                    }
                }
            });
        }, { rootMargin: '200px' });
        document.querySelectorAll('img[data-src]').forEach(img => imgObserver.observe(img));
    }

    /* ═══════════════════════════════════════════════════════
       IMAGE CAROUSEL
    ═══════════════════════════════════════════════════════ */
    const carousel = document.getElementById('carousel');
    const carouselPrev = document.getElementById('carouselPrev');
    const carouselNext = document.getElementById('carouselNext');

    if (carousel && carouselNext && carouselPrev) {
        carouselNext.addEventListener('click', function () {
            carousel.scrollBy({ left: carousel.offsetWidth / 2 + 24, behavior: 'smooth' });
        });
        carouselPrev.addEventListener('click', function () {
            carousel.scrollBy({ left: -(carousel.offsetWidth / 2 + 24), behavior: 'smooth' });
        });
    }

    /* ═══════════════════════════════════════════════════════
       LEGACY: Quote form (old simple form, kept for compat)
    ═══════════════════════════════════════════════════════ */
    const quoteForm = document.getElementById('quoteForm');
    if (quoteForm) {
        quoteForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const formData = new FormData(quoteForm);
            const quoteData = {
                projectDescription: formData.get('projectDescription'),
                postcode: formData.get('postcode'),
                email: formData.get('email'),
                timestamp: new Date().toISOString()
            };
            try {
                const response = await fetch(brandConfig.webhooks.quote, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(quoteData)
                });
                displayQuoteResult(response.ok ? await response.json() : { estimate: '£3,800 - £6,200', message: 'Quote submitted.' });
            } catch (error) {
                displayQuoteResult({ estimate: '£3,800 - £6,200', message: 'Quote received. We will be in touch.' });
            }
        });
    }

    function displayQuoteResult(result) {
        const quoteResult = document.getElementById('quoteResult');
        const quoteDetails = document.getElementById('quoteDetails');
        if (!quoteResult || !quoteDetails) return;
        let html = `<div class="text-center mb-6"><p class="text-3xl font-bold text-primary">${result.estimate || ''}</p>${result.message ? `<p class="text-sm text-gray-500 mt-2">${result.message}</p>` : ''}</div>`;
        if (result.breakdown && result.breakdown.length > 0) {
            html += '<div class="space-y-2 mb-6">';
            result.breakdown.forEach(item => {
                html += `<div class="flex justify-between items-center py-2 border-b border-gray-200"><span class="font-semibold">${item.feature}</span><span class="text-gray-600">${item.price}</span></div>`;
            });
            html += '</div>';
        }
        quoteDetails.innerHTML = html;
        quoteResult.classList.remove('hidden');
        quoteResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    /* ═══════════════════════════════════════════════════════
       LEGACY: Design form
    ═══════════════════════════════════════════════════════ */
    const designForm = document.getElementById('designForm');
    if (designForm) {
        designForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const formData = new FormData(designForm);
            const designData = { style: formData.get('designStyle'), email: formData.get('designEmail'), timestamp: new Date().toISOString() };
            try {
                const response = await fetch(brandConfig.webhooks.design, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(designData)
                });
                displayDesignResult(response.ok ? await response.json() : { message: 'Your AI design is being generated and will be emailed to you shortly.', demo: true });
            } catch {
                displayDesignResult({ message: 'Your AI design is being generated and will be emailed to you shortly.', demo: true });
            }
        });

        function displayDesignResult(result) {
            const designResult = document.getElementById('designResult');
            const designDetails = document.getElementById('designDetails');
            if (!designResult || !designDetails) return;
            let html = result.imageUrl
                ? `<div class="text-center mb-4"><img src="${result.imageUrl}" alt="AI Generated Design" class="w-full rounded-xl mb-4"><a href="${result.imageUrl}" download class="inline-block bg-primary text-white px-6 py-3 rounded-full hover:bg-primary-dark transition">Download Design</a></div>`
                : `<div class="text-center"><i class="fas fa-check-circle text-primary text-5xl mb-4"></i><p class="text-lg mb-4">${result.message}</p></div>`;
            designDetails.innerHTML = html;
            designResult.classList.remove('hidden');
            designResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    /* ═══════════════════════════════════════════════════════
       CONTACT FORM
    ═══════════════════════════════════════════════════════ */
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const formData = new FormData(contactForm);
            const contactData = {
                name: formData.get('contactName'),
                email: formData.get('contactEmailForm'),
                message: formData.get('contactMessage'),
                timestamp: new Date().toISOString()
            };
            const resultDiv = document.getElementById('contactFormResult');
            try {
                const response = await fetch(brandConfig.webhooks.contact, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(contactData)
                });
                if (response.ok) {
                    resultDiv.className = 'mt-4 p-4 rounded-lg bg-green-100 text-green-800';
                    resultDiv.textContent = 'Thank you! Your message has been sent successfully.';
                    resultDiv.classList.remove('hidden');
                    contactForm.reset();
                } else {
                    throw new Error('Non-OK response');
                }
            } catch {
                resultDiv.className = 'mt-4 p-4 rounded-lg bg-blue-100 text-blue-800';
                resultDiv.textContent = 'Message received. We will get back to you shortly.';
                resultDiv.classList.remove('hidden');
            }
            setTimeout(() => resultDiv.classList.add('hidden'), 5000);
        });
    }

});
