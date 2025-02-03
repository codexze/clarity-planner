from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Service
from .serializers import ServiceSerializer


class ServiceView(APIView):
    # permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request, service_id=None):
        """
        Retrieve a single service if service_id is provided,
        otherwise return all services.
        """
        if service_id:
            service = get_object_or_404(Service, id=service_id)
            serializer = ServiceSerializer(service)
        else:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new service"""
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, service_id):
        """Update an existing service"""
        service = get_object_or_404(Service, id=service_id)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_id):
        """Delete a service"""
        service = get_object_or_404(Service, id=service_id)
        service.delete()
        return Response({"message": "Service deleted successfully"}, status=status.HTTP_204_NO_CONTENT)