# ex09 — Write your own tests

**Target time:** 40 minutes. **Concepts:** Django's `TestCase`, the test client
(`self.client.get(url, params)`), `assertEqual` on status codes and JSON, thinking about
edge cases.

Goldman's Diagnostics description says you may need to *write* tests, not just pass them.
This exercise trains that.

The API below is already implemented correctly in `pricing.py`, `views.py` and `urls.py`.
Your job is to write tests in `ex09_write_tests/test_mine.py` that pin its behavior down.

`python score.py ex09` grades you in two steps:
1. Your tests must all **pass** against the correct API.
2. It then swaps in **six** subtly broken versions of the API, one at a time. A broken
   version is "caught" if at least one of your tests fails against it.
   Your score is how many of the six you catch.

Always test **through the HTTP API** (`self.client.get("/ex09/price", {...})`). The
grader swaps the API behind the URL, so tests that call `computePrice` directly can't
catch anything. Don't read the `mutants/` folder until you're done.

## The API: `GET /ex09/price?amount=<pence>&coupon=<code>`

- `amount` is required and must be a whole number greater than 0; otherwise 400.
- `coupon` is optional. Coupon codes are case-insensitive (`save10` works like `SAVE10`).
  - no coupon: no discount
  - `SAVE10`: 10% off, rounded down to whole pence
  - `SAVE20`: 20% off (rounded down), but only when `amount` is at least 5000; below that, 400
  - `HALF`: 50% off (rounded down), but the discount is capped at 1000
  - any other code: 400
- Success: 200 with `{"amount": <amount>, "discount": <discount>, "total": <amount - discount>}`.

Hint: for every rule above, ask "what is the boundary, and what would a typical bug look
like here?" Then write a test right on that boundary.
