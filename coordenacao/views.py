from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from gerenciamento_api.serializers import DisciplinaSerializer, SalaSerializer
from autenticacao.permissions import IsCoordenadorCurso, IsStaff
from .models import Disciplina, Sala


@permission_classes([IsAuthenticated, IsCoordenadorCurso])
class DisciplinaCreateView(generics.CreateAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer

@permission_classes([IsAuthenticated, IsCoordenadorCurso])
class DisciplinaUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    
@permission_classes([IsAuthenticated, IsStaff])
class SalaCreateView(generics.CreateAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    
@permission_classes([IsAuthenticated, IsStaff])
class SalaUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer