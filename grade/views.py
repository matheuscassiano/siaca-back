from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from gerenciamento_api.serializers import OfertaSerializer
from autenticacao.permissions import IsCoordenadorCurso
from .models import Oferta

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
        print(sala_disponivel)
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
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Oferta atualizado com sucesso.'
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            return Response({'message': 'Oferta deletado com sucesso.'}, status=200)
        return response