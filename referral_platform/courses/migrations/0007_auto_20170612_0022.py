# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-06-11 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20170611_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='partner',
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='status',
            field=models.CharField(choices=[(b'enrolled', b'enrolled'), (b'pre_test', b'pre_test'), (b'post_test', b'post_test')], default=b'enrolled', max_length=50),
        ),
    ]
