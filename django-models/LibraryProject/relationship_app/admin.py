# from django.contrib import admin
# from .models import Author, Book, Library, Librarian

# # Register your models here.

# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)
#     list_display_links = ('id',)

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     """
#     Custom admin configuration for the Book model.
#     """
    
#     # Fields to display in the list view
#     list_display = ('id', 'title', 'author')
    
#     # Specify which field should be the link to detail view
#     list_display_links = ('id',)
    
#     # Fields that can be used for searching
#     search_fields = ('title', 'author__name')
    
#     # Filters for the right sidebar
#     list_filter = ('author',)
    
#     # Fields that can be edited directly in the list view
#     list_editable = ('title', 'author')
    
#     # Ordering of the list
#     ordering = ('title',)

# @admin.register(Library)
# class LibraryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)
#     list_display_links = ('id',)
#     filter_horizontal = ('books',)  # Better interface for many-to-many

# @admin.register(Librarian)
# class LibrarianAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'library')
#     search_fields = ('name', 'library__name')
#     list_display_links = ('id',)
#     list_filter = ('library',)
