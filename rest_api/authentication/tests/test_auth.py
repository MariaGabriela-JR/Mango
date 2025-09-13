from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from patients.models import Patient
from scientists.models import Scientist

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient_password = "patientpass123"
        self.scientist_password = "scientistpass123"

        # Criar paciente
        self.patient = Patient.objects.create_user(
            email="patient@example.com",
            password=self.patient_password,
            first_name="John",
            last_name="Doe",
            age=25,
            gender="M"
        )

        # Criar cientista
        self.scientist = Scientist.objects.create_user(
            email="scientist@example.com",
            password=self.scientist_password,
            first_name="Alice",
            last_name="Smith",
            institution="UTFPR",
            specialization="Neurociência",
            is_verified=True
        )

    def test_patient_login_success(self):
        """Paciente consegue logar e receber tokens JWT"""
        url = reverse("patient-login")
        response = self.client.post(url, {
            "email": self.patient.email,
            "password": self.patient_password
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertEqual(response.data["email"], self.patient.email)
        self.assertEqual(response.data["user_type"], "patient")

    def test_scientist_login_success(self):
        """Cientista consegue logar e receber tokens JWT"""
        url = reverse("scientist-login")
        response = self.client.post(url, {
            "email": self.scientist.email,
            "password": self.scientist_password
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertEqual(response.data["email"], self.scientist.email)
        self.assertEqual(response.data["user_type"], "scientist")

    def test_patient_wrong_password(self):
        """Paciente com senha incorreta não consegue logar"""
        url = reverse("patient-login")
        response = self.client.post(url, {
            "email": self.patient.email,
            "password": "wrongpassword"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_scientist_as_patient_login_fail(self):
        """Um cientista não pode logar no endpoint de paciente"""
        url = reverse("patient-login")
        response = self.client.post(url, {
            "email": self.scientist.email,
            "password": self.scientist_password
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
