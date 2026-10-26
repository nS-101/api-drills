from django.test import TestCase

from . import queries
from .models import Book


def makeBooks():
    return [
        Book.objects.create(title="Nineteen Eighty-Four", author="Orwell", year=1949, pages=328),
        Book.objects.create(title="Animal Farm", author="Orwell", year=1945, pages=112),
        Book.objects.create(title="Emma", author="Austen", year=1815, pages=474),
        Book.objects.create(title="Dune", author="Herbert", year=1965, pages=474),
    ]


def ids(books):
    return [b.id for b in books]


class CreateAndGetTests(TestCase):
    def test_create_book(self):
        book = queries.createBook("Dune", "Herbert", 1965, 412)
        self.assertIsNotNone(book.id)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get(id=book.id).title, "Dune")

    def test_get_book_or_none(self):
        books = makeBooks()
        self.assertEqual(queries.getBookOrNone(books[2].id).title, "Emma")
        self.assertIsNone(queries.getBookOrNone(999))


class FilterTests(TestCase):
    def setUp(self):
        self.books = makeBooks()

    def test_books_by_author(self):
        self.assertEqual(ids(queries.booksByAuthor("Orwell")), [self.books[1].id, self.books[0].id])
        self.assertEqual(list(queries.booksByAuthor("Nobody")), [])

    def test_books_after_year_is_strict(self):
        self.assertEqual(ids(queries.booksAfterYear(1945)), [self.books[3].id, self.books[0].id])

    def test_title_search_ignores_case(self):
        self.assertEqual(ids(queries.titleSearch("FARM")), [self.books[1].id])
        self.assertEqual(ids(queries.titleSearch("e")), ids([self.books[0], self.books[2], self.books[3]]))


class UpdateAndDeleteTests(TestCase):
    def setUp(self):
        self.books = makeBooks()

    def test_update_pages(self):
        self.assertTrue(queries.updatePages(self.books[0].id, 999))
        self.assertEqual(Book.objects.get(id=self.books[0].id).pages, 999)
        self.assertFalse(queries.updatePages(12345, 1))

    def test_delete_book(self):
        self.assertTrue(queries.deleteBook(self.books[0].id))
        self.assertEqual(Book.objects.count(), 3)
        self.assertFalse(queries.deleteBook(self.books[0].id))


class AggregateTests(TestCase):
    def test_count_by_author(self):
        self.assertEqual(queries.countByAuthor(), {})
        makeBooks()
        self.assertEqual(queries.countByAuthor(), {"Orwell": 2, "Austen": 1, "Herbert": 1})

    def test_longest_book_tie_breaks_on_id(self):
        self.assertIsNone(queries.longestBook())
        books = makeBooks()
        self.assertEqual(queries.longestBook().id, books[2].id)


class PartBPublishedTests(TestCase):
    def test_published_defaults_to_false(self):
        book = Book.objects.create(title="Draft", author="Me", year=2026, pages=10)
        self.assertFalse(Book.objects.get(id=book.id).published)

    def test_publish_and_list(self):
        books = makeBooks()
        self.assertEqual(list(queries.publishedBooks()), [])
        self.assertTrue(queries.publishBook(books[3].id))
        self.assertTrue(queries.publishBook(books[1].id))
        self.assertFalse(queries.publishBook(999))
        self.assertEqual(ids(queries.publishedBooks()), [books[1].id, books[3].id])
