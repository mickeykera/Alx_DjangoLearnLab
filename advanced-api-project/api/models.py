from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores information about authors who have written books.
    It has a one-to-many relationship with the Book model, meaning
    one author can have multiple books.
    """
    name = models.CharField(max_length=100, help_text="The name of the author")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing a book with its details.
    
    This model stores information about books and maintains a foreign key
    relationship with the Author model. Each book belongs to one author,
    but an author can have multiple books.
    """
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(help_text="The year the book was published")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="The author who wrote this book"
    )
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']