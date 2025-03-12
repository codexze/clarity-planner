import datetime
from rest_framework import permissions, pagination, views, viewsets, response, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q

from .models import Appointment, Blocked
from .serializers import AppointmentSerializer, BlockedSerializer


        
class AppointmentPagination(pagination.PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow users to set custom page size
    max_page_size = 100  # Prevent very large page sizes

class AppointmentFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search', label="Search")
    type = filters.CharFilter(field_name='type', lookup_expr='iexact')
    status = filters.BooleanFilter(field_name='active', lookup_expr='exact')
    order_by = filters.CharFilter(method='filter_order_by', label="Order By")

    class Meta:
        model = Appointment
        fields = {
            # 'type': ['exact'],  # Filter by exact match
            # 'price': ['lt', 'gt', 'exact'],  # Less than, greater than, exact price
            # 'active': ['exact'],  # Active services only
        }

    def filter_search(self, queryset, name, value):
        # return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
        return queryset.filter()

    def filter_order_by(self, queryset, name, value):
        return queryset.filter().order_by(value)


class AppointmentView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AppointmentFilter
    pagination_class = AppointmentPagination

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

class BlockedView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlockedSerializer

    def get_queryset(self):
        queryset = Blocked.objects.all()
        return queryset

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
