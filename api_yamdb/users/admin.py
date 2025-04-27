from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

User = get_user_model()

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('role',)
