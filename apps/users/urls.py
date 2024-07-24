from django.urls import path, include

from apps.users import views

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create_paciente'),
    path('retrieve/', views.RetrieveUserView.as_view(), name='retrieve_paciente'),
]
