# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-04-13 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0019_delete_initassessmenthash'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentsubmission',
            name='updated',
            field=models.CharField(default='0', max_length=254),
        ),
    ]
