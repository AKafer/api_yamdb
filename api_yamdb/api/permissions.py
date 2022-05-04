from rest_framework import permissions


class NobodyAllow(permissions.BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsAdmin(permissions.BasePermission):
    """Класс разрешений для админа."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin' or request.user.is_superuser)
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role == 'admin' or request.user.is_superuser)
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс разрешений для админа или для всех пользователей на чтение."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс разрешений для владельца контента, модератора, админа или
    для всех пользователей на чтение.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role in ['moderator', 'admin']
                or request.method in permissions.SAFE_METHODS
                or obj.author == request.user
            )
        return request.method in permissions.SAFE_METHODS
