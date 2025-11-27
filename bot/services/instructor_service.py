"""
Service for working with instructors.
"""
from bot.services.database import Instructor, City
from typing import List
from asgiref.sync import sync_to_async


@sync_to_async
def _get_city_for_instructor(city_name: str):
    """Get city synchronously."""
    try:
        return City.objects.get(name=city_name, is_active=True)
    except City.DoesNotExist:
        return None


@sync_to_async
def _get_instructors(city, auto_type: str):
    """Get instructors synchronously."""
    if not city:
        return []
    instructors = Instructor.objects.filter(
        city=city,
        auto_type=auto_type,
        is_active=True
    ).order_by('-rating')
    return list(instructors)


@sync_to_async
def _get_instructor_by_id(instructor_id: int):
    """Get instructor by ID synchronously."""
    try:
        return Instructor.objects.get(id=instructor_id, is_active=True)
    except Instructor.DoesNotExist:
        return None


async def get_instructors_by_city_and_type(city_name: str, auto_type: str) -> List[Instructor]:
    """Get active instructors by city and auto type."""
    city = await _get_city_for_instructor(city_name)
    if not city:
        return []
    instructors = await _get_instructors(city, auto_type)
    return instructors


async def get_instructor_by_id(instructor_id: int) -> Instructor:
    """Get instructor by ID."""
    return await _get_instructor_by_id(instructor_id)

