from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Curso, Periodo
from autenticacao.models import User, Coordenador, Professor, Aluno
from autenticacao.migrations import *
from gerenciamento_api.serializers import PeriodoSerializer

class CreateCursoViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="Usuário de Teste",
            password="senhadiferente",
            cpf="12345678901",  # CPF válido
            telefone="82988997766",
            endereco="rua na cidade",
            bairro="Poço",
            cidade="maceió",
            estado="AL",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('criar_curso')
        self.data = {
            'nome': 'Curso de Teste',
            'descricao': 'Descrição do curso de teste contendo periodos de teste e disciplinas de teste',
            'periodos': 8,
            'horas_optat': 300,
        }

    def test_create_curso(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Curso.objects.count(), 1)
        curso = Curso.objects.first()
        self.assertEqual(curso.nome, 'Curso de Teste')

    def test_create_curso_with_invalid_data(self):
        invalid_data = {
            'descricao': 'Descrição do curso de teste contendo periodos de teste e disciplinas de teste',
            'periodos': 8,
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_curso_as_staff(self):
        user = User.objects.create_user(username='staffuser', password='password')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_curso_unauthenticated(self):
        self.client.logout()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


