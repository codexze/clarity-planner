from datetime import time
from rest_framework import serializers
from .models import ServiceType, Employee, EmployeeService

class EmployeeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeService
        fields = ['service_type', 'is_active']

class EmployeeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()

    class Meta:
        model = Employee
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
        """Return array of ServiceType IDs for active employee services"""
        return list(obj.employeeservice_set.filter(is_active=True).values_list('service_type_id', flat=True))
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

    def create(self, validated_data):
        # Extract services from initial_data since it's now a SerializerMethodField
        services_data = self.initial_data.get('services', [])
        
        # Create employee instance
        instance = super().create(validated_data)

        # Handle services if provided
        if services_data:
            # Create EmployeeService entries for each service ID
            for service_id in services_data:
                try:
                    service_type = ServiceType.objects.get(id=service_id)
                    EmployeeService.objects.create(employee=instance, service_type=service_type, is_active=True)
                except ServiceType.DoesNotExist:
                    continue

        return instance

    def update(self, instance, validated_data):
        # Extract services from initial_data since it's now a SerializerMethodField
        services_data = self.initial_data.get('services')
        
        # Update other employee fields
        instance = super().update(instance, validated_data)

        # Handle services update if provided
        if services_data is not None:
            # Get current active services
            current_services = set(instance.employeeservice_set.filter(is_active=True).values_list('service_type_id', flat=True))
            
            # Convert new services to set (they're already IDs)
            new_services = set(int(service_id) for service_id in services_data if service_id)

            # Services to deactivate
            to_deactivate = current_services - new_services
            if to_deactivate:
                instance.employeeservice_set.filter(service_type_id__in=to_deactivate).update(is_active=False)

            # Services to activate or create
            for service_type_id in new_services:
                EmployeeService.objects.update_or_create(
                    employee=instance,
                    service_type_id=service_type_id,
                    defaults={'is_active': True}
                )

        return instance
