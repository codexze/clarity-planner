from decimal import Decimal
from datetime import time
from .models import ServiceType, Service, Addon
from apps.authorize.models import User

def services():
    user = User.objects.get(username="super")

    def create(**kwargs):
        return ServiceType.objects.get_or_create(**kwargs)
    
    facials, _ = create(name="FACIALS")
    hair, _ = create(name="HAIR")
    makeup, _ = create(name="MAKEUP")
    massages, _ = create(name="MASSAGES")
    waxing, _ = create(name="WAXING")
    other, _ = create(name="OTHER")

    PLACEHOLDER_TXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla porta mattis metus, nec consequat mauris malesuada venenatis."

    def create(**kwargs):
        return Service.objects.get_or_create(**kwargs)
    
    service, _ = create(type=hair,       name="Wash & Dry",  description=PLACEHOLDER_TXT,    duration=time(0,45,0),  price=Decimal(10.00))
    service.set_record(user, False)
    service, _ = create(type=massages,   name="Relax Massage",     description=PLACEHOLDER_TXT,    duration=time(1,0,0),  price=Decimal(20.00))
    service.set_record(user, False)
    service, _ = create(type=massages,   name="Hot Stone Massage",     description=PLACEHOLDER_TXT,    duration=time(1,0,0),  price=Decimal(25.00))
    service.set_record(user, False)
    service, _ = create(type=waxing,     name="Bikini Waxing",      description=PLACEHOLDER_TXT,    duration=time(0,30,0),  price=Decimal(18.00))
    service.set_record(user, False)
    service, _ = create(type=waxing,     name="Brazilian Waxing",      description=PLACEHOLDER_TXT,    duration=time(0,30,0),  price=Decimal(18.00))
    service.set_record(user, False)
    service, _ = create(type=facials,    name="Facial",      description=PLACEHOLDER_TXT,    duration=time(0,40,0),  price=Decimal(10.00))
    service.set_record(user, False)


    def create(**kwargs):
        return Addon.objects.get_or_create(**kwargs)
    
    addon, _ = create(name="Booty Facial",    additional_time=time(0,5,0),    price=Decimal(15.00))
    addon.type.add(waxing)
    addon, _ = create(name="Vajacial",        additional_time=time(0,5,0),    price=Decimal(15.00))
    addon.type.add(waxing)
    addon, _ = create(name="Full Face Wax",   additional_time=time(0,5,0),    price=Decimal(18.00))
    addon.type.add(facials)

