# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-12-19 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0021_assessment_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='slug',
            field=models.SlugField(),
        ),
    ]