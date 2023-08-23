from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from autenticacao.models import User
from coordenacao.models import Curso
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from autenticacao.permissions import CanUpdateUserData, CanCreateUser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


@permission_classes([IsAuthenticated, CanCreateUser])
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Usuário criado com sucesso.'
        return response
    
@permission_classes([IsAuthenticated, CanUpdateUserData])
class UpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Usuário atualizado com sucesso.'
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            return Response({'message': 'Usuário deletado com sucesso.'}, status=200)
        return response