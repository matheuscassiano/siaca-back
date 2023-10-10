from rest_framework import serializers
from autenticacao.models import User, Coordenador, Professor, Aluno
from coordenacao.models import Disciplina, Sala, Curso, Periodo
from grade.models import Oferta, Matricula

class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=[('coordenador', 'Coordenador'), ('professor', 'Professor'), ('aluno', 'Aluno')])
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'cpf', 'telefone', 'endereco', 'bairro', 'cidade', 'estado', 'user_type', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},  # A senha será tratada apenas na criação
            'first_name': {'required': False},  # Torna o campo 'first_name' opcional
            'last_name': {'required': False},  # Torna o campo 'last_name' opcional
            'telefone': {'required': False},  # Torna o campo 'telefone' opcional
            'endereco': {'required': False},  # Torna o campo 'endereco' opcional
            'bairro': {'required': False},  # Torna o campo 'bairro' opcional
            'cidade': {'required': False},  # Torna o campo 'cidade' opcional
            'estado': {'required': False},  # Torna o campo 'estado' opcional
            'is_active': {'required': False},  # Torna o campo 'is_active' opcional
        }

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        
        validated_data['is_active'] = True

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
        fields = ['id', 'first_name', 'last_name', 'email', 'telefone', 'endereco', 'bairro', 'cidade', 'estado', 'is_active']
        extra_kwargs = {
            'first_name': {'required': False},  # Torna o campo 'first_name' opcional
            'last_name': {'required': False},  # Torna o campo 'last_name' opcional
            'email': {'required': False},
            'telefone': {'required': False},  # Torna o campo 'telefone' opcional
            'endereco': {'required': False},  # Torna o campo 'endereco' opcional
            'bairro': {'required': False},  # Torna o campo 'bairro' opcional
            'cidade': {'required': False},  # Torna o campo 'cidade' opcional
            'estado': {'required': False},  # Torna o campo 'estado' opcional
            'is_active': {'required': False},  # Torna o campo 'is_active' opcional
        }

        def update(self, instance, validated_data):        
            return super().update(instance, validated_data)

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


class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id', 'start_date', 'end_date']
        extra_kwargs = {
            'start_date': {'required': False},  # Torna o campo 'start_date' opcional
            'end_date': {'required': False},  # Torna o campo 'end_date' opcional
        }

    def create(self, validated_data):        
        return super().create(validated_data)

    def update(self, instance, validated_data):        
        return super().update(instance, validated_data)

class PeriodoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id', 'start_date', 'end_date']
        extra_kwargs = {
            'start_date': {'required': False},  # Torna o campo 'start_date' opcional
            'end_date': {'required': False},  # Torna o campo 'end_date' opcional
        }

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = '__all__'

class CreateMatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = ['oferta']

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno # especificar o modelo que será serializado
        fields = ('first_name', 'last_name', 'email') # especificar os campos que serão serializados

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor # especificar o modelo que será serializado
        fields = ('first_name', 'last_name', 'email') # especificar os campos que serão serializados

class CoordenadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenador # especificar o modelo que será serializado
        fields = ('first_name', 'last_name', 'email') # especificar os campos que serão serializados