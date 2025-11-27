"""
API views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.models import City, School, Instructor, Application
from api.serializers import (
    CitySerializer, SchoolSerializer, InstructorSerializer,
    ApplicationSerializer, ApplicationCreateSerializer
)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for cities."""
    queryset = City.objects.filter(is_active=True)
    serializer_class = CitySerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([AllowAny])
def schools_list(request):
    """Get schools filtered by city."""
    city_name = request.query_params.get('city', None)
    
    if city_name:
        try:
            city = City.objects.get(name=city_name, is_active=True)
            schools = School.objects.filter(city=city, is_active=True).order_by('-rating', '-trust_index')
        except City.DoesNotExist:
            schools = School.objects.none()
    else:
        schools = School.objects.filter(is_active=True).order_by('-rating', '-trust_index')
    
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def instructors_list(request):
    """Get instructors filtered by city and auto type."""
    city_name = request.query_params.get('city', None)
    auto_type = request.query_params.get('auto_type', None)
    
    instructors = Instructor.objects.filter(is_active=True)
    
    if city_name:
        try:
            city = City.objects.get(name=city_name, is_active=True)
            instructors = instructors.filter(city=city)
        except City.DoesNotExist:
            instructors = Instructor.objects.none()
    
    if auto_type:
        instructors = instructors.filter(auto_type=auto_type)
    
    instructors = instructors.order_by('-rating')
    serializer = InstructorSerializer(instructors, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def application_create(request):
    """Create a new application."""
    serializer = ApplicationCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        application = serializer.save()
        response_serializer = ApplicationSerializer(application)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def application_detail(request, pk):
    """Get application details."""
    application = get_object_or_404(Application, pk=pk)
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def telegram_auth(request):
    """Authenticate user via Telegram Web App initData."""
    from api.telegram_auth import get_user_from_init_data
    
    init_data = request.data.get('initData', '')
    
    if not init_data:
        return Response({
            'success': False,
            'error': 'initData is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_from_init_data(init_data)
    
    if not user:
        return Response({
            'success': False,
            'error': 'Invalid initData'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        'success': True,
        'user': {
            'id': user.id,
            'telegram_id': user.telegram_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    })

