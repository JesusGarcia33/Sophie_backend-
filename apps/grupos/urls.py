from django.urls import path, include

from apps.grupos.views import *

urlpatterns = [
    path('list/profesor', GrupoCreateListView.as_view(), name='grupo-create-list'),
    path('list/studiante/', ListAddEstudianteGrupo.as_view(), name='studiante-group-add-list'),
    path('estudiantes/<int:id>/', AlumnosListView.as_view(), name='estudiantes-list'),
]
