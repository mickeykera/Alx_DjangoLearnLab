# relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import LibraryDetailView

urlpatterns = [
    # Existing app views
    path("books.txt", views.book_list_text, name="book_list_text"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Auth views
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),
]
