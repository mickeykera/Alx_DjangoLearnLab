# Delete Operation - Book Instance

This document details how to delete `Book` objects from the database using the Django shell.

## Command

```python
from bookshelf.models import Book

# Delete the book you created and confirm the deletion by trying to retrieve all books again
# Method 1: Delete using the object instance
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Method 2: Delete using QuerySet delete method
Book.objects.filter(title="Nineteen Eighty-Four").delete()

# Method 3: Delete by ID
Book.objects.filter(id=1).delete()

# Method 4: Delete all books (use with caution!)
# Book.objects.all().delete()
```

## Expected Output

```python
# After deletion, verify the book is gone
try:
    book = Book.objects.get(title="Nineteen Eighty-Four")
    print("Book still exists")
except Book.DoesNotExist:
    print("Book successfully deleted")

# Expected output:
# Book successfully deleted

# Confirm deletion by retrieving all books
all_books = Book.objects.all()
print(all_books)
# Expected output: <QuerySet []>

# Check the count of books
book_count = Book.objects.count()
print(f"Total books in database: {book_count}")
# Expected output: Total books in database: 0

# Try to get the deleted book (will raise exception)
try:
    deleted_book = Book.objects.get(id=1)
except Book.DoesNotExist:
    print("Book with ID 1 no longer exists")
# Expected output: Book with ID 1 no longer exists
```

## Notes

- `delete()` method removes the object from the database permanently
- After deletion, the object instance still exists in Python memory but is no longer in the database
- `Book.DoesNotExist` exception is raised when trying to retrieve a deleted object
- `Book.objects.count()` returns the total number of objects in the database
- Deletion is irreversible - use with caution!
- You can delete multiple objects at once using filter conditions
