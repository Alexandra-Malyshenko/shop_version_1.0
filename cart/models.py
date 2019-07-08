# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductModel(models.Model):

    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    update = models.BooleanField()