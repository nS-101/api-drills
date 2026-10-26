from django.test import TestCase

URL = "/ex10/events"

MEETUP = {"name": "Python Meetup", "venue": "Kilburn", "date": "2026-11-12", "capacity": 40}


class EventTestCase(TestCase):
    def postJson(self, url, data):
        return self.client.post(url, data, content_type="application/json")


class VisibleTests(EventTestCase):
    def test_create(self):
        response = self.postJson(URL, MEETUP)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, **MEETUP, "booked": 0})

    def test_list(self):
        self.postJson(URL, MEETUP)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 1, **MEETUP, "booked": 0}])

    def test_get_one_and_missing(self):
        self.postJson(URL, MEETUP)
        self.assertEqual(self.client.get(f"{URL}/1").json()["name"], "Python Meetup")
        self.assertEqual(self.client.get(f"{URL}/2").status_code, 404)

    def test_book(self):
        self.postJson(URL, MEETUP)
        response = self.postJson(f"{URL}/1/book", {"seats": 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["booked"], 3)

    def test_delete(self):
        self.postJson(URL, MEETUP)
        response = self.client.delete(f"{URL}/1")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.client.get(f"{URL}/1").status_code, 404)
