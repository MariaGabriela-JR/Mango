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

    def test_me_as_patient(self):
        """Paciente autenticado consegue acessar /me/"""
        login_url = reverse("patient-login")
        response = self.client.post(login_url, {
            "email": self.patient.email,
            "password": self.patient_password
        }, format="json")

        access_token = response.data["access"]

        me_url = reverse("me")
        response = self.client.get(me_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_type"], "patient")
        self.assertEqual(response.data["data"]["email"], self.patient.email)

    def test_me_as_scientist(self):
        """Cientista autenticado consegue acessar /me/"""
        login_url = reverse("scientist-login")
        response = self.client.post(login_url, {
            "email": self.scientist.email,
            "password": self.scientist_password
        }, format="json")

        access_token = response.data["access"]

        me_url = reverse("me")
        response = self.client.get(me_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_type"], "scientist")
        self.assertEqual(response.data["data"]["email"], self.scientist.email)

    def test_me_unauthorized(self):
        """Usuário não autenticado não consegue acessar /me/"""
        me_url = reverse("me")
        response = self.client.get(me_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def _get_tokens_for_user(self, user, password, login_url_name):
        """Função auxiliar para gerar tokens via login"""
        url = reverse(login_url_name)
        response = self.client.post(url, {"email": user.email, "password": password}, format="json")
        return response.data["access"], response.data["refresh"]
    
    def test_patient_logout_success(self):
        """Paciente consegue fazer logout e invalidar refresh token"""
        _, refresh_token = self._get_tokens_for_user(self.patient, self.patient_password, "patient-login")
        url = reverse("logout")
        response = self.client.post(url, {"refresh": refresh_token}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logout realizado com sucesso")

    def test_scientist_logout_success(self):
        """Cientista consegue fazer logout e invalidar refresh token"""
        _, refresh_token = self._get_tokens_for_user(self.scientist, self.scientist_password, "scientist-login")
        url = reverse("logout")
        response = self.client.post(url, {"refresh": refresh_token}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logout realizado com sucesso")

    def test_logout_without_token(self):
        """Logout sem enviar refresh token retorna erro"""
        url = reverse("logout")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Refresh token não fornecido", response.data["detail"])

    def test_logout_with_invalid_token(self):
        """Logout com token inválido retorna erro"""
        url = reverse("logout")
        response = self.client.post(url, {"refresh": "token_invalido"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Token inválido ou já expirado", response.data["detail"])