# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .models import Category, Product
from decimal import Decimal
from .forms import RegistrationForm, LoginForm
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.template.context_processors import csrf


def base_view(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart = Cart(request)
    cart_product_form = CartAddProductForm()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'base.html', context)


def product_view(request, product_slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, slug=product_slug, available=True)
    # product = Product.objects.get(slug=product_slug, available=True)
    cart = Cart(request)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'categories': categories,
        'cart_product_form': cart_product_form,
        'cart': cart,
    }
    return render(request, 'product.html', context)


def category_view(request, category_slug):
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    products = Product.objects.filter(available=True, category=category)
    context = {
        'products': products,
        'categories': categories,
        'cart': cart,
        'cart_product_form': cart_product_form,

    }
    return render(request, 'category.html', context)



def registration_view(request):
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'login.html', context)