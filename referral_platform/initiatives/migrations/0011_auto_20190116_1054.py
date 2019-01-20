# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-01-16 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0010_auto_20190103_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='age_of_beneficiaries',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='challenges_face',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='description',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='indirect_beneficiaries',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='initiative_activities',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='lessons_learnt',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='mentor',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='mentor_was_helpful',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='needs_resources',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='number_of_beneficiaries',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='number_of_beneficiaries_reached',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='other_groups',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='resources_from',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='resources_type',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='support_helpful',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='why_this_initiative',
        ),
        migrations.AlterField(
            model_name='youthledinitiative',
            name='type',
            field=models.CharField(blank=True, choices=[('basic services', 'Basic Services)'), ('social Cohesion', 'Social cohesion'), ('environmental', 'Environmental'), ('health services', 'Health Services'), ('protection', 'Protection'), ('advocacy', 'Advocacy or Raising awareness'), ('political', 'Political'), ('religious and spiritual', 'Spiritual/Religious'), ('sports', 'Sports'), ('economic art cultural', 'Economic art cultural'), ('educational', 'educational)'), ('other', 'Other')], max_length=254, null=True, verbose_name='Initiative Types'),
        ),
    ]