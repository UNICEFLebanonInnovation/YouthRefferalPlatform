# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-01-02 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0007_assessmentsubmission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youthledinitiative',
            name='member',
            field=models.ManyToManyField(blank=True, related_name='_youthledinitiative_member_+', to='registrations.Registration'),
        ),
    ]