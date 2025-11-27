"""
Serializers for API.
"""
from rest_framework import serializers
from core.models import City, School, Instructor, Application, User
from django.db import models


class CitySerializer(serializers.ModelSerializer):
    """Serializer for City model."""
    
    class Meta:
        model = City
        fields = ['id', 'name', 'name_ru', 'is_active']


class SchoolSerializer(serializers.ModelSerializer):
    """Serializer for School model."""
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = School
        fields = [
            'id', 'name', 'city', 'city_name', 'address', 
            'rating', 'trust_index', 'whatsapp', 'telegram_contact',
            'payment_link_kaspi', 'payment_link_halyk', 'is_active'
        ]


class InstructorSerializer(serializers.ModelSerializer):
    """Serializer for Instructor model."""
    city_name = serializers.CharField(source='city.name', read_only=True)
    auto_type_display = serializers.CharField(source='get_auto_type_display', read_only=True)
    
    class Meta:
        model = Instructor
        fields = [
            'id', 'name', 'city', 'city_name', 'auto_type', 
            'auto_type_display', 'phone', 'rating',
            'payment_link_kaspi', 'payment_link_halyk', 'is_active'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model."""
    school_name = serializers.CharField(source='school.name', read_only=True, allow_null=True)
    instructor_name = serializers.CharField(source='instructor.name', read_only=True, allow_null=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    format_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    
    def get_format_display(self, obj):
        """Get format display name."""
        if obj.format:
            return dict(Application.FORMAT_CHOICES).get(obj.format, obj.format)
        return None
    
    def get_status_display(self, obj):
        """Get status display name."""
        if obj.status:
            return dict(Application.STATUS_CHOICES).get(obj.status, obj.status)
        return None
    
    class Meta:
        model = Application
        fields = [
            'id', 'student', 'school', 'school_name', 'instructor', 'instructor_name',
            'city', 'city_name', 'category', 'format', 'format_display',
            'time_slot', 'status', 'status_display', 'student_name', 
            'student_phone', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications."""
    telegram_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Application
        fields = [
            'telegram_id', 'school', 'instructor', 'city', 'category', 
            'format', 'time_slot', 'student_name', 'student_phone'
        ]
    
    def create(self, validated_data):
        telegram_id = validated_data.pop('telegram_id')
        student_name = validated_data.pop('student_name')
        student_phone = validated_data.pop('student_phone')
        
        # Get or create user
        user, _ = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': f'user_{telegram_id}',
                'role': 'student'
            }
        )
        
        application = Application.objects.create(
            student=user,
            student_name=student_name,
            student_phone=student_phone,
            status='new',
            **validated_data
        )
        
        return application

