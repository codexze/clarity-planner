import datetime
from rest_framework import permissions, pagination, views, viewsets, response, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

from django.db.models import Prefetch, Subquery, OuterRef, Q
from django.utils import timezone

from apps.planning.views import AppointmentFilter
from apps.planning.serializers import AppointmentSerializer, ReminderSerializer
from apps.planning.models import Appointment, Reminder

from .models import Gender, Client, KnownAddress, Company
from .serializers import ClientSerializer, ClientDetailSerializer, KnownAddressSerializer, CompanySerializer

class GenderView(viewsets.ViewSet):
    def list(self, request):
        choices = [{"value": choice.value, "label": choice.label} for choice in Gender]
        return response.Response(choices)

class Pagination(pagination.PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow users to set custom page size
    max_page_size = 100  # Prevent very large page sizes

class CompanyFilter(filters.FilterSet):
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Company
        fields = {
            'name': ['icontains'],
            'email': ['icontains'],
            'phone': ['startswith'],
            'is_active': ['exact'],
        }

    def order(self, queryset, name, value):
        return queryset.filter().order_by(value)
    
class CompanyView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CompanyFilter
    pagination_class = Pagination

    def get_queryset(self):
        return Company.objects.select_related().prefetch_related(
            'clients'  # Prefetch clients for company details
        )
    
    @action(methods=['get'], detail=False)
    def all(self, request):
        companies = Company.objects.all().order_by('name')
        serializer = CompanySerializer(companies, many=True)
        return response.Response(serializer.data)

    @action(methods=['get'], detail=False)
    def filter(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
    

class ClientFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name', label="Search Name")
    date_of_birth = filters.CharFilter(method='filter_date_of_birth', label="Search Date of Birth")
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Client
        fields = {
            'email': ['icontains'],
            'mobile': ['startswith'],
            'gender': ['exact'],  
            'company': ['exact'],
            'is_active': ['exact'], 
        }

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(surname__icontains=value))
    

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
                return queryset.filter().order_by('first_name', 'surname').reverse()
            return queryset.filter().order_by('first_name', 'surname')
        return queryset.filter().order_by(value)


class ClientView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ClientFilter
    pagination_class = Pagination

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

    def get_queryset(self):
        # Use annotations instead of properties for better performance
        today = timezone.now().date()

        last_appointment_subq = Appointment.objects.filter(
            client=OuterRef('pk'), 
            start__date__lt=today
        ).order_by('-start').values('start')[:1]

        next_appointment_subq = Appointment.objects.filter(
            client=OuterRef('pk'), 
            start__date__gte=today
        ).order_by('start').values('start')[:1]

        return Client.objects.select_related(
            'company',          # Fix company N+1
            'created_by',       # Fix audit fields N+1
            'updated_by'
        ).prefetch_related(
            # Optimize appointments with their related data
            Prefetch(
                'appointments',
                queryset=Appointment.objects.select_related(
                    'service__type',
                    'employee__calendarsettings',
                    'client', 
                    'onsite_address'
                ).prefetch_related('appointment_addons__addon')
            ),
            # Optimize known addresses
            'known_addresses'
        ).annotate(
            # Use annotations instead of properties
            last_appointment_date=Subquery(last_appointment_subq),
            next_appointment_date=Subquery(next_appointment_subq)
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
    
    @action(methods=['get'], detail=True)
    def appointments(self, request, pk=None):
        client = get_object_or_404(Client, pk=pk)
        appointments = Appointment.objects.filter(client=client)
        
        # Apply filtering and pagination
        filtered_appointments = AppointmentFilter(request.GET, queryset=appointments).qs
        paginator = Pagination()
        paginated_appointments = paginator.paginate_queryset(filtered_appointments, request)
        
        serializer = AppointmentSerializer(paginated_appointments, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(methods=['get'], detail=True)
    def reminders(self, request, pk=None):
        client = get_object_or_404(Client, pk=pk)
        reminders = Reminder.objects.filter(client=client).order_by('start')
                
        serializer = ReminderSerializer(reminders, many=True)
        return response.Response(serializer.data)
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.set_record(request.user, False)
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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            instance.refresh_from_db()
            instance.set_record(request.user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class KnownAddressFilter(filters.FilterSet):
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = KnownAddress
        fields = {
            'client': ['exact'],
            'address': ['icontains'],
            'is_active': ['exact'],
        }
    
    def order(self, queryset, name, value):
        return queryset.filter().order_by(value)
    
class KnownAddressView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = KnownAddress.objects.all()
    serializer_class = KnownAddressSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = KnownAddressFilter
    pagination_class = Pagination

    def get_queryset(self):
        last_appointment_subq = Appointment.objects.filter(
            client=OuterRef('client_id'), 
            start__date__lt=timezone.now().date()
        ).order_by('-start').values('start')[:1]

        next_appointment_subq = Appointment.objects.filter(
            client=OuterRef('client_id'), 
            start__date__gte=timezone.now().date()
        ).order_by('start').values('start')[:1] 

        queryset = KnownAddress.objects.select_related(
            'client',        
        ).annotate(
            # Use annotations instead of properties
            last_appointment_date=Subquery(last_appointment_subq),
            next_appointment_date=Subquery(next_appointment_subq)
        )
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

    # update is_active status
    @action(methods=['patch'], detail=True)
    def set_active(self, request, pk=None):
        instance = self.get_object()
        is_active = request.data.get('is_active')
        if is_active is None:
            return response.Response({"detail": "is_active field is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.is_active = is_active
        instance.save()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)