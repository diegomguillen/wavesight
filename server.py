import http.server
import urllib.request
import urllib.parse
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

class WaveSightHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith('/api/scope_fetch'):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(body)
            ip = params.get('ip', [''])[0]
            source = params.get('source', ['0'])[0]
            points = params.get('points', ['0'])[0]
            
            if not ip:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing IP")
                return

            scope_url = f"http://{ip}/chaninfo.htm"
            post_data = urllib.parse.urlencode({
                'lang': 'en',
                'source': source,
                'format': '1',
                'points': points,
                'button': 'Save'
            }).encode('utf-8')

            try:
                req = urllib.request.Request(scope_url, data=post_data, method='POST')
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/csv')
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                self.send_response(502)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Oscilloscope connection error: {e}".encode('utf-8'))
        else:
            super().do_POST()

if __name__ == '__main__':
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, WaveSightHandler)
    print(f"WaveSight Server running on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
