from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LabReservationsConfig(AppConfig):
    name = 'lab_reservations'
    verbose_name = _('reservations')
