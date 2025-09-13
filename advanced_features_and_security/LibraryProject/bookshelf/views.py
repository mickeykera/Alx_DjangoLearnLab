from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from .models import Book
from .forms import BookForm


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list_view(request):
    """
    View to list all books. Requires can_view permission.
    """
    books = Book.objects.all()
    context = {
        'books': books,
        'user': request.user,
        'can_create': request.user.has_perm('bookshelf.can_create'),
        'can_edit': request.user.has_perm('bookshelf.can_edit'),
        'can_delete': request.user.has_perm('bookshelf.can_delete'),
    }
    return render(request, 'bookshelf/book_list.html', context)


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail_view(request, book_id):
    """
    View to display book details. Requires can_view permission.
    """
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
        'user': request.user,
        'can_edit': request.user.has_perm('bookshelf.can_edit'),
        'can_delete': request.user.has_perm('bookshelf.can_delete'),
    }
    return render(request, 'bookshelf/book_detail.html', context)


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create_view(request):
    """
    View to create a new book. Requires can_create permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'title': 'Create New Book',
        'action': 'create'
    }
    return render(request, 'bookshelf/book_form.html', context)


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit_view(request, book_id):
    """
    View to edit an existing book. Requires can_edit permission.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'title': f'Edit {book.title}',
        'action': 'edit'
    }
    return render(request, 'bookshelf/book_form.html', context)


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete_view(request, book_id):
    """
    View to delete a book. Requires can_delete permission.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    context = {
        'book': book,
        'title': f'Delete {book.title}'
    }
    return render(request, 'bookshelf/book_confirm_delete.html', context)


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_api_view(request, book_id):
    """
    API endpoint to get book details. Requires can_view permission.
    """
    book = get_object_or_404(Book, id=book_id)
    
    data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'publication_year': book.publication_year,
        'created_at': book.created_at.isoformat(),
    }
    
    return JsonResponse(data)


@login_required
def user_permissions_view(request):
    """
    View to display user's permissions and group memberships.
    """
    user = request.user
    groups = user.groups.all()
    permissions = user.get_all_permissions()
    
    # Filter permissions by our custom permissions
    custom_permissions = [perm for perm in permissions if 'can_' in perm]
    
    context = {
        'user': user,
        'groups': groups,
        'permissions': permissions,
        'custom_permissions': custom_permissions,
    }
    return render(request, 'bookshelf/user_permissions.html', context)