import os
import django
import sys
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

try:
    django.setup()
    print("Django configurated with success")
except Exception as e:
    print(f"Error on configurating Django: {e}")
    sys.exit(1)

from patients.models import Patient

test_patients = [
    {
        "first_name": "Fulano", 
        "last_name": "Silva", 
        "cpf": "12345678901",
        "birth_date": "1993-05-15",
        "gender": "male"
    },
    {
        "first_name": "Ciclano", 
        "last_name": "Souza", 
        "cpf": "23456789012",
        "birth_date": "1995-08-20",
        "gender": "female"
    },
    {
        "first_name": "Beltrano", 
        "last_name": "Pereira", 
        "cpf": "34567890123",
        "birth_date": "1988-03-10",
        "gender": "male"
    },
]

print("Starting the script of populating test patients...")

for i, data in enumerate(test_patients, 1):
    try:
        print(f"Processing patient... {i}/{[len(test_patients)]}: {data['first_name']} {data['last_name']}")
        
        if Patient.objects.filter(cpf=data["cpf"]).exists():
            print(f"Patient {data['cpf']} already exists, skipping...")
            continue
        
        # Converte string para date
        birth_date = data["birth_date"]
        if isinstance(birth_date, str):
            from datetime import datetime
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        
        patient = Patient.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            cpf=data["cpf"],
            birth_date=birth_date,
            gender=data["gender"],
            is_test=True
        )
        
        print(f"Patient created: {patient.patient_iid} (CPF: {patient.cpf}, Idade: {patient.age})")
        
    except Exception as e:
        print(f"Error on creating patient: {data['cpf']}: {e}")

print("Populating patients done!")
print(f"Total of patients on database: {Patient.objects.count()}")