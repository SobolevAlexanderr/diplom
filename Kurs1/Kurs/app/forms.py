"""
Definition of forms.
"""
from django.db import models

from .models import Comment
from django import forms
from .models import Product
from .models import Blog
from .models import Order

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'имя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'пароль'}))


class AnketaForm(forms.Form):
    name=forms.CharField(label='Ваше имя', min_length=2, max_length=50)
    city=forms.CharField(label='Ваш город', min_length=2, max_length=50)
    gender=forms.ChoiceField(label='Ваш пол',
                             choices=[('1','Мужской'),('2','Женский')],
                             widget=forms.RadioSelect, initial=1)
    disain=forms.CharField(label='Как вам дизайн сайта', min_length=2, max_length=150)
    tehnik=forms.ChoiceField(label='Как часто вы пользуетесь интернет магазином',   
                             choices=(('1','Каждый день'),
                                      ('2','Несколько раз в недлю'),
                                      ('3','Несколько раз в месяц')), initial=1)
    notice=forms.BooleanField(label='Вы хотите получать новости с сайта на e-mail?',
                                     required=False)
    email= forms.EmailField(label='Ваш e-mail', min_length=7)
    polza=forms.CharField(label='Польза сайта',
                          widget=forms.Textarea(attrs={'rows':12,'cols':20}))
    nedostatki=forms.CharField(label='Недостатки сайта',
                          widget=forms.Textarea(attrs={'rows':12,'cols':20}))

class CommentForm (forms.ModelForm):

        class Meta:

            model = Comment # используемая модель

            fields = ('text',) # требуется заполнить только поле text

            labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = fields = ['name', 'description', 'category', 'price', 'image', 'area', 'floors', 'materials', 'discount']
        labels = {'name': "Заголовок", 'description': "Краткое содержание",'area': "Площадь",'floors': "Этажи",'materials': "Материалы",'category': "Категория", 'price': "Цена",'image': "Картинка","discount":"скидка"}

from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'name', 'email', 'phone_number'] 

from django import forms
from .models import ProductImage

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']