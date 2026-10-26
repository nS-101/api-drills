# ex03 — Basics: URLs, views and JSON

**Target time:** 25 minutes. **Concepts:** `urls.py`, function views, `request.method`,
query parameters, path parameters, reading a JSON body, `JsonResponse`, status codes.

Wire up each endpoint in `ex03_basics/urls.py` and write the view functions in
`ex03_basics/views.py`. All URLs below are relative to the site root and have
**no trailing slash**.

## Endpoints

### `GET /ex03/ping`
- Response code 200, body `{"message": "pong"}`.

### `GET /ex03/greet?name=<name>`
- Response code 200, body `{"greeting": "Hello, <name>!"}`.
- If `name` is missing or empty, response code 400 and body `{"error": "name is required"}`.

### `GET /ex03/add/<a>/<b>`
- `a` and `b` are non-negative integers in the URL path.
- Response code 200, body `{"result": a + b}` (a JSON number, not a string).
- If either part isn't an integer (for example `/ex03/add/2/x`), the response code is 404.
  (Hint: a path converter gives you this for free.)

### `POST /ex03/echo`
- The request body is any JSON object.
- Response code 200, body `{"received": <the object that was sent>}`.
- Any other method (GET, PUT, DELETE, ...) gets response code 405.

### `GET /ex03/stats?nums=<comma separated integers>`
- Example: `/ex03/stats?nums=3,1,2` gives `{"count": 3, "min": 1, "max": 3, "sum": 6}`.
- Numbers may be negative.
- If `nums` is missing or empty, response code 400 and body `{"error": "nums is required"}`.

Run the tests with `python manage.py test ex03_basics`.
