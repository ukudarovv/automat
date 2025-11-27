from django.urls import path
from . import views

app_name = 'instructors'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('applications/', views.applications_list, name='applications'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/accept/', views.accept_application, name='accept'),
    path('applications/<int:pk>/reject/', views.reject_application, name='reject'),
    path('applications/<int:pk>/complete/', views.complete_lesson, name='complete'),
]

