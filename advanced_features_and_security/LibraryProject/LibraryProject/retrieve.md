# Retrieve Operation - Book Instance

This document details how to retrieve `Book` objects from the database in the Django shell.

## Command

```python
from bookshelf.models import Book

# Retrieve and display all attributes of the book you just created
# Method 1: Get by ID (if you know the ID)
book = Book.objects.get(id=1)

# Method 2: Get by title
book = Book.objects.get(title="1984")

# Method 3: Get by author
book = Book.objects.get(author="George Orwell")

# Method 4: Get all books (returns QuerySet)
all_books = Book.objects.all()
```

## Expected Output

```python
# When retrieving a specific book
print(book)
# Output: 1984

# Display all attributes
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")

# Expected output:
# ID: 1
# Title: 1984
# Author: George Orwell
# Publication Year: 1949

# When retrieving all books
print(all_books)
# Output: <QuerySet [<Book: 1984>]>

# Iterate through all books
for book in all_books:
    print(f"{book.title} by {book.author} ({book.publication_year})")

# Expected output:
# 1984 by George Orwell (1949)
```

## Notes

- `Book.objects.get()` retrieves a single object (raises error if not found or multiple found)
- `Book.objects.all()` retrieves all objects as a QuerySet
- You can filter objects using various field lookups
- The `__str__` method in the model determines how the book is displayed
