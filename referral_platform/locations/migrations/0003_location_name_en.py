# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-04 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_remove_location_pilot_in_use'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='name_en',
            field=models.CharField(blank=True, default='', max_length=254, null=True),
        ),
    ]