# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-18 01:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab_reservations', '0005_auto_20170317_0542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='subject',
        ),
    ]
