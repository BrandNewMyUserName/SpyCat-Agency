from django.contrib import admin
from .models import SpyCat, Mission, Target


@admin.register(SpyCat)
class SpyCatAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'years_of_experience', 'salary', 'is_available', 'created_at']
    list_filter = ['is_available', 'breed', 'created_at']
    search_fields = ['name', 'breed']
    ordering = ['name']


class TargetInline(admin.TabularInline):
    model = Target
    extra = 0


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'cat', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['cat__name']
    inlines = [TargetInline]
    ordering = ['-created_at']


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'mission', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'country', 'created_at']
    search_fields = ['name', 'country']
    ordering = ['name']

