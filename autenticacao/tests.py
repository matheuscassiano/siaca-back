from .models import User, Aluno, Professor, Coordenador

from rest_framework.test import APIClient,  APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core import mail


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            cpf="12345678901",  # CPF válido
            telefone="123-456-7890",
            endereco="123 Main St",
            bairro="Downtown",
            cidade="Exampleville",
            estado="EX",
        )
        self.client.force_authenticate(user=self.user)

    def test_change_password_valid(self):
        url = reverse("change-password")
        data = {
            "password": "testpassword",
            "new_password": "newtestpassword",
            "confirm_new_password": "newtestpassword",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newtestpassword"))

    def test_change_password_invalid_current_password(self):
        url = reverse("change-password")
        data = {
            "password": "wrongpassword",
            "new_password": "newtestpassword",
            "confirm_new_password": "newtestpassword",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("testpassword"))

    def test_change_password_mismatched_passwords(self):
        url = reverse("change-password")
        data = {
            "password": "testpassword",
            "new_password": "newtestpassword",
            "confirm_new_password": "mismatchedpassword",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("testpassword"))

    def test_change_password_unauthenticated(self):
        self.client.logout()
        url = reverse("change-password")
        data = {
            "password": "testpassword",
            "new_password": "newtestpassword",
            "confirm_new_password": "newtestpassword",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("testpassword"))



class ResetPasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            cpf="12345678901",  # CPF válido
            telefone="123-456-7890",
            endereco="123 Main St",
            bairro="Downtown",
            cidade="Exampleville",
            estado="EX",
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_reset_password_valid(self):
        url = reverse("reset-password", args=[self.uidb64, self.token])
        data = {
            "new_password": "newtestpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newtestpassword"))

    def test_reset_password_invalid_link(self):
        invalid_uidb64 = urlsafe_base64_encode(force_bytes(12345))  # Non-existent user
        url = reverse("reset-password", args=[invalid_uidb64, self.token])
        data = {
            "new_password": "newtestpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("testpassword"))

    def test_reset_password_invalid_token(self):
        invalid_token = "invalidtoken"
        url = reverse("reset-password", args=[self.uidb64, invalid_token])
        data = {
            "new_password": "newtestpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("testpassword"))





