from decimal import Decimal
from datetime import time
from .models import ServiceType, Service, Addon
from apps.authorize.models import User

def services():

    user = User.objects.get(username="super")
    PLACEHOLDER_TXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla porta mattis metus, nec consequat mauris malesuada venenatis."

    def create(**kwargs):
        return Service.objects.get_or_create(**kwargs)
    
    service, _ = create(type=ServiceType.hair,       name="Wash & Dry",  description=PLACEHOLDER_TXT,    duration=time(0,45,0),  price=Decimal(10.00))
    service.set_record(user, False)
    service, _ = create(type=ServiceType.massages,   name="Relax Massage",     description=PLACEHOLDER_TXT,    duration=time(1,0,0),  price=Decimal(20.00))
    service.set_record(user, False)
    service, _ = create(type=ServiceType.massages,   name="Hot Stone Massage",     description=PLACEHOLDER_TXT,    duration=time(1,0,0),  price=Decimal(25.00))
    service.set_record(user, False)
    service, _ = create(type=ServiceType.waxing,     name="Bikini Waxing",      description=PLACEHOLDER_TXT,    duration=time(0,30,0),  price=Decimal(18.00))
    service.set_record(user, False)
    service, _ = create(type=ServiceType.waxing,     name="Brazilian Waxing",      description=PLACEHOLDER_TXT,    duration=time(0,30,0),  price=Decimal(18.00))
    service.set_record(user, False)
    service, _ = create(type=ServiceType.facials,    name="Facial",      description=PLACEHOLDER_TXT,    duration=time(0,40,0),  price=Decimal(10.00))
    service.set_record(user, False)


    def create(**kwargs):
        return Addon.objects.get_or_create(**kwargs)
    
    create(type=ServiceType.waxing,     name="Booty Facial",    additional_time=time(0,5,0),    price=Decimal(15.00))
    create(type=ServiceType.waxing,     name="Vajacial",        additional_time=time(0,5,0),    price=Decimal(15.00))
    create(type=ServiceType.facials,   name="Full Face Wax",   additional_time=time(0,5,0),    price=Decimal(18.00))

