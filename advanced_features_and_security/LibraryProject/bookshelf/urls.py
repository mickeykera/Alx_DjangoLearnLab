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
    
    # API endpoints
    path('api/book/<int:book_id>/', views.book_api_view, name='book_api'),
    
    # User permissions view
    path('permissions/', views.user_permissions_view, name='user_permissions'),
]
