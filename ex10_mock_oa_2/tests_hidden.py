# Simulated hidden tests. Don't read this file until you've finished ex10.
import json

from django.test import TestCase

from .models import Event

URL = "/ex10/events"


def event(name, venue="Kilburn", date="2026-11-12", capacity=10):
    return {"name": name, "venue": venue, "date": date, "capacity": capacity}


class HiddenTests(TestCase):
    def postJson(self, url, data):
        return self.client.post(url, data, content_type="application/json")

    def test_create_rejects_id_booked_and_bad_capacity(self):
        self.assertEqual(self.postJson(URL, {"id": 4, **event("a")}).status_code, 400)
        self.assertEqual(self.postJson(URL, {**event("a"), "booked": 2}).status_code, 400)
        self.assertEqual(self.postJson(URL, event("a", capacity=0)).status_code, 400)
        self.assertEqual(Event.objects.count(), 0)
        self.assertEqual(self.postJson(URL, event("a", capacity=1)).status_code, 201)

    def test_order_by_date_then_id(self):
        self.postJson(URL, event("late", date="2026-12-01"))
        self.postJson(URL, event("early", date="2026-11-01"))
        self.postJson(URL, event("late2", date="2026-12-01"))
        self.assertEqual([e["name"] for e in self.client.get(URL).json()], ["early", "late", "late2"])

    def test_venue_filter_ignores_case(self):
        self.postJson(URL, event("a", venue="Kilburn"))
        self.postJson(URL, event("b", venue="Alan Turing"))
        self.assertEqual([e["name"] for e in self.client.get(URL, {"venue": "KILBURN"}).json()], ["a"])
        self.assertEqual(self.client.get(URL, {"venue": "Nowhere"}).json(), [])

    def test_from_filter_is_inclusive(self):
        self.postJson(URL, event("a", date="2026-11-01"))
        self.postJson(URL, event("b", date="2026-11-02"))
        self.postJson(URL, event("c", date="2026-11-03"))
        self.assertEqual([e["name"] for e in self.client.get(URL, {"from": "2026-11-02"}).json()], ["b", "c"])

    def test_available_filter(self):
        self.postJson(URL, event("full", capacity=2))
        self.postJson(URL, event("open", capacity=2))
        self.postJson(f"{URL}/1/book", {"seats": 2})
        self.assertEqual([e["name"] for e in self.client.get(URL, {"available": "true"}).json()], ["open"])

    def test_filters_combined(self):
        self.postJson(URL, event("a", venue="Kilburn", date="2026-11-01"))
        self.postJson(URL, event("b", venue="kilburn", date="2026-11-05"))
        self.postJson(URL, event("c", venue="Other", date="2026-11-06"))
        names = [e["name"] for e in self.client.get(URL, {"venue": "Kilburn", "from": "2026-11-02"}).json()]
        self.assertEqual(names, ["b"])

    def test_book_exactly_to_capacity_then_conflict(self):
        self.postJson(URL, event("a", capacity=5))
        self.assertEqual(self.postJson(f"{URL}/1/book", {"seats": 5}).status_code, 200)
        self.assertEqual(self.postJson(f"{URL}/1/book", {"seats": 1}).status_code, 409)
        self.assertEqual(self.client.get(f"{URL}/1").json()["booked"], 5)

    def test_book_too_many_changes_nothing(self):
        self.postJson(URL, event("a", capacity=5))
        self.postJson(f"{URL}/1/book", {"seats": 2})
        self.assertEqual(self.postJson(f"{URL}/1/book", {"seats": 4}).status_code, 409)
        self.assertEqual(self.client.get(f"{URL}/1").json()["booked"], 2)

    def test_book_invalid_and_missing(self):
        self.postJson(URL, event("a"))
        self.assertEqual(self.postJson(f"{URL}/1/book", {"seats": 0}).status_code, 400)
        self.assertEqual(self.postJson(f"{URL}/9/book", {"seats": 1}).status_code, 404)

    def test_delete_with_bookings_conflicts(self):
        self.postJson(URL, event("a"))
        self.postJson(f"{URL}/1/book", {"seats": 1})
        self.assertEqual(self.client.delete(f"{URL}/1").status_code, 409)
        self.assertEqual(self.client.get(f"{URL}/1").status_code, 200)

    def test_delete_missing(self):
        self.assertEqual(self.client.delete(f"{URL}/1").status_code, 404)

    def test_wrong_methods(self):
        self.postJson(URL, event("a"))
        self.assertEqual(self.client.put(f"{URL}/1", json.dumps(event("b")), content_type="application/json").status_code, 405)
        self.assertEqual(self.client.delete(URL).status_code, 405)
        self.assertEqual(self.client.get(f"{URL}/1/book").status_code, 405)
