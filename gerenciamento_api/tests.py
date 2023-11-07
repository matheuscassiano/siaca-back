from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from autenticacao.models import User


class CreateUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="Denison Manager",
            password="senhadiferente",
            cpf="12345678901",  # CPF válido
            telefone="82988997766",
            endereco="rua na cidade",
            bairro="Poço",
            cidade="maceió",
            estado="AL",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_user_valid(self):
        url = reverse("criar_usuario")
        data = {
            "username": "Jesus da Shopee",
            "password": "senhadivina",
            "cpf": "98765432109",  # CPF válido
            "telefone": "82988997744",
            "endereco": "colado na praia",
            "bairro": "Mangabeiras",
            "cidade": "Maceió",
            "estado": "AL",
            "user_type": "coordenador",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)    

    def test_create_user_valid(self):
        url = reverse("criar_usuario")
        data = {
            "username": "Matheus Ninja",
            "password": "newtestpassword",
            "cpf": "98765432109",  # CPF válido
            "telefone": "82988997701",
            "endereco": "Rua em algum lugar",
            "bairro": "Jaragua",
            "cidade": "Maceió",
            "estado": "AL",
            "user_type": "professor",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_valid(self):
        url = reverse("criar_usuario")
        data = {
            "username": "Vandeco",
            "password": "maisumasenha",
            "cpf": "98765432109",  # CPF válido
            "telefone": "82988997755",
            "endereco": "Longe demais",
            "bairro": "Centro",
            "cidade": "Marechal Deodoro",
            "estado": "AL",
            "user_type": "aluno",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_create_user_invalid_data(self):
        url = reverse("criar_usuario")
        # Dados inválidos (falta o campo "user_type")
        data = {
            "username": "Isaac Fazendeiro",
            "password": "testedesenha123",
            "cpf": "98765432109",
            "telefone": "82988997733",
            "endereco": "Sítio do Isaac",
            "bairro": "Zona Rural",
            "cidade": "Branquinha",
            "estado": "AL",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserUpdateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="Usuario Teste CINCO",
            password="senhanova123",
            cpf="12345678901",  # CPF válido
            telefone="82988997711",
            endereco="rua da cidade",
            bairro="Pontal",
            cidade="Maceió",
            estado="AL",
        )
        self.client.force_authenticate(user=self.user)

    def test_update_user_valid(self):
        url = reverse("atualizar_deletar_usuario", kwargs={"id": self.user.id})
        data = {
            "first_name": "Antônia B",
            "last_name": "Atualização de nome",
            "email": "atualizado@googlemail.com",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Antônia B")
        self.assertEqual(self.user.last_name, "Atualização de nome")
        self.assertEqual(self.user.email, "atualizado@googlemail.com")