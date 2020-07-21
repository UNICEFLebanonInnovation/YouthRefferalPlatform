# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2020-07-21 10:20
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('partners', '0005_partnerorganization_dashboard_url'),
        ('locations', '0003_location_name_en'),
        ('registrations', '0002_auto_20200522_0320'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('enrolled', 'enrolled'), ('pre_test', 'pre_test'), ('post_test', 'post_test')], default='enrolled', max_length=254)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('new_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='registrations.Assessment')),
            ],
        ),
        migrations.CreateModel(
            name='YouthLedent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
                ('duration', models.CharField(blank=True, choices=[('1_2', '1-2 weeks'), ('3_4', '3-4 weeks'), ('4_6', '4-6 weeks'), ('6_plus', 'More than 6 weeks')], max_length=254, null=True, verbose_name='Duration of the initiative')),
                ('type', models.CharField(blank=True, choices=[('basic_services', 'Improving or installing basic services (electricity, water, sanitation, and waste removal)'), ('social', 'Enhancing social cohesion'), ('environmental', 'Environmental'), ('health_services', 'Health Services'), ('informational', 'Educational, informational or knowledge sharing'), ('advocacy', 'Advocacy or Raising awareness'), ('political', 'Political'), ('religious', 'Spiritual/Religious'), ('culture', 'Artistic/Cultural/Sports'), ('safety', 'Enhancing public safety'), ('public_spaces', 'Improving Public Spaces (parks, hospitals, buildings, schools, sidewalks)'), ('other', 'Other')], max_length=254, null=True, verbose_name='Initiative Types')),
                ('Participants', models.ManyToManyField(related_name='_youthledent_Participants_+', to='registrations.Registration', verbose_name='Participants')),
                ('center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='partners.Center', verbose_name='Center')),
                ('governorate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Location', verbose_name='Governorate')),
                ('partner_organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.PartnerOrganization', verbose_name='Partner Organization')),
            ],
        ),
        migrations.AddField(
            model_name='assessmentsubmission',
            name='entrepreneurship',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entrepreneurship.YouthLedent'),
        ),
    ]
