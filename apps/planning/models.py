import datetime, calendar
from django.db import models
from colorfield.fields import ColorField

from apps.core.models import *
from apps.authorize.models import User
from apps.clients.models import Client, KnownAddress
from apps.services.models import Service, Addon


DATE_FORMAT_REVERSED = "%Y-%m-%d"
WEEKDAY_FORMAT = "%A"
class CalendarViews(models.TextChoices):
    DAY = 'timeGridDay'
    WEEK = 'timeGridWeek'
    MONTH = 'dayGridMonth'

class CalendarSettings(Subrecord):
    default_view = models.CharField(max_length=20, default=CalendarViews.WEEK, choices=CalendarViews.choices)
    enable_weekends = models.BooleanField(default=False)
    business_hours = models.JSONField(default=list)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    inhouse_appointment_bgcolor = ColorField(default='#2b7fff')
    inhouse_appointment_textcolor = ColorField(default='#ffffff')
    onsite_appointment_bgcolor = ColorField(default='#4f39f6')
    onsite_appointment_textcolor = ColorField(default='#ffffff')

    blocked_bgcolor = ColorField(default='#fe9a00')
    blocked_textcolor = ColorField(default='#ffffff')
    reminder_bgcolor = ColorField(default='#8200db')
    reminder_textcolor = ColorField(default='#ffffff')
    
    processed_bgcolor = ColorField(default='#1c398e')
    processed_textcolor = ColorField(default='#ffffff')
    arrived_bgcolor = ColorField(default='#007a55')
    arrived_textcolor = ColorField(default='#ffffff')

    @classmethod
    def default_hour_start(cls):
        return datetime.time(5)

    @classmethod
    def default_hour_end(cls):
        return datetime.time(23)

    @classmethod
    def default_days(cls):
        return [
            (i + 1) % 7 for i, day in enumerate(calendar.day_name) if (i + 1) % 7 not in [6, 0]  # Exclude weekend days
        ]
    
    @property
    def current_day_hours(self):
        # Filter data based on the current day
        try:
            # Get the current weekday as an integer (0 for Monday, 6 for Sunday)
            current_day = datetime.date.today().weekday()
            today_hours = [
                {"hour_start": datetime.datetime.strptime(entry["hour_start"], "%H:%M:%S").time(), "hour_end": datetime.datetime.strptime(entry["hour_end"], "%H:%M:%S").time()} for entry in self.business_hours if current_day in entry["business_days"]
            ]

        except KeyError as e:
            raise ValueError(f"Invalid structure in business_hours: missing key {e}")
        except ValueError as e:
            raise ValueError(f"Error parsing time in business_hours: {e}")

        # Check if any hours are available for the current day
        if not today_hours:
            return self.default_hour_start(), self.default_hour_end()

        # Return the start and end times for the current day
        return today_hours[0]["hour_start"], today_hours[-1]["hour_end"]

    @classmethod
    def default_business_hours(cls):
        return [
            {
            'hour_start': cls.default_hour_start().strftime("%H:%M:%S"),
            'hour_end': cls.default_hour_end().strftime("%H:%M:%S"),
            'business_days' : cls.default_days()
            }
        ]
    
    @classmethod
    def create_default_settings_for(cls, user):
        settings, _ = cls.objects.get_or_create(
            user = user,
            business_hours=cls.default_business_hours()
        )
        return settings

    class Meta:
        verbose_name_plural = "calendar settings"

class Slot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
      ordering = ['start']

    @property
    def weekday(self):
        return self.start.strftime(WEEKDAY_FORMAT)

    @property
    def allday(self):
        return self.start.strftime(DATE_FORMAT_REVERSED)

    class Meta:
        abstract = True

