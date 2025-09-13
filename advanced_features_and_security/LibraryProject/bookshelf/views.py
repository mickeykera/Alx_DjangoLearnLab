from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.html import escape
import logging
from .models import Book
from .forms import BookForm, SecureSearchForm, ContactForm, ExampleForm
from .forms import ExampleForm
# Security: Set up logging for security events
logger = logging.getLogger('django.security')


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


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect
def secure_search_view(request):
    """
    Secure search view that demonstrates proper input validation and SQL injection prevention.
    Uses Django ORM with parameterized queries to prevent SQL injection.
    """
    books = Book.objects.none()  # Empty queryset by default
    search_query = ''
    search_type = 'both'
    
    if request.method == 'GET':
        # Security: Validate and sanitize input parameters
        search_query = request.GET.get('search_query', '').strip()
        search_type = request.GET.get('search_type', 'both')
        
        # Security: Input validation
        if search_query:
            # Security: Limit search query length to prevent DoS
            if len(search_query) > 100:
                messages.error(request, 'Search query is too long. Maximum 100 characters allowed.')
                logger.warning(f'Long search query attempted by user {request.user.username}: {len(search_query)} characters')
            else:
                # Security: Use Django ORM with parameterized queries to prevent SQL injection
                # This is safe because Django ORM automatically escapes parameters
                if search_type == 'title':
                    books = Book.objects.filter(title__icontains=search_query)
                elif search_type == 'author':
                    books = Book.objects.filter(author__icontains=search_query)
                elif search_type == 'both':
                    # Security: Use Q objects for complex queries (still parameterized)
                    books = Book.objects.filter(
                        Q(title__icontains=search_query) | Q(author__icontains=search_query)
                    )
                else:
                    # Security: Invalid search type - default to both
                    search_type = 'both'
                    books = Book.objects.filter(
                        Q(title__icontains=search_query) | Q(author__icontains=search_query)
                    )
                
                # Security: Limit results to prevent DoS
                books = books[:50]  # Limit to 50 results
                
                # Security: Log search activity
                logger.info(f'User {request.user.username} searched for "{search_query}" (type: {search_type}), found {books.count()} results')
    
    context = {
        'books': books,
        'search_query': escape(search_query),  # Security: Escape output to prevent XSS
        'search_type': escape(search_type),
        'user': request.user,
    }
    return render(request, 'bookshelf/secure_search.html', context)


@login_required
@csrf_protect
@require_http_methods(["POST"])
def secure_contact_view(request):
    """
    Secure contact form view that demonstrates proper form validation and CSRF protection.
    """
    if request.method == 'POST':
        # Security: Use Django form for validation and CSRF protection
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Security: Get cleaned data from form (already validated and sanitized)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Security: Log contact form submission
            logger.info(f'Contact form submitted by {request.user.username}: {name} ({email})')
            
            # Security: In a real application, you would send an email here
            # For demonstration, we'll just show a success message
            messages.success(request, f'Thank you {name}! Your message has been received.')
            
            # Security: Redirect to prevent duplicate submissions
            return redirect('bookshelf:secure_search')
        else:
            # Security: Log form validation errors
            logger.warning(f'Contact form validation failed for user {request.user.username}: {form.errors}')
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    # Security: If not POST, redirect to search page
    return redirect('bookshelf:secure_search')


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def secure_api_view(request, book_id):
    """
    Secure API endpoint that demonstrates proper input validation and output sanitization.
    """
    try:
        # Security: Validate book_id parameter
        book_id = int(book_id)
        if book_id <= 0:
            raise ValueError("Invalid book ID")
    except (ValueError, TypeError):
        # Security: Log invalid API requests
        logger.warning(f'Invalid API request from user {request.user.username}: book_id={book_id}')
        return HttpResponseBadRequest("Invalid book ID")
    
    # Security: Use get_object_or_404 to safely retrieve object
    book = get_object_or_404(Book, id=book_id)
    
    # Security: Log API access
    logger.info(f'API access by user {request.user.username} for book {book_id}')
    
    # Security: Return sanitized data
    data = {
        'id': book.id,
        'title': escape(book.title),  # Security: Escape to prevent XSS
        'author': escape(book.author),  # Security: Escape to prevent XSS
        'publication_year': book.publication_year,
        'created_at': book.created_at.isoformat(),
    }
    
    return JsonResponse(data)


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
def secure_book_create_view(request):
    """
    Enhanced secure book creation view with additional validation.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Security: Additional server-side validation
            book = form.save(commit=False)
            
            # Security: Validate publication year
            if book.publication_year and (book.publication_year < 1000 or book.publication_year > 2100):
                form.add_error('publication_year', 'Publication year must be between 1000 and 2100.')
                messages.error(request, 'Invalid publication year.')
            else:
                book.save()
                
                # Security: Log book creation
                logger.info(f'Book created by user {request.user.username}: "{book.title}" by {book.author}')
                
                messages.success(request, f'Book "{book.title}" created successfully!')
                return redirect('bookshelf:book_detail', book_id=book.id)
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'title': 'Create New Book (Secure)',
        'action': 'create'
    }
    return render(request, 'bookshelf/book_form.html', context)


@login_required
@csrf_protect
def example_form_view(request):
    """
    Example form view demonstrating security best practices.
    Shows proper form handling, validation, and security measures.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        
        if form.is_valid():
            # Security: Get cleaned data from form (already validated and sanitized)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            age = form.cleaned_data['age']
            bio = form.cleaned_data.get('bio', '')
            newsletter = form.cleaned_data.get('newsletter', False)
            
            # Security: Log form submission
            logger.info(f'Example form submitted by {request.user.username}: {name} ({email}), age: {age}')
            
            # Security: In a real application, you would save this data to the database
            # For demonstration, we'll just show a success message
            messages.success(request, f'Thank you {name}! Your information has been received successfully.')
            
            # Security: Redirect to prevent duplicate submissions
            return redirect('bookshelf:example_form')
        else:
            # Security: Log form validation errors
            logger.warning(f'Example form validation failed for user {request.user.username}: {form.errors}')
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExampleForm()
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'bookshelf/form_example.html', context)