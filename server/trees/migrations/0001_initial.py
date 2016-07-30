# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-30 05:49
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comId', models.IntegerField()),
                ('commonName', models.CharField(max_length=50)),
                ('scientificName', models.CharField(max_length=50)),
                ('genus', models.CharField(max_length=50)),
                ('family', models.CharField(max_length=50)),
                ('yearPlanted', models.IntegerField()),
                ('longLat', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
            ],
        ),
    ]
