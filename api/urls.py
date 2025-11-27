"""
API URL configuration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'cities', views.CityViewSet, basename='city')

urlpatterns = [
    path('', include(router.urls)),
    path('schools/', views.schools_list, name='schools-list'),
    path('instructors/', views.instructors_list, name='instructors-list'),
    path('applications/', views.application_create, name='application-create'),
    path('applications/<int:pk>/', views.application_detail, name='application-detail'),
    path('auth/telegram/', views.telegram_auth, name='telegram-auth'),
]

