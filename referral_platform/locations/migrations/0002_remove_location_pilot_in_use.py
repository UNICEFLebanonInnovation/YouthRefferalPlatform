# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-26 10:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='pilot_in_use',
        ),
    ]
