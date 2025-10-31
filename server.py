#!/usr/bin/env python3
"""
Premium Landscapes - Development Server
Serves static files and injects environment variables into JavaScript config
"""
import os
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Inject API key into config endpoint
        if self.path == '/api/config.js' or self.path == '/scripts/config-env.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Inject Google Maps API key from environment
            api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
            config_js = f"""
// Environment variables injected by server
window.ENV_GOOGLE_MAPS_API_KEY = '{api_key}';
console.log('✅ Environment config loaded');
""".strip()
            
            self.wfile.write(config_js.encode('utf-8'))
            return
        
        # Serve all other files normally
        return super().do_GET()

if __name__ == '__main__':
    PORT = 5000
    server = HTTPServer(('0.0.0.0', PORT), CustomHandler)
    print(f'🚀 Premium Landscapes server running on http://0.0.0.0:{PORT}')
    print(f'📍 Google Maps API Key: {"✅ Configured" if os.getenv("GOOGLE_MAPS_API_KEY") else "❌ Missing"}')
    server.serve_forever()
