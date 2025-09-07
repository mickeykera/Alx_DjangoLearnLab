from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library
from .models import Book
from django.views.generic.detail import DetailView
# Create your views here.

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
