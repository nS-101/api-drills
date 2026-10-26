import json

from django.test import TestCase

URL = "/ex06/products"

LAMP = {"name": "Desk Lamp", "category": "home", "price": 24.5, "stock": 12, "listed_on": "2026-03-01"}


class ProductTestCase(TestCase):
    def post(self, data):
        return self.client.post(URL, data, content_type="application/json")


class VisibleTests(ProductTestCase):
    def test_create(self):
        response = self.post(LAMP)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, **LAMP})

    def test_list(self):
        self.post(LAMP)
        self.post({**LAMP, "name": "Chair"})
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([p["name"] for p in response.json()], ["Desk Lamp", "Chair"])

    def test_get_one_and_missing(self):
        self.post(LAMP)
        self.assertEqual(self.client.get(f"{URL}/1").json(), {"id": 1, **LAMP})
        self.assertEqual(self.client.get(f"{URL}/2").status_code, 404)

    def test_patch(self):
        self.post(LAMP)
        response = self.client.patch(f"{URL}/1", json.dumps({"stock": 3}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, **LAMP, "stock": 3})

    def test_delete_not_allowed(self):
        self.post(LAMP)
        self.assertEqual(self.client.delete(f"{URL}/1").status_code, 405)
