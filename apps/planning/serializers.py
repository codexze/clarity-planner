from rest_framework import serializers

from .models import CalendarSettings, Appointment, BlockedTime, Reminder

class CalendarConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarSettings
        fields = '__all__'

    def to_representation(self, instance):
        business_hours = []
        for business_hour in instance.business_hours:
            business_hours.append({
                'daysOfWeek': business_hour['business_days'],
                'startTime': business_hour['hour_start'],
                'endTime': business_hour['hour_end']
            })

        return {
            'colors': {
                'INHOUSE' : instance.inhouse_appointment_bgcolor,
                'ONSITE' : instance.onsite_appointment_bgcolor,
                'BLOCKED' : instance.blocked_bgcolor,
                'REMINDER' : instance.reminder_bgcolor,
                'PROCESSED' : instance.processed_bgcolor,
                'ARRIVED' : instance.arrived_bgcolor,
            },
            'slot': {
                'INTERVAL': 5,
                'MIN': instance.current_day_hours[0],
                'MAX': instance.current_day_hours[1],
            },
            'default_view': instance.default_view,
            'options': {
                'slotMinTime': instance.current_day_hours[0],
                'slotMaxTime': instance.current_day_hours[1],
                
                'businessHours': business_hours
            }
        }
    
class AppointmentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    backgroundColor = serializers.SerializerMethodField()
    borderColor = serializers.SerializerMethodField()
    textColor = serializers.SerializerMethodField()
    addons = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    onsite_address_details = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()
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

    def get_onsite_address_details(self, obj):
        return obj.onsite_address.address if obj.onsite_address else None

    def get_title(self, obj):
        """Fetches the property from the model"""
        return obj.title

    def get_client_name(self, obj):
        """Returns the client's full name"""
        return obj.client.display if obj.client else None
    
    def get_employee_name(self, obj):
        """Returns the employee's full name"""
        return obj.employee.name if obj.employee else None

    def get_service_name(self, obj):
        """Returns the service name"""
        return  obj.service.display if obj.service else None

    def get_is_future(self, obj):
        return obj.is_future

    def get_is_past(self, obj):
        return obj.is_past

    def get_backgroundColor(self, obj):
        return obj.color
    
    def get_borderColor(self, obj):
        return obj.color
    
    def get_textColor(self, obj):
        return obj.textColor
    
    def get_addons(self, obj):
        return [addon.addon.id for addon in obj.addons] if obj.addons else []

    def validate(self, data):
        # Get is_onsite from data or instance
        is_onsite = data.get('is_onsite', False)
        
        # Get onsite_address from data or instance
        onsite_address = data.get('onsite_address', None)

        # If is_onsite is True, onsite_address is required
        if is_onsite and not onsite_address:
            raise serializers.ValidationError({
                'onsite_address': 'This field is required when the appointment is registered as onsite.'
            })
                
        # If is_onsite is False, ensure onsite_address is None
        if not is_onsite:
            data['onsite_address'] = None
            
        return data
    

class BlockedTimeSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    backgroundColor = serializers.SerializerMethodField()
    borderColor = serializers.SerializerMethodField()
    textColor = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = BlockedTime
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

    def get_title(self, obj):
        """Fetches the property from the model"""
        return obj.title

    def get_is_future(self, obj):
        return obj.is_future

    def get_is_past(self, obj):
        return obj.is_past

    def get_backgroundColor(self, obj):
        return obj.color
    
    def get_borderColor(self, obj):
        return obj.color
    
    def get_textColor(self, obj):
        return obj.textColor
    
class ReminderSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    backgroundColor = serializers.SerializerMethodField()
    borderColor = serializers.SerializerMethodField()
    textColor = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    isAllDay = serializers.ReadOnlyField(source='all_day')

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
    
    def get_title(self, obj):
        """Fetches the property from the model"""
        return obj.title

    def get_is_all_day(self, obj):
        return obj.all_day

    def get_is_future(self, obj):
        return obj.is_future

    def get_is_past(self, obj):
        return obj.is_past

    def get_backgroundColor(self, obj):
        return obj.color
    
    def get_borderColor(self, obj):
        return obj.color
    
    def get_textColor(self, obj):
        return obj.textColor

    

        
