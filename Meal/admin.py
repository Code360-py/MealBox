from django.contrib import admin
from .models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_name', 'meal_id', 'created_at')
    search_fields = ('meal_name', 'user__username')
    list_filter = ('created_at',)