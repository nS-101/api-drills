# ex02 — Build a todo API by hand (plain Python, no framework)

**Target time:** 60 to 75 minutes. **Read first:** sections 5 to 8 of *Web APIs from the
Ground Up* (this is the "Build it yourself" exercise from section 7, with tests).
**Concepts:** routing on the path, reading a request body, sending status codes and JSON,
validation (400), not found (404), method not allowed (405), 204 No Content.

Complete `ex02_http_server/server.py`. It already has helpers (`sendJson`, `sendEmpty`,
`readBody`) and a `makeServer` function. The todos live on the server object
(`self.server.todos`, `self.server.nextId`) so each test starts with an empty list.

The tests start your server on a free port and send it **real HTTP requests**, exactly
like curl would. You can also run it yourself with `python -m ex02_http_server.server` and
poke it with curl from a second Terminal window.

Each todo looks like `{"id": 1, "title": "Buy milk", "done": false}`.

## `/todos`

### `POST /todos`
- Body: a JSON object with `title` (a non-empty string) and optionally `done` (a boolean,
  default `false`). No other keys.
- Creates the todo with the next id (1, 2, 3, ...). Response 201 with the todo.
- If the body isn't valid JSON, isn't an object, or breaks a rule above: response 400 with
  `{"error": "<message>"}` and nothing is created. (Your ex01 `validateTodo` is handy here.)

### `GET /todos`
- Response 200 with all todos as an array, ordered by id.
- Optional `?done=true` or `?done=false` returns only finished or unfinished todos.

## `/todos/<id>`

### `GET /todos/<id>`
- 200 with the todo, or 404 if there's no todo with that id. A non-number id (`/todos/abc`)
  is also 404.

### `PATCH /todos/<id>`
- Body: an object with some of `title`, `done`. Only those change.
- 200 with the full updated todo; 404 if missing; 400 if a value is invalid
  (empty title, non-boolean done, unknown key, bad JSON), and then nothing changes.

### `DELETE /todos/<id>`
- 204 with an empty body, or 404 if missing.

## Everything else
- Any other path: 404.
- `PUT` on any path: 405. (Without a `do_PUT` method, Python answers 501 "Not
  Implemented". 405 is the right answer for "this server knows the URL but not that method".)

Run the tests with `python -m unittest ex02_http_server.tests` (or `python score.py ex02`).
If your code raises an exception while handling a request, the traceback prints above the
test results and the test reports that the server crashed.
