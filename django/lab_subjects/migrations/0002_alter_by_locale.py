# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-06 00:04
from __future__ import unicode_literals

import colorful.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab_subjects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name': 'color', 'verbose_name_plural': 'colors'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': 'department', 'verbose_name_plural': 'departments'},
        ),
        migrations.AlterModelOptions(
            name='reservationpermission',
            options={'verbose_name': 'reservation permission', 'verbose_name_plural': 'reservation permissions'},
        ),
        migrations.AlterModelOptions(
            name='semester',
            options={'verbose_name': 'semester', 'verbose_name_plural': 'semesters'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'subject', 'verbose_name_plural': 'subjects'},
        ),
        migrations.AlterField(
            model_name='color',
            name='code',
            field=colorful.fields.RGBColorField(verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=20, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='department',
            name='code',
            field=models.CharField(max_length=20, unique=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=50, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='department',
            name='rooms',
            field=models.ManyToManyField(to='lab_rooms.Room', verbose_name='rooms'),
        ),
        migrations.AlterField(
            model_name='department',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='usuarios'),
        ),
        migrations.AlterField(
            model_name='reservationpermission',
            name='biweekly_limit',
            field=models.IntegerField(default=0, verbose_name='biweekly limit'),
        ),
        migrations.AlterField(
            model_name='reservationpermission',
            name='block_limit',
            field=models.IntegerField(default=0, verbose_name='block limit'),
        ),
        migrations.AlterField(
            model_name='reservationpermission',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab_subjects.Department', verbose_name='department'),
        ),
        migrations.AlterField(
            model_name='reservationpermission',
            name='monthly_limit',
            field=models.IntegerField(default=0, verbose_name='monthly limit'),
        ),
        migrations.AlterField(
            model_name='reservationpermission',
            name='weekly_limit',
            field=models.IntegerField(default=0, verbose_name='weekly limit'),
        ),
        migrations.AlterField(
            model_name='semester',
            name='code',
            field=models.CharField(max_length=20, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='semester',
            name='end_date',
            field=models.DateField(verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='semester',
            name='present',
            field=models.BooleanField(verbose_name='present'),
        ),
        migrations.AlterField(
            model_name='semester',
            name='start_date',
            field=models.DateField(verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(max_length=20, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab_subjects.Color', verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab_subjects.Department', verbose_name='department'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=50, verbose_name='nombre'),
        ),
    ]
