from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^admin/order/(?P<order_id>\d+)/$', views.AdminOrderDetail, name='AdminOrderDetail'),
    url(r'^admin/order/(?P<order_id>\d+)/pdf/$', views.AdminOrderPDF, name='AdminOrderPDF'),
    url(r'^create_order/$', views.OrderCreate, name='OrderCreate'),
    # url(r'^send_email/$', views.SendEmail, name='SendEmail'),
]