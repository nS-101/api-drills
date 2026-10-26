# ex06 — Mock OA: Products API (timed)

**Time limit: 45 minutes. Set a timer before you scroll down.**
Exam rules: no notes, no old code. Allowed: the Django docs for syntax only (in the real
test you'd ask the built-in assistant narrow syntax questions instead).

---

Implement a simple REST API to manage a collection of products.

Each product is a JSON entry with the following keys:

- `id`: the unique ID of the product (Integer)
- `name`: the product name (String)
- `category`: the category (String)
- `price`: the price in pounds (Float, e.g. 19.99)
- `stock`: units in stock (Integer)
- `listed_on`: the date it was listed (String, `YYYY-MM-DD`)

Example:

```json
{"id": 1, "name": "Desk Lamp", "category": "home", "price": 24.5, "stock": 12, "listed_on": "2026-03-01"}
```

The `Product` model already exists. Implement a REST service that exposes the `/ex06/products`
endpoint as follows.

### `POST /ex06/products`
- creates a new product
- expects a JSON product object without an `id` property; all other keys are present
- if the body contains an `id` property, or `price` or `stock` is negative, the response
  code is 400 and nothing is created
- otherwise assigns a unique integer id (the first product is 1, the second 2, and so on);
  the response code is 201 and the body is the created product

### `GET /ex06/products`
- the response code is 200 and the body is an array of all products ordered by id ascending
- optional query parameter `category=<value>`: only products in that category (exact match)
- optional query parameter `sort=price` (cheapest first) or `sort=-price` (most expensive
  first); products with the same price stay in id order
- the two parameters can be combined

### `GET /ex06/products/<id>`
- if the product exists, the response code is 200 and the body is the product
- otherwise the response code is 404

### `PATCH /ex06/products/<id>`
- expects a JSON object with **some** product keys (never `id`); only those change
- if the product doesn't exist, the response code is 404
- if the new `price` or `stock` would be negative, the response code is 400 and nothing changes
- on success, the response code is 200 and the body is the full updated product

### `DELETE` or `PUT` on `/ex06/products/<id>`
- products can't be deleted or replaced: the response code is 405

---

`tests.py` holds the tests you can see. `tests_hidden.py` simulates HackerRank's hidden
tests: **don't open it until you're done**. `python score.py ex06` shows both scores
without revealing the hidden tests' contents.
