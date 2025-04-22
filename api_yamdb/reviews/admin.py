from django.contrib import admin

from .models import Review


admin.site.empty_value_display = 'Не задано'
admin.site.register(Review)
