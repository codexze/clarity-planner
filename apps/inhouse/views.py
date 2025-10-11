import datetime
from rest_framework import permissions, pagination, views, viewsets, response, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q

from apps.authorize.serializers import UserLimitedSerializer
from apps.planning.serializers import CalendarConfigSerializer, AppointmentSerializer, BlockedSerializer, ReminderSerializer

from .models import Service, Staff, ServiceType, Addon
from .serializers import ServiceSerializer, StaffSerializer, ServiceTypeSerializer, AddonSerializer

class ServiceTypeView(viewsets.ViewSet):
    def list(self, request):
        queryset = ServiceType.objects.all()
        serializer = ServiceTypeSerializer(queryset, many=True)
        return response.Response(serializer.data)
    
class Pagination(pagination.PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow users to set custom page size
    max_page_size = 100  # Prevent very large page sizes

class AddonFilter(filters.FilterSet):
    type = filters.CharFilter(field_name='type__id', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    status = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Addon
        fields = {
            'type': ['exact'],  # Filter by exact match
            'is_active': ['exact'],  # Active services only
        }

    def order(self, queryset, name, value):
        return queryset.filter().order_by(value)
    
class AddonView(viewsets.ModelViewSet):
    serializer_class = AddonSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AddonFilter
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Addon.objects.all()
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
        queryset = Addon.objects.filter(type__id=type)
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
        
class ServiceFilter(filters.FilterSet):
    type = filters.CharFilter(field_name='type', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    status = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Service
        fields = {
            'type_id': ['exact'],  # Filter by exact match
            'price': ['lt', 'gt', 'exact'],  # Less than, greater than, exact price
            'is_active': ['exact'],  # Active services only
        }

    def order(self, queryset, name, value):
        return queryset.filter().order_by(value)

class ServiceView(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ServiceFilter
    pagination_class = Pagination

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

class StaffFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name', label="Search Name")
    date_of_birth = filters.CharFilter(method='filter_date_of_birth')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    mobile = filters.CharFilter(field_name='mobile', lookup_expr='startswith')
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Staff
        fields = {
        }

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))
    

    def filter_date_of_birth(self, queryset, name, value):
        try:
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%d%m%Y']:
                try:
                    date = datetime.datetime.strptime(value, fmt).date()
                    return queryset.filter(date_of_birth=date)
                except ValueError:
                    continue
            return queryset
        except:
            return queryset

    def order(self, queryset, name, value):
        if 'name' in value:
            if value.startswith('-'):
                return queryset.filter().order_by('first_name', 'last_name').reverse()
            return queryset.filter().order_by('first_name', 'last_name')
        return queryset.filter().order_by(value)

    
class StaffView(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    lookup_field = 'username'
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = StaffFilter
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Staff.objects.all()
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
    
    @action(methods=['get'], detail=False, url_path='service_type/(?P<type>[^/.]+)')
    def by_type(self, request, type=None):
        if Staff.objects.filter(staffservice__service_type_id=type).exists():
            queryset = Staff.objects.filter(staffservice__service_type_id=type)
        else:
            queryset = Staff.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
    

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
    
    @action(methods=['get'], detail=True)
    def reminders(self, request, username=None):
        employee = self.get_object()

        start = datetime.datetime.strptime(self.request.query_params.get('start', None), "%Y-%m-%dT%H:%M:%S%z")
        end = datetime.datetime.strptime(self.request.query_params.get('end', None), "%Y-%m-%dT%H:%M:%S%z")

        queryset = employee.reminders.filter(start__date__gte=start, start__date__lte=end).filter(Q(global_reminder=True) | Q(employee=employee))

        reminders = ReminderSerializer(queryset, many=True)
        return response.Response(reminders.data)
    
class AddonFilter(filters.FilterSet):
    type = filters.CharFilter(field_name='type', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    status = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Addon
        fields = {
            'type': ['exact'],  # Filter by exact match
            'is_active': ['exact'],  # Active services only
        }

    def order(self, queryset, name, value):
        return queryset.filter().order_by(value)

class AddonView(viewsets.ModelViewSet):
    serializer_class = AddonSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AddonFilter
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Addon.objects.all()
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
        queryset = Addon.objects.filter(type__id=type)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            # instance.set_record(request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            self.perform_update(serializer)
            instance.refresh_from_db()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], detail=True)
    def activate(self, request, pk=None):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data, status=status.HTTP_200_OK)        