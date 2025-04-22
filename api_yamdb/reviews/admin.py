from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('role',)
    empty_value_display = '-пусто-'
