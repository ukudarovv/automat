"""
Service for creating and managing applications.
"""
from datetime import datetime
from bot.services.database import User, Application, School, Instructor, City
from typing import Optional
from asgiref.sync import sync_to_async


@sync_to_async
def _get_user(telegram_id: int):
    """Get user synchronously."""
    try:
        return User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None


@sync_to_async
def _create_user(telegram_id: int, username: str = None):
    """Create user synchronously."""
    user = User.objects.create_user(
        username=f"user_{telegram_id}",
        telegram_id=telegram_id,
        role='student'
    )
    if username:
        user.username = username
        user.save()
    return user


@sync_to_async
def _update_user_username(user, username: str):
    """Update user username synchronously."""
    user.username = username
    user.save()
    return user


async def get_or_create_user(telegram_id: int, username: str = None) -> User:
    """Get or create user by telegram_id."""
    user = await _get_user(telegram_id)
    if user:
        if username and user.username != username:
            user = await _update_user_username(user, username)
        return user
    user = await _create_user(telegram_id, username)
    return user


@sync_to_async
def _get_city_for_app(city_name: str):
    """Get city synchronously."""
    try:
        return City.objects.get(name=city_name)
    except City.DoesNotExist:
        return None


@sync_to_async
def _get_school_for_app(school_id: int):
    """Get school synchronously."""
    try:
        return School.objects.get(id=school_id)
    except School.DoesNotExist:
        return None


@sync_to_async
def _get_instructor_for_app(instructor_id: int):
    """Get instructor synchronously."""
    try:
        return Instructor.objects.get(id=instructor_id)
    except Instructor.DoesNotExist:
        return None


@sync_to_async
def _create_school_application(user, school, city_obj, category, format_value, name, phone):
    """Create school application synchronously."""
    return Application.objects.create(
        student=user,
        school=school,
        city=city_obj,
        category=category,
        format=format_value,
        status='new',
        student_name=name,
        student_phone=phone
    )


@sync_to_async
def _create_instructor_application(user, instructor, city_obj, name, phone, time_slot):
    """Create instructor application synchronously."""
    return Application.objects.create(
        student=user,
        instructor=instructor,
        city=city_obj,
        status='new',
        student_name=name,
        student_phone=phone,
        time_slot=time_slot
    )


async def create_school_application(
    telegram_id: int,
    name: str,
    phone: str,
    city: str,
    category: str,
    format_type: str,
    school_id: int
) -> Application:
    """Create school application."""
    user = await get_or_create_user(telegram_id)
    
    city_obj = await _get_city_for_app(city)
    school = await _get_school_for_app(school_id)
    
    if not city_obj or not school:
        raise ValueError(f"City or School not found: city={city}, school_id={school_id}")
    
    # Map format to model value
    format_map = {
        'Онлайн': 'online',
        'Оффлайн': 'offline',
        'Гибрид': 'hybrid'
    }
    format_value = format_map.get(format_type, 'offline')
    
    application = await _create_school_application(
        user, school, city_obj, category, format_value, name, phone
    )
    
    return application


async def create_instructor_application(
    telegram_id: int,
    name: str,
    phone: str,
    city: str,
    auto_type: str,
    instructor_id: int,
    time_slot: Optional[datetime] = None
) -> Application:
    """Create instructor application."""
    user = await get_or_create_user(telegram_id)
    
    city_obj = await _get_city_for_app(city)
    instructor = await _get_instructor_for_app(instructor_id)
    
    if not city_obj or not instructor:
        raise ValueError(f"City or Instructor not found: city={city}, instructor_id={instructor_id}")
    
    application = await _create_instructor_application(
        user, instructor, city_obj, name, phone, time_slot
    )
    
    return application

