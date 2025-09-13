from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Book views with permission checks
    path('', views.book_list_view, name='book_list'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('book/create/', views.book_create_view, name='book_create'),
    path('book/<int:book_id>/edit/', views.book_edit_view, name='book_edit'),
    path('book/<int:book_id>/delete/', views.book_delete_view, name='book_delete'),
    
    # Secure views demonstrating security best practices
    path('secure-search/', views.secure_search_view, name='secure_search'),
    path('secure-contact/', views.secure_contact_view, name='secure_contact'),
    path('secure-create/', views.secure_book_create_view, name='secure_book_create'),
    path('example-form/', views.example_form_view, name='example_form'),
    
    # API endpoints
    path('api/book/<int:book_id>/', views.book_api_view, name='book_api'),
    path('api/secure/book/<int:book_id>/', views.secure_api_view, name='secure_book_api'),
    
    # User permissions view
    path('permissions/', views.user_permissions_view, name='user_permissions'),
]
