from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from gerenciamento_api.serializers import ChangePasswordSerializer

from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import User, Aluno, Professor, Coordenador

from .utilities import pass_change_email
from gerenciamento_api.serializers import UserSerializer, AlunoSerializer, CoordenadorSerializer, ProfessorSerializer


# class ProfileView(generics.RetrieveAPIView):
    


@permission_classes([IsAuthenticated])
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Verificar a senha atual do usuário
        if not user.check_password(serializer.validated_data['password']):
            return Response({"message": "Senha atual incorreta."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar se as novas senhas coincidem
        if serializer.validated_data['new_password'] != serializer.validated_data['confirm_new_password']:
            return Response({"message": "As novas senhas não coincidem."}, status=status.HTTP_400_BAD_REQUEST)

        # Trocar a senha
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)
    
class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')

        user = User.objects.get(email=email)
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f'http://localhost:8000/reset-password/{uidb64}/{token}/'
            
            # try:
            pass_change_email(email, reset_url)
            return Response({'message': 'Link de reset de senha enviado para o e-mail.'})
            # except:
            #     return Response({'message': 'Erro no envio do e-mail.'}, status=400)
        else:
            return Response({'message': 'Usuário não encontrado.'}, status=400)
        
class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful.'})
        else:
            return Response({'message': 'Password reset link is invalid or has expired.'}, status=400)
        

@permission_classes([IsAuthenticated])
class ProfileView(APIView):
    def get(self, request):
        user = request.user # obter o usuário atual
        user_type = user.user_type # obter o tipo de usuário

        if user_type == 'aluno': # se o usuário for um aluno
            aluno = Aluno.objects.get(user=user) # obter o objeto aluno correspondente ao usuário
            serializer = AlunoSerializer(aluno) # serializar o objeto aluno

        elif user_type == 'professor': # se o usuário for um professor
            professor = Professor.objects.get(user=user) # obter o objeto professor correspondente ao usuário
            serializer = ProfessorSerializer(professor) # serializar o objeto professor

        elif user_type == 'coordenador': # se o usuário for um coordenador
            coordenador = Coordenador.objects.get(user=user) # obter o objeto coordenador correspondente ao usuário
            serializer = CoordenadorSerializer(coordenador) # serializar o objeto coordenador

        else:
            return Response({'message': 'Tipo de usuário inválido.'}, status=400) # retornar uma mensagem de erro se o tipo de usuário não for válido
        return Response(serializer.data) # retornar os dados serializados como uma resposta