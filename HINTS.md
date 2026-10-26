# Hints

Three levels per exercise. Read **one** level, close this file, try again. Level 3 is
close to the answer, so only use it after a real attempt.

---

## ex01 — JSON, URLs and status codes

<details><summary>Level 1</summary>

- `parseUrl`: the standard library already knows how to split a URL. Which function in
  `urllib.parse` returns an object with `.scheme`, `.hostname`, `.port`, `.path`, `.query`?
- `parseTodo`: what exception does `json.loads` raise on bad text? Is it a `ValueError`?
- `validateTodo`: why does `isinstance(True, int)` matter for the `done` rule?
</details>

<details><summary>Level 2</summary>

- `urlsplit(url)` gives you everything; `dict(parse_qsl(parts.query))` turns
  `"done=true&sort=title"` into `{"done": "true", "sort": "title"}`.
- `statusFamily`: `code // 100` gives the first digit.
- `json.JSONDecodeError` is a subclass of `ValueError`, so you only need to add the
  "not a dict" check yourself: `isinstance(data, dict)`.
- `validateTodo`: check `isinstance(value, bool)` for `done` (not `int`), and loop over
  `sorted(data)` for unknown keys.
</details>

<details><summary>Level 3</summary>

- `countDone`: `sum(1 for todo in json.loads(text) if todo.get("done") is True)`.
- `openTitles`: `sorted(t["title"] for t in todos if not t.get("done", False))`.
</details>

---

## ex02 — Todo API by hand

<details><summary>Level 1</summary>

- Start with `GET /todos` returning `self.server.todos`, then `POST /todos`. Most other tests
  create todos with POST first.
