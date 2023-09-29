from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from autenticacao.models import Aluno
from gerenciamento_api.serializers import MatriculaSerializer, OfertaSerializer, CreateMatriculaSerializer
from autenticacao.permissions import IsAluno, IsCoordenadorCurso, IsOfertaFromCoordenadorCurso
from .models import Matricula, Oferta


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
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Oferta atualizado com sucesso.'
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            return Response({'message': 'Oferta deletado com sucesso.'}, status=200)
        return response

@permission_classes([IsAuthenticated, IsAluno])
class MatriculaCreateView(generics.CreateAPIView):
    queryset = Matricula.objects.all()
    serializer_class = CreateMatriculaSerializer
    
    def create(self, request, *args, **kwargs):
        oferta_id = request.data.get('oferta')
        # aluno_id = request.data.get('aluno')
        try:
            oferta = Oferta.objects.get(pk=oferta_id)
            aluno = request.user.aluno
            qtd_matriculados = oferta.qtd_matriculas_relacionadas()
            lugares_disponiveis = oferta.sala.lugares - qtd_matriculados
            
            if oferta.disciplina.curso == aluno.curso:
                if lugares_disponiveis > 0:
                    matricula = Matricula(oferta=oferta, aluno=aluno)
                    matricula.save()
                    return Response(MatriculaSerializer(matricula).data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "Sala não tem lugares disponíveis."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                    return Response({"detail": "Oferta não pertence a uma disciplina do curso do aluno."}, status=status.HTTP_400_BAD_REQUEST)
        except Oferta.DoesNotExist:
            return Response({"detail": "Oferta não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except Aluno.DoesNotExist:
            return Response({"detail": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated, IsOfertaFromCoordenadorCurso])
class MatriculaListView(generics.ListAPIView):
    serializer_class = MatriculaSerializer

    def get_queryset(self):
        oferta_id = self.request.query_params.get('oferta')
        print(oferta_id)
        if oferta_id:
            return Matricula.objects.filter(oferta__pk=oferta_id)
        return Matricula.objects.none()  # Ou retorne a queryset desejada caso não seja necessário filtrar

    def get(self, request, *args, **kwargs):
        matriculas = self.get_queryset()
        if matriculas.exists():
            return Response(MatriculaSerializer(matriculas, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Oferta não tem matriculas."}, status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated, IsAluno])
class MyMatriculaListView(generics.ListAPIView):
    queryset = Matricula.objects.all()

    def get_queryset(self):
        aluno = self.request.user.aluno
        return Matricula.objects.filter(aluno=aluno)
    
    def get(self, request, *args, **kwargs):
        matriculas = self.get_queryset()
        return Response(MatriculaSerializer(matriculas, many=True).data, status=status.HTTP_200_OK)