# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-26 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youth', '0019_auto_20180105_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youngperson',
            name='governorate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Location', verbose_name='Governorate'),
        ),
    ]
