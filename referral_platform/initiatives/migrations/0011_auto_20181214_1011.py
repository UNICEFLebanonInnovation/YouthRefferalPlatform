# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-12-14 08:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0010_auto_20181213_2228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='age_of_beneficiaries',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='anticpated_challenges',
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
            name='how_to_ensure_sustainability',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='how_to_measure_progress',
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
            name='mitigation_of_challenges',
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
            name='planned_results',
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
            name='sex_of_beneficiaries',
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
            name='team_participation_rating',
        ),
        migrations.RemoveField(
            model_name='youthledinitiative',
            name='why_this_initiative',
        ),
    ]
