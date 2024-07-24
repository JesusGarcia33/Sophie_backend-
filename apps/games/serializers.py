from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.games.models import *
from apps.users.models import User
from apps.grupos.models import Grupos
from django.db import transaction


class GrupoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupos
        fields = ['nombre_grupo']
        read_only_fields = ['nombre_grupo']


class AsignacionCreate(serializers.ModelSerializer):
    class Meta:
        model = AsignacionActividad
        fields = ['id', 'nombre_actividad', 'puntaje', 'fecha_cierre', 'grupo', 'tipo_actividad']
        read_only_fields = ['id']


class AsignacionSerializer(serializers.ModelSerializer):
    grupo = serializers.CharField()

    class Meta:
        model = AsignacionActividad
        fields = ['id', 'nombre_actividad', 'puntaje', 'fecha_cierre', 'grupo', 'tipo_actividad']
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        grupo_nombre = instance.grupo.nombre_grupo
        representation['grupo'] = grupo_nombre
        return representation


class UsuarioPuntajeSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'email']
        read_only_fields = ['id']


class PuntajesSerializer(serializers.ModelSerializer):
    usuario = UsuarioPuntajeSerialzier()

    class Meta:
        model = Puntajes
        fields = ['id', 'usuario', 'puntaje', 'duracion']
        read_only_fields = ['id']


class PuntajeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puntajes
        fields = ['id', 'usuario', 'asignacion', 'puntaje', 'duracion']
        read_only_fields = ['id', 'usuario']


class ReactivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactivos
        fields = ['id', 'texto_reactivo', 'respuesta_correcta']
        read_only_fields = ['id']


class QuizzSerializer(serializers.ModelSerializer):
    reactivos = ReactivosSerializer(many=True)

    class Meta:
        model = Quizz
        fields = ['id', 'asignacion', 'reactivos']

    def create(self, validated_data):
        reactivos_data = validated_data.pop('reactivos')

        quizz = Quizz.objects.create(**validated_data)
        for reactivo_data in reactivos_data:
            Reactivos.objects.create(quizz=quizz, **reactivo_data)

        return quizz


class CartaCreateSerializer(serializers.ModelSerializer):
    carta_par = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Carta
        fields = ['id', 'texto_carta', 'carta_par']
        read_only_fields = ['id', 'carta_par']


class MemoramaCreateSerializer(serializers.ModelSerializer):
    cartas = CartaCreateSerializer(many=True)

    class Meta:
        model = Memorama
        fields = ['id', 'asignacion', 'cartas']
        read_only_fields = ['id']

    def create(self, validated_data):
        asignacion = validated_data.pop('asignacion')
        print(f'Asignacion: {asignacion}')
        cartas_data = validated_data.pop('cartas')
        print(f'Cartas: {cartas_data}')

        if len(cartas_data) != 16:
            raise ValueError("Debe proporcionar exactamente 16 cartas")

        try:
            with transaction.atomic():

                memorama = Memorama.objects.create(asignacion=asignacion)

                cartas = []
                for i in range(0, len(cartas_data), 2):
                    carta1_data = cartas_data[i]
                    carta2_data = cartas_data[i + 1]

                    carta1 = Carta.objects.create(texto_carta=carta1_data['texto_carta'],
                                                  memorama_id=memorama.id)
                    carta2 = Carta.objects.create(texto_carta=carta2_data['texto_carta'],
                                                  memorama_id=memorama.id)

                    carta1.carta_par = carta2
                    carta2.carta_par = carta1

                    carta1.save()
                    carta2.save()

                    cartas.append(carta1)
                    cartas.append(carta2)

                return memorama
        except Exception as e:
            raise ValidationError(str(e))


class CartaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carta
        fields = ['id', 'texto_carta', 'carta_par']
        read_only_fields = ['id', 'carta_par', 'texto_carta']


class PuntajesEstudiante(serializers.ModelSerializer):
    asignacion = serializers.CharField()

    class Meta:
        model = Puntajes
        fields = ['id', 'asignacion', 'puntaje', ]
        read_only_fields = ['id', 'asignacion', 'puntaje']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        asignacion = instance.asignacion.nombre_actividad
        representation['asignacion'] = asignacion
        return representation
