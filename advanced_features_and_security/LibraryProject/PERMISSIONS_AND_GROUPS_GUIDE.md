# Django Permissions and Groups Implementation Guide

This document explains the implementation of a comprehensive permissions and groups system in the Django Library Management System.

## Overview

The system implements role-based access control (RBAC) using Django's built-in permissions and groups functionality. Users are assigned to groups, and groups have specific permissions that control what actions users can perform.

## Architecture

### 1. Custom Permissions

Custom permissions are defined in model Meta classes using the `permissions` attribute:

```python
class Meta:
    permissions = (
        ("can_view", "Can view book details"),
        ("can_create", "Can create new books"),
        ("can_edit", "Can edit existing books"),
        ("can_delete", "Can delete books"),
    )
```

**Models with Custom Permissions:**
- `Book` (bookshelf app)
- `Author` (relationship_app)
- `Library` (relationship_app)

### 2. User Groups

Three main groups are created with different permission levels:

#### Viewers Group
- **Purpose**: Read-only access to the system
- **Permissions**:
  - `can_view` on all models
  - `view_*` permissions on all models
- **Use Case**: Users who need to browse and view content but cannot modify anything

#### Editors Group
- **Purpose**: Content management without deletion rights
- **Permissions**:
  - All Viewer permissions
  - `can_create` and `can_edit` on all models
  - `add_*` and `change_*` permissions on all models
- **Use Case**: Content creators and editors who can add and modify content

#### Admins Group
- **Purpose**: Full system access including deletion
- **Permissions**:
  - All Editor permissions
  - `can_delete` on all models
  - `delete_*` permissions on all models
- **Use Case**: System administrators with full control

## Implementation Details

### 1. Model Permissions

Custom permissions are defined in the following models:

**bookshelf/models.py:**
```python
class Book(models.Model):
    # ... fields ...
    
    class Meta:
        permissions = (
            ("can_view", "Can view book details"),
            ("can_create", "Can create new books"),
            ("can_edit", "Can edit existing books"),
            ("can_delete", "Can delete books"),
        )
```

**relationship_app/models.py:**
```python
class Author(models.Model):
    # ... fields ...
    
    class Meta:
        permissions = (
            ("can_view", "Can view author details"),
            ("can_create", "Can create new authors"),
            ("can_edit", "Can edit existing authors"),
            ("can_delete", "Can delete authors"),
        )

class Library(models.Model):
    # ... fields ...
    
    class Meta:
        permissions = (
            ("can_view", "Can view library details"),
            ("can_create", "Can create new libraries"),
            ("can_edit", "Can edit existing libraries"),
            ("can_delete", "Can delete libraries"),
        )
```

### 2. Permission Enforcement in Views

Views use Django's `@permission_required` decorator to enforce permissions:

```python
from django.contrib.auth.decorators import permission_required

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list_view(request):
    """View to list all books. Requires can_view permission."""
    # ... view logic ...

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create_view(request):
    """View to create a new book. Requires can_create permission."""
    # ... view logic ...

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit_view(request, book_id):
    """View to edit an existing book. Requires can_edit permission."""
    # ... view logic ...

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete_view(request, book_id):
    """View to delete a book. Requires can_delete permission."""
    # ... view logic ...
```

### 3. Template Permission Checks

Templates check user permissions to show/hide UI elements:

```html
{% if can_create %}
    <a href="{% url 'bookshelf:book_create' %}" class="btn btn-success">Add New Book</a>
{% endif %}

{% if can_edit %}
    <a href="{% url 'bookshelf:book_edit' book.id %}" class="btn">Edit</a>
{% endif %}

{% if can_delete %}
    <a href="{% url 'bookshelf:book_delete' book.id %}" class="btn btn-danger">Delete</a>
{% endif %}
```

### 4. Management Commands

Two management commands are provided for setup and testing:

#### setup_groups.py
Creates the three user groups and assigns appropriate permissions:
```bash
python manage.py setup_groups
```

