from django.test import TestCase


class PingTests(TestCase):
    def test_ping(self):
        response = self.client.get("/ex03/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "pong"})


class GreetTests(TestCase):
    def test_greet_with_name(self):
        response = self.client.get("/ex03/greet", {"name": "Neil"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"greeting": "Hello, Neil!"})

    def test_greet_missing_name(self):
        response = self.client.get("/ex03/greet")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "name is required"})

    def test_greet_empty_name(self):
        response = self.client.get("/ex03/greet", {"name": ""})
        self.assertEqual(response.status_code, 400)


class AddTests(TestCase):
    def test_add(self):
        response = self.client.get("/ex03/add/2/40")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": 42})

    def test_add_zero(self):
        response = self.client.get("/ex03/add/0/0")
        self.assertEqual(response.json(), {"result": 0})

    def test_add_not_a_number(self):
        response = self.client.get("/ex03/add/2/x")
        self.assertEqual(response.status_code, 404)


class EchoTests(TestCase):
    def test_echo_post(self):
        payload = {"a": 1, "nested": {"b": [1, 2, 3]}}
        response = self.client.post("/ex03/echo", payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"received": payload})

    def test_echo_wrong_method(self):
        self.assertEqual(self.client.get("/ex03/echo").status_code, 405)
        self.assertEqual(self.client.delete("/ex03/echo").status_code, 405)


class StatsTests(TestCase):
    def test_stats(self):
        response = self.client.get("/ex03/stats", {"nums": "3,1,2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"count": 3, "min": 1, "max": 3, "sum": 6})

    def test_stats_negative_and_single(self):
        self.assertEqual(self.client.get("/ex03/stats", {"nums": "-5,10"}).json(),
                         {"count": 2, "min": -5, "max": 10, "sum": 5})
        self.assertEqual(self.client.get("/ex03/stats", {"nums": "7"}).json(),
                         {"count": 1, "min": 7, "max": 7, "sum": 7})

    def test_stats_missing(self):
        response = self.client.get("/ex03/stats")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "nums is required"})
