import datetime
from django.db import models

from apps.core.models import *

class Gender(models.TextChoices):
    MALE = "MALE"
    FEMALE = "FEMALS"
    UNKNOWN = "UNKNOWN"

class Client(Subrecord):
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=Gender.choices, default=Gender.UNKNOWN)
    emailaddress = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True) #switched off make client inactive and not in default filter

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
    
    def __str__(self):
        return self.display
