# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-09 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clm', '0002_assessmentsubmission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assessment',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='assessment',
            name='order',
            field=models.TextField(default=1),
        ),
    ]
