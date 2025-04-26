from rest_framework import serializers
from .models import Gender, Client, KnownAddress

class GenderSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

class KnownAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnownAddress
        fields = '__all__'
    
class ClientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    last_appointment = serializers.SerializerMethodField()
    next_appointment = serializers.SerializerMethodField()
    last_used_address = serializers.SerializerMethodField()
    known_addresses = serializers.SerializerMethodField()
    active_known_addresses = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_name(self, obj):
        """Fetches the property from the model"""
        return obj.name  
    
    def get_age(self, obj):
        """Fetches the property from the model"""
        return obj.age  
    
    def get_display(self, obj):
        """Fetches the property from the model"""
        return obj.display
    
    def get_last_appointment(self, obj):
        """Fetches the property from the model"""
        if obj.last_appointment:
            return obj.last_appointment.start
        return None
    
    def get_next_appointment(self, obj):
        """Fetches the property from the model"""
        if obj.next_appointment:
            return obj.next_appointment.start
        return None
    
    def get_last_used_address(self, obj):
        """Fetches the property from the model"""
        return obj.last_used_address
    
    def get_known_addresses(self, obj):
        """Fetches the property from the model"""
        return KnownAddressSerializer(obj.known_addresses, many=True).data
    
    def get_active_known_addresses(self, obj):
        """Fetches the property from the model"""
        return KnownAddressSerializer(obj.active_known_addresses, many=True).data
    