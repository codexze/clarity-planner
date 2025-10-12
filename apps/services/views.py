import datetime
from rest_framework import permissions, pagination, views, viewsets, response, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q


from .models import ServiceType, Service, Addon
from .serializers import ServiceTypeSerializer, ServiceSerializer, AddonSerializer

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
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Addon
        fields = {
            'type': ['exact'], 
            'name': ['exact', 'icontains'], 
            'is_active': ['exact'], 
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
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Service
        fields = {
            'type': ['exact'],
            'name': ['iexact', 'icontains'],  
            'is_active': ['exact'], 
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
    
class AddonFilter(filters.FilterSet):
    ordering = filters.CharFilter(method='order', label="Order By")

    class Meta:
        model = Addon
        fields = {
            'type': ['exact'],  
            'name': ['exact', 'icontains'],
            'is_active': ['exact'],
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