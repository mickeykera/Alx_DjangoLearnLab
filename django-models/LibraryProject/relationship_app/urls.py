# relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import LibraryDetailView

urlpatterns = [
    path("books.txt", views.book_list_text, name="book_list_text"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Auth
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),

    # Role-based views
    path("role/admin/", views.admin_view, name="admin_view"),
    path("role/librarian/", views.librarian_view, name="librarian_view"),
    path("role/member/", views.member_view, name="member_view"),
]
