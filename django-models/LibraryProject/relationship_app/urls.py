# relationship_app/urls.py
from django.urls import path
from .views import LibraryDetailView, book_list_text

urlpatterns = [
    # Function-based view: plain text list of all books
    path("books.txt", book_list_text, name="book_list_text"),

    # Class-based view: details for a specific library and its books
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
]
