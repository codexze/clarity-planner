import datetime
from rest_framework import serializers

from apps.planning.models import Appointment, Reminder
from .models import Client, KnownAddress, Company

class GenderSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

class KnownAddressSerializer(serializers.ModelSerializer):
    last_appointment_date = serializers.DateTimeField(read_only=True)  # From annotation
    next_appointment_date = serializers.DateTimeField(read_only=True)  # From annotation

    class Meta:
        model = KnownAddress
        fields = ( 'id', 'address', 'is_active', 'last_appointment_date', 'next_appointment_date')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'address', 'email', 'phone', 'website', 'is_active')
    
class ClientSerializer(serializers.ModelSerializer):
    # Computed fields that don't hit database
    name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True) 
    display = serializers.CharField(read_only=True)

    # Use source fields instead of method fields to avoid N+1
    company_name = serializers.CharField(source='company.name', read_only=True)
    last_appointment_date = serializers.DateTimeField(read_only=True)  # From annotation
    next_appointment_date = serializers.DateTimeField(read_only=True)  # From annotation


    class Meta:
        model = Client
        fields = [
            "id", "name", "age", "display", 
            "last_appointment_date", "next_appointment_date", "known_addresses", 
            "company_name", "consistency_token", "created", "updated", 
            "first_name", "surname", "date_of_birth", "gender", 
            "email", "mobile", "is_active", 
            "created_by", "updated_by", "company"
        ]

class ClientDetailSerializer(ClientSerializer):
    """Serializer for detailed client view with related data"""
    known_addresses = KnownAddressSerializer(many=True, read_only=True)
    active_known_addresses = serializers.SerializerMethodField()
    company_details = CompanySerializer(source='company', read_only=True)
    
    class Meta(ClientSerializer.Meta):
        fields = ClientSerializer.Meta.fields + [
            'known_addresses', 'active_known_addresses', 'company_details'
        ]
    
    def get_active_known_addresses(self, obj):
        """Use prefetched known_addresses to avoid N+1"""
        active_addresses = [addr for addr in obj.known_addresses.all() if addr.is_active]
        return KnownAddressSerializer(active_addresses, many=True).data