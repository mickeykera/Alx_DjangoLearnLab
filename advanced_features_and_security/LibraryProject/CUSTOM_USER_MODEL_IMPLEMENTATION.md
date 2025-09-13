# Custom User Model Implementation

This document outlines the implementation of a custom user model in Django that extends the built-in `AbstractUser` class with additional fields and functionality.

## Overview

The custom user model (`CustomUser`) extends Django's `AbstractUser` to include:
- `date_of_birth`: A date field for storing user's birth date
- `profile_photo`: An image field for storing user's profile picture

## Files Modified/Created

### 1. Custom User Model (`accounts/models.py`)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds additional fields: date_of_birth and profile_photo.
    """
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        help_text="User's date of birth"
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text="User's profile photo"
    )
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
```

### 2. Custom User Manager (`accounts/managers.py`)

```python
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager for CustomUser model.
    """
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a regular user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a superuser with the given username, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)
```

### 3. Admin Configuration (`accounts/admin.py`)

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser model.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
```

### 4. Settings Configuration (`LibraryProject/settings.py`)

```python
# Add accounts app to INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",  # Added
    "bookshelf",
    "relationship_app",
]

# Set custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 5. Forms (`accounts/forms.py`)

Custom forms for user registration and profile updates that include the additional fields.

### 6. Views (`accounts/views.py`)

Views for user registration, profile management, and API endpoints.

## Key Features

### 1. Extended User Fields
- **date_of_birth**: Optional date field for storing user's birth date
- **profile_photo**: Optional image field for storing user's profile picture

### 2. Custom Manager
- Handles user creation with additional fields
- Maintains compatibility with Django's authentication system
- Supports both regular users and superusers

### 3. Admin Integration
- Custom admin interface for managing users
- Displays additional fields in list view
- Includes additional fields in add/edit forms
- Proper filtering and search capabilities

### 4. Media File Handling
- Configured to serve uploaded images during development
- Images are stored in `media/profile_photos/` directory

## Usage Examples

### Creating a User

```python
from accounts.models import CustomUser
from datetime import date

# Create a regular user
user = CustomUser.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password',
    first_name='John',
    last_name='Doe',
    date_of_birth=date(1990, 5, 15)
)

# Create a superuser
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin_password',
    first_name='Admin',
    last_name='User',
    date_of_birth=date(1985, 1, 1)
)
```

### Accessing Custom Fields

```python
# Access custom fields
print(user.date_of_birth)  # 1990-05-15
print(user.profile_photo)  # profile_photos/photo.jpg

# Update custom fields
user.date_of_birth = date(1991, 6, 20)
user.profile_photo = 'new_photo.jpg'
user.save()
```

## Migration Process

1. **Create migrations**: `python manage.py makemigrations accounts`
2. **Apply migrations**: `python manage.py migrate`
3. **Create superuser**: `python manage.py createsuperuser`

## Testing

Run the test script to verify the custom user model:

```bash
python test_custom_user.py
```

## Admin Interface

Access the Django admin at `/admin/` to:
- View all users with custom fields
- Add new users with additional fields
- Edit existing users
- Filter and search users

## API Endpoints

- `GET /accounts/api/user/<user_id>/` - Get user details including custom fields
- `GET /accounts/users/` - List all users
- `GET /accounts/profile/` - User profile management

## Benefits

1. **Extensibility**: Easy to add more custom fields as needed
2. **Compatibility**: Maintains full compatibility with Django's authentication system
3. **Admin Integration**: Seamless integration with Django admin
4. **Flexibility**: Supports both optional and required custom fields
5. **Media Handling**: Proper handling of file uploads

## Security Considerations

1. **File Uploads**: Profile photos are stored securely in the media directory
2. **Validation**: Forms include proper validation for all fields
3. **Permissions**: Maintains Django's built-in permission system
4. **Authentication**: Full compatibility with Django's authentication framework

This implementation provides a solid foundation for applications requiring extended user information while maintaining Django's security and functionality standards.
