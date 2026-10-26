import json

from django.test import TestCase

from .models import Note

URL = "/ex05/notes"


class NotesTestCase(TestCase):
    def post(self, data):
        return self.client.post(URL, data, content_type="application/json")

    def patch(self, noteId, data):
        return self.client.patch(f"{URL}/{noteId}", json.dumps(data), content_type="application/json")


class CreateTests(NotesTestCase):
    def test_create_returns_201_and_note(self):
        response = self.post({"title": "Shopping", "body": "eggs"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "title": "Shopping", "body": "eggs", "pinned": False})
        self.assertEqual(Note.objects.count(), 1)

    def test_ids_increase(self):
        self.post({"title": "a", "body": "1"})
        second = self.post({"title": "b", "body": "2", "pinned": True})
        self.assertEqual(second.json(), {"id": 2, "title": "b", "body": "2", "pinned": True})


class ListTests(NotesTestCase):
    def test_empty_list(self):
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_list_ordered_by_id(self):
        for i in range(3):
            self.post({"title": f"t{i}", "body": "x"})
        self.assertEqual([n["id"] for n in self.client.get(URL).json()], [1, 2, 3])

    def test_filter_pinned(self):
        self.post({"title": "a", "body": "x", "pinned": True})
        self.post({"title": "b", "body": "x"})
        self.post({"title": "c", "body": "x", "pinned": True})
        self.assertEqual([n["id"] for n in self.client.get(URL, {"pinned": "true"}).json()], [1, 3])
        self.assertEqual([n["id"] for n in self.client.get(URL, {"pinned": "false"}).json()], [2])

    def test_collection_wrong_method(self):
        self.assertEqual(self.client.put(URL).status_code, 405)
        self.assertEqual(self.client.delete(URL).status_code, 405)


class DetailTests(NotesTestCase):
    def test_get_one(self):
        self.post({"title": "a", "body": "x"})
        response = self.client.get(f"{URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "a")

    def test_get_missing(self):
        self.assertEqual(self.client.get(f"{URL}/42").status_code, 404)

    def test_detail_wrong_method(self):
        self.post({"title": "a", "body": "x"})
        self.assertEqual(self.client.post(f"{URL}/1", {}, content_type="application/json").status_code, 405)


class PatchTests(NotesTestCase):
    def test_patch_changes_only_given_fields(self):
        self.post({"title": "old", "body": "keep me"})
        response = self.patch(1, {"title": "new"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "title": "new", "body": "keep me", "pinned": False})
        self.assertEqual(self.client.get(f"{URL}/1").json()["title"], "new")

    def test_patch_pinned(self):
        self.post({"title": "a", "body": "x"})
        self.assertTrue(self.patch(1, {"pinned": True}).json()["pinned"])

    def test_patch_missing(self):
        self.assertEqual(self.patch(7, {"title": "x"}).status_code, 404)


class DeleteTests(NotesTestCase):
    def test_delete(self):
        self.post({"title": "a", "body": "x"})
        response = self.client.delete(f"{URL}/1")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(self.client.get(f"{URL}/1").status_code, 404)

    def test_delete_missing(self):
        self.assertEqual(self.client.delete(f"{URL}/1").status_code, 404)
