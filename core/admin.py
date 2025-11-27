"""
Django admin configuration for core models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, City, School, Instructor, Application


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'city', 'phone', 'telegram_id']
    list_filter = ['role', 'is_active', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'phone', 'city', 'telegram_id')}),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ru', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'name_ru']


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'rating', 'trust_index', 'is_active']
    list_filter = ['city', 'is_active']
    search_fields = ['name', 'city__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'auto_type', 'rating', 'is_active']
    list_filter = ['city', 'auto_type', 'is_active']
    search_fields = ['name', 'city__name']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'student_phone', 'city', 'status', 'created_at']
    list_filter = ['status', 'city', 'category', 'format', 'created_at']
    search_fields = ['student_name', 'student_phone']
    readonly_fields = ['created_at', 'updated_at', 'status_changed_at']

