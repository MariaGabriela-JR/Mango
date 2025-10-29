import os
import django
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest_api.settings")
django.setup()

from scientists.models import Scientist

DEFAULT_EMAIL = "scientist@default.com"
DEFAULT_PASSWORD = "12345678"

today = date.today()
min_birth_date = today - timedelta(days=365*25)

additional_scientists = [
    {
        "email": "marie.curie@science.com",
        "first_name": "Marie",
        "last_name": "Curie",
        "institution": "Universidade de Paris",
        "specialization": "Física e Química",
        "birth_date": date(1867, 11, 7)
    },
    {
        "email": "albert.einstein@science.com",
        "first_name": "Albert",
        "last_name": "Einstein",
        "institution": "Institute for Advanced Study",
        "specialization": "Física Teórica",
        "birth_date": date(1879, 3, 14)
    },
    {
        "email": "rosalind.franklin@science.com",
        "first_name": "Rosalind",
        "last_name": "Franklin",
        "institution": "King's College London",
        "specialization": "Química e Cristalografia",
        "birth_date": date(1920, 7, 25)
    },
    {
        "email": "nikola.tesla@science.com",
        "first_name": "Nikola",
        "last_name": "Tesla",
        "institution": "Tesla Electric Light & Manufacturing",
        "specialization": "Engenharia Elétrica",
        "birth_date": date(1856, 7, 10)
    },
    {
        "email": "ada.lovelace@science.com",
        "first_name": "Ada",
        "last_name": "Lovelace",
        "institution": "Universidade de Cambridge",
        "specialization": "Matemática e Computação",
        "birth_date": date(1815, 12, 10)
    },
    {
        "email": "stephen.hawking@science.com",
        "first_name": "Stephen",
        "last_name": "Hawking",
        "institution": "Universidade de Cambridge",
        "specialization": "Cosmologia",
        "birth_date": date(1942, 1, 8)
    },
    {
        "email": "jane.goodall@science.com",
        "first_name": "Jane",
        "last_name": "Goodall",
        "institution": "Jane Goodall Institute",
        "specialization": "Primatologia",
        "birth_date": date(1934, 4, 3)
    },
    {
        "email": "carl.sagan@science.com",
        "first_name": "Carl",
        "last_name": "Sagan",
        "institution": "Cornell University",
        "specialization": "Astronomia e Astrofísica",
        "birth_date": date(1934, 11, 9)
    }
]

if not Scientist.objects.filter(email=DEFAULT_EMAIL).exists():
    print("Creating standard scientist...")
    Scientist.objects.create_user(
        email=DEFAULT_EMAIL,
        password=DEFAULT_PASSWORD,
        first_name="Cientista",
        last_name="Padrão",
        institution="Instituto Inicial",
        specialization="Genética",
        birth_date=min_birth_date
    )
else:
    print("Standard scientist already exists!")

for scientist_data in additional_scientists:
    email = scientist_data["email"]
    if not Scientist.objects.filter(email=email).exists():
        print(f"Creating {scientist_data['first_name']} {scientist_data['last_name']}...")
        Scientist.objects.create_user(
            email=email,
            password=DEFAULT_PASSWORD,
            first_name=scientist_data["first_name"],
            last_name=scientist_data["last_name"],
            institution=scientist_data["institution"],
            specialization=scientist_data["specialization"],
            birth_date=scientist_data["birth_date"]
        )
    else:
        print(f"{scientist_data['first_name']} {scientist_data['last_name']} already exists!")

print("Population completed!")