class Appointment(Slot, Subrecord):
    HELP_DP    = "This field will be True if the data is processed."

    client = models.ForeignKey(Client, related_name='appointments', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='appointments', on_delete=models.PROTECT)
    service_price = models.DecimalField(max_digits=10, decimal_places=2) 
    employee = models.ForeignKey(User, related_name='appointments', on_delete=models.PROTECT)

    notes = models.TextField(null=True, blank=True)
    
    is_onsite = models.BooleanField(default=False)
    onsite_address = models.ForeignKey(KnownAddress, related_name='appointments', on_delete=models.PROTECT, null=True, blank=True)

    arrived = models.BooleanField(default=False)
    arrived_time = models.TimeField(null=True, blank=True)
    cancelation = models.BooleanField(default=False)
    cancelation_reason = models.CharField(max_length=255, null=True, blank=True)
    processed = models.BooleanField(default=False, help_text=HELP_DP)

    def __str__(self):
        return f"{self.client} - {self.service} on {self.start}"

    def get_textcolor(self):
        if hasattr(self.employee, 'calendarsettings'):
            settings = self.employee.calendarsettings

            if self.processed:
                return settings.processed_textcolor
            elif self.arrived:
                return settings.arrived_textcolor
            elif self.is_onsite:
                return settings.onsite_appointment_textcolor
            return settings.inhouse_appointment_textcolor

        return '#000000'
    
    def get_bgcolor(self):
        if hasattr(self.employee, 'calendarsettings'):
            settings = self.employee.calendarsettings

            if self.processed:
                return settings.processed_bgcolor
            elif self.arrived:
                return settings.arrived_bgcolor
            elif self.is_onsite:
                return settings.onsite_appointment_bgcolor
            return settings.inhouse_appointment_bgcolor

        return '#f58220'
    
    @property
    def resourceId(self):
        return 'appointmentSlot'
    
    @property
    def textColor(self):
        return self.get_textcolor()
    
    @property
    def color(self):
        return self.get_bgcolor()

    @property
    def title(self):
        return f"{self.client.name} - {self.service.type}"
    
    @property
    def addons(self):
        return self.appointment_addons.all()
    
    @property
    def payment_amount(self):
        pay = self.service_price
        if self.addons:
            for addon in self.addons:
                pay += addon.addon_price
        return pay

    @property
    def is_past(self):
        return datetime.date.today() > self.start.date()

    @property
    def is_future(self):
        return datetime.date.today() < self.start.date()
    
    @property
    def can_change_arrival(self):
        # todo check if between business hours?
        if self.is_past:
            return False
        
        if self.is_future:
            return False

        return True
    
    def update_arrived(self, user):
        self.arrived = False if self.arrived else True
        self.arrived_time = datetime.datetime.now() if self.arrived else None
        self.set_records(user)
        return self
    
    @property
    def can_change_processed(self):
        if self.is_future:
            return False

        if not self.arrived:
            return False

        return True
    
class AppointmentAddon(models.Model):
    appointment = models.ForeignKey(Appointment, related_name="appointment_addons", on_delete=models.CASCADE)
    addon = models.ForeignKey(Addon, related_name="appointment_addons", on_delete=models.PROTECT)
    addon_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.addon.name} - {self.addon_price}"
    
class BlockedTime(Slot, Subrecord):
    employee = models.ForeignKey(User, related_name='blocked', on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    reason = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "blocked"

    def get_bgcolor(self):
        if hasattr(self.employee, 'calendarsettings'):
            settings = self.employee.calendarsettings
            return settings.blocked_bgcolor

        return '#800080'

    def get_textcolor(self):
        if hasattr(self.employee, 'calendarsettings'):
            settings = self.employee.calendarsettings
            return settings.blocked_textcolor
        return '#ffffff'
    
    @property
    def resourceId(self):
        return 'blockedSlot'

    @property
    def constraint(self):
        return 'businessHours'

    @property
    def textColor(self):
        return self.get_textcolor()

    @property
    def color(self):
        return self.get_bgcolor()

    @property
    def title(self):
        return self.reason

    @property
    def is_past(self):
        return datetime.date.today() > self.start.date()
    
class ReminderReason(models.TextChoices):
    birthday = "BIRTHDAY"
    anniversary = "ANNIVERSARY"
    graduation = "GRADUATION"
    other = "OTHER"

class Reminder(Slot, Subrecord):
    global_reminder = models.BooleanField(default=False)
    employee = models.ForeignKey(User, blank=True, null=True, related_name='reminders', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='reminder', on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=ReminderReason.choices, default=ReminderReason.other)
    other_reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "reminders"

    def get_icon(self):
        icons = {
            ReminderReason.birthday: ['fas', 'cake-candles'],
            ReminderReason.anniversary: ['fas', 'champagne-glasses'],
            ReminderReason.graduation: ['fas', 'graduation-cap'],
            ReminderReason.other: ['fas', 'bell']
        }
        return icons.get(self.reason, ['fas', 'bell'])

    def get_bgcolor(self):
        if self.employee and hasattr(self.employee, 'calendarsettings'):
            settings = self.employee.calendarsettings
            return settings.reminder_bgcolor

        return '#8200db'

    def get_textcolor(self):
        if self.employee and hasattr(self.employee, 'calendarsettings'):
            settings = self.employee.calendarsettings
            return settings.reminder_textcolor
        return '#ffffff'

    @property
    def resourceId(self):
        return 'reminderSlot'
    
    @property
    def textColor(self):
        return self.get_textcolor()
    
    @property
    def color(self):
        return self.get_bgcolor()

    @property
    def icon(self):
        return self.get_icon()
    
    @property
    def title(self):
        return f'{self.client.name}'
    
    @property
    def all_day(self):
        return True

    @property
    def is_past(self):
        return datetime.date.today() > self.start.date()

    @property
    def is_future(self):
        return datetime.date.today() < self.start.date()

