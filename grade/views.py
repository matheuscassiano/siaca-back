from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from autenticacao.models import Aluno
from gerenciamento_api.serializers import MatriculaSerializer, OfertaSerializer, CreateMatriculaSerializer
from autenticacao.permissions import IsAluno, IsCoordenadorCurso, IsOfertaFromCoordenadorCurso, IsDisciplinaFromCoordenadorCurso
from grade.utilities import days_overlap
from .models import Matricula, Oferta
from django.db.models import Q

class OfertaBaseView:
    def is_sala_disponivel(self, sala_id, aula_dias, aula_hora_inicio, aula_hora_fim, periodo_id, oferta_id=None):
        for dia in aula_dias:
            queryset = Oferta.objects.filter(
                sala_id=sala_id,
                aula_dias__contains=dia,
                aula_hora_inicio__lt=aula_hora_fim,
                aula_hora_fim__gt=aula_hora_inicio,
                periodo_id=periodo_id
            )

            if oferta_id is not None:
                queryset = queryset.exclude(id=oferta_id)

            if queryset.exists():
                return False
        return True
    
    def check_professor_schedule_collision(self, professor_id, aula_dias, aula_hora_inicio, aula_hora_fim, oferta_id=None):
        # Obtém todas as ofertas do professor
        professor_ofertas = Oferta.objects.filter(professor_id=professor_id)
        if oferta_id is not None:
            professor_ofertas = professor_ofertas.exclude(id=oferta_id)
        # Verifica colisões de horários com outras ofertas do mesmo Professor
        colisoes = []
        for oferta in professor_ofertas:
            if days_overlap(oferta.aula_dias, aula_dias) and \
                    oferta.aula_hora_inicio < aula_hora_fim and \
                    oferta.aula_hora_fim > aula_hora_inicio:
                colisoes.append(oferta)
        print(colisoes)
        return colisoes
    


@permission_classes([IsAuthenticated, IsDisciplinaFromCoordenadorCurso])
class OfertaCreateView(OfertaBaseView, generics.CreateAPIView):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer

    def perform_create(self, serializer):
        # Verificar disponibilidade da sala
        sala_id = self.request.data.get('sala')
        aula_dias = self.request.data.get('aula_dias')
        aula_hora_inicio = self.request.data.get('aula_hora_inicio')
        aula_hora_fim = self.request.data.get('aula_hora_fim')
        periodo_id = self.request.data.get('periodo')
        professor_id = self.request.data.get('professor')
        # Verificar se a sala está disponível nos dias e horários escolhidos
        sala_disponivel = self.is_sala_disponivel(sala_id, aula_dias, aula_hora_inicio, aula_hora_fim, periodo_id)
        if sala_disponivel:
            # Verificar colisão de horários com as Ofertas do Professor
            colisoes = self.check_professor_schedule_collision(professor_id, aula_dias, aula_hora_inicio, aula_hora_fim)

            if colisoes:
                return Response({'message': 'Conflito de horário com ofertas do professor.'}, status=400)
            
            serializer.save()
        else:
            return Response({'message': 'Sala não está disponível nos dias e horários escolhidos'}, status=400)

@permission_classes([IsAuthenticated, IsDisciplinaFromCoordenadorCurso])
class OfertaUpdateDeleteView(OfertaBaseView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = request.method == 'PATCH'  # Define partial com base no método HTTP
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Verificar disponibilidade da sala
        if instance.sala is not None: 
            sala_id = instance.sala.pk
        else:
            sala_id = request.data.get('sala')

        # Verifica se os parâmetros estão presentes no request, caso contrário, usa os valores da instância
        aula_dias = request.data.get('aula_dias', instance.aula_dias)
        aula_hora_inicio = request.data.get('aula_hora_inicio', instance.aula_hora_inicio)
        aula_hora_fim = request.data.get('aula_hora_fim', instance.aula_hora_fim)
        periodo_id = request.data.get('periodo', instance.periodo_id)
        professor_id = request.data.get('professor')

        # Verificar se a sala está disponível nos dias e horários escolhidos
        sala_disponivel = self.is_sala_disponivel(sala_id, aula_dias, aula_hora_inicio, aula_hora_fim, periodo_id, instance.id)

        if not sala_disponivel:
            return Response({'message': 'Sala não está disponível nos dias e horários escolhidos.'}, status=400)

        colisoes = []

        if professor_id == None:
            if instance.professor is not None:
                professor_id = instance.professor.pk
        else:
            colisoes = self.check_professor_schedule_collision(
                professor_id=professor_id,
                aula_dias=aula_dias,
                aula_hora_inicio=aula_hora_inicio,
                aula_hora_fim=aula_hora_fim,
                oferta_id=instance.id
            )

        if len(colisoes) > 0:
            return Response({'message': 'Conflito de horários com outras Ofertas do mesmo período do Professor.'}, status=400)

        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            return Response({'message': 'Oferta deletado com sucesso.'}, status=200)
        return response

@permission_classes([IsAuthenticated, IsAluno])
class MatriculaCreateView(generics.CreateAPIView):
    queryset = Matricula.objects.all()
    serializer_class = CreateMatriculaSerializer

    def is_disciplina_done(self, oferta, aluno):
        """
        Realiza uma query para verificar se a disciplina da oferta já foi paga pelo aluno
        """
        return Matricula.objects.filter(aluno=aluno, oferta__disciplina=oferta.disciplina, \
                                        aprovado=True).exists()

    def create(self, request, *args, **kwargs):
        oferta_id = request.data.get('oferta')
        try:
            oferta = Oferta.objects.get(pk=oferta_id)
            aluno = request.user.aluno
            qtd_matriculados = oferta.qtd_matriculas_relacionadas()
            lugares_disponiveis = oferta.sala.lugares - qtd_matriculados

            if oferta.disciplina.curso == aluno.curso:

                # Verificar se disciplina já foi paga pelo aluno
                if not self.is_disciplina_done(oferta, aluno):
                    if lugares_disponiveis > 0:

                        # Verificar se há choque de dia/horário com outras matrículas do aluno no mesmo período
                        periodos_do_aluno = Matricula.objects.filter(aluno=aluno).values_list('oferta__periodo', flat=True)
                        matriculas = Matricula.objects.filter(Q(oferta__periodo=oferta.periodo) &
                            Q(oferta__aula_hora_inicio__lt=oferta.aula_hora_fim, oferta__aula_hora_fim__gt=oferta.aula_hora_inicio)
                        )

                        # Cria um queryset vazio para dar append em todas as matriculas que contém os mesmos dias que a oferta atual
                        query_set = Matricula.objects.none() 
                        for dia in oferta.aula_dias:
                            query_set = query_set | matriculas.filter(oferta__aula_dias__contains=dia)
                        choque_horario = query_set.exists()

                        if not choque_horario:
                            matricula = Matricula(oferta=oferta, aluno=aluno)
                            matricula.save()
                            return Response(MatriculaSerializer(matricula).data, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"detail": "Choque de dia/horário com outra matrícula do mesmo período."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"detail": "Sala não tem lugares disponíveis."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "Disciplina da oferta já foi paga pelo aluno."}, status=status.HTTP_400_BAD_REQUEST)
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