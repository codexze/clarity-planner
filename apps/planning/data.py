import math, random, datetime
from faker import Faker
from apps.clients.models import Client
from apps.employees.models import  Employee
from apps.services.models import Service
from .models import CalendarSettings, Appointment
from apps.authorize.models import User

fake = Faker()

def calendar_settings():
    for employee in Employee.objects.all():
        if not hasattr(employee, 'calendarsettings'):
            settings = CalendarSettings.create_default_settings_for(employee)
            settings.save()

def appointments(n=20):
    appointments = []
    for _ in range(n):
        # Get random instances of related models
        client = Client.objects.order_by("?").first()
        service = Service.objects.order_by("?").first()
        employee = Employee.objects.order_by("?").first()
        
        timestamp = fake.date_time_this_month(after_now=True)
        start = datetime.datetime(day=timestamp.day, month=timestamp.month, year=timestamp.year, hour=timestamp.hour, minute=(math.ceil(n / 5) * 5), second=0)
        end = start + datetime.timedelta(hours=service.duration.hour, minutes=service.duration.minute, seconds=service.duration.second )
        price = service.price

        appointment = Appointment(client=client ,service=service ,employee=employee ,start=start ,end=end ,service_price=price)
        appointments.append(appointment)

    user = User.objects.get(username="super")
    created_appointments = Appointment.objects.bulk_create(appointments)
    for appointment in created_appointments:
        appointment.set_record(user, False)
    print(f"✅ CREATED {n} FAKE APPOINTMENTS!")