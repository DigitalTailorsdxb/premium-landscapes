#!/usr/bin/env python3
"""
Premium Landscapes - Development Server
Simple static file server
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler

if __name__ == '__main__':
    PORT = 5000
    server = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    print(f'🚀 Premium Landscapes running on port {PORT}')
    server.serve_forever()
