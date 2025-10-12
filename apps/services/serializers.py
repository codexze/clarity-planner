from datetime import time
from rest_framework import serializers
from .models import ServiceType, Service, Addon


class DurationField(serializers.Field):
    """Custom field to convert between {hours, minutes} and TimeField."""
    
    def to_representation(self, value):
        """Convert TimeField value to { hours, minutes } format for output."""
        if value:
            return {"hours": value.hour, "minutes": value.minute}
        return {"hours": 0, "minutes": 0}

    def to_internal_value(self, data):
        """Convert { hours, minutes } input to a TimeField value."""
        if not isinstance(data, dict) or "hours" not in data or "minutes" not in data:
            raise serializers.ValidationError("Invalid format. Expected { hours: int, minutes: int }.")

        hours = data.get("hours", 0)
        minutes = data.get("minutes", 0)

        # Ensure values are within valid ranges
        if not (0 <= hours < 24) or not (0 <= minutes < 60):
            raise serializers.ValidationError("Hours must be 0-23 and minutes must be 0-59.")

        return time(hour=hours, minute=minutes)  # Converts to Python time object
    
class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name']

class ServiceSerializer(serializers.ModelSerializer):
    duration = DurationField()  # Use custom field instead of TimeField
    type = ServiceTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(source='type', queryset=ServiceType.objects.all(), write_only=True )
    time_display = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_time_display(self, obj):    
        """Fetches the property from the model"""
        return obj.time_display
    
class AddonSerializer(serializers.ModelSerializer):
    additional_time = DurationField()  # Use custom field instead of TimeField
    time_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Addon
        fields = '__all__'

    def get_time_display(self, obj):    
        """Fetches the property from the model"""
        return obj.time_display
    
    
