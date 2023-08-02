from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    print('Bem vindo!')
    if request.user.is_authenticated:
        # Retorna uma mensagem específica para usuários autenticados
        return Response({'message': 'Você está autenticado. Acesso autorizado.'})
    else:
        # Retorna uma mensagem para usuários não autenticados
        return Response({'message': 'Acesso negado. Faça login para continuar.'})
