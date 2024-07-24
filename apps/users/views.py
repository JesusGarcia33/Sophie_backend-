from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.users.serializers import *


# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """
    Crea un nuevo paciente
    """
    serializer_class = UsuarioCreateSerializer


class RetrieveUserView(generics.RetrieveAPIView):
    """
    Obtiene la información de un usuario
    """
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
