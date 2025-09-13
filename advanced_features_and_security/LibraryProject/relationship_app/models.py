from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# Create your models here.

class Author(models.Model):
    """
    Author model representing book authors.
    Has a one-to-many relationship with Book.
    """
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    """
    Book model representing individual books.
    Has a many-to-one relationship with Author (ForeignKey).
    Has a many-to-many relationship with Library.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        unique_together = ['title', 'author']
        permissions = (
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        )


class Library(models.Model):
    """
    Library model representing libraries.
    Has a many-to-many relationship with Book.
    Has a one-to-one relationship with Librarian.
    """
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    books = models.ManyToManyField(Book, related_name='libraries', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'


class Librarian(models.Model):
    """
    Librarian model representing library staff.
    Has a one-to-one relationship with Library.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (Librarian at {self.library.name})"
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Librarian'
        verbose_name_plural = 'Librarians'


class UserProfile(models.Model):
    ROLE_ADMIN = "Admin"
    ROLE_LIBRARIAN = "Librarian"
    ROLE_MEMBER = "Member"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_LIBRARIAN, "Librarian"),
        (ROLE_MEMBER, "Member"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure profile always exists
    if hasattr(instance, "profile"):
        instance.profile.save()
    else:
        UserProfile.objects.get_or_create(user=instance)