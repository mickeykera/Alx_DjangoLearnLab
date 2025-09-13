# Update Operation - Book Instance

This document details how to update `Book` objects in the database using the Django shell.

## Command

```python
from bookshelf.models import Book

# Update the title of "1984" to "Nineteen Eighty-Four" and save the changes
# Method 1: Update using the object instance
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Method 2: Update using QuerySet update method (more efficient)
Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")

# Method 3: Update by ID
Book.objects.filter(id=1).update(title="Nineteen Eighty-Four")
```

## Expected Output

```python
# After updating using Method 1
print(book.title)
# Output: Nineteen Eighty-Four

# Verify the change in the database
updated_book = Book.objects.get(id=1)
print(f"Updated Title: {updated_book.title}")
print(f"Author: {updated_book.author}")
print(f"Publication Year: {updated_book.publication_year}")

# Expected output:
# Updated Title: Nineteen Eighty-Four
# Author: George Orwell
# Publication Year: 1949

# Check all books to confirm the update
all_books = Book.objects.all()
for book in all_books:
    print(f"{book.title} by {book.author} ({book.publication_year})")

# Expected output:
# Nineteen Eighty-Four by George Orwell (1949)
```

## Notes

- Method 1: Updates the object instance and saves it (good for single object updates)
- Method 2: Updates directly in the database (more efficient for bulk updates)
- Always call `.save()` after modifying object attributes when using Method 1
- The update is immediately reflected in the database
- You can update multiple fields at once
