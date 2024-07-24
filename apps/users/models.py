from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, nombre, user_rol, password=None):
        if not email:
            raise ValueError('Se requiere de un correo electronico.')

        user = self.model(nombre=nombre, user_rol=user_rol, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_ROL = (
        (1, 'estudiante'),
        (2, 'profesor'),
    )
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=150)
    user_rol = models.IntegerField(choices=USER_ROL, default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email
