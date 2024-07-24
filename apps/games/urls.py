from django.urls import path, include

from apps.games.views import *

urlpatterns = [
    path('list/', AsignacionCreateListView.as_view(), name='asignacion-list-create'),
    path('create/quizz/', QuizzCreateView.as_view(), name='quizz-create'),

    path('puntajes/<int:id>/', PuntajeListView.as_view(), name='puntaje-list'),
    path('puntajes/create/', PuntajeCreateView.as_view(), name='puntaje-create'),

    path('create/memorama/', MemoramaCreateView.as_view(), name='memorama-create'),
    path('memorama/<int:id>/', MemroramaView.as_view(), name='memorama-view'),
    path('quizz/<int:id>/', QuizzView.as_view(), name='quizz-view'),

    path('estudiantes/', ActividadesEstudianteView.as_view(), name='actividades-list'),


    path('puntaje/estudiante/', PuntajeEStudiantesView.as_view(), name='puntaje-estudiante'),

]
