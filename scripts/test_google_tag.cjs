// Run: node scripts/test_google_tag.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const publicPages = [
    ...fs.readdirSync(root).filter(name => name.endsWith('.html')),
    ...fs.readdirSync(path.join(root, 'projects'))
        .filter(name => name.endsWith('.html'))
        .map(name => 'projects/' + name)
].filter(name => !['admin-edit-request.html', 'projects/_template.html'].includes(name));
const consentFields = [
    'analytics_storage', 'ad_storage', 'ad_user_data', 'ad_personalization'
];

for (const page of publicPages) {
    const html = fs.readFileSync(path.join(root, page), 'utf8');
    const head = html.match(/<head\b[^>]*>([\s\S]*?)<\/head>/i)?.[1];
    assert.ok(head, page + ': missing head');
    const loaders = [...head.matchAll(/<script\b[^>]*src=["'][^"']*googletagmanager\.com\/gtag\/js[^"']*["'][^>]*>/gi)];
    assert.equal(loaders.length, 1, page + ': needs exactly one Google tag loader');

    const tagScripts = [...head.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)]
        .map(match => match[1])
        .filter(code => /gtag\(['"]config['"]/.test(code));
    assert.equal(tagScripts.length, 1, page + ': expected one configuration script');
    const context = { window: {}, Date };
    context.window = context;
    vm.createContext(context);
    vm.runInContext(tagScripts[0], context);
    const commands = context.dataLayer.map(args => Array.from(args));
    const configs = commands.filter(command => command[0] === 'config');
    for (const id of ['G-9PGX32QB99', 'AW-18528338310']) {
        assert.equal(configs.filter(command => command[1] === id).length, 1,
            page + ': destination missing or duplicated: ' + id);
    }
    const consentIndex = commands.findIndex(command =>
        command[0] === 'consent' && command[1] === 'default');
    assert.ok(consentIndex >= 0, page + ': default consent missing');
    for (const field of consentFields) {
        assert.equal(commands[consentIndex][2][field], 'denied',
            page + ': consent must default to denied: ' + field);
    }
    assert.ok(consentIndex < commands.findIndex(command => command[0] === 'config'),
        page + ': consent must precede destination configuration');
    assert.ok(html.includes('scripts/cookie-consent.js'),
        page + ': cookie consent updater missing');
    assert.equal(commands.filter(command => command[0] === 'event'
        && command[1] === 'conversion').length, 0,
    page + ': base tag must not count page loads as leads');
}

const cookieScript = fs.readFileSync(path.join(root, 'scripts/cookie-consent.js'), 'utf8');
for (const choice of ['accepted', 'rejected']) {
    const commands = [];
    const context = {
        window: { gtag: (...args) => commands.push(args) },
        localStorage: { getItem: () => choice }
    };
    vm.createContext(context);
    vm.runInContext(cookieScript, context);
    assert.equal(commands.length, 1);
    assert.equal(commands[0][0], 'consent');
    assert.equal(commands[0][1], 'update');
    for (const field of consentFields) {
        assert.equal(commands[0][2][field], choice === 'accepted' ? 'granted' : 'denied');
    }
}
console.log(`PASS: ${publicPages.length} public pages each have one Google loader, GA4 + Ads destinations, default-denied consent, and no page-load conversion.`);
console.log('PASS: saved accepted/rejected choices update all four Consent Mode v2 fields.');
