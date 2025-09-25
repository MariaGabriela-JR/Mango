from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from patients.models import Patient
from scientists.models import Scientist
from datetime import date, timedelta

class PatientTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient_password = "patientpass123"
        self.scientist_password = "scientistpass123"

        # Criar um cientista
        self.scientist = Scientist.objects.create_user(
            email="scientist@example.com",
            password=self.scientist_password,
            first_name="Alice",
            last_name="Smith",
            institution="UTFPR",
            specialization="Neurociência",
            is_verified=True
        )

        # Criar paciente vinculado ao cientista
        self.patient = Patient.objects.create_user(
            cpf="12345678901",
            password=self.patient_password,
            first_name="John",
            last_name="Doe",
            birth_date=date(1998, 5, 15),
            gender="M",
            scientist=self.scientist
        )

    def test_create_patient(self):
        """Criação de paciente via endpoint"""
        url = reverse("patient-register")
        data = {
            "cpf": "98765432100",
            "password": "SenhaForte123!",
            "first_name": "Novo",
            "last_name": "Paciente",
            "birth_date": "1995-03-20"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("cpf", response.data)
        self.assertEqual(response.data["cpf"], "98765432100")
        self.assertIn("age", response.data)
        self.assertNotIn("password", response.data)

    def test_create_patient_with_invalid_cpf(self):
        """Tentativa de criar paciente com CPF inválido"""
        url = reverse("patient-register")
        data = {
            "cpf": "123",  # CPF inválido
            "password": "SenhaForte123!",
            "first_name": "Teste",
            "last_name": "Paciente"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cpf", response.data)

    def test_create_patient_with_duplicate_cpf(self):
        """Tentativa de criar paciente com CPF duplicado"""
        url = reverse("patient-register")
        data = {
            "cpf": "12345678901",  # CPF já usado no setUp
            "password": "SenhaForte123!",
            "first_name": "Teste",
            "last_name": "Paciente"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cpf", response.data)

    def test_complete_profile_fail(self):
        """Atualização de perfil sem birth_date/gender deve falhar"""
        patient = Patient.objects.create_user(
            cpf="11122233344",
            password="Senha123!",
            first_name="Teste",
            last_name="Paciente"
        )
        self.client.force_authenticate(user=patient)
        url = reverse("patient-complete-profile")
        response = self.client.put(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_complete_profile_success(self):
        """Completar perfil com birth_date/gender deve passar"""
        patient = Patient.objects.create_user(
            cpf="55566677788",
            password="Senha123!",
            first_name="Teste",
            last_name="Paciente"
        )
        self.client.force_authenticate(user=patient)
        url = reverse("patient-complete-profile")
        data = {
            "birth_date": "1990-08-10",
            "gender": "F"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["birth_date"], "1990-08-10")
        self.assertEqual(response.data["gender"], "F")
        self.assertIn("age", response.data)  # Idade calculada automaticamente

    def test_age_calculation(self):
        """Verifica se a idade é calculada corretamente"""
        # Paciente com 25 anos
        birth_date = date.today() - timedelta(days=25*365 + 100)  # 25 anos + 100 dias
        patient = Patient.objects.create_user(
            cpf="99988877766",
            password="Senha123!",
            first_name="Teste",
            last_name="Idade",
            birth_date=birth_date
        )
        
        self.assertEqual(patient.age, 25)  # Propriedade calculada

    def test_patient_list_for_scientist(self):
        """Lista pacientes vinculados ao cientista"""
        self.client.force_authenticate(user=self.scientist)
        url = reverse("patient-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
        # Verifica se a idade calculada está presente
        if len(response.data) > 0:
            self.assertIn("age", response.data[0])

    def test_link_patient_to_scientist(self):
        """Vincula paciente disponível a cientista"""
        available_patient = Patient.objects.create_user(
            cpf="44455566677",
            password="Senha123!"
        )
        self.client.force_authenticate(user=self.scientist)
        url = reverse("link-patient", kwargs={"pk": available_patient.id})
        response = self.client.patch(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["scientist"], self.scientist.id)

    def test_check_session_eligibility(self):
        """Verifica elegibilidade do paciente para sessão"""
        self.client.force_authenticate(user=self.patient)
        url = reverse("check-eligibility")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("eligible", response.data)
        self.assertIn("patient_data", response.data)
        self.assertIn("calculated_age", response.data)  # Nova informação
        self.assertEqual(response.data["calculated_age"], self.patient.age)

    def test_patient_with_future_birth_date(self):
        """Tentativa de criar paciente com data de nascimento no futuro"""
        url = reverse("patient-register")
        future_date = (date.today() + timedelta(days=365)).isoformat()
        data = {
            "cpf": "12131415161",
            "password": "SenhaForte123!",
            "first_name": "Teste",
            "last_name": "Futuro",
            "birth_date": future_date
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birth_date", response.data)

    def test_patient_serializer_includes_age(self):
        """Verifica se o serializer inclui a idade calculada"""
        patient = Patient.objects.create_user(
            cpf="77788899900",
            password="Senha123!",
            first_name="Teste",
            last_name="Serializer",
            birth_date=date(1985, 12, 1)
        )
        
        from patients.serializers import PatientSerializer
        serializer = PatientSerializer(patient)
        self.assertIn("age", serializer.data)
        self.assertEqual(serializer.data["age"], patient.age)

    def test_cpf_normalization(self):
        """Verifica se o CPF é normalizado (remove formatação)"""
        url = reverse("patient-register")
        data = {
            "cpf": "123.456.789-00",  # CPF formatado
            "password": "SenhaForte123!",
            "first_name": "Teste",
            "last_name": "CPF Formatado"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Deve salvar sem formatação
        self.assertEqual(response.data["cpf"], "12345678900")

    def test_patient_str_representation(self):
        """Verifica a representação em string do paciente"""
        patient = Patient.objects.create_user(
            cpf="33322211100",
            password="Senha123!",
            first_name="Maria",
            last_name="Silva"
        )
        self.assertIn(patient.cpf, str(patient))
        self.assertIn(patient.patient_iid, str(patient))