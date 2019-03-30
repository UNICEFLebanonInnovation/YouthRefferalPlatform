# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-03-30 20:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0017_auto_20190319_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youthledinitiative',
            name='partner_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.PartnerOrganization', verbose_name='Partner Organization'),
        ),
    ]
