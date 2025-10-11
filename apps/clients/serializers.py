import datetime
from rest_framework import serializers

from apps.planning.models import Appointment, Reminder
from .models import Client, KnownAddress, Company

class GenderSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

class KnownAddressSerializer(serializers.ModelSerializer):
    appointment = serializers.SerializerMethodField()
    class Meta:
        model = KnownAddress
        fields = ( 'id', 'address', 'is_active', 'appointment')

    def get_appointment(self, obj):
        """Fetches the most recent appointment associated with this address"""
        last_onsite_appointment = Appointment.objects.filter(client=obj.client, is_onsite=True, onsite_address=obj.id).order_by('-start').first()
        if last_onsite_appointment:
            return {"appointment_date": last_onsite_appointment.start.astimezone().date().isoformat(), "is_past": last_onsite_appointment.is_past, "is_future": last_onsite_appointment.is_future}
        next_onsite_appointment = Appointment.objects.filter(client=obj.client, is_onsite=True, onsite_address=obj.id, start__gte=datetime.datetime.now()).order_by('start').first()
        if next_onsite_appointment:
            return {"appointment_date": next_onsite_appointment.start.astimezone().date().isoformat(), "is_past": next_onsite_appointment.is_past, "is_future": next_onsite_appointment.is_future}
        return None

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'address', 'email', 'phone', 'website', 'is_active')
    
class ClientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    last_appointment = serializers.SerializerMethodField()
    next_appointment = serializers.SerializerMethodField()
    last_used_address = serializers.SerializerMethodField()
    known_addresses = serializers.SerializerMethodField()
    active_known_addresses = serializers.SerializerMethodField()
    company_details = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'
        
    def get_company_details(self, obj):
        """Returns the company details if the client is associated with one"""
        if obj.company:
            return CompanySerializer(obj.company).data
        return None

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
        return KnownAddressSerializer(obj.last_used_address).data
    
    def get_known_addresses(self, obj):
        """Fetches the property from the model"""
        return KnownAddressSerializer(obj.known_addresses, many=True).data
    
    def get_active_known_addresses(self, obj):
        """Fetches the property from the model"""
        return KnownAddressSerializer(obj.active_known_addresses, many=True).data
    
class AppointmentSerializer(serializers.ModelSerializer):  
    appointment_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()
    addons = serializers.SerializerMethodField()
    payment_amount = serializers.SerializerMethodField()
    is_future = serializers.SerializerMethodField()
    is_past = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = '__all__'

    def get_appointment_date(self, obj):
        """Returns the appointment date in YYYY-MM-DD format"""
        return obj.start.astimezone().date().isoformat()
    
    def get_start_time(self, obj):
        """Returns the start time in HH:mm format"""
        return obj.start.astimezone().strftime("%H:%M")
    
    def get_end_time(self, obj):
        """Returns the end time in HH:mm format"""
        return obj.end.astimezone().strftime("%H:%M")
    
    def get_client_name(self, obj):
        """Returns the client's full name"""
        return obj.client.display if obj.client else None
    
    def get_employee_name(self, obj):
        """Returns the employee's full name"""
        return obj.employee.name if obj.employee else None

    def get_service_name(self, obj):
        """Returns the service name"""
        return  obj.service.display if obj.service else None
    
    def get_addons(self, obj):
        return [addon.addon.name for addon in obj.addons] if obj.addons else []
    
    def get_payment_amount(self, obj):
        return obj.payment_amount
    
    def get_is_future(self, obj):
        return obj.is_future

    def get_is_past(self, obj):
        return obj.is_past

class ReminderSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Reminder
        fields = '__all__'

    def get_appointment_date(self, obj):
        """Returns the appointment date in YYYY-MM-DD format"""
        return obj.start.astimezone().date().isoformat()
    
    def get_start_time(self, obj):
        """Returns the start time in HH:mm format"""
        return obj.start.astimezone().strftime("%H:%M")
    
    def get_end_time(self, obj):
        """Returns the end time in HH:mm format"""
        return obj.end.astimezone().strftime("%H:%M")

    def get_icon(self, obj):
        """Fetches the property from the model"""
        return obj.icon

    def get_is_future(self, obj):
        return obj.is_future

    def get_is_past(self, obj):
        return obj.is_past
