# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-02 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amt', '0005_imageranking_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gameround',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='imageranking',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
