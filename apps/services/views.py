import datetime
from rest_framework import permissions, pagination, views, viewsets, response, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q

from apps.authorize.serializers import UserLimitedSerializer
from apps.planning.serializers import CalendarConfigSerializer, AppointmentSerializer, BlockedSerializer

from .models import Service, Staff, ServiceType
from .serializers import ServiceSerializer, StaffSerializer, ServiceTypeSerializer

class ServiceTypeView(viewsets.ViewSet):
    def list(self, request):
        queryset = [{"value": choice.value, "label": choice.label} for choice in ServiceType]
        serializer = ServiceTypeSerializer(queryset, many=True)
        return response.Response(serializer.data)
        
class ServicePagination(pagination.PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow users to set custom page size
    max_page_size = 100  # Prevent very large page sizes

class ServiceFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search', label="Search")
    type = filters.CharFilter(field_name='type', lookup_expr='iexact')
    status = filters.BooleanFilter(field_name='active', lookup_expr='exact')
    order_by = filters.CharFilter(method='filter_order_by', label="Order By")

    class Meta:
        model = Service
        fields = {
            'type': ['exact'],  # Filter by exact match
            'price': ['lt', 'gt', 'exact'],  # Less than, greater than, exact price
            'active': ['exact'],  # Active services only
        }

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    def filter_order_by(self, queryset, name, value):
        return queryset.filter().order_by(value)

class ServiceView(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ServiceFilter
    pagination_class = ServicePagination

    def get_queryset(self):
        queryset = Service.objects.all()
        return queryset

    @action(methods=['get'], detail=False)
    def filter(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='type/(?P<type>[^/.]+)')
    def by_type(self, request, type=None):
        queryset = Service.objects.filter(type=type)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.set_record(request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            self.perform_update(serializer)
            instance.refresh_from_db()
            instance.set_record(request.user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffView(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = 'username'

    @action(methods=['get'], detail=True)
    def config(self, request, username=None):
        employee = self.get_object()

        if hasattr(employee, 'calendarsettings'):
            obj = employee.calendarsettings 
            settings = CalendarConfigSerializer(obj)

            return response.Response(settings.data)
        else:
            raise Http404
        
    @action(methods=['get'], detail=False)
    def limited(self, request):
        queryset = self.get_queryset()
        
        employee = UserLimitedSerializer(queryset, many=True)
        return response.Response(employee.data)
    
    @action(methods=['get'], detail=True)
    def appointments(self, request, username=None):
        employee = self.get_object()

        start = datetime.datetime.strptime(self.request.query_params.get('start', None), "%Y-%m-%dT%H:%M:%S%z")
        end = datetime.datetime.strptime(self.request.query_params.get('end', None), "%Y-%m-%dT%H:%M:%S%z")

        queryset = employee.appointments.filter(start__date__gte=start, start__date__lte=end)
        
        appointments = AppointmentSerializer(queryset, many=True)
        return response.Response(appointments.data)
    
    @action(methods=['get'], detail=True)
    def blocked(self, request, username=None):
        employee = self.get_object()

        start = datetime.datetime.strptime(self.request.query_params.get('start', None), "%Y-%m-%dT%H:%M:%S%z")
        end = datetime.datetime.strptime(self.request.query_params.get('end', None), "%Y-%m-%dT%H:%M:%S%z")

        queryset = employee.blocked.filter(start__date__gte=start, start__date__lte=end)

        blocked = BlockedSerializer(queryset, many=True)
        return response.Response(blocked.data)