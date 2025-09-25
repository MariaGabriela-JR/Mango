from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from patients.models import Patient
from scientists.models import Scientist
from datetime import date, timedelta

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient_password = "patientpass123"
        self.scientist_password = "scientistpass123"

        # Criar paciente
        self.patient = Patient.objects.create_user(
            cpf="12345678901",
            password=self.patient_password,
            first_name="John",
            last_name="Doe",
            birth_date=date.today() - timedelta(days=25*365),  # 25 anos
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

    # -------------------- LOGIN TESTS --------------------
    def test_patient_login_success(self):
        url = reverse("patient-login")
        response = self.client.post(url, {
            "cpf": self.patient.cpf,   # CPF obrigatório
            "password": self.patient_password
        }, format="json")

        # Se der 400, podemos printar o erro
        if response.status_code != 200:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["cpf"], self.patient.cpf)
        self.assertEqual(response.data["user_type"], "patient")

    def test_scientist_login_success(self):
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
        url = reverse("patient-login")
        response = self.client.post(url, {
            "cpf": self.patient.cpf,
            "password": "wrongpassword"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_scientist_as_patient_login_fail(self):
        url = reverse("patient-login")
        response = self.client.post(url, {
            "cpf": "00000000000",  # CPF inválido de cientista
            "password": self.scientist_password
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    # -------------------- /ME TESTS --------------------
    def test_me_as_patient(self):
        login_url = reverse("patient-login")
        response = self.client.post(login_url, {
            "cpf": self.patient.cpf,
            "password": self.patient_password
        }, format="json")
        access_token = response.data["access"]

        me_url = reverse("me")
        response = self.client.get(me_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_type"], "patient")
        self.assertEqual(response.data["data"]["cpf"], self.patient.cpf)

    def test_me_as_scientist(self):
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
        me_url = reverse("me")
        response = self.client.get(me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -------------------- HELPER --------------------
    def _get_tokens_for_user(self, user, password, login_url_name, cpf_login=True):
        url = reverse(login_url_name)
        payload = {"password": password}
        if cpf_login:
            payload["cpf"] = user.cpf
        else:
            payload["email"] = user.email
        response = self.client.post(url, payload, format="json")
        if response.status_code != 200:
            print("LOGIN ERROR:", response.data)
            raise Exception("Falha ao logar para gerar token")
        return response.data["access"], response.data["refresh"]

    # -------------------- LOGOUT TESTS --------------------
    def test_patient_logout_success(self):
        _, refresh_token = self._get_tokens_for_user(self.patient, self.patient_password, "patient-login")
        url = reverse("logout")
        response = self.client.post(url, {"refresh": refresh_token}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logout realizado com sucesso")

    def test_scientist_logout_success(self):
        _, refresh_token = self._get_tokens_for_user(self.scientist, self.scientist_password, "scientist-login", cpf_login=False)
        url = reverse("logout")
        response = self.client.post(url, {"refresh": refresh_token}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logout realizado com sucesso")

    def test_logout_without_token(self):
        url = reverse("logout")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Refresh token não fornecido", response.data["detail"])

    def test_logout_with_invalid_token(self):
        url = reverse("logout")
        response = self.client.post(url, {"refresh": "token_invalido"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Token inválido ou já expirado", response.data["detail"])

    # -------------------- UPDATE PROFILE --------------------
    def test_patient_update_profile_success(self):
        login_url = reverse("patient-login")
        response = self.client.post(login_url, {
            "cpf": self.patient.cpf,
            "password": self.patient_password
        }, format="json")
        access_token = response.data["access"]

        update_url = reverse("user-update")
        payload = {
            "first_name": "Joao",
            "last_name": "Silva",
            "email": "joao.silva@example.com",
            "password": "novaSenha123"
        }
        response = self.client.patch(update_url, payload, HTTP_AUTHORIZATION=f"Bearer {access_token}", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], payload["first_name"])
        self.assertEqual(response.data["last_name"], payload["last_name"])
        self.assertEqual(response.data["email"], payload["email"])

        self.patient.refresh_from_db()
        self.assertTrue(self.patient.check_password("novaSenha123"))

    def test_patient_update_profile_invalid_password(self):
        login_url = reverse("patient-login")
        response = self.client.post(login_url, {
            "cpf": self.patient.cpf,
            "password": self.patient_password
        }, format="json")
        access_token = response.data["access"]

        update_url = reverse("user-update")
        payload = {"password": "123"}  # inválida
        response = self.client.patch(update_url, payload, HTTP_AUTHORIZATION=f"Bearer {access_token}", format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("A senha deve ter pelo menos 8 caracteres", str(response.data))
