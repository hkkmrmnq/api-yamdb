from django.contrib import admin

from .models import Review, Comment

admin.site.empty_value_display = 'Не задано'
admin.site.register(Review)
admin.site.register(Comment)
