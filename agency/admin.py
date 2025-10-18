from django.contrib import admin
from .models import SpyCat


@admin.register(SpyCat)
class SpyCatAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'years_of_experience', 'salary', 'is_available', 'created_at']
    list_filter = ['is_available', 'breed', 'created_at']
    search_fields = ['name', 'breed']
    ordering = ['name']


