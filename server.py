#!/usr/bin/env python3
"""
Premium Landscapes - Development Server
Static file server with custom 404, cache headers, WebP support,
and a /webhook-proxy endpoint that forwards to n8n server-to-server
(avoids browser CORS restrictions when testing from Replit preview).
"""
import os
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

ALLOWED_PROXY_TARGETS = {
    # Original quote webhooks
    'premium-landscapes-quote':         'https://n8n.trade-engine.co.uk/webhook/premium-landscapes-quote',
    'premium-landscapes-full-redesign': 'https://n8n.trade-engine.co.uk/webhook/premium-landscapes-full-redesign',
    # Active edit webhook
    'pl-editor':                        'https://n8n.trade-engine.co.uk/webhook/pl-editor',
    # Legacy edit webhooks (kept for backwards compatibility)
    'edit-request':                     'https://n8n.trade-engine.co.uk/webhook/edit-request',
    'quote-editor-test':                'https://n8n.trade-engine.co.uk/webhook/quote-editor-test',
    'image-editor-test':                'https://n8n.trade-engine.co.uk/webhook/image-editor-test',
    'combined-editor-test':             'https://n8n.trade-engine.co.uk/webhook/combined-editor-test',
}

class PremiumLandscapesHandler(SimpleHTTPRequestHandler):

    # ── Proxy POST handler ────────────────────────────────────────────────────
    def do_POST(self):
        if not self.path.startswith('/webhook-proxy/'):
            self.send_response(404)
            self.end_headers()
            return

        slug = self.path.replace('/webhook-proxy/', '').split('?')[0]
        target_url = ALLOWED_PROXY_TARGETS.get(slug)

        if not target_url:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': f'Unknown webhook slug: {slug}'}).encode())
            return

        # Read the incoming body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b''

        # Forward headers: Content-Type + any X-Webhook-Secret the browser sent
        forward_headers = {'Content-Type': 'application/json'}
        secret = self.headers.get('X-Webhook-Secret')
        if secret:
            forward_headers['X-Webhook-Secret'] = secret

        try:
            req = urllib.request.Request(target_url, data=body, headers=forward_headers, method='POST')
            with urllib.request.urlopen(req, timeout=180) as resp:
                status  = resp.status
                content = resp.read()

            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content if content else b'{}')
            print(f'✅ Proxy [{slug}] → {status}')

        except urllib.error.HTTPError as e:
            body_err = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body_err if body_err else b'{}')
            print(f'⚠️  Proxy [{slug}] → HTTP {e.code}')

        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
            print(f'❌ Proxy [{slug}] → {e}')

    # ── CORS preflight for proxy ──────────────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Webhook-Secret')
        self.end_headers()

    # ── Static file 404 ───────────────────────────────────────────────────────
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            try:
                with open('404.html', 'rb') as f:
                    content = f.read()
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                super().send_error(code, message, explain)
        else:
            super().send_error(code, message, explain)

    def end_headers(self):
        path = self.path.split('?')[0]
        if path.endswith(('.webp', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')):
            self.send_header('Cache-Control', 'public, max-age=86400')
        elif path.endswith(('.css', '.js')):
            self.send_header('Cache-Control', 'public, max-age=3600')
        else:
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        super().end_headers()

    def guess_type(self, path):
        if str(path).endswith('.webp'):
            return 'image/webp'
        return super().guess_type(path)

    def log_message(self, format, *args):
        if args and str(args[1]) in ('200', '304') and any(
            str(args[0]).endswith(ext) for ext in ('.webp', '.png', '.jpg', '.css', '.js', '.ico')
        ):
            return
        super().log_message(format, *args)

if __name__ == '__main__':
    PORT = 5000
    server = HTTPServer(('0.0.0.0', PORT), PremiumLandscapesHandler)
    print(f'🚀 Premium Landscapes running on port {PORT}')
    server.serve_forever()
