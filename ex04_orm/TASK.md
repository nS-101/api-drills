# ex04 — Models and the ORM

**Target time:** 30 minutes. **Concepts:** model fields, `objects.create`, `get`,
`filter` with lookups (`__gt`, `__icontains`), `order_by`, `save`, `delete`, counting,
adding a field with a migration.

There is no HTTP in this exercise. You write plain Python functions in
`ex04_orm/queries.py` that use the `Book` model in `ex04_orm/models.py`.
The tests call your functions directly.

Each function's docstring in `queries.py` says exactly what it must do.

## Part A: queries (functions 1-9)
Fill in every function that currently raises `NotImplementedError`.

## Part B: change the model (function 10 and 11)
The library now tracks whether a book is published.

1. Add a field `published` to `Book`: a boolean that defaults to `False`.
2. Create a migration for it: `python manage.py makemigrations ex04_orm`.
   (Try running the tests *before* making the migration, so you recognize the error
   message when you see it in the wild.)
3. Implement `publishedBooks` and `publishBook`.

Useful while you work: `python manage.py shell` gives you a Python prompt where you
can run `from ex04_orm.models import Book` and try queries by hand. (Run
`python manage.py migrate` once first so the shell has a database.)

Run the tests with `python manage.py test ex04_orm`.
