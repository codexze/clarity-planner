import datetime
from rest_framework import permissions, pagination, views, viewsets, response, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.db.models import Q

from apps.planning.views import AppointmentFilter, AppointmentPagination
from apps.planning.models import Appointment

from .models import Gender, Client
from .serializers import ClientSerializer, AppointmentSerializer

class GenderView(viewsets.ViewSet):
    def list(self, request):
        choices = [{"value": choice.value, "label": choice.label} for choice in Gender]
        return response.Response(choices)

class ClientPagination(pagination.PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow users to set custom page size
    max_page_size = 100  # Prevent very large page sizes

class ClientFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name', label="Search Name")
    date_of_birth = filters.CharFilter(method='filter_date_of_birth')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    mobile = filters.CharFilter(field_name='mobile', lookup_expr='startswith')
    gender = filters.CharFilter(field_name='gender', lookup_expr='iexact')
    sorting = filters.CharFilter(method='do_sorting', label="Order By")

    class Meta:
        model = Client
        fields = {
            'gender': ['exact'],  # Filter by exact match
            'is_active': ['exact'],  # Active services only
        }

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(surname__icontains=value))
    

    def filter_date_of_birth(self, queryset, name, value):
        try:
            # Try common date formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%d%m%Y']:
                try:
                    date = datetime.datetime.strptime(value, fmt).date()
                    return queryset.filter(date_of_birth=date)
                except ValueError:
                    continue
            return queryset
        except:
            return queryset

    def do_sorting(self, queryset, name, value):
        return queryset.filter().order_by(value)


class ClientView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ClientFilter
    pagination_class = ClientPagination  # Enable pagination

    def get_queryset(self):
        queryset = Client.objects.all()
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
    
    @action(methods=['get'], detail=True)
    def appointments(self, request, pk=None):
        client = get_object_or_404(Client, pk=pk)
        appointments = Appointment.objects.filter(client=client)
        
        # Apply filtering and pagination
        filtered_appointments = AppointmentFilter(request.GET, queryset=appointments).qs
        paginator = AppointmentPagination()
        paginated_appointments = paginator.paginate_queryset(filtered_appointments, request)
        
        serializer = AppointmentSerializer(paginated_appointments, many=True)
        return paginator.get_paginated_response(serializer.data)
    

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
