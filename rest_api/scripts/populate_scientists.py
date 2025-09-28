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
