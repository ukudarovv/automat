"""
Database connection and Django ORM integration for bot.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Now we can import Django models
from core.models import User, School, Instructor, Application, City

