from django.urls import path
from . import views

app_name = 'schools'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('applications/', views.applications_list, name='applications'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/update-status/', views.update_status, name='update_status'),
    path('applications/<int:pk>/send-response/', views.send_response, name='send_response'),
]

