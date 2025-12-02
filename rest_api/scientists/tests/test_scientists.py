from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from scientists.models import Scientist
from django.utils.crypto import get_random_string

class ScientistTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_email = "admin@example.com"
        self.admin_password = "Admin123!"
        self.scientist_password = "Scientist123!"

        # Criar cientista administrador
        self.admin = Scientist.objects.create_superuser(
            email=self.admin_email,
            password=self.admin_password,
            first_name="Admin",
            last_name="User",
            institution="Admin Instituição",
            specialization="Admin Especialização"
        )

        # Cientista comum
        self.scientist_data = {
            "email": "scientist@example.com",
            "password": self.scientist_password,
            "first_name": "Alice",
            "last_name": "Smith",
            "institution": "UTFPR",
            "specialization": "Neurociência"
        }

    def test_register_scientist(self):
        """Registro de cientista via endpoint"""
        url = reverse("scientist-register")
        response = self.client.post(url, self.scientist_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], self.scientist_data["email"])
        self.assertFalse(response.data["is_verified"])
        self.assertNotIn("password", response.data)
        self.assertIn("message", response.data)

        scientist = Scientist.objects.get(email=self.scientist_data["email"])
        self.assertFalse(scientist.is_verified)
        self.assertIsNotNone(scientist.verification_token)

    def test_profile_update(self):
        """Atualização de perfil do cientista"""
        # Criar cientista para o teste
        scientist = Scientist.objects.create_user(**self.scientist_data)
        self.client.force_authenticate(user=scientist)

        url = reverse("scientist-profile")
        update_data = {"first_name": "Alicia", "last_name": "Smith", "institution": "UTFPR", "specialization": "Genética"}
        response = self.client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Alicia")
        self.assertEqual(response.data["specialization"], "Genética")

    def test_verify_scientist(self):
        """Verificação do cientista pelo admin"""
        # Criar cientista manualmente com token, igual a view faz
        scientist = Scientist.objects.create_user(**self.scientist_data)
    
        # DEFINIR MANUALMENTE OS CAMPOS COMO A VIEW FAZ
        scientist.is_verified = False
        scientist.verification_token = get_random_string(50)
        scientist.save()

        # Autenticar como admin
        self.client.force_authenticate(user=self.admin)
        url = reverse("verify-scientist", kwargs={"token": scientist.verification_token})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        scientist.refresh_from_db()
        self.assertTrue(scientist.is_verified)
        self.assertIsNone(scientist.verification_token)