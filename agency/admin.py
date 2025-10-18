from django.contrib import admin
from .models import SpyCat, Mission


@admin.register(SpyCat)
class SpyCatAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'years_of_experience', 'salary', 'is_available', 'created_at']
    list_filter = ['is_available', 'breed', 'created_at']
    search_fields = ['name', 'breed']
    ordering = ['name']


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'cat', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['cat__name']
    ordering = ['-created_at']

