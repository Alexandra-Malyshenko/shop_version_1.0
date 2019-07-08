# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ecomapp.models import Product
from django.conf import settings

ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняеться', 'Выполняеться'),
    ('Оплачен', 'Оплачен'),
)


class Order(models.Model):

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь')
    first_name = models.CharField(verbose_name='Имя', max_length=200)
    last_name = models.CharField(verbose_name='Фамилия', max_length=200, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)

    phone = models.CharField(verbose_name='Телефон', max_length=20)
    address = models.CharField(verbose_name='Адрес', max_length=200, null=True, blank=True)
    date_of_delivery = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    comments = models.TextField(verbose_name='Комментарии', blank=True, default='no comments')
    status = models.CharField(verbose_name='Статус заказа', max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __unicode__(self):
        return "Заказ №{0}".format(str(self.id))

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Продукт')
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __unicode__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity