# relationship_app/urls.py
from django.urls import path
from .views import (
    LibraryDetailView,
    book_list_text,
    UserLoginView,
    UserLogoutView,
    register,
)

urlpatterns = [
    path("books.txt", book_list_text, name="book_list_text"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Auth
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
]
