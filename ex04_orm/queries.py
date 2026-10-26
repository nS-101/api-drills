from .models import Book


def createBook(title, author, year, pages):
    """1. Create a Book, save it to the database and return it."""
    raise NotImplementedError


def getBookOrNone(bookId):
    """2. Return the Book with this id, or None if there isn't one."""
    raise NotImplementedError


def booksByAuthor(author):
    """3. Return the books by this exact author, oldest (smallest year) first."""
    raise NotImplementedError


def booksAfterYear(year):
    """4. Return books published strictly after `year`, ordered by title A to Z."""
    raise NotImplementedError


def titleSearch(text):
    """5. Return books whose title contains `text`, ignoring case, ordered by id."""
    raise NotImplementedError


def updatePages(bookId, pages):
    """6. Set the page count of the book with this id.
    Return True if a book was updated, False if there is no such book."""
    raise NotImplementedError


def deleteBook(bookId):
    """7. Delete the book with this id. Return True if one was deleted, else False."""
    raise NotImplementedError


def countByAuthor():
    """8. Return a dict mapping each author to how many books they have,
    e.g. {"Orwell": 2, "Austen": 1}. Return {} if there are no books."""
    raise NotImplementedError


def longestBook():
    """9. Return the book with the most pages (if tied, the one with the smallest id),
    or None if there are no books."""
    raise NotImplementedError


def publishedBooks():
    """10. (Part B) Return the books where published is True, ordered by id."""
    raise NotImplementedError


def publishBook(bookId):
    """11. (Part B) Mark the book with this id as published and save it.
    Return True if found, False if there is no such book."""
    raise NotImplementedError
