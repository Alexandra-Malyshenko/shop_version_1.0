# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Category, Brand, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']



class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price',
                    'available']
    list_filter = ['available']
    list_editable = ['price', 'available']



admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)



