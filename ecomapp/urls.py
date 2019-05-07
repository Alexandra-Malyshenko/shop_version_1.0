from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .views import (
    base_view,
    category_view,
    product_view,
    # account_view,
    registration_view,
    login_view,
    )


urlpatterns = [
    url(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
    # url(r'^account/$', account_view, name='account'),
    url(r'^registration/$', registration_view, name='registration'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    url(r'^$', base_view, name='base'),
]
