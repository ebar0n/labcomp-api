from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
class Department(models.Model):
    """
    Department: Departamento

    Almacena los departamentos de docencia en la universidad.

    **Atributos db:**
        - name (CharField): Nombre del departamento.
        - code (CharField): Codigo de referencia del departamento.
        - users (ManyToManyField): Usuarios(profesores) pertenecientes al departamento.
        - rooms (ManyToManyField): Salas del laboratorio a las que tienen permiso los
          profesores del departamento.
    """

    name = models.CharField(verbose_name=_('Name'), max_length=50)
    code = models.CharField(verbose_name=_('Code'), unique=True, max_length=20)
    users = models.ManyToManyField('lab_accounts.User', verbose_name=_('Users'))
    rooms = models.ManyToManyField('lab_rooms.Room', verbose_name=_('Rooms'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')


class ReservationPermission(models.Model):
    """
    ReservationPermission: Permiso de reservacion.

    Almacena los limites por departamento de reservacion. Los profesores de ciertos
    departamentos tienen un valor maximo de reservaciones cada cierto periodo de tiempo.

    **Atributos db:**
        - block_limit (IntegerField): Limite de bloques de horas en una reservacion.
        - weekly_limit (IntegerField): Limite semanal de reservaciones.
        - biweekly_limit (IntegerField): Limite quincenal de reservaciones.
        - monthly_limit (IntegerField): Limite mensual de reservaciones.
        - department (ForeignKey): Departamento asociado a los limites.
    """
    block_limit = models.IntegerField(verbose_name=_('Block limit'), default=0)
    weekly_limit = models.IntegerField(verbose_name=_('Weekly limit'),default=0)
    biweekly_limit = models.IntegerField(verbose_name=_('Biweekly limit'), default=0)
    monthly_limit = models.IntegerField(verbose_name=_('Monthly limit'), default=0)
    department = models.ForeignKey('Department', verbose_name=_('Department'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Color(models.Model):
    """
    Color: Color

    Almacena los codigos de los colores que representaran las materias dentro del horario.

    **Atributos db:**
        - name (CharField): Nombre del color.
        - code (CharField): Codigo hexadecimal del color.
    """

    name = models.CharField(verbose_name=_('Name'), max_length=20)
    code = models.CharField(verbose_name=_('Code'), max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')


class Subject(models.Model):
    """
    Subject: Asignatura, materia o curso

    Almacena las materias o cursos que se dictan en el laboratorio.

    **Atributos db:**
        - name (CharField): Nombre de la materia.
        - code (CharField): Codigo de la materia.
        - department (CharField): Departamento que dicta la materia.
        - color (CharField): Color de la materia.
    """

    name = models.CharField(verbose_name=_('Name'), max_length=50)
    code = models.CharField(verbose_name=_('Code'), max_length=20)
    department = models.ForeignKey('Department', verbose_name=_('Department'))
    color = models.ForeignKey('Color', verbose_name=_('Color'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')


class Semester(models.Model):
    """
    Semester: Semestre

    Almacena los semestres o periodos de actividad academica.

     **Atributos db:**
        - code (CharField): Codigo del semestre.
        - present (BooleanField): Representa el semestre actual si es True.
        - start_date (CharField): Fecha de inicio del semestre.
        - end_date (CharField): Fecha de fin del semestre.
    """

    code = models.CharField(verbose_name=_('Code'), max_length=20)
    present = models.BooleanField(verbose_name=_('Present'))
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        verbose_name = _('Semester')
        verbose_name_plural = _('Semesters')