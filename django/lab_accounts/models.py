from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _


class User(AbstractUser):
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

    Los siguientes atributos se heredan de la clase PermissionsMixin
        * is_superuser
        * groups
        * user_permissions

    **Atributos db:**
        - photo (ImageField): Foto del usuario.
        - identity_card (CharField): Tarjeta de identificacion.
    """
    photo = models.ImageField(upload_to='accounts/photos/', blank=True)
    identity_card = models.CharField(max_length=8)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')