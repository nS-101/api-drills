# ex05 — A full CRUD API

**Target time:** 40 minutes. **Concepts:** one URL handling several methods, creating and
reading rows, partial updates (PATCH), deleting, 201/204/404/405, turning a model into
a dict.

The `Note` model already exists in `ex05_crud/models.py` (with its migration). Build a
REST API for it in `ex05_crud/urls.py` and `ex05_crud/views.py`.

Each note looks like this in JSON:

```json
{"id": 1, "title": "Shopping", "body": "eggs, milk", "pinned": false}
```

## `/ex05/notes`

### `POST /ex05/notes`
- The body is a JSON note **without** `id`. `title` and `body` are always present;
  `pinned` is optional and defaults to `false`.
- Creates the note and gives it a unique integer id (the first note is 1, then 2, ...).
- Response code 201; the body is the created note, including its id.

### `GET /ex05/notes`
- Response code 200; the body is an array of all notes, ordered by id ascending.
- Optional query parameter `pinned=true`: only return pinned notes (`pinned=false`
  returns only unpinned ones).

### Any other method on `/ex05/notes`
- Response code 405.

## `/ex05/notes/<id>`

### `GET /ex05/notes/<id>`
- 200 with the note, or 404 if no note has that id.

### `PATCH /ex05/notes/<id>`
- The body contains **some** of `title`, `body`, `pinned`. Only those fields change.
- 200 with the full updated note, or 404 if no note has that id.

### `DELETE /ex05/notes/<id>`
- 204 with an empty body, or 404 if no note has that id.

### Any other method on `/ex05/notes/<id>`
- Response code 405.

Do POST first: every other test creates notes through POST.

Run the tests with `python manage.py test ex05_crud`.
