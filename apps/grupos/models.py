from django.db import models
from django.db.models.functions import datetime

from apps.users.models import User


# Create your models here.

class Grupos(models.Model):
    nombre_grupo = models.CharField(max_length=50)
    codigo_grupo = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)
    alumnos = models.ManyToManyField(User, related_name='alumnos')

    def alumnos_count(self):
        return self.alumnos.count()

    def __str__(self):
        return self.nombre_grupo
