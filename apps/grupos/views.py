from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.grupos.models import Grupos
from apps.grupos.serializers import *


# Create your views here.

class GrupoCreateListView(generics.ListCreateAPIView):
    """
    POST: Permite asignar un cuestionario a un paciente
    GET: Obtiene los cuestionarios que el terapeuta ha asignado
    """

    def perform_create(self, serializer):
        grupo = serializer.save(profesor=self.request.user)
        self.generate_codigo_grupo(grupo)

    @staticmethod
    def generate_codigo_grupo(grupo):
        if not grupo.codigo_grupo:
            fecha_actual = grupo.created_at
            second = fecha_actual.second
            initials = grupo.nombre_grupo[:2].upper()
            grupo.codigo_grupo = f"{second:02d}{initials}{grupo.id}"
            grupo.save()

    def get_queryset(self):
        return Grupos.objects.filter(profesor=self.request.user).order_by('nombre_grupo')

    def get_serializer_class(self):
        return GruposSerializer if self.request.method == 'GET' else GruposCreateSerializer


class ListAddEstudianteGrupo(generics.ListCreateAPIView):
    """
    Agrega un alumno a un grupo
    Lista los grupos de un alumno
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Grupos.objects.filter(alumnos=self.request.user).order_by('nombre_grupo')

    def get_serializer_class(self):
        return GrupoAddStudentSerializer if self.request.method == 'POST' else GruposSerializer

    def perform_create(self, serializer):
        serializer.save(request=self.request)


class AlumnosListView(generics.ListAPIView):
    """
    Obtiene la lista de alumnos inscritos en un grupo
    """
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        grupo_id = self.kwargs['id']
        grupo = Grupos.objects.get(id=grupo_id)
        return grupo.alumnos.all().order_by('nombre')
