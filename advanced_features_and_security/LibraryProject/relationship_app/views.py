from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django import forms
from .models import Book, Library, UserProfile
from django.contrib.auth.decorators import permission_required
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "publication_date", "pages", "description"]

def book_list_text(request):
    books = Book.objects.all().select_related('author').order_by('title')
    return render(request, "relationship_app/list_books.html", {"books": books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["books"] = self.object.books.all().select_related("author").order_by("title")
        return ctx

class UserLoginView(LoginView):
    template_name = "relationship_app/login.html"

class UserLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("book_list_text")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

def _has_role(user, role):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == role

@login_required
@user_passes_test(lambda u: _has_role(u, UserProfile.ROLE_ADMIN))
def admin_view(request):
    return render(request, "relationship_app/admin_view.html", {"role": "Admin"})

@login_required
@user_passes_test(lambda u: _has_role(u, UserProfile.ROLE_LIBRARIAN))
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html", {"role": "Librarian"})

@login_required
@user_passes_test(lambda u: _has_role(u, UserProfile.ROLE_MEMBER))
def member_view(request):
    return render(request, "relationship_app/member_view.html", {"role": "Member"})

@login_required
@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list_text")
    else:
        form = BookForm()
    return render(request, "relationship_app/book_form.html", {"form": form, "action": "Add"})

@login_required
@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list_text")
    else:
        form = BookForm(instance=book)
    return render(request, "relationship_app/book_form.html", {"form": form, "action": "Edit"})

@login_required
@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list_text")
    return render(request, "relationship_app/book_confirm_delete.html", {"book": book})
