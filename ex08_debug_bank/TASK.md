# ex08 — Debugging: Bank accounts (Diagnostics practice)

**Time limit: 45 minutes.** Same rules as ex07: the app exists, the tests are the spec,
fix the bugs with small changes, don't edit `tests.py`.

Start by running the tests. If *every* test fails with the same error, that's one bug
that's hiding all the others. Read the error message carefully before touching any code.

There are **five or more** independent bugs.

## The spec

Money is stored as integer pence. An account looks like:

```json
{"id": 1, "owner": "Alice", "balance": 0, "frozen": false}
```

- `POST /ex08/accounts`: body `{"owner": "..."}`. Creates an account with balance 0, not
  frozen. 201 with the account.
- `GET /ex08/accounts?min_balance=<n>`: 200, accounts whose balance is **at least** `n`,
  ordered by balance **highest first** (ties by id ascending). Without `min_balance`,
  all accounts in that same order.
- `GET /ex08/accounts/<id>`: 200 or 404.
- `POST /ex08/accounts/<id>/deposit`: body `{"amount": n}`. `n` must be greater than 0,
  else 400. 200 with the updated account; 404 if the account doesn't exist.
- `POST /ex08/accounts/<id>/withdraw`: body `{"amount": n}`. 400 if `n` is not greater than
  0, if the account is frozen, or if `n` is more than the balance (withdrawing the
  **whole** balance is allowed). 200 with the updated account; 404 if missing.
- `POST /ex08/transfer`: body `{"from": id, "to": id, "amount": n}`. Moves money between
  accounts. 404 if either account doesn't exist; 400 if the amount isn't positive or the
  source doesn't have enough. On any error, **no balance changes**. On success 200 with
  `{"from": <source account>, "to": <destination account>}`.

Run the tests with `python manage.py test ex08_debug_bank`.
