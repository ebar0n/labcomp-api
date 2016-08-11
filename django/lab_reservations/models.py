from django.db import models
from django.utils.translation import ugettext as _

choices_blocks = [
    [1, '7:00'],
    [2, '8:00'],
    [3, '9:00'],
    [4, '10:00'],
    [5, '11:00'],
    [6, '12:00'],
    [7, '13:00'],
    [8, '14:00'],
    [9, '15:00'],
    [10, '16:00'],
    [11, '17:00'],
    [12, '18:00'],
    [13, '19:00'],
    [14, '20:00'],
    [15, '21:00'],
    [16, '22:00'],
]

choices_days = [
    [1, 'Lunes'],
    [2, 'Martes'],
    [3, 'Miércoles'],
    [4, 'Jueves'],
    [5, 'Viernes'],
    [6, 'Sábado'],
    [7, 'Domingo'],
]

choices_type_reservations = [
    [1, 'Parcial'],
    [2, 'Quiz'],
    [3, 'Preparaduria'],
    [4, 'Conferencia'],
    [5, 'Revisión'],
    [6, 'Clase Recuperativa'],
    [7, 'Otra'],
]

choices_status_reservations = [
    [1, 'Aprobado'],
    [2, 'Pendiente'],
    [3, 'Rechazado'],
    [4, 'Cancelado'],
]


# Create your models here.
class Section(models.Model):
    """
    Section: Seccion

    Almacena las secciones de clases del laboratorio.

    **Atributos db:**
        - code (CharField): Codigo de la seccion de clases.
        - semester (ForeignKey): Clave foranea del semestre a la que pertenece la seccion.
        - subject (ForeignKey): Clave foranea de la materia a la que pertenece la seccion.
        - user (ForeignKey): Clave foranea del usuario o profesor de la seccion.
    """

    code = models.CharField(verbose_name=_('Code'), max_length=20)
    semester = models.ForeignKey('lab_subjects.Semester', verbose_name=_('Semester'))
    subject = models.ForeignKey('lab_subjects.Subject', verbose_name=_('Subject'))
    user = models.ForeignKey('lab_accounts.User', verbose_name=_('User'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')


class TimeTable(models.Model):
    """
    TimeTable: Horario

    Almacena los bloques de horas del horario

    **Atributos db:**
        - block (IntegerField): Bloque que representa la hora.
        - day (IntegerField): Dia de la semana en el horario.
        - section (ForeignKey): Clave foranea que hace referencia a la seccion.
        - room (ForeignKey): Clave foranea que hace referencia a la sala.
    """

    block = models.IntegerField(verbose_name=_('Block'), choices=choices_blocks)
    day = models.IntegerField(verbose_name=_('Day'), choices=choices_days)
    section = models.ForeignKey('Section', verbose_name=_('Section'))
    room = models.ForeignKey('lab_rooms.Room', verbose_name=_('Room'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('TimeTable')
        verbose_name_plural = _('TimeTables')


class HourFreed(models.Model):
    """
    HourFreed: Hora liberada

    Almacena los bloques de horas liberadas del horario.

    **Atributos db:**
        - date (DateTimeField): Fecha en la que fue liberado el bloque.
        - timetable (ForeignKey): Bloque del horario que fue liberado.
    """

    date = models.DateTimeField(verbose_name=_('Date'))
    timetable = models.ForeignKey('TimeTable', verbose_name=_('TimeTable'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Hour Freed')
        verbose_name_plural = _('Hours Freed')


class Reservation(models.Model):
    """
    Reservation:	Reservacion

    Almacena los bloques de horas que han sido reservadas por los usuarios.

    **Atributos db:**
        - date (DateTimeField): Fecha de la solicitud de reservacion.
        - description (CharField): Descripcion o motivo de reservacion.
        - type (IntegerField): Choices con los tipos de reservacion.
        - semester (ForeignKey): Clave foranea que hace referencia al semestre.
        - subject (ForeignKey): Clave foranea que hace referencia a la materia.
        - user (IntegerField): Clave foranea que hace referencia al usuario que reservo.
        - timetable (ManyToManyField): Almacena los bloques de horas que ocupan en el horario la reservacion.
    """

    date = models.DateTimeField(verbose_name=_('Date'))
    description = models.CharField(verbose_name=_('Description'), max_length=200)
    type = models.IntegerField(verbose_name=_('Type of reservation'), choices=choices_type_reservations)
    semester = models.ForeignKey('lab_subjects.Semester', verbose_name=_('Semester'))
    subject = models.ForeignKey('lab_subjects.Subject', verbose_name=_('Subject'))
    user = models.ForeignKey('lab_accounts.User', verbose_name=_('User'))
    timetable = models.ManyToManyField('TimeTable', verbose_name=_('TimeTable'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')


class StatusReservationHistoric(models.Model):
    """
    StatusReservationHistoric:	Estado de Reservacion historico

    Almacena el historico de los status de las reservaciones.

    **Atributos db:**
        - start_date (DateTimeField): Fecha de inicio.
        - end_date (DateTimeField): Fecha de fin.
        - status (IntegerField): Choices con los status de la reservaciones.
        - reservation (ForeignKey): Clave foranea que hace referencia a la reservacion.
    """

    start_date = models.DateTimeField(verbose_name=_('Start date'))
    end_date = models.DateTimeField(verbose_name=_('End date'))
    status = models.IntegerField(verbose_name=_('Status'), choices=choices_status_reservations)
    reservation = models.ForeignKey('Reservation', verbose_name=_('Reservation'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
