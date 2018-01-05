# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-22 08:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0004_center'),
        ('clm', '0003_auto_20171009_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.PartnerOrganization'),
        ),
    ]