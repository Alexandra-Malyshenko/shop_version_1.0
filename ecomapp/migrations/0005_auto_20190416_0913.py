# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-04-16 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0004_auto_20190415_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, to='ecomapp.CartItem'),
        ),
    ]
