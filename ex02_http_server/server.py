import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit


class TodoHandler(BaseHTTPRequestHandler):
    # ----- helpers you can use ---------------------------------------------

    def sendJson(self, status, data):
        """Send `data` as a JSON response with the given status code."""
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def sendEmpty(self, status):
        """Send a response with no body (e.g. 204)."""
        self.send_response(status)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def readBody(self):
        """Return the request body as text ("" if there is none)."""
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode()

    def log_message(self, format, *args):
        pass  # keeps test output quiet; delete this method to see every request logged

    # ----- your code goes below ----------------------------------------------
    # The data lives on the server object, so each test starts empty:
    #     self.server.todos   a list of todo dicts
    #     self.server.nextId  the next id to hand out
    # self.path is the full path including any query string, e.g. "/todos?done=true".
    # urlsplit(self.path).path gives "/todos"; parse_qs(urlsplit(self.path).query)
    # gives {"done": ["true"]}.

    def do_GET(self):
        self.sendJson(404, {"error": "not implemented yet"})


def makeServer(port=8000):
    server = ThreadingHTTPServer(("127.0.0.1", port), TodoHandler)
    server.todos = []
    server.nextId = 1
    return server


if __name__ == "__main__":
    server = makeServer()
    print("Listening on http://127.0.0.1:8000  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
