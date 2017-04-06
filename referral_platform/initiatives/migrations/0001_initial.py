# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-06 12:25
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        ('youth', '__first__'),
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YouthLedInitiative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('duration', models.CharField(blank=True, choices=[('1_2', '1-2 weeks'), ('3_4', '3-4 weeks'), ('4_6', '4-6 weeks'), ('6_plus', 'More than 6 weeks')], max_length=50, null=True)),
                ('initiative_types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('basic_services', 'Improving or installing basic services (electricity, water, sanitation, and waste removal)'), ('social', 'Enhancing social cohesion'), ('environmental', 'Environmental'), ('health_services', 'Health Services'), ('informational', 'Educational, informational or knowledge sharing'), ('advocacy', 'Advocacy or Raising awareness'), ('political', 'Political'), ('religious', 'Spiritual/Religious'), ('culture', 'Artistic/Cultural/Sports'), ('safety', 'Enhancing public safety'), ('public_spaces', 'Improving Public Spaces (parks, hospitals, buildings, schools, sidewalks)'), ('other', 'Other')], max_length=50, null=True), blank=True, null=True, size=None)),
                ('knowledge_areas', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('self-management', 'Self-Management'), ('teamwork', 'Cooperation & Teamwork'), ('creativity', 'Creativity'), ('critical_thinking', 'Critical Thinking'), ('negotiation', 'Negotiation'), ('diversity', 'Respect for diversity'), ('decision_making', 'Decision Making'), ('participation', 'Participation'), ('communication', 'Communication'), ('empathy', 'Empathy'), ('problem_solving', 'Problem-Solving'), ('resilience', 'Resilience')], max_length=50, null=True), blank=True, null=True, size=None)),
                ('why_this_initiative', models.TextField(blank=True, null=True)),
                ('other_groups', models.CharField(blank=True, choices=[('ngos', 'Other NGOs'), ('schools', 'Schools'), ('municipality', 'Municipality'), ('other', 'Other')], max_length=50, null=True)),
                ('number_of_beneficiaries', models.CharField(blank=True, choices=[('1-50', '1-50'), ('51-100 ', '51-100'), ('501-1000', '501-1000'), ('1000-plus', 'greater than 1000')], max_length=50, null=True)),
                ('age_of_beneficiaries', models.CharField(blank=True, choices=[('1-6', '1-6 years'), ('7-13', '7-13 years'), ('14-24', '14-24 years'), ('25-50', '25-50 years'), ('50-plus', '50 years and above')], max_length=50, null=True)),
                ('sex_of_beneficiaries', models.CharField(blank=True, choices=[('both', 'Both male and females'), ('male', 'Only males'), ('female', 'only female')], max_length=50, null=True)),
                ('indirect_beneficiaries', models.CharField(blank=True, choices=[('1-50', '1-50'), ('51-100 ', '51-100'), ('501-1000', '501-1000'), ('1000-plus', 'greater than 1000')], max_length=50, null=True)),
                ('needs_resources', models.BooleanField(default=False)),
                ('resources_from', models.CharField(blank=True, choices=[('unicef', 'UNICEF'), ('local ', 'Local Business'), ('organization', 'Organisation')], max_length=50, null=True)),
                ('resources_type', models.CharField(blank=True, choices=[('financial', 'Financial (self-explanatory)'), ('technical', 'Technical (for ex. developing awareness tools materials, trainings..etc)'), ('in-kind', 'In-Kind (posters, booklet,etc)')], max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('planned_results', models.TextField(blank=True, null=True)),
                ('anticpated_challenges', models.TextField(blank=True, null=True)),
                ('mitigation_of_challenges', models.TextField(blank=True, null=True)),
                ('how_to_measure_progress', models.TextField(blank=True, null=True)),
                ('how_to_ensure_sustainability', models.TextField(blank=True, null=True)),
                ('team_participation_rating', models.CharField(blank=True, choices=[('excellent', 'Excellent - All of our team members were committed to the initiative'), ('good', 'Good - Most of our team was committed to the initiative'), ('low', 'Low - Some team members stopped participating')], max_length=100, null=True)),
                ('initiative_activities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('basic_services', 'Improving or installing basic services (electricity, water, sanitation, and waste removal)'), ('social', 'Enhancing social cohesion'), ('environmental', 'Environmental'), ('health_services', 'Health Services'), ('informational', 'Educational, informational or knowledge sharing'), ('advocacy', 'Advocacy or Raising awareness'), ('political', 'Political'), ('religious', 'Spiritual/Religious'), ('culture', 'Artistic/Cultural/Sports'), ('safety', 'Enhancing public safety'), ('public_spaces', 'Improving Public Spaces (parks, hospitals, buildings, schools, sidewalks)'), ('other', 'Other')], max_length=50, null=True), blank=True, null=True, size=None)),
                ('number_of_beneficiaries_reached', models.CharField(blank=True, choices=[('exceeded', 'Exceeded the total number of direct beneficiaries that we planned to reach (greater than 100%)'), ('reached', 'Reached all of the direct beneficiaries planned (100%)'), ('half', 'Reached more than half of the direct beneficiaries planned (50% or more)'), ('less', 'Reached less than half of the direct beneficiaries planned (Less then 49%)" (50% or more)')], max_length=100, null=True)),
                ('mentor', models.NullBooleanField()),
                ('mentor_was_helpful', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('somewhat', 'Somewhat')], max_length=50, null=True)),
                ('support_helpful', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('somewhat', 'Somewhat')], max_length=50, null=True)),
                ('challenges_face', models.TextField(blank=True, null=True)),
                ('lessons_learnt', models.TextField(blank=True, null=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
                ('members', models.ManyToManyField(blank=True, null=True, to='youth.YoungPerson')),
                ('partner_organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.PartnerOrganization')),
            ],
        ),
    ]
