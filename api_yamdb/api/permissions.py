from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminLevel(BasePermission):
    """Доступном администраторам, персоналу (is_staff) и суперпользователям."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and any((
            request.user.is_admin,
            request.user.is_staff,
            request.user.is_superuser
        ))


class AdminLevelOrReadOnly(BasePermission):
    """
    Просмотр не ограничен,
    редактирование/удаление доступно только
    администраторам, персоналу (is_staff) и суперпользователям.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and any((
                request.user.is_admin,
                request.user.is_staff,
                request.user.is_superuser
            ))
        )


class OwnerOrModeratorLevelOrReadOnly(BasePermission):
    """
    Просмотр не ограничен,
    редактирование/удаление доступно только
    владельцам,
    модераторам, персоналу (is_staff), администраторам, суперпользователям.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or any(
            (
                obj.author == request.user,
                request.user.is_moderator,
                request.user.is_staff,
                request.user.is_admin,
                request.user.is_superuser,
            )
        )
