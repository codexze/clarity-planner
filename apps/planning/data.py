import math, random, datetime
from faker import Faker
from apps.clients.models import Client
from apps.inhouse.models import Service, Staff
from .models import CalendarSettings, CalendarEventSlot, Appointment
from apps.authorize.models import User

fake = Faker()

def calendar_settings():
    def create(**kwargs):
        return CalendarEventSlot.objects.get_or_create(**kwargs)

    event1, _ = create(duration=datetime.time(0,5,0))
    event2, _ = create(duration=datetime.time(0,10,0))
    event3, _ = create(duration=datetime.time(0,15,0))
    event4, _ = create(duration=datetime.time(0,20,0))
    event5, _ = create(duration=datetime.time(0,25,0))
    event6, _ = create(duration=datetime.time(0,30,0))
    event7, _ = create(duration=datetime.time(0,35,0))
    event8, _ = create(duration=datetime.time(0,40,0))
    event9, _ = create(duration=datetime.time(0,45,0))
    event10, _ = create(duration=datetime.time(0,50,0))
    event11, _ = create(duration=datetime.time(0,55,0))
    event12, _ = create(duration=datetime.time(1,0,0))

    staff = Staff.objects.filter()

    for employee in staff:
        CalendarSettings.create_default_settings_for(employee)

def appointments(n=10):
    appointments = []
    for _ in range(n):
        # Get random instances of related models
        client = Client.objects.order_by("?").first()
        service = Service.objects.order_by("?").first()
        employee = Staff.objects.order_by("?").first()
        
        timestamp = fake.date_time_this_month(after_now=True)
        start = datetime.datetime(day=timestamp.day, month=timestamp.month, year=timestamp.year, hour=timestamp.hour, minute=(math.ceil(n / 5) * 5), second=0)
        end = start + datetime.timedelta(hours=service.duration.hour, minutes=service.duration.minute, seconds=service.duration.second )
        charges = service.price

        appointment = Appointment(client=client ,service=service ,employee=employee ,start=start ,end=end ,charges=charges)
        appointments.append(appointment)

    user = User.objects.get(username="super")
    created_appointments = Appointment.objects.bulk_create(appointments)
    for appointment in created_appointments:
        appointment.set_record(user, False)
    print(f"✅ CREATED {n} FAKE APPOINTMENTS!")