# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-09-19 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youth', '0012_auto_20170919_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youngperson',
            name='looking_for_work',
            field=models.NullBooleanField(),
        ),
    ]
