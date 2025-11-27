"""
Analytics models for tracking user behavior and trust indices.
"""
from django.db import models
from core.models import User, School


class AnalyticsEvent(models.Model):
    """Event tracking for user behavior."""
    EVENT_TYPES = [
        ('button_click', 'Нажатие кнопки'),
        ('step_completed', 'Завершение шага'),
        ('return', 'Возврат'),
        ('application_created', 'Создание заявки'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics_events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    step_name = models.CharField(max_length=100, blank=True)
    time_since_last = models.FloatField(null=True, blank=True)  # Seconds
    
    class Meta:
        verbose_name = 'Событие аналитики'
        verbose_name_plural = 'События аналитики'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.get_event_type_display()} ({self.timestamp})"


class DisciplineIndex(models.Model):
    """Student discipline index calculation."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='discipline_index')
    average_step_time = models.FloatField(default=0.0)  # Average time between steps
    return_count = models.IntegerField(default=0)
    reaction_delay = models.FloatField(default=0.0)  # Average reaction delay
    total_clicks = models.IntegerField(default=0)
    index_value = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    last_calculated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Индекс дисциплины'
        verbose_name_plural = 'Индексы дисциплины'
    
    def __str__(self):
        return f"Дисциплина {self.user}: {self.index_value}"


class TrustIndex(models.Model):
    """School trust index calculation."""
    school = models.OneToOneField(School, on_delete=models.CASCADE, related_name='trust_index_calc')
    average_response_time = models.FloatField(default=0.0)  # Hours
    confirmation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Percentage
    payment_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Percentage
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Percentage
    average_processing_delay = models.FloatField(default=0.0)  # Hours
    index_value = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    last_calculated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Индекс доверия'
        verbose_name_plural = 'Индексы доверия'
    
    def __str__(self):
        return f"Доверие {self.school.name}: {self.index_value}"

