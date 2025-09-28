# Advanced API Project with Django REST Framework

This project demonstrates advanced API development using Django REST Framework with custom serializers, generic views, and proper permission handling.

## Project Overview

The project implements a book and author management system with the following features:
- **Models**: Author and Book with one-to-many relationship
- **Serializers**: Custom serializers with nested relationships and validation
- **Views**: Generic views for CRUD operations with permission controls
- **API Endpoints**: RESTful API with proper HTTP methods and status codes

## Models

### Author Model
```python
class Author(models.Model):
    name = models.CharField(max_length=100)
```

### Book Model
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

## Serializers

### BookSerializer
- Serializes all Book model fields
- **Custom Validation**: Ensures `publication_year` is not in the future
- Handles foreign key relationship with Author

### AuthorSerializer
- Includes author name field
- **Nested BookSerializer**: Automatically serializes all related books
- Handles one-to-many relationship between Author and Book

## API Endpoints

### Base URL
All API endpoints are prefixed with `/api/`

### Book Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/books/` | List all books | Not required |
| POST | `/api/books/` | Create new book | Required |
| GET | `/api/books/<id>/` | Get specific book | Not required |
| PUT | `/api/books/<id>/` | Update book (full) | Required |
| PATCH | `/api/books/<id>/` | Update book (partial) | Required |
| DELETE | `/api/books/<id>/` | Delete book | Required |

### Author Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/authors/` | List all authors with books | Not required |
| POST | `/api/authors/` | Create new author | Required |
| GET | `/api/authors/<id>/` | Get specific author with books | Not required |
| PUT | `/api/authors/<id>/` | Update author (full) | Required |
| PATCH | `/api/authors/<id>/` | Update author (partial) | Required |
| DELETE | `/api/authors/<id>/` | Delete author | Required |

### API Root
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/` | API root with endpoint links | Not required |

## Views Implementation

### Generic Views Used

1. **ListCreateAPIView**: For listing and creating resources
2. **RetrieveUpdateDestroyAPIView**: For retrieving, updating, and deleting specific resources

### Custom View Features

#### Permission Handling
- **Read Operations (GET)**: Available to everyone (`AllowAny`)
- **Write Operations (POST, PUT, PATCH, DELETE)**: Require authentication (`IsAuthenticated`)

#### Custom Methods
- `get_permissions()`: Dynamic permission assignment based on HTTP method
- `perform_update()`: Custom update logic with additional validation
- `perform_destroy()`: Custom delete logic with logging capabilities

## URL Configuration

### Main Project URLs (`advanced_api_project/urls.py`)
```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
```

### API URLs (`api/urls.py`)
```python
urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]
```

## Data Validation

### BookSerializer Validation
- **Publication Year**: Cannot be in the future
- **Required Fields**: title, publication_year, author
- **Author Relationship**: Must reference existing author

### Error Handling
- Custom validation error messages
- Proper HTTP status codes (400 for validation errors)
- Detailed error responses with field-specific messages

## Usage Examples

### Creating a Book
```bash
POST /api/books/
Content-Type: application/json

{
    "title": "The Great Gatsby",
    "publication_year": 1925,
    "author": 1
}
```

### Creating an Author
```bash
POST /api/authors/
Content-Type: application/json

{
    "name": "F. Scott Fitzgerald"
}
```

### Retrieving Author with Books
```bash
GET /api/authors/1/
```

Response:
```json
{
    "id": 1,
    "name": "F. Scott Fitzgerald",
    "books": [
        {
            "id": 1,
            "title": "The Great Gatsby",
            "publication_year": 1925,
            "author": 1
        }
    ]
}
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install django djangorestframework
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser (for authentication)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access API**
   - API Root: http://localhost:8000/api/
   - Books: http://localhost:8000/api/books/
   - Authors: http://localhost:8000/api/authors/

## Testing the API

### Using curl

1. **List all books** (no authentication required):
   ```bash
   curl http://localhost:8000/api/books/
   ```

2. **Create a book** (authentication required):
   ```bash
   curl -X POST http://localhost:8000/api/books/ \
        -H "Content-Type: application/json" \
        -u username:password \
        -d '{"title": "Test Book", "publication_year": 2023, "author": 1}'
   ```

3. **Get specific author with books**:
   ```bash
   curl http://localhost:8000/api/authors/1/
   ```

### Using Django Admin
- Access: http://localhost:8000/admin/
- Create authors and books through the admin interface
- Test the API endpoints with the created data

## Key Features

1. **Nested Serialization**: Authors include their books automatically
2. **Custom Validation**: Business logic validation for publication years
3. **Permission Control**: Read access for all, write access for authenticated users
4. **RESTful Design**: Proper HTTP methods and status codes
5. **Generic Views**: Efficient CRUD operations with minimal code
6. **Comprehensive Documentation**: Clear API documentation and examples

## Architecture Benefits

- **Scalable**: Generic views handle common patterns efficiently
- **Secure**: Proper permission controls and authentication
- **Maintainable**: Clear separation of concerns and well-documented code
- **Extensible**: Easy to add new features and customizations
- **Standards Compliant**: Follows REST API best practices
