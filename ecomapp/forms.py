# -*- coding: utf-8 -*-
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Product


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином не зарегистрирован в системе!')
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Электронная почта'
        self.fields['email'].help_text = 'Пожалуйста, указывайте реальный адресс'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином уже зарегистрирован в системе!')
        if password != password_check:
            raise forms.ValidationError('Ваши пароли не совпадают! Попробуйте снова.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с данным почтовым адресом уже зарегистрирован в системе!')



CHOICES_OF_BRAND = [
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
]


def choices_of_volume():
    list_volume = []
    for product in Product.objects.all():
        if product.volume not in list_volume:
            list_volume.append(int(product.volume))
    list_volume.sort()
    return list_volume


def choices_of_brand():
    list_brand = []
    for product in Product.objects.all():
        if product.brand not in list_brand:
            list_brand.append(product.brand)
    list_brand.sort()
    return list_brand


PRODUCT_VOLUME_CHOICES = [(i, str(i)) for i in choices_of_volume()]
PRODUCT_BRAND_CHOICES = [(i, i) for i in choices_of_brand()]



class ProductFilterForm(forms.Form):
    min_price = forms.IntegerField(label="от", required=False)
    max_price = forms.IntegerField(label="до", required=False)
    the_choices = forms.MultipleChoiceField(choices=PRODUCT_VOLUME_CHOICES, required=False,
                                                 widget=forms.CheckboxSelectMultiple)
    the_brand = forms.MultipleChoiceField(choices=PRODUCT_BRAND_CHOICES, required=False,
                                            widget=forms.CheckboxSelectMultiple)
    ordering = forms.ChoiceField(label=None, required=False, choices=[
        ('title', 'по алфавиту'),
        ('price', 'цена по возрастанию'),
        ('-price', 'цена по убыванию'),
    ])


class SortFilterForm(forms.Form):
    ordering = forms.ChoiceField(label=None, required=False, choices=[
        ('title', 'по алфавиту'),
        ('price', 'цена по возрастанию'),
        ('-price', 'цена по убыванию'),
    ])