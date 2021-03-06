# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
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
from .forms import ProductFilterForm, SortFilterForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib.postgres.search import SearchQuery
# from django.contrib.postgres.search import SearchVector
import json
from django.forms.models import model_to_dict
from django.core import serializers
import decimal


def base_view(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart = Cart(request)
    cart_product_form = CartAddProductForm()
    list_products = []
    counter = 0
    for category in categories:
        for prod in products:
            if (prod.category == category) and (counter <=3):
                counter += 1
                list_products.append(prod)
        counter = 0
    context = {
        'categories': categories,
        'products': list_products,
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

    volume = []
    for item in products:
        volume.append(float(item.volume))
    volume = list(set(volume))
    volume_ser = (json.dumps(volume))

    sae = []
    for item in products:
        if item.sae not in sae:
            sae.append(item.sae)
    sae = list(set(sae))
    sae_ser = (json.dumps(sae))

    # sort_form = SortFilterForm(request.GET)
    # filter_form = filter_form_search(request, category_slug)
    filter_form = ProductFilterForm(request.GET)
    if filter_form.is_valid():

        # products = sort_by(filter_form, products)

        if filter_form.cleaned_data["min_price"]:
            products = products.filter(price__gte=filter_form.cleaned_data["min_price"])

        if filter_form.cleaned_data["max_price"]:
            products = products.filter(price__lte=filter_form.cleaned_data["max_price"])

        if filter_form.cleaned_data["ordering"]:
            products = products.order_by(filter_form.cleaned_data["ordering"])

        if filter_form.cleaned_data["the_brand"]:
            list_items = filter_form.cleaned_data["the_brand"]
            list_items_=[]
            for i in list_items:
                list_items_.append(i)

            products = products.filter(brand__name__in=list_items_)

        if filter_form.cleaned_data["the_sae"]:
            list_items = filter_form.cleaned_data["the_sae"]
            list_items_=[]
            for i in list_items:
                list_items_.append(i)

            products = products.filter(sae__in=list_items_)

        if filter_form.cleaned_data["the_choices"]:

            items = filter_form.cleaned_data["the_choices"]
            items_ =[]
            if items:
                for i in items:
                    items_.append(i)

                products = products.filter(volume__in=items_)



    current_page = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = current_page.page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        products= current_page.page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        products = current_page.page(current_page.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'category': category,
        'cart': cart,
        'cart_product_form': cart_product_form,
        'filter_form': filter_form,
        'volume': volume_ser,
        'sae': sae_ser,
        # 'sort_form': sort_form,
    }

    # products = paginator.page(page)
    # paginator = Paginator(products, 6)
    # page = request.GET.get('page')
    # try:
    #     products = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     products = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     products = paginator.page(paginator.num_pages)

    # if sort_form.is_valid():
    #     if sort_form.cleaned_data["ordering"]:
    #         products = products.order_by(sort_form.cleaned_data["ordering"])

    # if request.is_ajax():  # os request.GET()
    #     ordering = request.POST.get("sort_type")
    #     # category_slug = request.POST.get("category_slug")
    #     # category = Category.objects.get(name=category_slug)
    #     products = products.order_by(ordering)



    return render(request, 'category.html', context)

# def sort_by(form, items):
#     if form.cleaned_data["ordering"]:
#         items = items.order_by(form.cleaned_data["ordering"])
#     return items

def all_category_view(request):
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    volume = []
    for item in products:
        volume.append(float(item.volume))
    volume = list(set(volume))
    volume_ser = (json.dumps(volume))

    sae = []
    for item in products:
        sae.append(item.sae)
    sae = list(set(sae))
    sae_ser = (json.dumps(sae))

    # sort_form = SortFilterForm(request.GET)
    # filter_form = filter_form_search(request, category_slug)
    filter_form = ProductFilterForm(request.GET)
    if filter_form.is_valid():

        # products = sort_by(filter_form, products)

        if filter_form.cleaned_data["min_price"]:
            products = products.filter(price__gte=filter_form.cleaned_data["min_price"])

        if filter_form.cleaned_data["max_price"]:
            products = products.filter(price__lte=filter_form.cleaned_data["max_price"])

        if filter_form.cleaned_data["ordering"]:
            products = products.order_by(filter_form.cleaned_data["ordering"])

        if filter_form.cleaned_data["the_brand"]:
            list_items = filter_form.cleaned_data["the_brand"]
            list_items_=[]
            for i in list_items:
                list_items_.append(i)

            products = products.filter(brand__name__in=list_items_)

        if filter_form.cleaned_data["the_sae"]:
            list_items = filter_form.cleaned_data["the_sae"]
            list_items_=[]
            for i in list_items:
                list_items_.append(i)

            products = products.filter(sae__in=list_items_)

        if filter_form.cleaned_data["the_choices"]:

            items = filter_form.cleaned_data["the_choices"]
            items_ =[]
            if items:
                for i in items:
                    items_.append(i)

                products = products.filter(volume__in=items_)


    current_page = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = current_page.page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        products= current_page.page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        products = current_page.page(current_page.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'cart': cart,
        'cart_product_form': cart_product_form,
        'filter_form': filter_form,
        'volume': volume_ser,
        'sae': sae_ser,
        # 'sort_form': sort_form,
    }

    # products = paginator.page(page)
    # paginator = Paginator(products, 6)
    # page = request.GET.get('page')
    # try:
    #     products = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     products = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     products = paginator.page(paginator.num_pages)

    # if sort_form.is_valid():
    #     if sort_form.cleaned_data["ordering"]:
    #         products = products.order_by(sort_form.cleaned_data["ordering"])

    # if request.is_ajax():  # os request.GET()
    #     ordering = request.POST.get("sort_type")
    #     # category_slug = request.POST.get("category_slug")
    #     # category = Category.objects.get(name=category_slug)
    #     products = products.order_by(ordering)


    return render(request, 'all_categories.html', context)


def contact_view(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart = Cart(request)
    cart_product_form = CartAddProductForm()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
        'cart_product_form': cart_product_form
    }
    return render(request, 'contact.html', context)


def product_search_view(request):
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    question = str(request.GET.get('q'))
    if question is not None:
        # filters = Q()
        # for word in question.split(" "):
        #     filters |= Q(title__icontains=word)
        found_search = Product.objects.filter(title__search=question)

        filter_form = ProductFilterForm(request.GET)
        if filter_form.is_valid():
            if filter_form.cleaned_data["min_price"]:
                found_search = found_search.filter(price__gte=filter_form.cleaned_data["min_price"])

            if filter_form.cleaned_data["max_price"]:
                found_search = found_search.filter(price__lte=filter_form.cleaned_data["max_price"])

            if filter_form.cleaned_data["ordering"]:
                found_search = found_search.order_by(filter_form.cleaned_data["ordering"])

            if filter_form.cleaned_data["the_brand"]:
                found_search = found_search.filter(filter_form.cleaned_data["the_brand"])

            if filter_form.cleaned_data["the_choices"]:

                items = filter_form.cleaned_data["the_choices"]
                items_ =[]
                if items:
                    for i in items:
                        items_.append(int(i))

                    found_search = found_search.filter(volume__in=items_)

        context ={
            'categories': categories,
            'cart': cart,
            'cart_product_form': cart_product_form,
            'products': products,
            'found_search': found_search,
            'filter_form': filter_form
        }
        return render(request, 'search.html', context)


# def sorting_products_view(request):
#     cart_product_form = CartAddProductForm()
#     cart = Cart(request)
#     categories = Category.objects.all()
#     if request.is_ajax():  # os request.GET()
#         ordering = request.POST.get("sort_type")
#         category_slug = request.POST.get("category_slug")
#         category = Category.objects.get(name=category_slug)
#         products = Product.objects.filter(available=True, category=category).order_by(ordering)
#
#         filter_form = ProductFilterForm(request.GET)
#         if filter_form.is_valid():
#             if filter_form.cleaned_data["min_price"]:
#                 products = products.filter(price__gte=filter_form.cleaned_data["min_price"])
#             if filter_form.cleaned_data["max_price"]:
#                 products = products.filter(price__lte=filter_form.cleaned_data["max_price"])
#             if filter_form.cleaned_data["ordering"]:
#                 products = products.order_by(filter_form.cleaned_data["ordering"])
#             if filter_form.cleaned_data["the_choices"]:
#                 items = filter_form.cleaned_data["the_choices"]
#                 if items:
#                     items_products = []
#                     for i in items:
#                         items_products += products.filter(volume=int(i))
#                         products = items_products
#
#         data = {
#             'products': products,
#             'categories': categories,
#             'category': category,
#             'cart': cart,
#             'cart_product_form': cart_product_form,
#             'filter_form': filter_form,
#         }
#         # return redirect(reverse('category_detail'))
#         return render(request, 'category.html', data)

        # products_serialized = serializers.serialize('json', products)
        # # Do your logic here coz you got data in `get_value`
        # data = {'products': products_serialized}
        # # if categories:
        # #     data['text'] = 'true'
        # # else:
        # #     data['text'] = 'false'
        # return JsonResponse(data)


# for word in question :
        #     search_query = SearchQuery(word)
        #     search_vector = SearchVector('title')
        # found_search = Product.objects.anotate(search=search_vector).filter(search=search_query)
#
# def filter_form_search(request, category_slug):
#     category = Category.objects.get(slug=category_slug)
#     filterform = ProductFilterForm()
#     products = Product.objects.filter(available=True, category=category)
#
#     if filterform.is_valid():
#         if filterform.cleaned_data["min_price"]:
#             products = products.filter(price_gte=filterform.cleaned_data["min_price"])
#         if filterform.cleaned_data["max_price"]:
#             products = products.filter(price_gte=filterform.cleaned_data["max_price"])
#
#     return products


# def product_list_view(request):
#     f = ProductFilterForm(request.GET, queryset=Product.objects.all())
#     return render(request, 'base.html', {'filter': f})
#

#
# def change_view(request):
#
#     products = Product.objects.filter(available=True)
#     form = ChengProductPriceForm()
#     url = 'https://api.privatbank.ua/p24api/pubinfo?jsonp=success&exchange&coursid=5'
#     data = requests.get(url).json()
#     for d in data:
#         if d["ccy"] == 'USD' and d["base_ccy"] == "UAH":
#             for product in products :
#                 product.price = product.price * int(data["buy"])
#     return render(request, 'base.html', {})



