import random
from faker import Faker
from .models import Company, Client, Gender
from apps.authorize.models import User

fake = Faker()

def companies(n=15):
    companies = []
    for _ in range(n):
        company = Company(
            name=fake.company(),
            address=fake.address(),
            email=fake.company_email(),
            phone=fake.phone_number(),
            website=fake.url(),
        )
        companies.append(company)

    user = User.objects.get(username="super")
    created_companies = Company.objects.bulk_create(companies)
    for company in created_companies:
        company.set_record(user, False)
    print(f"✅ CREATED {n} FAKE COMPANIES!")

def clients(n=10):
    clients = []
    for _ in range(n):
        company_choices = list(Company.objects.all())
        company = random.choice(company_choices) if company_choices and random.choice([True, False]) else None
        client = Client(
            company=company,
            first_name=fake.first_name(),
            surname=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
            gender=random.choice([Gender.male, Gender.female, Gender.unknown]),
        )
        clients.append(client)

    user = User.objects.get(username="super")
    created_clients = Client.objects.bulk_create(clients)
    for client in created_clients:
        client.set_record(user, False)
    print(f"✅ CREATED {n} FAKE CLIENTS!")
