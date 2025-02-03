from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Gender, Client
from .serializers import GenderSerializer, ClientSerializer


class GenderView(APIView):
    # permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request, gender_value=None):
        """
        Retrieve a single gender if gender_value is provided,
        otherwise return all genders.
        """
        if gender_value:
            serializer_data = GenderSerializer.get_choice(gender_value)
            if not serializer_data:
                return Response({"error": "Gender not found"}, status=404)
        else:
            serializer_data = GenderSerializer.get_choices()
        
        return Response(serializer_data, status=status.HTTP_200_OK)
    
class ClientView(APIView):
    # permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request, client_id=None):
        """
        Retrieve a single client if client_id is provided,
        otherwise return all clients.
        """
        if client_id:
            client = get_object_or_404(Client, id=client_id)
            serializer = ClientSerializer(client)
        else:
            clients = Client.objects.all()
            serializer = ClientSerializer(clients, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new client"""
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, client_id):
        """Update an existing client"""
        client = get_object_or_404(Client, id=client_id)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, client_id):
        """Delete a client"""
        client = get_object_or_404(Client, id=client_id)
        client.delete()
        return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
