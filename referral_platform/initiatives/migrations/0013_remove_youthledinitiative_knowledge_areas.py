# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-12-14 09:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0012_remove_youthledinitiative_initiative_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='knowledge_areas',
        ),
    ]
