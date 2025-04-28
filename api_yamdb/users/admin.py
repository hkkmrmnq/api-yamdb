from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

User = get_user_model()

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    """Кастомизация админки пользователей."""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (None, {'fields': ('first_name', 'last_name', 'email')}),
        (
            None,
            {
                'fields': (
                    'is_active',
                    'is_superuser',
                ),
            },
        ),
        (None, {'fields': ('last_login', 'date_joined')}),
        (
            None,
            {'fields': ('role', 'bio')},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'role',
                    'bio',
                    'is_superuser',
                ),
            },
        ),
    )

    list_display = (
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
    )
