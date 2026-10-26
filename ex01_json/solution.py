import json
from urllib.parse import parse_qsl, urlsplit


def parseUrl(url):
    """1. Take a URL apart.

    parseUrl("http://127.0.0.1:8000/todos/3?done=true&sort=title") returns
        {"scheme": "http", "host": "127.0.0.1", "port": 8000,
         "path": "/todos/3", "query": {"done": "true", "sort": "title"}}

    - port is an int, or None if the URL has no port
    - path is "" if the URL has no path
    - query is a dict of strings ({} if there is no query string)
    """
    raise NotImplementedError


def statusFamily(code):
    """2. Return the family of an HTTP status code:
    1xx "informational", 2xx "success", 3xx "redirect",
    4xx "client error", 5xx "server error".
    Raise ValueError for anything outside 100-599."""
    raise NotImplementedError


def parseTodo(text):
    """3. Parse JSON text that should contain one JSON object, and return it as a dict.
    Raise ValueError if the text isn't valid JSON, or if it's valid JSON but not an
    object (for example a list or a number)."""
    raise NotImplementedError


def todoToJson(todo):
    """4. Turn a todo dict into JSON text (a str) and return it."""
    raise NotImplementedError


def validateTodo(data):
    """5. Check a dict that a client sent to create a todo. Return a list of error
    messages, or [] if it's valid. Rules, checked in this order:

    - "title" missing                     -> "title is required"
    - "title" present but not a string    -> "title must be a string"
    - "title" is an empty string          -> "title is required"
    - "done" present but not a boolean    -> "done must be true or false"
    - every other key (sorted A to Z)     -> "unknown field: <key>"

    Example: validateTodo({"done": 1, "zzz": 0, "colour": "red"}) returns
        ["title is required", "done must be true or false",
         "unknown field: colour", "unknown field: zzz"]
    Careful: in Python, True is also an int, and 1 == True.
    """
    raise NotImplementedError


def countDone(text):
    """6. `text` is a JSON array of todo objects. Return how many have "done": true.
    A todo without a "done" key counts as not done."""
    raise NotImplementedError


def openTitles(text):
    """7. `text` is a JSON array of todo objects. Return the titles of the todos that
    are NOT done, sorted A to Z."""
    raise NotImplementedError
