"""Tiny benign HTTP server for local testing only."""
from http.server import HTTPServer, SimpleHTTPRequestHandler

ADDR = ("127.0.0.1", 8000)

if __name__ == "__main__":
    print(f"Starting benign HTTP server on http://{ADDR[0]}:{ADDR[1]}")
    httpd = HTTPServer(ADDR, SimpleHTTPRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        httpd.server_close()
