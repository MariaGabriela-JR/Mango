from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from patients.models import Patient
from scientists.models import Scientist

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
            email="patient@example.com",
            password=self.patient_password,
            first_name="John",
            last_name="Doe",
            age=25,
            gender="M",
            scientist=self.scientist
        )

    def test_create_patient(self):
        """Criação de paciente via endpoint"""
        url = reverse("patient-register")
        data = {
            "email": "novo_patient@example.com",
            "password": "SenhaForte123!",
            "first_name": "Novo",
            "last_name": "Paciente"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], data["email"])
        self.assertNotIn("password", response.data)

    def test_complete_profile_fail(self):
        """Atualização de perfil sem age/gender deve falhar"""
        patient = Patient.objects.create_user(
            email="incompleto@example.com",
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
        """Completar perfil com age/gender deve passar"""
        patient = Patient.objects.create_user(
            email="completo@example.com",
            password="Senha123!",
            first_name="Teste",
            last_name="Paciente"
        )
        self.client.force_authenticate(user=patient)
        url = reverse("patient-complete-profile")
        data = {"age": 30, "gender": "F"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["age"], 30)
        self.assertEqual(response.data["gender"], "F")

    def test_patient_list_for_scientist(self):
        """Lista pacientes vinculados ao cientista"""
        self.client.force_authenticate(user=self.scientist)
        url = reverse("patient-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_link_patient_to_scientist(self):
        """Vincula paciente disponível a cientista"""
        available_patient = Patient.objects.create_user(
            email="disponivel@example.com",
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