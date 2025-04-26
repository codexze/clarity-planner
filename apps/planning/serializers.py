from rest_framework import serializers

from apps.clients.serializers import ClientSerializer
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

    class Meta:
        model = Appointment
        fields = '__all__'

    def get_title(self, obj):
        """Fetches the property from the model"""
        return obj.title  
    
    def get_backgroundColor(self, obj):
        return obj.color
    
    def get_borderColor(self, obj):
        return obj.color
    
    def get_textColor(self, obj):
        return obj.textColor
    

class BlockedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blocked
        fields = '__all__'

