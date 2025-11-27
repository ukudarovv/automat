"""
Views for instructor CRM.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Instructor, Application


def login_view(request):
    """Instructor login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.role == 'instructor' and hasattr(user, 'instructor_profile'):
            login(request, user)
            return redirect('instructors:dashboard')
        else:
            messages.error(request, 'Неверные учетные данные или вы не являетесь инструктором.')
    return render(request, 'instructors/login.html')


@login_required
def dashboard(request):
    """Instructor dashboard."""
    instructor = request.user.instructor_profile
    applications = Application.objects.filter(instructor=instructor).order_by('-created_at')
    pending = applications.filter(status='new').count()
    completed = applications.filter(status='completed').count()
    
    context = {
        'instructor': instructor,
        'applications': applications[:5],  # Last 5
        'pending': pending,
        'completed': completed,
    }
    return render(request, 'instructors/dashboard.html', context)


@login_required
def applications_list(request):
    """List of applications for instructor."""
    instructor = request.user.instructor_profile
    applications = Application.objects.filter(instructor=instructor).order_by('-created_at')
    
    context = {
        'applications': applications,
    }
    return render(request, 'instructors/applications_list.html', context)


@login_required
def application_detail(request, pk):
    """Application detail view."""
    instructor = request.user.instructor_profile
    application = get_object_or_404(Application, pk=pk, instructor=instructor)
    
    context = {
        'application': application,
    }
    return render(request, 'instructors/application_detail.html', context)


@login_required
def accept_application(request, pk):
    """Accept application."""
    instructor = request.user.instructor_profile
    application = get_object_or_404(Application, pk=pk, instructor=instructor)
    
    application.status = 'confirmed'
    application.save()
    messages.success(request, 'Заявка принята.')
    
    return redirect('instructors:application_detail', pk=pk)


@login_required
def reject_application(request, pk):
    """Reject application."""
    instructor = request.user.instructor_profile
    application = get_object_or_404(Application, pk=pk, instructor=instructor)
    
    application.status = 'cancelled'
    application.save()
    messages.success(request, 'Заявка отклонена.')
    
    return redirect('instructors:application_detail', pk=pk)


@login_required
def complete_lesson(request, pk):
    """Mark lesson as completed."""
    instructor = request.user.instructor_profile
    application = get_object_or_404(Application, pk=pk, instructor=instructor)
    
    application.status = 'completed'
    application.save()
    messages.success(request, 'Урок отмечен как проведенный.')
    
    return redirect('instructors:application_detail', pk=pk)

