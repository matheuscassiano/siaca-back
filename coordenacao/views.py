from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from gerenciamento_api.serializers import DisciplinaSerializer, SalaSerializer, CursoSerializer, PeriodoSerializer, OfertaSerializer
from autenticacao.permissions import IsCoordenadorCurso, IsStaff, CanCreateCurso, CanUpdateDeleteCurso
from .models import Disciplina, Sala, Curso, Periodo


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

@permission_classes([IsAuthenticated, CanCreateCurso])
class CreateCursoView(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Curso criado com sucesso.'
        return response

@permission_classes([IsAuthenticated, CanUpdateDeleteCurso])
class UpdateDeleteCursoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Curso atualizado com sucesso.'
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            return Response({'message': 'Curso deletado com sucesso.'}, status=200)
        return response
  
@permission_classes([IsAuthenticated])
class CreatePeriodoView(generics.ListCreateAPIView):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Periodo criado com sucesso.'
        return response

@permission_classes([IsAuthenticated])
class UpdateDeletePeriodoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Periodo atualizado com sucesso.'
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            return Response({'message': 'Periodo deletado com sucesso.'}, status=200)
        return response
    
@permission_classes([IsAuthenticated, CanCreateCurso])
class SalaListView(generics.ListAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

@permission_classes([IsAuthenticated, CanCreateCurso])
class DisciplinaListView(generics.ListAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    
    def get_queryset(self):
        # Filtra as disciplinas pelo curso do coordenador
        return Disciplina.objects.filter(curso=self.request.user.coordenador.curso)