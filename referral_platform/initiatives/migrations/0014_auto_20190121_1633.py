# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-01-21 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0013_assessmenthash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youthledinitiative',
            name='member',
            field=models.ManyToManyField(related_name='_youthledinitiative_member_+', to='registrations.Registration'),
        ),
    ]