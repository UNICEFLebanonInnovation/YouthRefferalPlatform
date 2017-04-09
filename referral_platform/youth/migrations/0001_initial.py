 # -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-06 12:35
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partners', '0001_initial'),
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
            name='IDType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('inuse', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'ID Type',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('code', models.CharField(max_length=5, null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'Nationalities',
            },
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='YoungPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('first_name', models.CharField(max_length=75)),
                ('last_name', models.CharField(max_length=75)),
                ('father_name', models.CharField(max_length=75)),
                ('full_name', models.CharField(blank=True, max_length=225, null=True)),
                ('mother_fullname', models.CharField(max_length=255)),
                ('mother_firstname', models.CharField(max_length=75)),
                ('mother_lastname', models.CharField(max_length=75)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50)),
                ('birthday_year', models.CharField(blank=True, choices=[(b'1970', 1970), (b'1971', 1971), (b'1972', 1972), (b'1973', 1973), (b'1974', 1974), (b'1975', 1975), (b'1976', 1976), (b'1977', 1977), (b'1978', 1978), (b'1979', 1979), (b'1980', 1980), (b'1981', 1981), (b'1982', 1982), (b'1983', 1983), (b'1984', 1984), (b'1985', 1985), (b'1986', 1986), (b'1987', 1987), (b'1988', 1988), (b'1989', 1989), (b'1990', 1990), (b'1991', 1991), (b'1992', 1992), (b'1993', 1993), (b'1994', 1994), (b'1995', 1995), (b'1996', 1996), (b'1997', 1997), (b'1998', 1998), (b'1999', 1999), (b'2000', 2000), (b'2001', 2001), (b'2002', 2002), (b'2003', 2003), (b'2004', 2004), (b'2005', 2005), (b'2006', 2006), (b'2007', 2007), (b'2008', 2008), (b'2009', 2009), (b'2010', 2010), (b'2011', 2011), (b'2012', 2012), (b'2013', 2013), (b'2014', 2014), (b'2015', 2015), (b'2016', 2016), (b'2017', 2017), (b'2018', 2018), (b'2019', 2019), (b'2020', 2020), (b'2021', 2021), (b'2022', 2022), (b'2023', 2023), (b'2024', 2024), (b'2025', 2025), (b'2026', 2026), (b'2027', 2027), (b'2028', 2028), (b'2029', 2029), (b'2030', 2030), (b'2031', 2031), (b'2032', 2032), (b'2033', 2033), (b'2034', 2034), (b'2035', 2035), (b'2036', 2036), (b'2037', 2037), (b'2038', 2038), (b'2039', 2039), (b'2040', 2040), (b'2041', 2041), (b'2042', 2042), (b'2043', 2043), (b'2044', 2044), (b'2045', 2045), (b'2046', 2046), (b'2047', 2047), (b'2048', 2048), (b'2049', 2049), (b'2050', 2050)], default=0, max_length=4, null=True)),
                ('birthday_month', models.CharField(blank=True, choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], default=0, max_length=2, null=True)),
                ('birthday_day', models.CharField(blank=True, choices=[(b'1', 1), (b'2', 2), (b'3', 3), (b'4', 4), (b'5', 5), (b'6', 6), (b'7', 7), (b'8', 8), (b'9', 9), (b'10', 10), (b'11', 11), (b'12', 12), (b'13', 13), (b'14', 14), (b'15', 15), (b'16', 16), (b'17', 17), (b'18', 18), (b'19', 19), (b'20', 20), (b'21', 21), (b'22', 22), (b'23', 23), (b'24', 24), (b'25', 25), (b'26', 26), (b'27', 27), (b'28', 28), (b'29', 29), (b'30', 30), (b'31', 31), (b'32', 32)], default=0, max_length=2, null=True)),
                ('age', models.CharField(blank=True, max_length=4, null=True)),
                ('phone', models.CharField(blank=True, max_length=64, null=True)),
                ('phone_prefix', models.CharField(blank=True, max_length=10, null=True)),
                ('id_number', models.CharField(max_length=45)),
                ('address', models.TextField(blank=True, null=True)),
                ('number', models.CharField(blank=True, max_length=45, null=True)),
                ('parents_phone_number', models.CharField(blank=True, max_length=64, null=True)),
                ('disability', models.CharField(blank=True, max_length=100, null=True)),
                ('education_status', models.CharField(choices=[('currently_studying', 'Yes, I am currently studying'), ('stopped_studying', 'Yes, but I stopped studying'), ('never_studied', 'Never been to an educational institution'), ('na', 'NA')], max_length=50)),
                ('education_type', models.CharField(choices=[('non-formal', 'Non formal Education'), ('formal', 'Formal Education')], max_length=50)),
                ('leaving_education_reasons', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('employment_status', models.CharField(choices=[('full_time', 'Currently Working - full time'), ('part_time', 'Currently Working - part time'), ('summer_only', 'Work in Summer Only'), ('unemployed', 'Currently Unemployed'), ('never_worked', 'Never worked')], max_length=50)),
                ('employment_sectors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), size=None)),
                ('looking_for_work', models.BooleanField()),
                ('through_whom', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('obstacles_for_work', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), size=None)),
                ('supporting_family', models.NullBooleanField()),
                ('household_composition', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('household_working', models.IntegerField(blank=True, null=True)),
                ('safety', models.CharField(blank=True, choices=[('safe', ' I always feel totally safe in my community '), ('mostly_safe', 'Most of the days I feel safe in my community'), ('mostly_unsafe', "Most of the days I don't feel safe in my community "), ('unsafe', 'I never feel safe in my community')], max_length=50, null=True)),
                ('safety_reasons', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('trained_before', models.BooleanField(default=False)),
                ('not_trained_reason', models.CharField(blank=True, choices=[('no_interest', 'No Interest'), ('no_money', 'Financial barrier'), ('family_pressure', 'Family pressure'), ('discrimination', 'Discrimination'), ('disability', 'Disability'), ('distance', 'Distance'), ('safety', 'Safety')], max_length=50, null=True)),
                ('sports_group', models.BooleanField(default=False)),
                ('referred_by', models.CharField(blank=True, choices=[('ngo', 'Through an NGO'), ('sports_ngo', 'Through a Sports Club/NGO'), ('friends', 'Through friends'), ('others', 'Others')], max_length=50, null=True)),
                ('communication_preference', models.CharField(blank=True, choices=[('facebook', 'Facebook'), ('email', 'E-mail'), ('mobile', 'Mobile'), ('ngo', 'Through the NGO partner'), ('none', "I don't want follow up")], max_length=50, null=True)),
                ('education_grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='youth.Grade')),
                ('education_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youth.EducationLevel')),
                ('id_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youth.IDType')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
                ('mother_nationality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='youth.Nationality')),
                ('nationality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='youth.Nationality')),
                ('partner_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.PartnerOrganization')),
                ('sport_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='youth.Sport')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
