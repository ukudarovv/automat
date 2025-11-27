"""
Analytics service for tracking user behavior.
"""
from datetime import datetime, timezone
from bot.services.database import User
from crm.analytics.models import AnalyticsEvent, DisciplineIndex
from typing import Optional, Dict, Any
from asgiref.sync import sync_to_async
from bot.services.application_service import get_or_create_user


@sync_to_async
def _get_last_event(user):
    """Get last event synchronously."""
    return AnalyticsEvent.objects.filter(
        user=user
    ).order_by('-timestamp').first()


@sync_to_async
def _create_analytics_event(user, event_type, step_name, event_data, time_since_last):
    """Create analytics event synchronously."""
    return AnalyticsEvent.objects.create(
        user=user,
        event_type=event_type,
        step_name=step_name,
        event_data=event_data or {},
        time_since_last=time_since_last
    )


async def track_event(
    user_id: int,
    event_type: str,
    step_name: str = "",
    event_data: Optional[Dict[str, Any]] = None,
    time_since_last: Optional[float] = None
):
    """Track analytics event."""
    user = await get_or_create_user(user_id)
    
    # Calculate time since last event if not provided
    if time_since_last is None:
        last_event = await _get_last_event(user)
        
        if last_event:
            time_since_last = (datetime.now(timezone.utc) - last_event.timestamp).total_seconds()
    
    await _create_analytics_event(user, event_type, step_name, event_data, time_since_last)
    
    # Update discipline index
    await update_discipline_index(user)


@sync_to_async
def _get_events(user):
    """Get events synchronously."""
    return list(AnalyticsEvent.objects.filter(user=user).order_by('timestamp'))


@sync_to_async
def _update_discipline_index_sync(user, average_step_time, return_count, reaction_delay, total_clicks, index):
    """Update discipline index synchronously."""
    discipline_index, created = DisciplineIndex.objects.get_or_create(user=user)
    discipline_index.average_step_time = average_step_time
    discipline_index.return_count = return_count
    discipline_index.reaction_delay = reaction_delay
    discipline_index.total_clicks = total_clicks
    discipline_index.index_value = index
    discipline_index.save()
    return discipline_index


async def update_discipline_index(user: User):
    """Update user's discipline index."""
    events = await _get_events(user)
    
    if not events:
        return
    
    # Calculate metrics
    step_times = [e.time_since_last for e in events if e.time_since_last]
    average_step_time = sum(step_times) / len(step_times) if step_times else 0
    
    return_count = sum(1 for e in events if e.event_type == 'return')
    
    button_click_events = [e for e in events if e.event_type == 'button_click']
    reaction_delays = [e.time_since_last for e in button_click_events if e.time_since_last]
    reaction_delay = sum(reaction_delays) / len(reaction_delays) if reaction_delays else 0
    
    total_clicks = len(button_click_events)
    
    # Calculate index (simplified formula for MVP)
    # Higher is better (100 = perfect)
    index = 100.0
    if average_step_time > 300:  # More than 5 minutes between steps
        index -= 10
    if return_count > 3:
        index -= 5 * return_count
    if reaction_delay > 60:  # More than 1 minute reaction
        index -= 5
    
    index = max(0, min(100, index))
    
    # Update or create discipline index
    await _update_discipline_index_sync(user, average_step_time, return_count, reaction_delay, total_clicks, index)

