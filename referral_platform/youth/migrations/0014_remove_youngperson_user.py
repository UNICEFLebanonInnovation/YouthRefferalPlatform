# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-09-19 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youth', '0013_auto_20170919_2144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youngperson',
            name='user',
        ),
    ]
