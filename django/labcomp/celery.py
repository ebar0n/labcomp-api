from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labcomp.settings.development')

# set the default Django settings module for the 'celery' program.
app = Celery('labcomp', include=[])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('labcomp.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
