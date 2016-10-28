from django.db import models
from django.utils.translation import ugettext as _

CHOICES_BLOCKS = [
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

CHOICES_DAYS = [
    [0, _('Monday')],
    [1, _('Tuesday')],
    [2, _('Wednesday')],
    [3, _('Thursday')],
    [4, _('Friday')],
    [5, _('Saturday')],
    [6, _('Sunday')],
]

choices_type_reservations = [
    [1, _('Partial')],
    [2, _('Quiz')],
    [3, _('Preparaduria')],
    [4, _('Conference')],
    [5, _('Review')],
    [6, _('Recuperative class')],
    [7, _('Other')],
]

choices_status_reservations = [
    [1, _('Approved')],
    [2, _('Pending')],
    [3, _('Rejected')],
    [4, _('Canceled')],
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

    code = models.CharField(verbose_name=_('code'), max_length=20)
    semester = models.ForeignKey('lab_subjects.Semester', verbose_name=_('semester'))
    subject = models.ForeignKey('lab_subjects.Subject', verbose_name=_('subject'))
    user = models.ForeignKey('lab_accounts.User', verbose_name=_('user'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')

    def __str__(self):
        return '{} Sec.{}'.format(
            self.subject,
            self.code
        )


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

    block_start = models.IntegerField(verbose_name=_('block'), choices=CHOICES_BLOCKS)
    block_end = models.IntegerField(verbose_name=_('block'), choices=CHOICES_BLOCKS)
    day = models.IntegerField(verbose_name=_('day'), choices=CHOICES_DAYS)
    section = models.ForeignKey('Section', verbose_name=_('section'), null=True)
    room = models.ForeignKey('lab_rooms.Room', verbose_name=_('room'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('timetable')
        verbose_name_plural = _('timetables')

    def get_block_valid(block_start, block_end, day, room):
        timetable = TimeTable.objects.filter(day=day, room=room)

        hours = []
        for t in timetable:
            for block in range(t.block_start, t.block_end):
                hours.append(block)

        for block in range(block_start, block_end):
            if block in hours:
                return False
        return True


class HourFreed(models.Model):
    """
    HourFreed: Hora liberada

    Almacena los bloques de horas liberadas del horario.

    **Atributos db:**
        - date (DateTimeField): Fecha en la que fue liberado el bloque.
        - timetable (ForeignKey): Bloque del horario que fue liberado.
    """

    date = models.DateTimeField(verbose_name=_('date'))
    timetable = models.ForeignKey('TimeTable', verbose_name=_('timetable'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('hour freed')
        verbose_name_plural = _('hours freed')


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

    date = models.DateTimeField(verbose_name=_('date'))
    description = models.CharField(verbose_name=_('description'), max_length=200)
    type = models.IntegerField(verbose_name=_('type of reservation'), choices=choices_type_reservations)
    semester = models.ForeignKey('lab_subjects.Semester', verbose_name=_('semester'))
    subject = models.ForeignKey('lab_subjects.Subject', verbose_name=_('subject'))
    user = models.ForeignKey('lab_accounts.User', verbose_name=_('user'))
    timetable = models.ForeignKey('TimeTable', verbose_name=_('timetable'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')


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

    start_date = models.DateTimeField(verbose_name=_('start date'))
    end_date = models.DateTimeField(verbose_name=_('end date'))
    status = models.IntegerField(verbose_name=_('status'), choices=choices_status_reservations)
    reservation = models.ForeignKey('Reservation', verbose_name=_('reservation'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
