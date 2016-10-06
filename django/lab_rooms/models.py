from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.
class TypeCharacteristic(models.Model):
    """
    TypeCharacteristic: Tipo de caracteristica

    Almacena los tipos de caracteristicas que pueden presentarse dentro de una sala
    del laboratorio.

    **Atributos db:**
        - name (CharField): Nombre del tipo caracteristica.
        - icon (CharField): Icono del tipo caracteristica.

    """
    name = models.CharField(verbose_name=_('name'), max_length=50)
    icon = models.CharField(verbose_name=_('icon'), max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('type of characteristic')
        verbose_name_plural = _('types of characteristics')


class Characteristic(models.Model):
    """
    Characteristic: Caracteristica

    Almacena las caracteristicas que pueden presentarse dentro de una sala
    del laboratorio.

    **Atributos db:**
        - name (CharField): Nombre de la caracteristica.
        - icon (CharField): Icono de la caracteristica.
    """
    name = models.CharField(verbose_name=_('name'), max_length=50)
    icon = models.CharField(verbose_name=_('icon'), max_length=20)
    type = models.ForeignKey('TypeCharacteristic', verbose_name=_('type of characteristic'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('characteristic')
        verbose_name_plural = _('characteristics')


class TypeInfrastructure(models.Model):
    """
    TypeInfrastructure: Tipo de infraestructura

    Almacena los tipos de infraestructuras donde pueden dictarse los cursos.

    **Atributos db:**
        - name (CharField): Nombre del tipo de infraestructura.
        - icon (CharField): Icono del tipo de infraestructura.
    """
    name = models.CharField(verbose_name=_('name'), max_length=50)
    icon = models.CharField(verbose_name=_('icon'), max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('type of infrastructure')
        verbose_name_plural = _('types of infrastructures')


class Room(models.Model):
    """
    Room: Sala

    Almacena las salas donde se dictan cursos en el laboratorio.

    **Atributos db:**
        - name (CharField): Nombre de la sala.
        - type (ForeignKey): Tipo de infraestructura donde se dictara clases.
    """
    name = models.CharField(verbose_name=_('name'), max_length=50)
    type = models.ForeignKey('TypeInfrastructure', verbose_name=_('type of infrastructure'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')


class RoomCharacteristic(models.Model):
    """
    RoomCharacteristic: Caracterisiticas de la sala

    Almacena las caracteristicas de las salas de laboratorio asi como un valor que representa
    la cantidad.

    **Atributos db:**
        - value (CharField): Valor que representa la cantidad de propiedades en una sala.
        - room (ForeignKey): Clave foranea que hace referencia a la sala.
        - characteristic (ForeignKey): Clave foranea que hace referencia a la caracteristica.
    """

    value = models.CharField(verbose_name=_('value'), max_length=20)
    room = models.ForeignKey('Room', verbose_name=_('room'))
    characteristic = models.ForeignKey('Characteristic', verbose_name=_('characteristic'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('characteristic of the room')
        verbose_name_plural = _('characteristics of the rooms')
