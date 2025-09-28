from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
class BookListView(generics.ListCreateAPIView):
    """
    Generic view for listing all books and creating new books.
    
    GET /books/ - Retrieve all books
    POST /books/ - Create a new book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow read access to everyone
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "publication_year", "author"]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_year", "id"]
    ordering = ["title"]
    
    def get_permissions(self):
        """
        Customize permissions based on the HTTP method.
        Allow read access to everyone, but require authentication for creation.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view for retrieving, updating, or deleting a specific book.
    
    GET /books/<id>/ - Retrieve a specific book
    PUT /books/<id>/ - Update a specific book (requires authentication)
    PATCH /books/<id>/ - Partially update a specific book (requires authentication)
    DELETE /books/<id>/ - Delete a specific book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Customize permissions based on the HTTP method.
        Allow read access to everyone, but require authentication for modifications.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_update(self, serializer):
        """
        Custom update logic to add additional validation or logging.
        """
        # Add any custom update logic here
        serializer.save()
    
    def perform_destroy(self, instance):
        """
        Custom delete logic to add logging or additional checks.
        """
        # Add any custom delete logic here
        instance.delete()


# Explicit single-responsibility generic views for Book CRUD operations
class BookCreateView(generics.CreateAPIView):
    """
    CreateView dedicated to creating a new book.
    
    POST /books/create/ - Create a new book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        # Write operation requires authentication
        return [IsAuthenticated()]


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView dedicated to updating an existing book.
    
    PUT/PATCH /books/<id>/update/ - Update a book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        # Write operation requires authentication
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView dedicated to deleting an existing book.
    
    DELETE /books/<id>/delete/ - Delete a book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        # Write operation requires authentication
        return [IsAuthenticated()]


class AuthorListView(generics.ListCreateAPIView):
    """
    Generic view for listing all authors and creating new authors.
    
    GET /authors/ - Retrieve all authors with their books
    POST /authors/ - Create a new author (requires authentication)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]  # Allow read access to everyone
    
    def get_permissions(self):
        """
        Customize permissions based on the HTTP method.
        Allow read access to everyone, but require authentication for creation.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view for retrieving, updating, or deleting a specific author.
    
    GET /authors/<id>/ - Retrieve a specific author with their books
    PUT /authors/<id>/ - Update a specific author (requires authentication)
    PATCH /authors/<id>/ - Partially update a specific author (requires authentication)
    DELETE /authors/<id>/ - Delete a specific author (requires authentication)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        """
        Customize permissions based on the HTTP method.
        Allow read access to everyone, but require authentication for modifications.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root endpoint that provides links to all available endpoints.
    
    GET / - List all available API endpoints
    """
    return Response({
        'books': {
            'list': request.build_absolute_uri('/books/'),
            'create': request.build_absolute_uri('/books/'),
        },
        'authors': {
            'list': request.build_absolute_uri('/authors/'),
            'create': request.build_absolute_uri('/authors/'),
        },
        'documentation': 'This API provides CRUD operations for Books and Authors with nested relationships.'
    })
