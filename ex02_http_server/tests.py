import http.client
import json
import threading
import unittest
import urllib.error
import urllib.request

from .server import makeServer


class ServerTestCase(unittest.TestCase):
    """Starts your server on a free port before each test and stops it afterwards."""

    def setUp(self):
        self.server = makeServer(0)  # port 0 = let the OS pick a free port
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        self.thread.start()
        self.baseUrl = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def request(self, method, path, body=None, rawBody=None):
        """Send a request. Returns (statusCode, parsedJsonOrNone, rawBytes)."""
        data, headers = None, {}
        if body is not None:
            data = json.dumps(body).encode()
        if rawBody is not None:
            data = rawBody.encode()
        if data is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(self.baseUrl + path, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                status, raw = resp.status, resp.read()
        except urllib.error.HTTPError as error:
            status, raw = error.code, error.read()
        except (http.client.RemoteDisconnected, ConnectionError, urllib.error.URLError) as error:
            self.fail(f"the server crashed while handling {method} {path} "
                      f"(look for a traceback above): {error}")
        try:
            parsed = json.loads(raw) if raw else None
        except ValueError:
            parsed = None
        return status, parsed, raw

    def create(self, title, done=None):
        body = {"title": title} if done is None else {"title": title, "done": done}
        return self.request("POST", "/todos", body)


class CreateTests(ServerTestCase):
    def test_create(self):
        status, data, _ = self.create("Buy milk")
        self.assertEqual(status, 201)
        self.assertEqual(data, {"id": 1, "title": "Buy milk", "done": False})

    def test_create_done_and_ids_increase(self):
        self.create("a")
        status, data, _ = self.create("b", True)
        self.assertEqual((status, data), (201, {"id": 2, "title": "b", "done": True}))

    def test_create_invalid_body(self):
        for body in ({}, {"title": ""}, {"title": 5}, {"title": "x", "done": "yes"}, {"title": "x", "colour": "red"}):
            status, data, _ = self.request("POST", "/todos", body)
            self.assertEqual(status, 400, f"body {body} should be rejected")
            self.assertIn("error", data)
        self.assertEqual(self.request("GET", "/todos")[1], [])

    def test_create_bad_json(self):
        self.assertEqual(self.request("POST", "/todos", rawBody="{oops")[0], 400)
        self.assertEqual(self.request("POST", "/todos", rawBody="[1, 2]")[0], 400)


class ListTests(ServerTestCase):
    def test_empty(self):
        status, data, _ = self.request("GET", "/todos")
        self.assertEqual((status, data), (200, []))

    def test_list_in_id_order(self):
        for title in ("a", "b", "c"):
            self.create(title)
        self.assertEqual([t["id"] for t in self.request("GET", "/todos")[1]], [1, 2, 3])

    def test_filter_done(self):
        self.create("a", True)
        self.create("b")
        self.create("c", True)
        self.assertEqual([t["id"] for t in self.request("GET", "/todos?done=true")[1]], [1, 3])
        self.assertEqual([t["id"] for t in self.request("GET", "/todos?done=false")[1]], [2])


class GetOneTests(ServerTestCase):
    def test_get_one(self):
        self.create("a")
        self.create("b")
        status, data, _ = self.request("GET", "/todos/2")
        self.assertEqual((status, data), (200, {"id": 2, "title": "b", "done": False}))

    def test_missing_and_bad_ids(self):
        self.create("a")
        self.assertEqual(self.request("GET", "/todos/9")[0], 404)
        self.assertEqual(self.request("GET", "/todos/abc")[0], 404)


class PatchTests(ServerTestCase):
    def test_patch_one_field(self):
        self.create("old")
        status, data, _ = self.request("PATCH", "/todos/1", {"done": True})
        self.assertEqual((status, data), (200, {"id": 1, "title": "old", "done": True}))
        self.assertEqual(self.request("GET", "/todos/1")[1]["done"], True)

    def test_patch_missing(self):
        self.assertEqual(self.request("PATCH", "/todos/1", {"done": True})[0], 404)

    def test_patch_invalid_changes_nothing(self):
        self.create("keep")
        for body in ({"title": ""}, {"done": "yes"}, {"title": "new", "colour": "red"}):
            self.assertEqual(self.request("PATCH", "/todos/1", body)[0], 400, f"body {body} should be rejected")
        self.assertEqual(self.request("PATCH", "/todos/1", rawBody="{oops")[0], 400)
        self.assertEqual(self.request("GET", "/todos/1")[1], {"id": 1, "title": "keep", "done": False})


class DeleteTests(ServerTestCase):
    def test_delete(self):
        self.create("a")
        status, _, raw = self.request("DELETE", "/todos/1")
        self.assertEqual((status, raw), (204, b""))
        self.assertEqual(self.request("GET", "/todos/1")[0], 404)
        self.assertEqual(self.request("GET", "/todos")[1], [])

    def test_delete_missing(self):
        self.assertEqual(self.request("DELETE", "/todos/3")[0], 404)


class OtherTests(ServerTestCase):
    def test_unknown_path(self):
        self.assertEqual(self.request("GET", "/nope")[0], 404)
        self.assertEqual(self.request("POST", "/nope", {"title": "x"})[0], 404)

    def test_put_is_405(self):
        self.create("a")
        self.assertEqual(self.request("PUT", "/todos/1", {"title": "b"})[0], 405)
        self.assertEqual(self.request("PUT", "/todos", {"title": "b"})[0], 405)
