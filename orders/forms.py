# -*- coding: utf-8 -*-
from django import forms
from django.utils import timezone
from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'comments']

    # name = forms.CharField()
    # last_name = forms.CharField(required=False)
    # phone = forms.CharField()
    # email = forms.EmailField()
    # date_of_delivery = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    # address = forms.CharField(required=False)
    # comments = forms.CharField(widget=forms.Textarea, required=False)
    #
    #
    # def __init__(self, *args, **kwargs):
    #     super(OrderCreateForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].label = 'Имя'
    #     self.fields['last_name'].label = 'Фамилия'
    #     self.fields['phone'].label = 'Контактный номер телефона'
    #     self.fields['phone'].help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться.'
    #     self.fields['address'].label = 'Адрес доставки'
    #     self.fields['address'].help_text = 'Обязательно указывайте город!'
    #     self.fields['date_of_delivery'].label = 'Дата доставки'
    #     self.fields['date_of_delivery'].help_text = 'Доставка производиться на следующий день после оформления заказа. Менеджер предварительно с Вами свяжеться.'
    #     self.fields['comments'].label = 'Комментарии к заказу'
    #
