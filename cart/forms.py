# -*- coding: utf-8 -*-
from django import forms
from django.forms import NumberInput
from cart.models import CartAddProductModel


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.ModelForm):
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    class Meta:
        model = CartAddProductModel
        fields = ['quantity', 'update']
        widgets = {
            'quantity': NumberInput(attrs={'style': 'width:50px'}),
        }
