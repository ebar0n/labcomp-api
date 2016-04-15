from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Personalizacion del modelo de usuarios de Django `AbstractUser`

    Los siguientes atributos se heredan de la clase AbstracBaseUser
        * first_name
        * last_name
        * username
        * password
        * email
        * is_active
        * is_staff
        * last_login

    Inherits the following attributes: PermissionsMixin
        * is_superuser
        * groups
        * user_permissions
    """
    foto = models.ImageField(upload_to='usuarios/', blank=True)
    cedula = models.CharField(max_length=8, unique=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
