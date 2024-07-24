from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.users.models import User


class UsuarioCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'nombre', 'user_rol', 'password', 'password2']
        read_only_fields = ['is_active', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'nombre', 'user_rol']
