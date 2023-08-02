from rest_framework import serializers
from autenticacao.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'cpf']
        extra_kwargs = {
            'password': {'write_only': True},  # A senha será tratada apenas na criação
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user