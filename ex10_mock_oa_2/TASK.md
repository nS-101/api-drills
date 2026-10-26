# ex10 — Mock OA 2: Events API (timed, final rehearsal)

**Time limit: 45 minutes. Set a timer before you scroll down.** Do this one the day before
the real OA, under exam rules: no notes, no old code, Django docs for syntax only.

---

Implement a REST API to manage events that people can book seats for.

Each event is a JSON entry with the following keys:

- `id`: the unique ID of the event (Integer)
- `name`: the event name (String)
- `venue`: where it happens (String)
- `date`: the date of the event (String, `YYYY-MM-DD`)
- `capacity`: total number of seats (Integer)
- `booked`: number of seats already booked (Integer)

Example:

```json
{"id": 1, "name": "Python Meetup", "venue": "Kilburn", "date": "2026-11-12", "capacity": 40, "booked": 0}
```

The `Event` model already exists. Implement the following endpoints.

### `POST /ex10/events`
- expects a JSON object with `name`, `venue`, `date` and `capacity`, and **without** `id` or `booked`
- if the body contains `id` or `booked`, or `capacity` is less than 1, the response code is 400
  and nothing is created
- otherwise creates the event with `booked` = 0 and a unique integer id (1, 2, ...); the
  response code is 201 and the body is the created event

### `GET /ex10/events`
- the response code is 200 and the body is an array of events ordered by `date` ascending;
  events on the same date are ordered by id ascending
- optional filters, which can be combined:
  - `venue=<name>`: only events at that venue, ignoring case
  - `from=<YYYY-MM-DD>`: only events on or after that date
  - `available=true`: only events that still have at least one free seat

### `GET /ex10/events/<id>`
- 200 with the event, or 404 if it doesn't exist

### `POST /ex10/events/<id>/book`
- expects `{"seats": n}`
- 404 if the event doesn't exist
- 400 if `n` is less than 1
- 409 if there aren't enough free seats (`booked + n` would exceed `capacity`); nothing changes
- otherwise adds `n` to `booked`; the response code is 200 and the body is the updated event

### `DELETE /ex10/events/<id>`
- 404 if the event doesn't exist
- 409 if any seats are booked (an event with bookings can't be deleted)
- otherwise deletes it; the response code is 204 with an empty body

### Any other method on these URLs
- the response code is 405

---

`tests.py` holds the visible tests. `tests_hidden.py` simulates hidden tests: don't open it
until you're done. `python score.py ex10` shows both scores.
