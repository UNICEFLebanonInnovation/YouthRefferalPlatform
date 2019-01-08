# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-01-03 14:40
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0009_remove_youthledinitiative_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='youthledinitiative',
            name='age_of_beneficiaries',
            field=models.CharField(blank=True, choices=[('1-6', '1-6 years'), ('7-13', '7-13 years'), ('14-24', '14-24 years'), ('25-50', '25-50 years'), ('50-plus', '50 years and above')], max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='challenges_face',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='indirect_beneficiaries',
            field=models.CharField(blank=True, choices=[('1-50', '1-50'), ('51-100 ', '51-100'), ('501-1000', '501-1000'), ('1000-plus', 'greater than 1000')], max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='initiative_activities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('basic_services', 'Improving or installing basic services (electricity, water, sanitation, and waste removal)'), ('social', 'Enhancing social cohesion'), ('environmental', 'Environmental'), ('health_services', 'Health Services'), ('informational', 'Educational, informational or knowledge sharing'), ('advocacy', 'Advocacy or Raising awareness'), ('political', 'Political'), ('religious', 'Spiritual/Religious'), ('culture', 'Artistic/Cultural/Sports'), ('safety', 'Enhancing public safety'), ('public_spaces', 'Improving Public Spaces (parks, hospitals, buildings, schools, sidewalks)'), ('other', 'Other')], max_length=254, null=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='lessons_learnt',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='mentor',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='mentor_was_helpful',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('somewhat', 'Somewhat')], max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='needs_resources',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='number_of_beneficiaries',
            field=models.CharField(blank=True, choices=[('1-50', '1-50'), ('51-100 ', '51-100'), ('501-1000', '501-1000'), ('1000-plus', 'greater than 1000')], max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='number_of_beneficiaries_reached',
            field=models.CharField(blank=True, choices=[('exceeded', 'Exceeded the total number of direct beneficiaries that we planned to reach (greater than 100%)'), ('reached', 'Reached all of the direct beneficiaries planned (100%)'), ('half', 'Reached more than half of the direct beneficiaries planned (50% or more)'), ('less', 'Reached less than half of the direct beneficiaries planned (Less then 49%)" (50% or more)')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='other_groups',
            field=models.CharField(blank=True, choices=[('ngos', 'Other NGOs'), ('schools', 'Schools'), ('municipality', 'Municipality'), ('other', 'Other')], max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='resources_from',
            field=models.CharField(blank=True, choices=[('unicef', 'UNICEF'), ('local ', 'Local Business'), ('organization', 'Organisation')], max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='resources_type',
            field=models.CharField(blank=True, choices=[('financial', 'Financial (self-explanatory)'), ('technical', 'Technical (for ex. developing awareness tools materials, trainings..etc)'), ('in-kind', 'In-Kind (posters, booklet,etc)')], max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='sex_of_beneficiaries',
            field=models.CharField(blank=True, choices=[('both', 'Both male and females'), ('male', 'Only males'), ('female', 'only female')], max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='support_helpful',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('somewhat', 'Somewhat')], max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='youthledinitiative',
            name='why_this_initiative',
            field=models.TextField(blank=True, null=True),
        ),
    ]