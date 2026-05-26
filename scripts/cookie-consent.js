(function () {
    'use strict';
    var STORAGE_KEY = 'pl_cookie_consent';

    function setConsent(val) { try { localStorage.setItem(STORAGE_KEY, val); } catch (e) {} }
    function getConsent()    { try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; } }

    function updateGA(granted) {
        if (typeof window.gtag === 'function') {
            window.gtag('consent', 'update', {
                analytics_storage: granted ? 'granted' : 'denied',
                ad_storage:        granted ? 'granted' : 'denied'
            });
        }
    }

    var existing = getConsent();
    if (existing === 'accepted') { updateGA(true);  return; }
    if (existing === 'rejected') { updateGA(false); return; }

    var banner = document.createElement('div');
    banner.id = 'pl-cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.style.cssText = [
        'position:fixed', 'bottom:0', 'left:0', 'right:0', 'z-index:99999',
        'background:#fff', 'border-top:3px solid #2563eb',
        'padding:14px 20px', 'box-shadow:0 -4px 24px rgba(0,0,0,0.12)',
        'font-family:Inter,Open Sans,sans-serif'
    ].join(';');

    banner.innerHTML = [
        '<div style="max-width:960px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;',
            'gap:14px;justify-content:space-between;">',
            '<div style="flex:1;min-width:200px;">',
                '<p style="margin:0;font-size:13px;line-height:1.65;color:#374151;">',
                    '<strong style="color:#1e3a8a;">We use cookies</strong> to improve your experience, ',
                    'measure site performance and support our advertising. ',
                    'View our <a href="/privacy-policy" ',
                    'style="color:#2563eb;text-decoration:underline;">Privacy Policy</a> for details.',
                '</p>',
            '</div>',
            '<div style="display:flex;gap:10px;flex-shrink:0;flex-wrap:wrap;">',
                '<button id="pl-cookie-reject" ',
                    'style="padding:9px 18px;border-radius:50px;border:1px solid #d1d5db;',
                    'background:#fff;color:#374151;font-size:13px;font-weight:600;cursor:pointer;',
                    'white-space:nowrap;">',
                    'Reject Non-Essential',
                '</button>',
                '<button id="pl-cookie-accept" ',
                    'style="padding:9px 22px;border-radius:50px;border:none;background:#2563eb;',
                    'color:#fff;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap;">',
                    'Accept All',
                '</button>',
            '</div>',
        '</div>'
    ].join('');

    function dismiss(consent) {
        setConsent(consent);
        updateGA(consent === 'accepted');
        banner.style.transform   = 'translateY(100%)';
        banner.style.transition  = 'transform 0.3s ease';
        setTimeout(function () {
            if (banner.parentNode) banner.parentNode.removeChild(banner);
        }, 350);
    }

    function init() {
        document.body.appendChild(banner);
        document.getElementById('pl-cookie-accept').addEventListener('click', function () { dismiss('accepted'); });
        document.getElementById('pl-cookie-reject').addEventListener('click', function () { dismiss('rejected'); });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
