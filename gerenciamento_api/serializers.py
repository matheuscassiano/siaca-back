from rest_framework import serializers
from autenticacao.models import User, Coordenador, Professor, Aluno
from coordenacao.models import Disciplina, Sala, Curso

class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=[('coordenador', 'Coordenador'), ('professor', 'Professor'), ('aluno', 'Aluno')])
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'cpf', 'telefone', 'endereco', 'bairro', 'cidade', 'estado', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},  # A senha será tratada apenas na criação
            'first_name': {'required': False},  # Torna o campo 'first_name' opcional
            'last_name': {'required': False},  # Torna o campo 'last_name' opcional
            'telefone': {'required': False},  # Torna o campo 'telefone' opcional
            'endereco': {'required': False},  # Torna o campo 'endereco' opcional
            'bairro': {'required': False},  # Torna o campo 'bairro' opcional
            'cidade': {'required': False},  # Torna o campo 'cidade' opcional
            'estado': {'required': False},  # Torna o campo 'estado' opcional
        }

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')

        user = User.objects.create_user(**validated_data)

        if user_type == 'coordenador':
            Coordenador.objects.create(user=user)
        elif user_type == 'professor':
            Professor.objects.create(user=user)
        elif user_type == 'aluno':
            Aluno.objects.create(user=user)

        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'telefone', 'endereco', 'bairro', 'cidade', 'estado']
        extra_kwargs = {
            'first_name': {'required': False},  # Torna o campo 'first_name' opcional
            'last_name': {'required': False},  # Torna o campo 'last_name' opcional
            'email': {'required': False},
            'telefone': {'required': False},  # Torna o campo 'telefone' opcional
            'endereco': {'required': False},  # Torna o campo 'endereco' opcional
            'bairro': {'required': False},  # Torna o campo 'bairro' opcional
            'cidade': {'required': False},  # Torna o campo 'cidade' opcional
            'estado': {'required': False},  # Torna o campo 'estado' opcional
        }

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'