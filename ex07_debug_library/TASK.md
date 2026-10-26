# ex07 — Debugging: Library loans (Diagnostics practice)

**Time limit: 45 minutes.** This one is like the Software Diagnostics section: the code
is already written by "a colleague", the tests describe the correct behavior, and some
of them fail. Find and fix the bugs. Don't rewrite the app from scratch, and don't edit
`tests.py`: the tests are the spec.

**Suggested routine:** run the tests -> pick one failing test -> read its name, the
assertion message and the traceback (bottom-up) -> find the line of app code responsible
-> make the smallest fix -> re-run everything. Keep a note of each bug you fix.

There are **several** independent bugs (more than three). Some tests fail for two
reasons at once, so a fix may move a test from one error to a different one: that's
progress.

## The spec

Each loan looks like:

```json
{"id": 1, "book_title": "Dune", "member": "Alice", "due_date": "2026-11-01", "returned": false}
```

- `POST /ex07/loans`: body is a loan without `id` and without `returned`. Creates it with
  `returned` false. 201 with the loan.
- `GET /ex07/loans`: 200, all loans ordered by id ascending. Optional filters:
  - `member=<name>`: only that member's loans, **ignoring case** (`alice` matches `Alice`).
  - `overdue=true&as_of=<YYYY-MM-DD>`: only loans that are not returned and whose due date
    is **strictly before** `as_of`.
- `GET /ex07/loans/<id>`: 200 with the loan, or 404.
- `PATCH /ex07/loans/<id>/return`: marks the loan as returned. 200 with the updated loan;
  404 if it doesn't exist; 409 if it was already returned.

Run the tests with `python manage.py test ex07_debug_library`.
