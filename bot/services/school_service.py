"""
Service for working with schools.
"""
from bot.services.database import School, City
from typing import List
from asgiref.sync import sync_to_async


@sync_to_async
def _get_city(city_name: str):
    """Get city synchronously."""
    try:
        # Use select_related/prefetch_related if needed
        city = City.objects.get(name=city_name, is_active=True)
        # Force evaluation to avoid lazy loading issues
        return city
    except City.DoesNotExist:
        return None


@sync_to_async
def _get_schools(city):
    """Get schools synchronously."""
    if not city:
        return []
    # Force evaluation immediately to avoid lazy loading in async context
    schools_queryset = School.objects.filter(city=city, is_active=True).order_by('-rating', '-trust_index')
    schools_list = list(schools_queryset)
    return schools_list


@sync_to_async
def _get_school_by_id(school_id: int):
    """Get school by ID synchronously."""
    try:
        return School.objects.get(id=school_id, is_active=True)
    except School.DoesNotExist:
        return None


async def get_schools_by_city(city_name: str) -> List[School]:
    """Get active schools by city name."""
    city = await _get_city(city_name)
    if not city:
        return []
    schools = await _get_schools(city)
    return schools


async def get_school_by_id(school_id: int) -> School:
    """Get school by ID."""
    return await _get_school_by_id(school_id)

