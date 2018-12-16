# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-12-16 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0004_auto_20181216_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='initiative_types',
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='type',
            field=models.CharField(blank=True, choices=[('basic_services', 'Improving or installing basic services (electricity, water, sanitation, and waste removal)'), ('social', 'Enhancing social cohesion'), ('environmental', 'Environmental'), ('health_services', 'Health Services'), ('informational', 'Educational, informational or knowledge sharing'), ('advocacy', 'Advocacy or Raising awareness'), ('political', 'Political'), ('religious', 'Spiritual/Religious'), ('culture', 'Artistic/Cultural/Sports'), ('safety', 'Enhancing public safety'), ('public_spaces', 'Improving Public Spaces (parks, hospitals, buildings, schools, sidewalks)'), ('other', 'Other')], max_length=254, null=True, verbose_name='Initiative Types'),
        ),
    ]
