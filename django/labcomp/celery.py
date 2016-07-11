from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labcomp.settings')

# set the default Django settings module for the 'celery' program.
app = Celery('labcomp', include=['utils.task'])

app.config_from_object('labcomp.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
