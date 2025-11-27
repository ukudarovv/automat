"""
Core models for AvtoMat project.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Extended user model with role support."""
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('school', 'Автошкола'),
        ('instructor', 'Инструктор'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    telegram_id = models.BigIntegerField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class City(models.Model):
    """Cities in Kazakhstan."""
    name = models.CharField(max_length=100, unique=True)
    name_ru = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']
    
    def __str__(self):
        return self.name_ru or self.name


class School(models.Model):
    """Driving school model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='school_profile')
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='schools')
    address = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    trust_index = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    whatsapp = models.CharField(max_length=20, blank=True)
    telegram_contact = models.CharField(max_length=100, blank=True)
    payment_link_kaspi = models.URLField(blank=True)
    payment_link_halyk = models.URLField(blank=True)
    nearest_intake = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Автошкола'
        verbose_name_plural = 'Автошколы'
        ordering = ['-rating', '-trust_index']
    
    def __str__(self):
        return f"{self.name} ({self.city})"


class Instructor(models.Model):
    """Instructor model."""
    AUTO_TYPE_CHOICES = [
        ('automatic', 'Автомат'),
        ('manual', 'Механика'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='instructors')
    auto_type = models.CharField(max_length=20, choices=AUTO_TYPE_CHOICES)
    phone = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    payment_link_kaspi = models.URLField(blank=True)
    payment_link_halyk = models.URLField(blank=True)
    schedule = models.JSONField(default=dict, blank=True)  # Free time slots
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Инструктор'
        verbose_name_plural = 'Инструкторы'
        ordering = ['-rating']
    
    def __str__(self):
        return f"{self.name} ({self.city}, {self.get_auto_type_display()})"


class Application(models.Model):
    """Application model for student requests."""
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('paid', 'Оплачено'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]
    
    CATEGORY_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('BE', 'BE'),
        ('C', 'C'),
        ('CE', 'CE'),
        ('D', 'D'),
        ('DE', 'DE'),
        ('A1', 'A1'),
        ('C1', 'C1'),
        ('D1', 'D1'),
    ]
    
    FORMAT_CHOICES = [
        ('online', 'Онлайн'),
        ('offline', 'Оффлайн'),
        ('hybrid', 'Гибрид'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name='applications')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True, related_name='applications')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, blank=True)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, blank=True)
    time_slot = models.DateTimeField(blank=True, null=True)  # For instructor appointments
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    student_name = models.CharField(max_length=200)
    student_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_changed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.school:
            return f"Заявка в {self.school.name} от {self.student_name}"
        elif self.instructor:
            return f"Заявка к {self.instructor.name} от {self.student_name}"
        return f"Заявка от {self.student_name}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Application.objects.get(pk=self.pk).status
            if old_status != self.status:
                self.status_changed_at = timezone.now()
        super().save(*args, **kwargs)

