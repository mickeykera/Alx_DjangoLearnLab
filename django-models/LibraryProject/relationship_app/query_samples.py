"""
Django Relationship Query Examples
This script demonstrates various queries using different relationship types:
- One-to-Many (ForeignKey): Author -> Book
- Many-to-Many: Library <-> Book
- One-to-One: Library -> Librarian
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name=None):
    """
    ONE-TO-MANY RELATIONSHIP QUERIES
    Query all books by a specific author using ForeignKey relationship
    """
    print("=" * 60)
    print("ONE-TO-MANY RELATIONSHIP QUERIES")
    print("=" * 60)
    
    # Use provided author_name or default
    if not author_name:
        author_name = "J.K. Rowling"
    
    # Method 1: Get author first, then access related books
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Using related_name='books'
        print(f"\nBooks by {author.name}:")
        for book in books:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")
    
    # Method 2: Direct query using the foreign key
    books_by_author = Book.objects.filter(author__name=author_name)
    print(f"\nDirect query - Books by {author_name}:")
    for book in books_by_author:
        print(f"  - {book.title}")
    
    # Method 3: Get all authors and their books
    print(f"\nAll authors and their books:")
    authors = Author.objects.all()
    for author in authors:
        books = author.books.all()
        print(f"{author.name}: {[book.title for book in books]}")


def query_books_in_library(library_name=None):
    """
    MANY-TO-MANY RELATIONSHIP QUERIES
    List all books in a library using ManyToMany relationship
    """
    print("\n" + "=" * 60)
    print("MANY-TO-MANY RELATIONSHIP QUERIES")
    print("=" * 60)
    
    # Use provided library_name or default
    if not library_name:
        library_name = "Central Library"
    
    # Method 1: Get library first, then access related books
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Using related_name='books'
        print(f"\nBooks in {library.name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
    
    # Method 2: Direct query using the many-to-many field
    books_in_library = Book.objects.filter(libraries__name=library_name)
    print(f"\nDirect query - Books in {library_name}:")
    for book in books_in_library:
        print(f"  - {book.title} by {book.author.name}")
    
    # Method 3: Get all libraries and their books
    print(f"\nAll libraries and their books:")
    libraries = Library.objects.all()
    for library in libraries:
        books = library.books.all()
        book_titles = [book.title for book in books]
        print(f"{library.name}: {book_titles}")


def query_librarian_for_library(library_name=None):
    """
    ONE-TO-ONE RELATIONSHIP QUERIES
    Retrieve the librarian for a library using OneToOne relationship
    """
    print("\n" + "=" * 60)
    print("ONE-TO-ONE RELATIONSHIP QUERIES")
    print("=" * 60)
    
    # Use provided library_name or default
    if not library_name:
        library_name = "Central Library"
    
    # Method 1: Get library first, then access related librarian
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Using related_name='librarian'
        print(f"\nLibrarian for {library.name}:")
        print(f"  - {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library_name}")
    
    # Method 2: Direct query using the one-to-one field
    try:
        librarian = Librarian.objects.get(library__name=library_name)
        print(f"\nDirect query - Librarian for {library_name}:")
        print(f"  - {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library_name}")
    
    # Method 3: Get all libraries and their librarians
    print(f"\nAll libraries and their librarians:")
    libraries = Library.objects.all()
    for library in libraries:
        try:
            librarian = library.librarian
            print(f"{library.name}: {librarian.name}")
        except Librarian.DoesNotExist:
            print(f"{library.name}: No librarian assigned")


def additional_relationship_queries():
    """
    ADDITIONAL RELATIONSHIP QUERY EXAMPLES
    Demonstrating more complex queries and reverse relationships
    """
    print("\n" + "=" * 60)
    print("ADDITIONAL RELATIONSHIP QUERY EXAMPLES")
    print("=" * 60)
    
    # Reverse relationship: Find libraries that have a specific book
    try:
        book = Book.objects.get(title="Harry Potter")
        libraries = book.libraries.all()  # Using related_name='libraries'
        print(f"\nLibraries that have '{book.title}':")
        for library in libraries:
            print(f"  - {library.name}")
    except Book.DoesNotExist:
        print("Book 'Harry Potter' not found")
    
    # Complex query: Books by authors whose names start with 'J'
    books_by_j_authors = Book.objects.filter(author__name__startswith='J')
    print(f"\nBooks by authors whose names start with 'J':")
    for book in books_by_j_authors:
        print(f"  - {book.title} by {book.author.name}")
    
    # Complex query: Libraries that have books by a specific author
    libraries_with_rowling_books = Library.objects.filter(books__author__name="J.K. Rowling")
    print(f"\nLibraries that have books by J.K. Rowling:")
    for library in libraries_with_rowling_books:
        print(f"  - {library.name}")
    
    # Count queries
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_libraries = Library.objects.count()
    total_librarians = Librarian.objects.count()
    
    print(f"\nDatabase Statistics:")
    print(f"  - Total Books: {total_books}")
    print(f"  - Total Authors: {total_authors}")
    print(f"  - Total Libraries: {total_libraries}")
    print(f"  - Total Librarians: {total_librarians}")


def create_sample_data():
    """
    Create sample data for testing the queries
    """
    print("\n" + "=" * 60)
    print("CREATING SAMPLE DATA")
    print("=" * 60)
    
    # Create authors
    author1, created = Author.objects.get_or_create(name="J.K. Rowling")
    author2, created = Author.objects.get_or_create(name="George Orwell")
    author3, created = Author.objects.get_or_create(name="Jane Austen")
    
    print(f"Created authors: {author1.name}, {author2.name}, {author3.name}")
    
    # Create books
    book1, created = Book.objects.get_or_create(title="Harry Potter", author=author1)
    book2, created = Book.objects.get_or_create(title="1984", author=author2)
    book3, created = Book.objects.get_or_create(title="Pride and Prejudice", author=author3)
    book4, created = Book.objects.get_or_create(title="Animal Farm", author=author2)
    
    print(f"Created books: {book1.title}, {book2.title}, {book3.title}, {book4.title}")
    
    # Create libraries
    library1, created = Library.objects.get_or_create(name="Central Library")
    library2, created = Library.objects.get_or_create(name="Community Library")
    
    print(f"Created libraries: {library1.name}, {library2.name}")
    
    # Add books to libraries (many-to-many relationship)
    library1.books.add(book1, book2, book3)
    library2.books.add(book2, book4)
    
    print(f"Added books to libraries")
    
    # Create librarians (one-to-one relationship)
    librarian1, created = Librarian.objects.get_or_create(name="Alice Johnson", library=library1)
    librarian2, created = Librarian.objects.get_or_create(name="Bob Smith", library=library2)
    
    print(f"Created librarians: {librarian1.name}, {librarian2.name}")


def interactive_queries():
    """
    Interactive function to demonstrate queries with user input
    """
    print("\n" + "=" * 60)
    print("INTERACTIVE QUERY EXAMPLES")
    print("=" * 60)
    
    # Example with variable library name
    library_name = "Central Library"
    print(f"\nQuerying books in library: {library_name}")
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library.name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
    
    # Example with variable author name
    author_name = "J.K. Rowling"
    print(f"\nQuerying books by author: {author_name}")
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"Books by {author.name}:")
        for book in books:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")


def main():
    """
    Main function to run all query examples
    """
    print("Django Relationship Query Examples")
    print("This script demonstrates various relationship queries")
    
    # Create sample data first
    create_sample_data()
    
    # Run all query examples
    query_books_by_author()
    query_books_in_library()
    query_librarian_for_library()
    additional_relationship_queries()
    interactive_queries()
    
    print("\n" + "=" * 60)
    print("QUERY EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
