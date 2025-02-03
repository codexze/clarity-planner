from decimal import Decimal
from datetime import time
from .models import ServiceType, Service, Addon

def services():

    PLACEHOLDER_TXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla porta mattis metus, nec consequat mauris malesuada venenatis."

    def create(**kwargs):
        return Service.objects.get_or_create(**kwargs)
    
    create(type=ServiceType.HAIR,       name="Wash & Dry",  description=PLACEHOLDER_TXT,    duration=time(0,45,0),  price=Decimal(10.00))
    create(type=ServiceType.MASSAGES,   name="Massage",     description=PLACEHOLDER_TXT,    duration=time(0,45,0),  price=Decimal(10.00))
    create(type=ServiceType.WAXING,     name="Waxing",      description=PLACEHOLDER_TXT,    duration=time(0,30,0),  price=Decimal(15.00))
    create(type=ServiceType.FACIALS,    name="Facial",      description=PLACEHOLDER_TXT,    duration=time(0,40,0),  price=Decimal(10.00))


    def create(**kwargs):
        return Addon.objects.get_or_create(**kwargs)
    
    create(type=ServiceType.WAXING,     name="Booty Facial",    additional_time=time(0,5,0),    price=Decimal(15.00))
    create(type=ServiceType.WAXING,     name="Vajacial",        additional_time=time(0,5,0),    price=Decimal(15.00))
    create(type=ServiceType.MASSAGES,   name="Full Face Wax",   additional_time=time(0,5,0),    price=Decimal(18.00))
