from rest_framework import serializers
from apps.grupos.models import Grupos
from apps.users.models import User


class GruposSerializer(serializers.ModelSerializer):
    alumnos_inscritos = serializers.SerializerMethodField()

    class Meta:
        model = Grupos
        fields = ['id', 'codigo_grupo', 'nombre_grupo', 'alumnos_inscritos']
        read_only_fields = ['id', 'alumnos_inscritos']

    @staticmethod
    def get_alumnos_inscritos(obj) -> int:
        return obj.alumnos_count()


class GruposCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupos
        fields = ['nombre_grupo']


class GrupoAddStudentSerializer(serializers.Serializer):
    codigo_grupo = serializers.CharField()

    def create(self, validated_data):
        try:
            grupo = Grupos.objects.get(codigo_grupo=validated_data['codigo_grupo'])
            grupo.alumnos.add(self.context['request'].user)
            return grupo
        except Grupos.DoesNotExist:
            raise serializers.ValidationError('El grupo no existe')


class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'email']
        read_only_fields = ['id']
