from django.contrib import admin
from .models import Book

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Book model.
    Provides enhanced display, filtering, and search capabilities.
    """
    
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year', 'id', 'created_at')
    
    # Fields that can be used for searching
    search_fields = ('title', 'author')
    
    # Filters for the right sidebar
    list_filter = ('publication_year', 'author', 'created_at')
    
    # Fields to display in the detail view
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'publication_year')
        }),
        ('System Information', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Fields that are read-only
    readonly_fields = ('id', 'created_at')
    
    # Number of items to display per page
    list_per_page = 20
    
    # Enable date hierarchy navigation
    date_hierarchy = 'created_at'
    
    # Fields that can be edited directly in the list view
    list_editable = ('title', 'author', 'publication_year')
    
    # Ordering of the list
    ordering = ('-created_at', 'title')
    
    # Custom admin actions
    actions = ['mark_as_classic', 'duplicate_book']
    
    def mark_as_classic(self, request, queryset):
        """Mark selected books as classics by updating their titles."""
        updated = queryset.update(title=queryset.first().title + " (Classic)")
        self.message_user(request, f'{updated} book(s) marked as classic.')
    mark_as_classic.short_description = "Mark selected books as classics"
    
    def duplicate_book(self, request, queryset):
        """Duplicate selected books with '(Copy)' suffix."""
        for book in queryset:
            Book.objects.create(
                title=book.title + " (Copy)",
                author=book.author,
                publication_year=book.publication_year
            )
        self.message_user(request, f'{queryset.count()} book(s) duplicated.')
    duplicate_book.short_description = "Duplicate selected books"
    
    # Customize the change form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].help_text = "Enter the full title of the book"
        form.base_fields['author'].help_text = "Enter the author's full name"
        form.base_fields['publication_year'].help_text = "Enter the year the book was first published"
        return form
