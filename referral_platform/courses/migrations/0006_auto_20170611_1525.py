# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-06-11 12:25
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20170610_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='scores',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='status',
            field=models.CharField(default=b'enrolled', max_length=50),
        ),
    ]
