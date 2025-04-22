from django.contrib import admin

from .models import Category, Genre, Review, Title


admin.site.empty_value_display = 'Не задано'
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Title)
