# Create a Book Instance

This document details the command to create a `Book` object in the Django shell.

## Python Command

```python
# First, import the model from your app
from bookshelf.models import Book

# Create and save the new Book instance in one step
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

## Expected Output

```python
# The book object is created and returned
print(book)
# Output: 1984

# Check the book's attributes
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"ID: {book.id}")

# Expected output:
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
# ID: 1
```

## Notes

- The `objects.create()` method creates and saves the object in one step
- The book is automatically assigned a unique ID
- The object is immediately available in the database
- You can access all fields using dot notation
