# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 02:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('birthday', models.DateField()),
                ('favorite_ice_cream', models.CharField(max_length=100)),
            ],
        ),
    ]
