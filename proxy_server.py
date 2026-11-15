import http.server
import urllib.request
import urllib.parse

PORT = 8080

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/proxy/'):
            target_url = 'https://' + self.path[7:]
            try:
                req = urllib.request.Request(
                    target_url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                        'Origin': 'https://www.iwanttfc.com',
                        'Referer': 'https://www.iwanttfc.com/'
                    }
                )
                with urllib.request.urlopen(req) as response:
                    self.send_response(response.status)
                    for header, value in response.headers.items():
                        if header.lower() not in ['transfer-encoding', 'content-encoding']:
                            self.send_header(header, value)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.copyfile(response, self.wfile)
            except Exception as e:
                self.send_error(500, str(e))
        else:
            super().do_GET()

if __name__ == '__main__':
    print(f"PBB Python Proxy Server running at http://localhost:{PORT}")
    http.server.HTTPServer(('localhost', PORT), ProxyHandler).serve_forever()
