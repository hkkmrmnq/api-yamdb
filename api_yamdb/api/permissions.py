from rest_framework.permissions import BasePermission, SAFE_METHODS


class ModeratorLevel(BasePermission):
    """Доступно модераторам, администраторам и суперпользователям."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role in ('moderator', 'admin')
            or request.user.is_superuser
        )


class AdminLevel(BasePermission):
    """Доступном администраторам и суперпользователям."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )


class AdminLevelOrReadOnly(BasePermission):
    """
    Просмотр не ограничен,
    редактирование/удаление доступно только
    администраторам и суперпользователям.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )


class OwnerOrModeratorLevelOrReadOnly(BasePermission):
    """
    Просмотр не ограничен,
    редактирование/удаление доступно только
    модкраторам, администраторам, суперпользователям и владельцам.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or any(
            (
                obj.author == request.user,
                request.user.role in ('admin', 'moderator'),
                request.user.is_superuser,
            )
        )
