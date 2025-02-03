import random
from faker import Faker
from .models import Client, Gender

fake = Faker()

def clients(n=10):
    clients = []
    for _ in range(n):
        client = Client(
            first_name=fake.first_name(),
            surname=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
            gender=random.choice([Gender.MALE, Gender.FEMALE, Gender.UNKNOWN]),
            emailaddress=fake.email() if random.choice([True, False]) else None,
            mobile=fake.phone_number() if random.choice([True, False]) else None,
        )
        clients.append(client)

    Client.objects.bulk_create(clients)
    print(f"✅ CREATED {n} FAKE CLIENTS!")