#### create_test_users.py
Creates test users for each group:
```bash
python manage.py create_test_users
```

## Setup Instructions

### 1. Initial Setup

1. **Run migrations** to create custom permissions:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create groups and assign permissions**:
   ```bash
   python manage.py setup_groups
   ```

3. **Create test users** (optional):
   ```bash
   python manage.py create_test_users
   ```

4. **Create sample data** (optional):
   ```bash
   python manage.py create_sample_books
   ```

### 2. Testing the System

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Test with different users**:
   - Go to `/admin/` and log in with different test users
   - Visit `/bookshelf/` to test the permission-protected views
   - Check `/bookshelf/permissions/` to see user's permissions

### 3. Test Users

The following test users are created:

| Username | Password | Group | Permissions |
|----------|----------|-------|-------------|
| `viewer_user` | `viewer123` | Viewers | View only |
| `editor_user` | `editor123` | Editors | View, Create, Edit |
| `admin_user` | `admin123` | Admins | All permissions |
| `no_permissions_user` | `noperms123` | None | No permissions |

## URL Structure

The bookshelf app provides the following permission-protected URLs:

- `/bookshelf/` - Book list (requires `can_view`)
- `/bookshelf/book/<id>/` - Book detail (requires `can_view`)
- `/bookshelf/book/create/` - Create book (requires `can_create`)
- `/bookshelf/book/<id>/edit/` - Edit book (requires `can_edit`)
- `/bookshelf/book/<id>/delete/` - Delete book (requires `can_delete`)
- `/bookshelf/permissions/` - User permissions view
- `/bookshelf/api/book/<id>/` - API endpoint (requires `can_view`)

## Permission Checking Methods

### 1. View Decorators
```python
@permission_required('app_name.permission_name', raise_exception=True)
def my_view(request):
    # View code
```

### 2. Template Checks
```html
{% if user.has_perm('app_name.permission_name') %}
    <!-- Permission-specific content -->
{% endif %}
```

### 3. Programmatic Checks
```python
if request.user.has_perm('bookshelf.can_edit'):
    # Allow editing
else:
    # Deny access
```

## Security Considerations

1. **Always use `raise_exception=True`** in permission decorators to return 403 Forbidden instead of redirecting to login
2. **Check permissions in templates** to provide appropriate UI feedback
3. **Validate permissions in views** even if they're checked in templates
4. **Use HTTPS in production** to protect authentication and session data
5. **Regularly audit group memberships** to ensure proper access control

## Extending the System

### Adding New Permissions

1. **Add to model Meta class**:
   ```python
   class Meta:
       permissions = (
           ("can_export", "Can export data"),
           ("can_import", "Can import data"),
       )
   ```

2. **Create and run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Update groups** (manually in admin or via management command)

4. **Add permission checks to views**:
   ```python
   @permission_required('app_name.can_export', raise_exception=True)
   def export_view(request):
       # Export logic
   ```

### Adding New Groups

1. **Create group in Django admin** or via management command
2. **Assign appropriate permissions**
3. **Update documentation**

## Troubleshooting

### Common Issues

1. **Permission not found**: Ensure migrations have been run after adding new permissions
2. **User can't access view**: Check group membership and permission assignments
3. **Template not showing buttons**: Verify permission checks in template context

### Debugging

1. **Check user permissions**:
   ```python
   user.get_all_permissions()
   user.get_group_permissions()
   ```

2. **Check group memberships**:
   ```python
   user.groups.all()
   ```

3. **Use Django admin** to inspect groups and permissions

## Best Practices

1. **Use descriptive permission names** that clearly indicate the action
2. **Group related permissions** logically in model Meta classes
3. **Test permission enforcement** with different user types
4. **Document permission requirements** for each view
5. **Regularly review and audit** group memberships and permissions
6. **Use the principle of least privilege** - give users only the permissions they need

This implementation provides a robust foundation for role-based access control in Django applications while maintaining security and usability.
