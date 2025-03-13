import datetime, calendar
from django.db import models
from colorfield.fields import ColorField

from apps.core.models import *
from apps.authorize.models import User
from apps.clients.models import Client
from apps.inhouse.models import Service


DATE_FORMAT_REVERSED = "%Y-%m-%d"
WEEKDAY_FORMAT = "%A"

class CalendarEventSlot(models.Model):
    duration = models.TimeField()

    @property
    def title(self):
        title = ""
        if self.duration.hour > 0:
            title += f"{self.duration.hour} hour"

        if self.duration.minute > 0:
            title += f"{self.duration.minute} minutes"

        return title

    def __str__(self):
        return self.title

# See Fullcalendar view options
class CalendarViews(models.TextChoices):
    DAY = 'timeGridDay'
    WEEK = 'timeGridWeek'
    MONTH = 'dayGridMonth'

class CalendarSettings(Subrecord):
    default_view = models.CharField(default=CalendarViews.MONTH, choices=CalendarViews.choices)
    enable_weekends = models.BooleanField(default=False)
    business_hours = models.JSONField(default=list)
    event_slots = models.ManyToManyField(CalendarEventSlot)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    appointment_bgcolor = ColorField(default='#f58220')
    appointment_textcolor = ColorField(default='#ffffff')
    blocked_bgcolor = ColorField(default='#800080')
    blocked_textcolor = ColorField(default='#ffffff')
    processed_bgcolor = ColorField(default='#25408f')
    processed_textcolor = ColorField(default='#ffffff')
    arrived_bgcolor = ColorField(default='#93c842')
    arrived_textcolor = ColorField(default='#ffffff')

    @classmethod
    def default_hour_start(cls):
        return datetime.time(7)

    @classmethod
    def default_hour_end(cls):
        return datetime.time(20)

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
        
        events = CalendarEventSlot.objects.all()[:5]
        settings.event_slots.set(events)

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
    start = models.DateTimeField()
    end = models.DateTimeField()

    client = models.ForeignKey(Client, related_name='appointments', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='appointments', on_delete=models.PROTECT)
    charges = models.DecimalField(max_digits=10, decimal_places=2) # this save the price in time, useful for reporting
    employee = models.ForeignKey(User, related_name='appointments', on_delete=models.PROTECT)
    
    is_walkin = models.BooleanField(default=False) # tells us if it was a last minute booking, useful for reporting

    arrived = models.BooleanField(default=False)
    arrived_time = models.TimeField(null=True, blank=True) # helpfull to know

    cancelation = models.BooleanField(default=False) # helpfull to know
    cancelation_reason = models.CharField(max_length=255, null=True, blank=True) # helpfull to know
    processed = models.BooleanField(default=False, help_text=HELP_DP)

    def get_textcolor(self):
        if hasattr(self.employee, 'calendarsettings'):
            settings = self.employee.calendarsettings
            if self.processed:
                return settings.processed_textcolor
            elif self.arrived:
                return settings.arrived_textcolor

            return settings.appointment_textcolor

        return '#000000'
    
    def get_bgcolor(self):
        if hasattr(self.employee, 'calendarsettings'):
            settings = self.employee.calendarsettings
            if self.processed:
                return settings.processed_bgcolor
            elif self.arrived:
                return settings.arrived_bgcolor

            return settings.appointment_bgcolor

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
        return f"{self.client.name} ({self.service.type}) "
    
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
    
class Blocked(Slot, Subrecord):
    employee = models.ForeignKey(User, related_name='blocked', on_delete=models.CASCADE)
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

