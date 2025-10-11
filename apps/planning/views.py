import datetime
from rest_framework import permissions, pagination, viewsets, response, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.db.models import Q
from django.db import transaction

from apps.clients.models import KnownAddress
from apps.inhouse.models import Addon

from .models import Appointment, Blocked, Reminder,AppointmentAddon
from .serializers import AppointmentSerializer, BlockedSerializer, ReminderSerializer



class Pagination(pagination.PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow users to set custom page size
    max_page_size = 100  # Prevent very large page sizes

class AppointmentFilter(filters.FilterSet):
    appointment_date = filters.CharFilter(method='filter_appointment_date', label="Search Appointment Date")
    client__name = filters.CharFilter(method='filter_client', label="Search Client Name")
    service__name = filters.CharFilter(method='filter_service', label="Search Service Name")
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Appointment
        fields = { }

    def filter_appointment_date(self, queryset, name, value):
        try:
            # Try common date formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%d%m%Y']:
                try:
                    date = datetime.datetime.strptime(value, fmt).date()
                    return queryset.filter(start__date=date)
                except ValueError:
                    continue
            return queryset
        except:
            return queryset

    def filter_client(self, queryset, name, value):
        return queryset.filter(Q(client__first_name__icontains=value) | Q(client__surname__icontains=value))


    def filter_service(self, queryset, name, value):
        return queryset.filter(Q(service__name__icontains=value))
    
    def order(self, queryset, name, value):
        if 'client__name' in value:
            if value.startswith('-'):
                return queryset.filter().order_by('client__first_name', 'client__surname').reverse()
            return queryset.filter().order_by('client__first_name', 'client__surname')
        
        if 'appointment_date' in value:
            if value.startswith('-'):
                return queryset.filter().order_by('start').reverse()
            return queryset.filter().order_by('start')
        return queryset.filter().order_by(value)


class AppointmentView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AppointmentFilter
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Appointment.objects.all()
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
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        if data.get('is_onsite') and data.get('onsite_address'):
            address = data.pop('onsite_address')
            known_address, _ = KnownAddress.objects.get_or_create(address=address, client_id=data.get('client'))
            data['onsite_address'] = known_address.id
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.set_record(request.user, False)

            addons = data.pop('addons')
            if addons:
                for addon_id in addons:
                    addon = Addon.objects.get(id=addon_id)
                    AppointmentAddon.objects.create(appointment=instance, addon=addon, addon_price=addon.price)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    @action(methods=['put'], detail=True, url_path='reschedule')
    def reschedule(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            instance.refresh_from_db()
            instance.set_record(request.user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        # Update onsite_address if provided
        if data.get('is_onsite') and data.get('onsite_address'):
            address = data.pop('onsite_address')
            known_address, _ = KnownAddress.objects.get_or_create(address=address, client_id=data.get('client'))
            data['onsite_address'] = known_address.id

        # Update addons if provided and only if changed
        addons = data.pop('addons', None)
        if addons is not None:
            # Get current addon IDs for the appointment
            current_addon_ids = set(AppointmentAddon.objects.filter(appointment=instance).values_list('addon_id', flat=True))
            new_addon_ids = set(addons)
            if current_addon_ids != set(map(int, new_addon_ids)):
            # Remove existing addons
                AppointmentAddon.objects.filter(appointment=instance).delete()
                # Add new addons
                for addon_id in new_addon_ids:
                    addon = Addon.objects.get(id=addon_id)
                    AppointmentAddon.objects.create(appointment=instance, addon=addon, addon_price=addon.price)

        serializer = self.get_serializer(instance, data=data, partial=False)
        if serializer.is_valid():
            self.perform_update(serializer)
            instance.refresh_from_db()
            instance.set_record(request.user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlockedView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlockedSerializer

    def get_queryset(self):
        queryset = Blocked.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        data["employee"] = request.user.id

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.set_record(request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=['put'], detail=True, url_path='reschedule')
    def reschedule(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            instance.refresh_from_db()
            instance.set_record(request.user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
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

class ReminderView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReminderSerializer

    def get_queryset(self):
        queryset = Reminder.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data

        date = data.pop("appointment_date", datetime.datetime.now().date().isoformat())
        data["start"] = date
        data["end"] = date

        if data.get('global_reminder'):
            data['employee'] = None
        else:
            data['employee'] = request.user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.set_record(request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)