from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from gerenciamento_api.serializers import DisciplinaSerializer, SalaSerializer, CursoSerializer, PeriodoSerializer, OfertaSerializer
from autenticacao.permissions import IsCoordenadorCurso, IsStaff, CanCreateCurso, CanUpdateDeleteCurso
from .models import Disciplina, Sala, Curso, Periodo, Oferta


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

@permission_classes([IsAuthenticated, IsCoordenadorCurso])
class OfertaCreateView(generics.CreateAPIView):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer

    def perform_create(self, serializer):
        # Verificar disponibilidade da sala
        sala_id = self.request.data.get('sala')
        aula_dias = self.request.data.get('aula_dias')
        aula_hora_inicio = self.request.data.get('aula_hora_inicio')
        aula_hora_fim = self.request.data.get('aula_hora_fim')

        # Verificar se a sala está disponível nos dias e horários escolhidos
        sala_disponivel = self.is_sala_disponivel(sala_id, aula_dias, aula_hora_inicio, aula_hora_fim)

        if sala_disponivel:
            serializer.save()
        else:
            return Response({'message': 'Sala não está disponível nos dias e horários escolhidos'}, status=400)

    def is_sala_disponivel(self, sala_id, aula_dias, aula_hora_inicio, aula_hora_fim):
        for dia in aula_dias:
            colisoes = Oferta.objects.filter(
                sala_id=sala_id,
                aula_dias__contains=dia,
                aula_hora_inicio__lt=aula_hora_fim,
                aula_hora_fim__gt=aula_hora_inicio
            )

            if colisoes.exists():
                return False

        return True

@permission_classes([IsAuthenticated, IsCoordenadorCurso])
class OfertaUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer

    def perform_update(self, serializer):
        # Verificar disponibilidade da sala ao atualizar
        sala_id = self.request.data.get('sala')
        aula_dias = self.request.data.get('aula_dias')
        aula_hora_inicio = self.request.data.get('aula_hora_inicio')
        aula_hora_fim = self.request.data.get('aula_hora_fim')

        sala_disponivel = self.is_sala_disponivel(sala_id, aula_dias, aula_hora_inicio, aula_hora_fim)

        if sala_disponivel:
            serializer.save()
        else:
            return Response({'message': 'Sala não está disponível nos dias e horários escolhidos'}, status=400)

    def is_sala_disponivel(self, sala_id, aula_dias, aula_hora_inicio, aula_hora_fim):
        for dia in aula_dias:
            colisoes = Oferta.objects.filter(
                sala_id=sala_id,
                aula_dias__contains=dia,
                aula_hora_inicio__lt=aula_hora_fim,
                aula_hora_fim__gt=aula_hora_inicio
            )

            if colisoes.exists():
                return False

        return True
    
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