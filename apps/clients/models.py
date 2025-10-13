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
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.unknown)
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
    
    # Optimized methods that work with prefetched data
    def get_last_appointment(self):
        """Use when appointments are prefetched to avoid DB hit"""
        today = datetime.date.today()
        appointments = [apt for apt in self.appointments.all() if apt.start.date() < today]
        if appointments:
            return max(appointments, key=lambda x: x.start)
        return None
    
    def get_next_appointment(self):
        """Use when appointments are prefetched to avoid DB hit"""
        today = datetime.date.today()
        appointments = [apt for apt in self.appointments.all() if apt.start.date() >= today]
        if appointments:
            return min(appointments, key=lambda x: x.start)
        return None
    
    def get_last_used_address_optimized(self):
        """Use when appointments are prefetched to avoid DB hit"""
        onsite_appointments = [apt for apt in self.appointments.all() if apt.is_onsite]
        if onsite_appointments:
            last_appointment = max(onsite_appointments, key=lambda x: x.start)
            return last_appointment.onsite_address
        return None
    
    def __str__(self):
        return self.display
    
class KnownAddress(models.Model):
    client = models.ForeignKey(Client, related_name='known_addresses', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) #switched off make address inactive and not in default filter

    def __str__(self):
        return f"{self.client.name} - {self.address}"
