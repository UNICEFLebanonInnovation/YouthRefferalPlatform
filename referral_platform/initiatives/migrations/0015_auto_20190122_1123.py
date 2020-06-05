# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-01-22 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0017_auto_20190102_1606'),
        ('initiatives', '0014_auto_20190121_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='member',
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='Participants',
            field=models.ManyToManyField(related_name='_youthledinitiative_Participants_+', to='registrations.Registration'),
        ),
    ]