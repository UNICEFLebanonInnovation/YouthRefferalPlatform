# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-04-01 06:36
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0018_auto_20190330_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youthledinitiative',
            name='type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('basic_services', 'Improving or installing basic services (electricity, water, sanitation, and waste removal)'), ('social', 'Enhancing social cohesion'), ('environmental', 'Environmental'), ('health_services', 'Health Services'), ('informational', 'Educational, informational or knowledge sharing'), ('advocacy', 'Advocacy or Raising awareness'), ('political', 'Political'), ('religious', 'Spiritual/Religious'), ('culture', 'Artistic/Cultural/Sports'), ('safety', 'Enhancing public safety'), ('public_spaces', 'Improving Public Spaces (parks, hospitals, buildings, schools, sidewalks)'), ('other', 'Other')], max_length=129),
        ),
    ]
