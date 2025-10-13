import datetime
from rest_framework import permissions, pagination, views, viewsets, response, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q

from apps.authorize.serializers import UserLimitedSerializer
from apps.planning.serializers import CalendarConfigSerializer, AppointmentSerializer, BlockedTimeSerializer, ReminderSerializer

from .models import Employee
from .serializers import  EmployeeSerializer

    
class Pagination(pagination.PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow users to set custom page size
    max_page_size = 100  # Prevent very large page sizes
    
class EmployeeFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name', label="Search Name")
    date_of_birth = filters.CharFilter(method='filter_date_of_birth')
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Employee
        fields = {
            'email': ['exact', 'icontains'],  # Filter by exact match or contains
            'mobile': ['exact', 'startswith'],  # Filter by exact match or starts with
            'is_active': ['exact'],  # Active employees only
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

    
class EmployeeView(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    lookup_field = 'username'
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EmployeeFilter
    pagination_class = Pagination

    def get_queryset(self):
        return Employee.objects.select_related(
        ).prefetch_related(
            'groups',  # Prefetch user groups to avoid N+1 in has_role
            'employeeservice_set__service_type'  # Prefetch services
        )

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
        if Employee.objects.filter(employeeservice__service_type_id=type).exists():
            queryset = Employee.objects.filter(employeeservice__service_type_id=type)
        else:
            queryset = Employee.objects.all()
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

        blocked = BlockedTimeSerializer(queryset, many=True)
        return response.Response(blocked.data)
    
    @action(methods=['get'], detail=True)
    def reminders(self, request, username=None):
        employee = self.get_object()

        start = datetime.datetime.strptime(self.request.query_params.get('start', None), "%Y-%m-%dT%H:%M:%S%z")
        end = datetime.datetime.strptime(self.request.query_params.get('end', None), "%Y-%m-%dT%H:%M:%S%z")

        queryset = employee.reminders.filter(start__date__gte=start, start__date__lte=end).filter(Q(global_reminder=True) | Q(employee=employee))

        reminders = ReminderSerializer(queryset, many=True)
        return response.Response(reminders.data)