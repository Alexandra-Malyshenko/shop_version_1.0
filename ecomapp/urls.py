from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .views import (
    base_view,
    category_view,
    product_view,
    contact_view,
    # product_list_view,
    product_search_view,
    # sorting_products_view,
    all_category_view,
    )


urlpatterns = [
    url(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    url(r'^product_search/$', product_search_view , name='product_search'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
    url(r'^contact/$', contact_view, name='contact'),
    url(r'^all_products', all_category_view, name='all_categories'),
    # url(r'^search$', product_list_view, name='search'),
    # url(r'^sort_by/$', sorting_products_view , name='sorting_products'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    url(r'^$', base_view, name='base')
]
