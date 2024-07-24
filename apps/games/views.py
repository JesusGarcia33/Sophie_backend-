from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from apps.games.models import *
from apps.games.serializers import *


class AsignacionCreateListView(generics.ListCreateAPIView):
    """
    POST: Permite crear una asignacion de un juego a un grupo
    GET: Obtiene la lista de asignaciones a juegos creadas por el profesor logueado
    """
    serializer_class = AsignacionCreate
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AsignacionActividad.objects.filter(grupo__profesor=self.request.user).order_by('-created_at')


class QuizzCreateView(generics.CreateAPIView):
    """
    Crea un nuevo quizz
    """
    serializer_class = QuizzSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(f'Validated data before save: {serializer.validated_data}')
        serializer.save()
        print(f'Validated data after save: {serializer.validated_data}')


class PuntajeListView(generics.ListAPIView):
    """
    Obtiene la lista de puntajes de los alumnos
    """
    serializer_class = PuntajesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        asignacion_id = self.kwargs['id']
        return Puntajes.objects.filter(asignacion_id=asignacion_id).order_by('puntaje')


class PuntajeCreateView(generics.CreateAPIView):
    """
    Crea un nuevo puntaje
    """
    serializer_class = PuntajeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class MemoramaCreateView(generics.CreateAPIView):
    """
    Crea un nuevo memorama
    """
    serializer_class = MemoramaCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(f'Validated data before save: {serializer.validated_data}')
        serializer.save()


class MemroramaView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return CartaSerializer

    def get_queryset(self):
        asignacion_id = self.kwargs['id']
        return Carta.objects.filter(memorama__asignacion=asignacion_id)


class QuizzView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ReactivosSerializer

    def get_queryset(self):
        asignacion_id = self.kwargs['id']
        return Reactivos.objects.filter(quizz__asignacion=asignacion_id)


class ActividadesEstudianteView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return AsignacionSerializer

    def get_queryset(self):
        return AsignacionActividad.objects.filter(
            grupo__alumnos=self.request.user
        ).exclude(
            puntajes__usuario=self.request.user
        ).order_by('-fecha_cierre')


class PuntajeEStudiantesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return PuntajesEstudiante

    def get_queryset(self):
        return Puntajes.objects.filter(usuario=self.request.user).order_by('puntaje')
