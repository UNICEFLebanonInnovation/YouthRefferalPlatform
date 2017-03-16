# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-14 08:45
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('note', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'ALP Level',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='youngperson',
            name='communication_preference',
            field=models.CharField(blank=True, choices=[('facebook', 'Facebook'), ('email', 'E-mail'), ('mobile', 'Mobile'), ('ngo', 'Through the NGO partner'), ('none', "I don't want follow up")], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='disability',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='education_status',
            field=models.CharField(choices=[('currently_studying', 'Currently Studying'), ('stopped_studying', 'Stopped Studying'), ('never_studied', 'Never been to an educational institution'), ('na', 'NA')], default='none', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youngperson',
            name='education_type',
            field=models.CharField(choices=[('non-formal', 'Non formal Education'), ('formal', 'Formal Education')], default='none', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youngperson',
            name='employment_sectors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youngperson',
            name='employment_status',
            field=models.CharField(choices=[('full_time', 'Currently Working - full time'), ('part_time', 'Currently Working - part time'), ('summer_only', 'Work in Summer Only'), ('unemployed', 'Currently Unemployed'), ('never_worked', 'Never worked')], default='none', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youngperson',
            name='household_composition',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='household_working',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='leaving_education_reasons',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='looking_for_work',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youngperson',
            name='not_trained_reason',
            field=models.CharField(blank=True, choices=[('no_interest', 'No Interest'), ('no_money', 'Financial barrier'), ('family_pressure', 'Family pressure'), ('discrimination', 'Discrimination'), ('disability', 'Disability'), ('distance', 'Distance'), ('safety', 'Safety')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='obstacles_for_work',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youngperson',
            name='referred_by',
            field=models.CharField(blank=True, choices=[('ngo', 'Through an NGO'), ('sports_ngo', 'Through a Sports Club/NGO'), ('friends', 'Through friends'), ('others', 'Others')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='safety',
            field=models.CharField(blank=True, choices=[('safe', ' I always feel totally safe in my community '), ('mostly_safe', 'Most of the days I feel safe in my community'), ('mostly_unsafe', "Most of the days I don't feel safe in my community "), ('unsafe', 'I never feel safe in my community')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='safety_reasons',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='sports_group',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='supporting_family',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='through_whom',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='trained_before',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='youngperson',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Location'),
        ),
        migrations.AlterField(
            model_name='youngperson',
            name='partner_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.PartnerOrganization'),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='education_grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.Grade'),
        ),
        migrations.AddField(
            model_name='youngperson',
            name='education_level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='portfolios.EducationLevel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youngperson',
            name='sport_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.Sport'),
        ),
    ]
