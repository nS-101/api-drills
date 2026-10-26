# Simulated hidden tests. Don't read this file until you've finished ex06.
import json

from django.test import TestCase

from .models import Product

URL = "/ex06/products"


def product(name, category="home", price=10.0, stock=1, listedOn="2026-01-01"):
    return {"name": name, "category": category, "price": price, "stock": stock, "listed_on": listedOn}


class HiddenTests(TestCase):
    def post(self, data):
        return self.client.post(URL, data, content_type="application/json")

    def patch(self, productId, data):
        return self.client.patch(f"{URL}/{productId}", json.dumps(data), content_type="application/json")

    def test_create_rejects_id(self):
        self.assertEqual(self.post({"id": 5, **product("x")}).status_code, 400)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_rejects_negative_price_and_stock(self):
        self.assertEqual(self.post(product("x", price=-0.01)).status_code, 400)
        self.assertEqual(self.post(product("x", stock=-1)).status_code, 400)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_allows_zero(self):
        self.assertEqual(self.post(product("free", price=0, stock=0)).status_code, 201)

    def test_empty_list(self):
        self.assertEqual(self.client.get(URL).json(), [])

    def test_filter_category(self):
        self.post(product("a", "home"))
        self.post(product("b", "garden"))
        self.post(product("c", "home"))
        self.assertEqual([p["id"] for p in self.client.get(URL, {"category": "home"}).json()], [1, 3])
        self.assertEqual(self.client.get(URL, {"category": "toys"}).json(), [])

    def test_sort_price_both_ways_with_ties(self):
        self.post(product("a", price=5))
        self.post(product("b", price=1))
        self.post(product("c", price=5))
        self.post(product("d", price=9))
        self.assertEqual([p["name"] for p in self.client.get(URL, {"sort": "price"}).json()], ["b", "a", "c", "d"])
        self.assertEqual([p["name"] for p in self.client.get(URL, {"sort": "-price"}).json()], ["d", "a", "c", "b"])

    def test_filter_and_sort_combined(self):
        self.post(product("a", "home", price=5))
        self.post(product("b", "garden", price=1))
        self.post(product("c", "home", price=2))
        names = [p["name"] for p in self.client.get(URL, {"category": "home", "sort": "price"}).json()]
        self.assertEqual(names, ["c", "a"])

    def test_patch_missing(self):
        self.assertEqual(self.patch(99, {"stock": 1}).status_code, 404)

    def test_patch_negative_changes_nothing(self):
        self.post(product("a", price=5, stock=5))
        self.assertEqual(self.patch(1, {"name": "renamed", "price": -1}).status_code, 400)
        self.assertEqual(self.patch(1, {"stock": -3}).status_code, 400)
        self.assertEqual(self.client.get(f"{URL}/1").json(), {"id": 1, **product("a", price=5, stock=5)})

    def test_patch_date_and_persisted(self):
        self.post(product("a"))
        self.assertEqual(self.patch(1, {"listed_on": "2026-12-25"}).json()["listed_on"], "2026-12-25")
        self.assertEqual(self.client.get(f"{URL}/1").json()["listed_on"], "2026-12-25")

    def test_put_not_allowed(self):
        self.post(product("a"))
        self.assertEqual(self.client.put(f"{URL}/1", json.dumps(product("b")), content_type="application/json").status_code, 405)

    def test_delete_missing_is_still_405(self):
        self.assertEqual(self.client.delete(f"{URL}/1").status_code, 405)
