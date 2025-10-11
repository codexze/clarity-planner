import datetime
from django.db import models

from apps.core.models import *

class Gender(models.TextChoices):
    male = "MALE"
    female = "FEMALE"
    unknown = "UNKNOWN"

class Company(Subrecord):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True) #switched off make company inactive and not in default filter

    def __str__(self):
        return self.name

class Client(Subrecord):
    company = models.ForeignKey(Company, blank=True, null=True, related_name='clients', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=Gender.choices, default=Gender.unknown)
    email = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True) #switched off make client inactive and not in default filter

    @property
    def name(self):
        return f"{self.first_name} {self.surname}"
    
    @property
    def age(self):
        today = datetime.date.today()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
    @property
    def display(self):
        return f"{self.name} ({self.age}Y)"
    
    @property
    def last_appointment(self):
        today = datetime.date.today()
        return self.appointments.filter(start__date__lt=today).order_by('-start').first()
    
    @property
    def next_appointment(self):
        today = datetime.date.today()
        return self.appointments.filter(start__date__gte=today).order_by('-start').first()
    
    @property
    def last_used_address(self):
        last_onsite_appointment = self.appointments.filter(is_onsite=True).order_by('-start').first()
        if last_onsite_appointment:
            return last_onsite_appointment.onsite_address
        return None
    
    @property
    def known_addresses(self):
        return self.known_addresses.filter()
    
    @property
    def active_known_addresses(self):
        return self.known_addresses.filter(is_active=True)
    
    def get_appointments(self):
        return self.appointments.all()
    
    def __str__(self):
        return self.display
    
class KnownAddress(models.Model):
    client = models.ForeignKey(Client, related_name='known_addresses', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) #switched off make address inactive and not in default filter

    def __str__(self):
        return f"{self.client.name} - {self.address}"
