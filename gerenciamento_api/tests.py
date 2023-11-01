from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from autenticacao.models import User


class CreateUserViewTest(TestCase):
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

    def test_create_user_valid(self):
        url = reverse("criar_usuario")
        data = {
            "username": "newuser",
            "password": "newtestpassword",
            "cpf": "98765432109",  # CPF válido
            "telefone": "987-654-3210",
            "endereco": "456 Elm St",
            "bairro": "Uptown",
            "cidade": "Sampletown",
            "estado": "ST",
            "user_type": "aluno",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid_data(self):
        url = reverse("criar_usuario")
        # Dados inválidos (falta o campo "user_type")
        data = {
            "username": "newuser",
            "password": "newtestpassword",
            "cpf": "98765432109",
            "telefone": "987-654-3210",
            "endereco": "456 Elm St",
            "bairro": "Uptown",
            "cidade": "Sampletown",
            "estado": "ST",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserUpdateViewTest(TestCase):
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

    def test_update_user_valid(self):
        url = reverse("atualizar_deletar_usuario", kwargs={"id": self.user.id})
        data = {
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "email": "updated@example.com",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated First Name")
        self.assertEqual(self.user.last_name, "Updated Last Name")
        self.assertEqual(self.user.email, "updated@example.com")