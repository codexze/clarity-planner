from rest_framework import serializers

from .models import CalendarEventSlot, CalendarSettings, Appointment, Blocked

class CalendarEventSlotSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()
    
    class Meta:
        model = CalendarEventSlot
        fields = '__all__'

class CalendarConfigSerializer(serializers.ModelSerializer):
    event_slots = CalendarEventSlotSerializer(many=True, read_only=True)
    
    class Meta:
        model = CalendarSettings
        fields = '__all__'

    def to_representation(self, instance):
        event_slots = CalendarEventSlotSerializer(instance.event_slots, many=True)

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
            'events': event_slots.data,
            'default_view': instance.default_view,
            'options': {
                # 'slotLabelInterval': 20,
                'slotMinTime': instance.current_day_hours[0],
                'slotMaxTime': instance.current_day_hours[1],
                # 'slotDuration': 20,
                
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
    onsite_address = serializers.SerializerMethodField()
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

    def get_onsite_address(self, obj):
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
        is_onsite = data.get('is_onsite', getattr(self.instance, 'is_onsite', False))
        
        # Get onsite_address from data or instance
        onsite_address = data.get('onsite_address', getattr(self.instance, 'onsite_address', None))
        print(onsite_address)
        # If is_onsite is True, onsite_address is required
        if is_onsite:
            if not onsite_address and not data.get('onsite_address_id'):
                raise serializers.ValidationError({
                    'onsite_address': 'This field is required when the appointment is registered as onsite.'
                })
                
        # If is_onsite is False, ensure onsite_address is None
        if not is_onsite:
            data['onsite_address'] = None
            
        return data

    def create(self, validated_data):
        # Ensure onsite_address is properly handled
        if not validated_data.get('is_onsite'):
            validated_data['onsite_address'] = None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure onsite_address is properly handled
        if not validated_data.get('is_onsite'):
            validated_data['onsite_address'] = None
        return super().update(instance, validated_data)
    

class BlockedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blocked
        fields = '__all__'

