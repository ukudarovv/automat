"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('crm/schools/', include('crm.schools.urls')),
    path('crm/instructors/', include('crm.instructors.urls')),
]