- `self.path` includes the query string. How do you get just `/todos` out of
  `/todos?done=true`? (There's an import at the top of `server.py`.)
- Which methods does `BaseHTTPRequestHandler` call for PATCH, DELETE and PUT requests?
</details>

<details><summary>Level 2</summary>

- One method per HTTP method: `do_GET`, `do_POST`, `do_PATCH`, `do_DELETE`, `do_PUT`.
- Write a helper `findTodo(path)` that returns the todo for `/todos/3`, or None. Use
  `str.isdigit()` so `/todos/abc` gives None (then you send 404).
- Write a helper that reads the body, parses it inside `try/except ValueError`, checks it's
  a dict, and returns a list of errors. POST and PATCH can share it (PATCH just doesn't
  require `title`).
- For PATCH, validate everything **before** changing anything; then `todo.update(data)`.
- `do_PUT` just sends 405.
</details>

<details><summary>Level 3</summary>

- Filter: `done = parse_qs(urlsplit(self.path).query).get("done")` gives `["true"]` or None.
  Compare `done[0] == "true"`.
- Delete: `self.server.todos.remove(todo)` then `self.sendEmpty(204)`.
- New todo: `{"id": self.server.nextId, "title": data["title"], "done": data.get("done", False)}`,
  then `self.server.nextId += 1`.
</details>

---

## ex03 — Basics

<details><summary>Level 1</summary>

- Nothing works yet? Every test gets a 404 until the URL is in `urlpatterns`. Start with `ping`.
- Which attribute of `request` holds the query string values? Which holds the raw body?
</details>

<details><summary>Level 2</summary>

- `path("ping", views.ping)`: no leading slash, and no trailing slash (the tests use none).
- Query parameters live in `request.GET` (a dict-like object); use `.get("name", "")`.
- `add/<int:a>/<int:b>`: the converter turns the text into ints and 404s on anything else.
- The JSON body is `request.body` (bytes): parse it with `json.loads`. `request.POST` is
  only for HTML form posts and will be empty here.
- For 405, check `request.method` yourself, or use the `require_POST` / `require_GET`
  decorators from `django.views.decorators.http`.
</details>

<details><summary>Level 3</summary>

- `return JsonResponse({"error": "name is required"}, status=400)`
- `nums = [int(x) for x in raw.split(",")]` then build the dict with `len`, `min`, `max`, `sum`.
- `echo` needs `@csrf_exempt` above it to work outside tests (the test client skips CSRF).
</details>

---

## ex04 — ORM

<details><summary>Level 1</summary>

- Which manager method creates and saves in one step?
- "Return None if missing": would `get` or `filter(...).first()` be less work here?
- Part B errors with `no such column`? What changed in the model that the database
  doesn't know about yet?
</details>

<details><summary>Level 2</summary>

- Lookups are written `field__operator=value`: `year__gt`, `title__icontains`.
- `order_by("year")` ascending, `order_by("-pages", "id")` descending then tie-break.
- `filter(...).update(...)` returns how many rows changed; `filter(...).delete()` returns
  a pair `(count, details)`.
- `countByAuthor`: build the dict in a loop over `Book.objects.all()`, or use
  `values("author").annotate(total=Count("id"))`.
</details>

<details><summary>Level 3</summary>

- `published = models.BooleanField(default=False)` then `python manage.py makemigrations ex04_orm`.
- `longestBook`: `Book.objects.order_by("-pages", "id").first()` (returns None when empty).
</details>

---

## ex05 — CRUD

<details><summary>Level 1</summary>

- How many URL patterns do you need? (Hint: one for the collection, one for a single note.)
- Every endpoint returns a note as JSON. What small helper would save you repeating that?
</details>

<details><summary>Level 2</summary>

- One view per URL, branching on `request.method`. Anything unhandled falls through to a 405
  (`HttpResponseNotAllowed([...])` or `JsonResponse({...}, status=405)`).
- Detail view: look the note up first (`try: Note.objects.get(id=noteId)` /
  `except Note.DoesNotExist:` -> 404), then branch on the method.
- PATCH: loop over the allowed field names; only set the ones present in the body; `save()`.
- A list response needs `JsonResponse(listOfDicts, safe=False)`.
- 204 means "no content": `HttpResponse(status=204)`, not a JsonResponse.
</details>

<details><summary>Level 3</summary>

- `pinned` filter: `request.GET.get("pinned")` is the *string* `"true"`/`"false"`;
  compare it: `filter(pinned=(value == "true"))`.
- `setattr(note, field, data[field])` sets a field by name.
</details>

---

## ex06 — Mock OA

No hints during the timed attempt: that's the point. Afterwards, if hidden tests fail:

<details><summary>After your attempt: what the hidden tests check</summary>

Validation on create (an `id` in the body, negative price or stock, zero is fine); empty
list; category filter with no matches; sorting both ways with ties kept in id order
(`order_by("price", "id")`); filter and sort together; PATCH 404; a PATCH with a negative
value must change **nothing** (validate before setting any field); PATCH of the date
persists; PUT and DELETE are 405 even for ids that don't exist.
</details>

---

## ex07 — Debugging: Library

<details><summary>Level 1</summary>

Fix in this order: anything that crashes (an ERROR) before anything that's merely wrong
(a FAIL). For each failing test, the assertion message tells you "expected vs got".
</details>

<details><summary>Level 2: where to look</summary>

`urls.py` (one line), the POST branch, the list ordering, both list filters, the detail
view, and the return view (two separate problems there).
</details>

<details><summary>Level 3: the bug list</summary>

1. POST returns 200 instead of 201.
2. List ordered by `-id` instead of `id`.
3. Member filter is case-sensitive: use `member__iexact`.
4. Overdue uses `due_date__lte`; the spec says strictly before: `__lt`.
5. Detail view has no `try/except Loan.DoesNotExist` -> crashes instead of 404.
6. The return URL has a trailing slash; the tests call it without one (you see a 301).
7. "Already returned" compares a boolean to the string `"true"`, so it's never true.
8. The return view never calls `loan.save()`.
</details>

---

## ex08 — Debugging: Bank

<details><summary>Level 1</summary>

Every test fails with the same `OperationalError`. Read the message: what is the database
missing, and which command creates it?
</details>

<details><summary>Level 2: where to look</summary>

Migrations (one command), list ordering, deposit validation, the withdraw arithmetic and
its balance check, and the order of operations in `transfer`.
</details>

<details><summary>Level 3: the bug list</summary>

1. `frozen` is in the model but not in any migration: `python manage.py makemigrations ex08_debug_bank`.
2. List ordered by `balance` ascending; the spec wants `-balance`, then `id`.
3. Deposit accepts 0 (`< 0` should be `<= 0`).
4. Withdraw adds instead of subtracting.
5. Withdraw rejects the whole balance (`>=` should be `>`).
6. Transfer debits and saves the source before checking the destination exists: look up
   **both** accounts first (or wrap it in `transaction.atomic()`).
</details>

---

## ex09 — Write tests

<details><summary>Level 1</summary>

For each rule in the spec, what's the *boundary*? A good test sits exactly on it.
</details>

<details><summary>Level 2</summary>

Things worth a test each: an amount where rounding matters; a lowercase coupon; SAVE20
exactly at 5000 and just below it; HALF below and above the cap; amount 0; an unknown
coupon. Check the whole JSON body, not just the status code.
</details>

<details><summary>Level 3: what the six broken versions do</summary>

SAVE10 takes off a flat 10; HALF has no cap; unknown coupons are ignored; amount 0 is
accepted; SAVE20 needs *more than* 5000; coupon codes are case-sensitive.
</details>

---

## ex10 — Mock OA 2

No hints during the timed attempt. Afterwards, if hidden tests fail:

<details><summary>After your attempt: what the hidden tests check</summary>

400 for a body containing `id` or `booked` and for capacity 0; ordering by date **then** id
(`order_by("date", "id")`); case-insensitive venue (`venue__iexact`); `from` includes the
date itself (`date__gte`); `available=true` (booked less than capacity); filters combined;
booking exactly up to capacity is fine and one more seat is 409 with nothing changed; seats 0
is 400; booking a missing event is 404; deleting an event with bookings is 409; PUT on an
event, DELETE on the collection and GET on `/book` are all 405.
</details>
