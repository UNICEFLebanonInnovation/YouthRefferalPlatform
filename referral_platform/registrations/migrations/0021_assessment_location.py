# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-12-18 08:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_location_name_en'),
        ('registrations', '0020_assessmentsubmission_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Location'),
        ),
    ]