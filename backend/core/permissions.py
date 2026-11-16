from rest_framework import permissions


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    """Safe methods for everyone; write only for the author or a moderator."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return bool(
            user.is_authenticated
            and (obj.author_id == user.id or getattr(user, "role", None) == "moderator")
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and getattr(request.user, "role", None) == "moderator")
