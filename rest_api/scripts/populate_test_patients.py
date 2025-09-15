import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from patients.models import Patient

test_patients = [
    {"first_name": "Fulano", "last_name": "Silva", "email": "fulano1@teste.com", "age": 30, "gender": "male"},
    {"first_name": "Ciclano", "last_name": "Souza", "email": "ciclano2@teste.com", "age": 28, "gender": "female"},
    {"first_name": "Beltrano", "last_name": "Pereira", "email": "beltrano3@teste.com", "age": 35, "gender": "male"},
    {"first_name": "Maria", "last_name": "Oliveira", "email": "maria4@teste.com", "age": 40, "gender": "female"},
    {"first_name": "João", "last_name": "Martins", "email": "joao5@teste.com", "age": 50, "gender": "male"},
]

for data in test_patients:
    if not Patient.objects.filter(email=data["email"]).exists():
        Patient.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            age=data["age"],
            gender=data["gender"],
            is_test=True
        )

print("Pacientes de teste populados com sucesso!")