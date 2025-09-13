from django.core.management.base import BaseCommand
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create sample books for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample books...')
        
        # Delete existing books
        Book.objects.all().delete()
        
        sample_books = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'publication_year': 1925
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'publication_year': 1960
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'publication_year': 1949
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'publication_year': 1813
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'publication_year': 1951
            }
        ]
        
        for book_data in sample_books:
            book = Book.objects.create(**book_data)
            self.stdout.write(f'Created: {book.title} by {book.author}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(sample_books)} sample books!'))
