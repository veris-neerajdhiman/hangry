# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terminals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='widget name')),
                ('widgets', models.ManyToManyField(to='widgets.Widgets')),
            ],
        ),
    ]
