# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-12-16 14:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('initiatives', '0003_youthledinitiative_center'),
    ]

    operations = [
        migrations.AddField(
            model_name='youthledinitiative',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
