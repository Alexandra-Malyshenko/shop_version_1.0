# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from transliterate import translit
# from django.contib.postgres.indexes import GinIndex
from decimal import Decimal


class CategoryManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(CategoryManager, self).get_queryset().all()


class Category(models.Model):

    objects = None
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(blank=True, unique=True)
    objects = CategoryManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class Brand(models.Model):

    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


def image_folder(instance, filename):
       filename = instance.slug + '.' + filename.split('.')[1]
       return "{0}/{1}".format(str(instance.slug), filename)


class ProductManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)



class Product(models.Model):

    objects = None
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name="Категория")
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT)
    title = models.CharField(max_length=120, verbose_name="Название")
    slug = models.SlugField(blank=True, max_length=200, db_index=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to=image_folder, verbose_name="Изображение товара")
    price = models.DecimalField(verbose_name="Цена", max_digits=9, decimal_places=2)
    volume = models.DecimalField(default=True, verbose_name="Объем", max_digits=4, decimal_places=1)
    sae = models.CharField(default=True, max_length=20, verbose_name="SAE")
    available = models.BooleanField(verbose_name="Доступен", default=True)
    in_order = models.BooleanField(verbose_name="Под заказ", default=True)
    objects = ProductManager()

    class Meta:
        ordering = ['title']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        index_together = [
            ['id', 'slug']
        ]
        # index = [GinIndex(fields=['title'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])


def pre_save_product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.title), 'ru', reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_product_slug, sender=Product)




# class CartItem(models.Model):

#     product = models.ForeignKey(Product)
#     qty = models.PositiveIntegerField(verbose_name='Количество', default=1)
#     item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)


#     def __unicode__(self):
#         return "Cart item for product {0}".format(self.product.title)


# class Cart(models.Model):

#     items = models.ManyToManyField(CartItem, blank=True, verbose_name="Товары в корзине")
#     cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name="Сумма")

#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзины'

#     def __unicode__(self):
#         return str(self.id)

#     def add_to_cart(self, product_slug):
#         cart = self
#         product = Product.objects.get(slug=product_slug)
#         new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
#         if new_item not in cart.items.all():
#             cart.items.add(new_item)
#             cart.save()

#     def remove_from_cart(self, product_slug):
#         cart = self
#         product = Product.objects.get(slug=product_slug)
#         for cart_item in cart.items.all():
#             if cart_item.product == product:
#                 cart.items.remove(cart_item)
#                 cart.save()

#     def change_qty(self, qty, item_id):
#         cart = self
#         cart_item = CartItem.objects.get(id=int(item_id))
#         cart_item.qty = int(qty)
#         cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
#         cart_item.save()
#         new_cart_total = 0.00
#         for item in cart.items.all():
#             new_cart_total += float(item.item_total)
#         cart.cart_total = new_cart_total
#         cart.save()


# ORDER_STATUS_CHOICES = (
#     ('Принят в обработку', 'Принят в обработку'),
#     ('Выполняеться', 'Выполняеться'),
#     ('Оплачен', 'Оплачен'),
# )


# class Order(models.Model):

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь')
#     items = models.ForeignKey(Cart, verbose_name='Корзина №')
#     total = models.DecimalField(verbose_name='Сумма заказа', max_digits=9, decimal_places=2, default=0.00)
#     first_name = models.CharField(verbose_name='Имя', max_length=200)
#     last_name = models.CharField(verbose_name='Фамилия', max_length=200)
#     email = models.EmailField(verbose_name='Email')
#     phone = models.CharField(verbose_name='Телефон', max_length=20)
#     address = models.CharField(verbose_name='Адрес', max_length=255)
#     buying_type = models.CharField(verbose_name='Тип доставки', max_length=40, choices=(('Самовывоз', 'Самовывоз'),
#                                    ('Доставка куръером', 'Доставка куръером'),
#                                    ('Доставка Новой Почтой', 'Доставка Новой Почтой')),
#                                    default='Самовывоз')
#     date = models.DateTimeField(verbose_name='Дата создания заказа', auto_now=True)
#     comments = models.TextField(verbose_name='Комментарии')
#     status = models.CharField(verbose_name='Статус заказа', max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

#     class Meta:
#         ordering = ('-date',)
#         verbose_name = 'Заказ'
#         verbose_name_plural = 'Заказы'

#     def __unicode__(self):
#         return "Заказ №{0}".format(str(self.id))


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order)
#     product = models.ForeignKey(Product, verbose_name='Продукт')
#     price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
#     qty = models.PositiveIntegerField(verbose_name='Количество', default=1)

#     class Meta:
#         verbose_name = 'Товар'
#         verbose_name_plural = 'Товары'

#     def __unicode__(self):
#         return '{}'.format(self.id)

#     def get_cost(self):
#         return self.price * self.qty
