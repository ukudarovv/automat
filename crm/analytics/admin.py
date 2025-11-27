"""
Admin for analytics models.
"""
from django.contrib import admin
from .models import AnalyticsEvent, DisciplineIndex, TrustIndex


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_type', 'step_name', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['user__username', 'step_name']
    readonly_fields = ['timestamp']


@admin.register(DisciplineIndex)
class DisciplineIndexAdmin(admin.ModelAdmin):
    list_display = ['user', 'index_value', 'average_step_time', 'return_count', 'last_calculated']
    list_filter = ['last_calculated']
    search_fields = ['user__username']
    readonly_fields = ['last_calculated']


@admin.register(TrustIndex)
class TrustIndexAdmin(admin.ModelAdmin):
    list_display = ['school', 'index_value', 'confirmation_rate', 'payment_rate', 'last_calculated']
    list_filter = ['last_calculated']
    search_fields = ['school__name']
    readonly_fields = ['last_calculated']

