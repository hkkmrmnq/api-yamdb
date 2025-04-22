from django.contrib import admin

from .models import CustomUser, Review, Comment


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

    
admin.site.empty_value_display = 'Не задано'
admin.site.register(Review)
admin.site.register(Comment)