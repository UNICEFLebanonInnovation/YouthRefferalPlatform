# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-05 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0002_assessmentsubmission_registration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registration',
            options={'ordering': ['pk'], 'verbose_name': '\u0627\u0644\u062a\u0633\u062c\u064a\u0644', 'verbose_name_plural': '\u0627\u0644\u062a\u0633\u062c\u064a\u0644'},
        ),
        migrations.AlterField(
            model_name='registration',
            name='partner_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='partners.PartnerOrganization', verbose_name='\u0627\u0644\u062c\u0645\u0639\u064a\u0629'),
        ),
    ]