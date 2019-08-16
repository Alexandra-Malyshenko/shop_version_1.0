# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from ecomapp.models import Category
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from io import BytesIO
from django.template.loader import get_template
from django.template import Context
import os
# import pdfkit
import weasyprint



def OrderCreate(request):
    cart = Cart(request)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Sending email when user click Send-button
            if order.email != "":
                subject = 'Масла для автолюбителя - заказ: {}'.format(order.id)
                message = 'К email сообщению прикреплен PDF файл с информацией о вашем заказе.'
                email = EmailMessage(subject, message, 'alexandra.samoilenko94@gmail.com', [order.email])

                html = render_to_string('pdf.html', {'order': order})
                out = BytesIO()
                weasyprint.HTML(string=html).write_pdf(out,
                                                        stylesheets=[
                                                            weasyprint.CSS(settings.STATIC_ROOT + 'css/bootstrap.min.css')])
                email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
                email.send()

            cart.clear()

            return render(request, 'thank_you.html', {'order': order, 'categories': categories})

    form = OrderCreateForm()
    return render(request, 'order.html', {'cart': cart, 'form': form, 'categories': categories})


@staff_member_required
def AdminOrderDetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})


@staff_member_required
def AdminOrderPDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/bootstrap.min.css')])
    return response






# @staff_member_required
# def AdminOrderPDF(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     template = get_template("pdf.html")
#     # data is the context data that is sent to the html file to render the output.
#     html = template.render({'order': order})  # Renders the template with the context data.
#     pdfkit.from_string(html, 'out.pdf')
#     pdf = open("out.pdf")
#     response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
#     response['Content-Disposition'] = 'attachment; filename=output.pdf'
#     pdf.close()
#     os.remove("out.pdf")  # remove the locally created pdf file.
#     return response  # returns the response.
