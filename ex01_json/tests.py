import json
import unittest

from . import solution


class ParseUrlTests(unittest.TestCase):
    def test_full_url(self):
        self.assertEqual(solution.parseUrl("http://127.0.0.1:8000/todos/3?done=true&sort=title"),
                         {"scheme": "http", "host": "127.0.0.1", "port": 8000,
                          "path": "/todos/3", "query": {"done": "true", "sort": "title"}})

    def test_no_port_no_query(self):
        self.assertEqual(solution.parseUrl("https://example.com/students"),
                         {"scheme": "https", "host": "example.com", "port": None,
                          "path": "/students", "query": {}})

    def test_no_path(self):
        result = solution.parseUrl("http://localhost:5000")
        self.assertEqual((result["port"], result["path"]), (5000, ""))


class StatusFamilyTests(unittest.TestCase):
    def test_families(self):
        self.assertEqual([solution.statusFamily(c) for c in (100, 200, 201, 204, 301, 400, 404, 405, 500, 599)],
                         ["informational", "success", "success", "success", "redirect",
                          "client error", "client error", "client error", "server error", "server error"])

    def test_out_of_range(self):
        for bad in (99, 600, 0, -200):
            with self.assertRaises(ValueError):
                solution.statusFamily(bad)


class ParseTodoTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(solution.parseTodo('{"title": "Buy milk", "done": false, "tags": null}'),
                         {"title": "Buy milk", "done": False, "tags": None})

    def test_invalid_json(self):
        for bad in ("{'title': 'x'}", '{"title": "x",}', "", '{"title": True}'):
            with self.assertRaises(ValueError):
                solution.parseTodo(bad)

    def test_not_an_object(self):
        for bad in ("[1, 2]", "42", '"hello"'):
            with self.assertRaises(ValueError):
                solution.parseTodo(bad)


class TodoToJsonTests(unittest.TestCase):
    def test_round_trip(self):
        todo = {"id": 1, "title": "Buy milk", "done": True, "tags": ["home"], "due": None}
        text = solution.todoToJson(todo)
        self.assertIsInstance(text, str)
        self.assertEqual(json.loads(text), todo)
        self.assertIn("true", text)
        self.assertIn("null", text)


class ValidateTodoTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(solution.validateTodo({"title": "Buy milk"}), [])
        self.assertEqual(solution.validateTodo({"title": "Buy milk", "done": True}), [])

    def test_title_problems(self):
        self.assertEqual(solution.validateTodo({}), ["title is required"])
        self.assertEqual(solution.validateTodo({"title": ""}), ["title is required"])
        self.assertEqual(solution.validateTodo({"title": 42}), ["title must be a string"])

    def test_done_must_be_boolean(self):
        self.assertEqual(solution.validateTodo({"title": "x", "done": "true"}), ["done must be true or false"])
        self.assertEqual(solution.validateTodo({"title": "x", "done": 1}), ["done must be true or false"])

    def test_everything_wrong(self):
        self.assertEqual(solution.validateTodo({"done": 1, "zzz": 0, "colour": "red"}),
                         ["title is required", "done must be true or false",
                          "unknown field: colour", "unknown field: zzz"])


class ListTests(unittest.TestCase):
    TODOS = json.dumps([
        {"id": 1, "title": "Walk dog", "done": True},
        {"id": 2, "title": "Buy milk", "done": False},
        {"id": 3, "title": "Call mum"},
        {"id": 4, "title": "Answer email", "done": True},
    ])

    def test_count_done(self):
        self.assertEqual(solution.countDone(self.TODOS), 2)
        self.assertEqual(solution.countDone("[]"), 0)

    def test_open_titles(self):
        self.assertEqual(solution.openTitles(self.TODOS), ["Buy milk", "Call mum"])
        self.assertEqual(solution.openTitles("[]"), [])
