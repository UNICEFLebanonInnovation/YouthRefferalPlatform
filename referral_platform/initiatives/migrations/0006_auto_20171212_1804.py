# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-12 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0005_auto_20170704_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youthledinitiative',
            name='number_of_beneficiaries_reached',
            field=models.CharField(blank=True, choices=[('exceeded', '\u062a\u062c\u0627\u0648\u0632 \u0627\u0644\u0639\u062f\u062f \u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a \u0644\u0644\u0645\u0633\u062a\u0641\u064a\u062f\u064a\u0646 \u0627\u0644\u0645\u0628\u0627\u0634\u0631\u064a\u0646 \u0627\u0644\u0630\u064a\u0646 \u062e\u0637\u0637\u0646\u0627 \u0644\u0644\u0648\u0635\u0648\u0644 \u0625\u0644\u064a\u0647\u0645 (\u0623\u0643\u062b\u0631 \u0645\u0646 100\u066a)'), ('reached', '\u062a\u0645 \u0627\u0644\u0648\u0635\u0648\u0644 \u0625\u0644\u0649 \u062c\u0645\u064a\u0639 \u0627\u0644\u0645\u0633\u062a\u0641\u064a\u062f\u064a\u0646 \u0627\u0644\u0645\u0628\u0627\u0634\u0631\u064a\u0646 \u0627\u0644\u0645\u0642\u0631\u0651\u0631\u064a\u0646 (100\u066a)'), ('half', 'Reached more than half of the direct beneficiaries planned (50% or more)'), ('less', '\u0644\u0645 \u064a\u062a\u0645 \u0627\u0644\u0648\u0635\u0648\u0644 \u0625\u0644\u0649 \u0627\u0644\u0639\u062f\u062f \u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a \u0644\u0644\u0645\u0633\u062a\u0641\u064a\u062f\u064a\u0646 \u0627\u0644\u0645\u0628\u0627\u0634\u0631\u064a\u0646 (\u0623\u0642\u0644 \u0645\u0646 49\u066a)')], max_length=100, null=True),
        ),
    ]