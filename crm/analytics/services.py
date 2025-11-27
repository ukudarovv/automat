"""
Services for calculating trust and discipline indices.
"""
from datetime import timedelta
from django.utils import timezone
from core.models import School, Application
from crm.analytics.models import TrustIndex, DisciplineIndex


def calculate_trust_index(school: School) -> TrustIndex:
    """Calculate and update school trust index."""
    applications = Application.objects.filter(school=school)
    
    if not applications.exists():
        # Default values for new schools
        trust_index, created = TrustIndex.objects.get_or_create(school=school)
        trust_index.index_value = 100.00
        trust_index.save()
        return trust_index
    
    total = applications.count()
    
    # Calculate average response time (time from creation to first status change)
    response_times = []
    for app in applications.filter(status_changed_at__isnull=False):
        if app.status_changed_at and app.created_at:
            response_time = (app.status_changed_at - app.created_at).total_seconds() / 3600  # Hours
            response_times.append(response_time)
    
    average_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    # Calculate confirmation rate
    confirmed = applications.filter(status__in=['confirmed', 'paid', 'completed']).count()
    confirmation_rate = (confirmed / total * 100) if total > 0 else 0
    
    # Calculate payment rate
    paid = applications.filter(status__in=['paid', 'completed']).count()
    payment_rate = (paid / total * 100) if total > 0 else 0
    
    # Calculate completion rate
    completed = applications.filter(status='completed').count()
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    # Calculate average processing delay
    processing_delays = []
    for app in applications.filter(status_changed_at__isnull=False):
        if app.status_changed_at and app.created_at:
            delay = (app.status_changed_at - app.created_at).total_seconds() / 3600
            processing_delays.append(delay)
    
    average_processing_delay = sum(processing_delays) / len(processing_delays) if processing_delays else 0
    
    # Calculate index (simplified formula for MVP)
    # Higher is better (100 = perfect)
    index = 100.0
    
    # Penalties
    if average_response_time > 24:  # More than 24 hours
        index -= 10
    if average_response_time > 48:
        index -= 10
    
    if confirmation_rate < 50:
        index -= 20
    elif confirmation_rate < 70:
        index -= 10
    
    if payment_rate < 30:
        index -= 20
    elif payment_rate < 50:
        index -= 10
    
    if completion_rate < 20:
        index -= 15
    
    if average_processing_delay > 48:
        index -= 10
    
    # Bonuses
    if confirmation_rate > 80:
        index += 5
    if payment_rate > 70:
        index += 5
    if completion_rate > 50:
        index += 5
    
    index = max(0, min(100, index))
    
    # Update or create trust index
    trust_index, created = TrustIndex.objects.get_or_create(school=school)
    trust_index.average_response_time = average_response_time
    trust_index.confirmation_rate = confirmation_rate
    trust_index.payment_rate = payment_rate
    trust_index.completion_rate = completion_rate
    trust_index.average_processing_delay = average_processing_delay
    trust_index.index_value = index
    trust_index.save()
    
    # Update school's trust_index field
    school.trust_index = index
    school.save()
    
    return trust_index


def update_all_trust_indices():
    """Update trust indices for all schools."""
    schools = School.objects.filter(is_active=True)
    for school in schools:
        calculate_trust_index(school)

