import random
from faker import Faker
from .models import Client, Gender
from apps.authorize.models import User

fake = Faker()

def clients(n=10):
    clients = []
    for _ in range(n):
        client = Client(
            first_name=fake.first_name(),
            surname=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
            gender=random.choice([Gender.male, Gender.female, Gender.unknown]),
            emailaddress=fake.email() if random.choice([True, False]) else None,
            mobile=fake.phone_number() if random.choice([True, False]) else None,
        )
        clients.append(client)

    user = User.objects.get(username="super")
    created_clients = Client.objects.bulk_create(clients)
    for client in created_clients:
        client.set_record(user, False)
    print(f"✅ CREATED {n} FAKE CLIENTS!")
