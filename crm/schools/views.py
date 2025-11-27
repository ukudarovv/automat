"""
Views for school CRM.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from core.models import School, Application
from bot.services.messaging import send_auto_response
import asyncio


def login_view(request):
    """School login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.role == 'school' and hasattr(user, 'school_profile'):
            login(request, user)
            return redirect('schools:dashboard')
        else:
            messages.error(request, 'Неверные учетные данные или вы не являетесь автошколой.')
    return render(request, 'schools/login.html')


@login_required
def dashboard(request):
    """School dashboard."""
    school = request.user.school_profile
    applications_count = Application.objects.filter(school=school).count()
    new_applications = Application.objects.filter(school=school, status='new').count()
    paid_applications = Application.objects.filter(school=school, status='paid').count()
    
    context = {
        'school': school,
        'applications_count': applications_count,
        'new_applications': new_applications,
        'paid_applications': paid_applications,
    }
    return render(request, 'schools/dashboard.html', context)


@login_required
def applications_list(request):
    """List of applications for school."""
    school = request.user.school_profile
    applications = Application.objects.filter(school=school).order_by('-created_at')
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    context = {
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'schools/applications_list.html', context)


@login_required
def application_detail(request, pk):
    """Application detail view."""
    school = request.user.school_profile
    application = get_object_or_404(Application, pk=pk, school=school)
    
    context = {
        'application': application,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'schools/application_detail.html', context)


@login_required
def update_status(request, pk):
    """Update application status."""
    from crm.analytics.services import calculate_trust_index
    
    school = request.user.school_profile
    application = get_object_or_404(Application, pk=pk, school=school)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            
            # Recalculate trust index
            calculate_trust_index(school)
            
            messages.success(request, f'Статус заявки изменен на: {application.get_status_display()}')
        else:
            messages.error(request, 'Неверный статус.')
    
    return redirect('schools:application_detail', pk=pk)


@login_required
def send_response(request, pk):
    """Send auto-response to student."""
    school = request.user.school_profile
    application = get_object_or_404(Application, pk=pk, school=school)
    
    try:
        # Run async function in sync context
        asyncio.run(send_auto_response(application))
        messages.success(request, 'Автоответ отправлен студенту.')
    except Exception as e:
        messages.error(request, f'Ошибка при отправке: {str(e)}')
    
    return redirect('schools:application_detail', pk=pk)

