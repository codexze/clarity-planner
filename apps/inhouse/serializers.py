from datetime import time
from rest_framework import serializers
from .models import ServiceType, Service, Staff, StaffService, Addon


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
    
class StaffServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffService
        fields = ['service_type', 'is_active']

class StaffSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        exclude = ['password', 'is_staff', 'is_superuser']
    
    def get_name(self, obj):
        """Fetches the property from the model"""
        return obj.name  
    
    def get_age(self, obj):
        """Fetches the property from the model"""
        return obj.age  
    
    def get_display(self, obj):
        """Fetches the property from the model"""
        return obj.display
    
    def get_services(self, obj):
        """Return array of ServiceType IDs for active staff services"""
        return list(obj.staffservice_set.filter(is_active=True).values_list('service_type_id', flat=True))
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

    def create(self, validated_data):
        # Extract services from initial_data since it's now a SerializerMethodField
        services_data = self.initial_data.get('services', [])
        
        # Create staff instance
        instance = super().create(validated_data)

        # Handle services if provided
        if services_data:
            # Create StaffService entries for each service ID
            for service_id in services_data:
                try:
                    service_type = ServiceType.objects.get(id=service_id)
                    StaffService.objects.create(staff=instance, service_type=service_type, is_active=True)
                except ServiceType.DoesNotExist:
                    continue

        return instance

    def update(self, instance, validated_data):
        # Extract services from initial_data since it's now a SerializerMethodField
        services_data = self.initial_data.get('services')
        
        # Update other staff fields
        instance = super().update(instance, validated_data)

        # Handle services update if provided
        if services_data is not None:
            # Get current active services
            current_services = set(instance.staffservice_set.filter(is_active=True).values_list('service_type_id', flat=True))
            
            # Convert new services to set (they're already IDs)
            new_services = set(int(service_id) for service_id in services_data if service_id)

            # Services to deactivate
            to_deactivate = current_services - new_services
            if to_deactivate:
                instance.staffservice_set.filter(service_type_id__in=to_deactivate).update(is_active=False)

            # Services to activate or create
            for service_type_id in new_services:
                StaffService.objects.update_or_create(
                    staff=instance,
                    service_type_id=service_type_id,
                    defaults={'is_active': True}
                )

        return instance
    
class AddonSerializer(serializers.ModelSerializer):
    additional_time = DurationField()  # Use custom field instead of TimeField
    time_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Addon
        fields = '__all__'

    def get_time_display(self, obj):    
        """Fetches the property from the model"""
        return obj.time_display
    
    
