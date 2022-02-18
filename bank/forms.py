from django import forms
from django_countries.fields import CountryField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='Имя пользователя')
    first_name = forms.CharField(max_length=30, label="Имя")
    last_name = forms.CharField(max_length=30, label="Фамилия")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class SendMoney(forms.Form):
    receiver = forms.CharField(max_length=10, min_length=10, label='Код ЦБ получателя')
    amount = forms.IntegerField(min_value=100, label="Сумма")

class getCitizenShip(forms.Form):
    minecraft_username = forms.CharField(label="Ваш ник в Minecraft", min_length=3, max_length=16)
    discord_username = forms.CharField(label='Ваш ник в Discord')
    country = CountryField().formfield()

class RegisterProperty(forms.ModelForm):
    property_type = forms.CharField(label='Тип имущества')
    market_price = forms.IntegerField(label="Рыночная стоимость", min_value=0)
    name = forms.CharField(label="Имя")
    description = forms.CharField(label='Описание')
    class Meta:
        model = Property
        fields = ('property_type', 'market_price', 'name', 'description')


