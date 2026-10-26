import json
from urllib.parse import parse_qsl, urlsplit

#json.dumps converts python object to JSON string
#json.loads converts JSON string to python object

def parseUrl(url):
    """1. Take a URL apart.

    parseUrl("http://127.0.0.1:8000/todos/3?done=true&sort=title") returns
        {"scheme": "http", "host": "127.0.0.1", "port": 8000,
         "path": "/todos/3", "query": {"done": "true", "sort": "title"}}

    - port is an int, or None if the URL has no port
    - path is "" if the URL has no path
    - query is a dict of strings ({} if there is no query string)
    """

    parts = urlsplit(url)
    queryDict = dict(parse_qsl(parts.query))
    dictionary = {
        "scheme": parts.scheme,
        "host": parts.hostname,
        "port": parts.port if parts.port else None,
        "path": parts.path if parts.path else "",
        "query":  queryDict if queryDict != {} else {}
    }
    return dictionary

def statusFamily(code):
    """2. Return the family of an HTTP status code:
    1xx "informational", 2xx "success", 3xx "redirect",
    4xx "client error", 5xx "server error".
    Raise ValueError for anything outside 100-599."""

    
    if code < 100 or code > 599:
        raise ValueError(f"bad status code: {code}")
    else:
        num = int(str(code)[0])
        if num == 1:
            return "informational"
        elif num == 2:
            return "success"
        elif num == 3:
            return "redirect"
        elif num == 4:
            return "client error"
        elif num == 5:
            return "server error"
    


def parseTodo(text):
    """3. Parse JSON text that should contain one JSON object, and return it as a dict.
    Raise ValueError if the text isn't valid JSON, or if it's valid JSON but not an
    object (for example a list or a number)."""

    obj = json.loads(text)
    if isinstance(obj, dict):
        return obj
    else:
        raise ValueError("Expected a JSON object")

def todoToJson(todo):
    """4. Turn a todo dict into JSON text (a str) and return it."""
    string = json.dumps(todo)
    return string


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
    arrOfErrors = []
    keysList = sorted(list(data.keys())) #create list of dictionary keys in alphabetical order

    if "title" not in data:
        arrOfErrors.append("title is required")
    elif not isinstance(data["title"], str):
        arrOfErrors.append("title must be a string")
    elif data["title"] == "":
        arrOfErrors.append("title is required")

    if "done" in data and not isinstance(data["done"], bool):
        arrOfErrors.append("done must be true or false")

    for key in keysList:
        if key == "title" or key == "done":
            continue
        else:
            arrOfErrors.append(f"unknown field: {key}")

    return arrOfErrors


def countDone(text):
    """6. `text` is a JSON array of todo objects. Return how many have "done": true.
    A todo without a "done" key counts as not done."""

    count = 0
    reText = json.loads(text)
    for obj in reText:
        if "done" not in obj:
            continue
        elif obj["done"] is True: #is True and not == True since if it is 1, which is Truthy, it will count it when it shouldn't
            count+=1
    return count


def openTitles(text):
    """7. `text` is a JSON array of todo objects. Return the titles of the todos that
    are NOT done, sorted A to Z."""

    arr = []
    todoObjects = json.loads(text)
    for obj in todoObjects:
        if "done" not in obj or obj["done"] is not True:
            if obj["title"]:
                arr.append(obj["title"])
    return sorted(arr)
