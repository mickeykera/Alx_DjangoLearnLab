# Complete CRUD Operations for Book Model in Django

This document demonstrates all CRUD (Create, Read, Update, Delete) operations for the Book model in Django with practical examples.

## Prerequisites

```python
# Import the Book model
from bookshelf.models import Book
```

## 1. CREATE Operation

### Command

```python
# Create a Book instance with title "1984", author "George Orwell", and publication year 1949
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
```

### Expected Output

```python
print("=== CREATE ===")
print(book)  # Depends on __str__ method, usually the title
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"ID: {book.id}")

# Expected output:
# === CREATE ===
# 1984
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
# ID: 1
```

## 2. RETRIEVE Operation

### Command1

```python
# Retrieve the book by ID, title, author, or get all books
book = Book.objects.get(id=book.id)
book_by_title = Book.objects.get(title="1984")
book_by_author = Book.objects.get(author="George Orwell")
all_books = Book.objects.all()
```

### Expected Output1

```python
print("=== RETRIEVE ===")
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"All Books: {all_books}")

# Expected output:
# === RETRIEVE ===
# ID: 1
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
# All Books: <QuerySet [<Book: 1984>]>
```

## 3. UPDATE Operation

### Command2

```python
# Update the title of "1984" to "Nineteen Eighty-Four" and save the changes
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Alternative bulk update (more efficient)
# Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")

# Verify the update
updated_book = Book.objects.get(id=book.id)
```

### Expected Output2

```python
print("=== UPDATE ===")
print(f"Updated Title: {updated_book.title}")
print(f"Author: {updated_book.author}")
print(f"Publication Year: {updated_book.publication_year}")

# Expected output:
# === UPDATE ===
# Updated Title: Nineteen Eighty-Four
# Author: George Orwell
# Publication Year: 1949
```

## 4. DELETE Operation

### Command3

```python
# Delete the book and confirm the deletion
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Alternative bulk delete
# Book.objects.filter(title="Nineteen Eighty-Four").delete()

# Verify deletion
all_books = Book.objects.all()
book_count = Book.objects.count()
```

### Expected Output3

```python
print("=== DELETE ===")
try:
    Book.objects.get(title="Nineteen Eighty-Four")
    print("Book still exists")
except Book.DoesNotExist:
    print("Book successfully deleted")

print(f"All Books: {all_books}")
print(f"Total books in database: {book_count}")

# Expected output:
# === DELETE ===
# Book successfully deleted
# All Books: <QuerySet []>
# Total books in database: 0
```

## Complete CRUD Sequence Example

```python
# Complete workflow in one session
from bookshelf.models import Book

print("=== COMPLETE SEQUENCE ===")

# CREATE
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
print(f"Created: {book}")

# READ
retrieved_book = Book.objects.get(id=book.id)
print(f"Retrieved: {retrieved_book.title} by {retrieved_book.author}")

# UPDATE
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title to: {book.title}")

# DELETE
book.delete()
print("Book deleted")

# VERIFY
print(f"Books remaining: {Book.objects.count()}")

# Expected output:
# === COMPLETE SEQUENCE ===
# Created: 1984
# Retrieved: 1984 by George Orwell
# Updated title to: Nineteen Eighty-Four
# Book deleted
# Books remaining: 0
```

## Key Points

- **Create**: Use `Book.objects.create()` for immediate creation and saving
- **Read**: Use `Book.objects.get()` for single objects, `Book.objects.all()` for all objects
- **Update**: Modify attributes and call `.save()`, or use `.update()` for bulk updates
- **Delete**: Use `.delete()` method (permanent and irreversible)
- Always handle exceptions when retrieving objects that might not exist
- The `__str__` method in your model determines how objects are displayed
- All operations are immediately reflected in the database
- Use bulk operations (`.update()`, `.delete()`) for better performance with multiple objects
