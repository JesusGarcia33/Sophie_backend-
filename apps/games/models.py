from django.db import models
from apps.grupos.models import Grupos
from apps.users.models import User


# Create your models here.

class AsignacionActividad(models.Model):
    TIPO_ACTIVIDAD = (
        (1, 'quizz'),
        (2, 'memorama'),
    )
    nombre_actividad = models.CharField(max_length=100)
    puntaje = models.IntegerField()
    fecha_cierre = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE, related_name='actividades')
    tipo_actividad = models.IntegerField(choices=TIPO_ACTIVIDAD, default=1)


class Puntajes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='puntajes')
    asignacion = models.ForeignKey(AsignacionActividad, on_delete=models.CASCADE, related_name='puntajes')
    puntaje = models.IntegerField()
    duracion = models.DurationField()


class Quizz(models.Model):
    asignacion = models.OneToOneField(AsignacionActividad, on_delete=models.CASCADE, related_name='quizz')


class Reactivos(models.Model):
    texto_reactivo = models.CharField(max_length=100)
    respuesta_correcta = models.BooleanField()
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE, related_name='reactivos')


class Memorama(models.Model):
    asignacion = models.OneToOneField(AsignacionActividad, on_delete=models.CASCADE, related_name='memorama')

    def __str__(self):
        return f'Memorama de {self.asignacion}'


class Carta(models.Model):
    texto_carta = models.CharField(max_length=100)
    carta_par = models.OneToOneField('self', on_delete=models.CASCADE, related_name='pareja', null=True, blank=True)
    memorama = models.ForeignKey(Memorama, on_delete=models.CASCADE, related_name='cartas')

    def __str__(self):
        return f'Carta {self.id} del memorama {self.memorama}'
