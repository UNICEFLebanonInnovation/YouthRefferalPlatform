# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-04 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0011_assessment_training_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessment',
            name='training_type',
        ),
        migrations.AddField(
            model_name='registration',
            name='training_type',
            field=models.CharField(blank=True, choices=[('tr_type_1', 'Life skills'), ('tr_type_2', 'Entrepreneurship'), ('tr_type_3', 'Civic engagement'), ('tr_type_4', 'Sports for development')], max_length=50, null=True),
        ),
    ]