from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LabRoomsConfig(AppConfig):
    name = 'lab_rooms'
    verbose_name = _('rooms')
