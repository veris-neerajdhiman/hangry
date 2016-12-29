# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='resource_end_point',
            field=models.URLField(editable=False, max_length=255, unique=True, verbose_name='End Point used by Process'),
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('host', 'request_path')]),
        ),
    ]
