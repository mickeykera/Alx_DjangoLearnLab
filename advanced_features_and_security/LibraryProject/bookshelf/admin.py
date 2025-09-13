from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Book model.
    Provides enhanced display, filtering, and search capabilities.
    """
    
    # Fields to display in the list view
    list_display = ('id', 'title', 'author', 'publication_year', 'created_at')
    
    # Specify which field should be the link to detail view
    list_display_links = ('id',)
    
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
    list_editable = ('author', 'publication_year')
    
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


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser model.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

# Register the CustomUser model with the admin
admin.site.register(CustomUser, CustomUserAdmin)
