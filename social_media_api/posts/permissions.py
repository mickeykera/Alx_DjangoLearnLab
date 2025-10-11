from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow safe methods for anyone, write methods only to the author."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the author
        return getattr(obj, "author", None) == request.user
