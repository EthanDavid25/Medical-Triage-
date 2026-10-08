import http.server
import socketserver
import webbrowser
import os
import sys

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def start_server():
    ports = [3000, 3001, 3002, 5000, 8000, 8080]
    httpd = None
    active_port = None

    socketserver.TCPServer.allow_reuse_address = True

    for p in ports:
        try:
            httpd = socketserver.TCPServer(("", p), CustomHandler)
            active_port = p
            break
        except OSError:
            continue

    if not httpd:
        print("ERROR: Could not bind to any available port.")
        sys.exit(1)

    url = f"http://localhost:{active_port}/"
    print("\n=======================================================")
    print(f"  MediCare Medical Symptoms Triage Advisor is RUNNING! ")
    print(f"  Local URL: {url}")
    print("=======================================================\n")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping MediCare server...")
        httpd.server_close()

if __name__ == '__main__':
    start_server()
