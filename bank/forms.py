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
    property_type = forms.CharField(label='Тип имущества (квартира, машина и тд)')
    market_price = forms.IntegerField(label="Рыночная стоимость в рублях", min_value=0)
    name = forms.CharField(label="Название")
    description = forms.CharField(label='Описание')
    class Meta:
        model = Property
        fields = ('property_type', 'market_price', 'name', 'description')

class JobOfferForm(forms.ModelForm):
    job_name = forms.CharField(label='Название работы')
    salary = forms.IntegerField(min_value=0, label='Зарплата в рублях')
    location = forms.CharField(label="Расположение")
    description = forms.CharField(widget=forms.Textarea, label="Описание работы")
    class Meta:
        model = JobOffer
        exclude = ('employer', 'pub_time',)

class CreateBusinessForm(forms.ModelForm):
    name = forms.CharField(label='Название компании')
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Введите описание вашего бизнеса, например, род деятельности, местоположение и целевую аудиторию.'}), label="Описание")
    class Meta:
        model = Business
        exclude = ('owner', 'creation_date', 'bank_account')

class CreateJobPosition(forms.ModelForm):
    name = forms.CharField(label="Название должности")
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Введите описание должности, требования и обязанности и тд.'}), label="Описание")
    salary = forms.IntegerField(min_value=100, label='Зарплата в рублях за день')
    class Meta:
        model = JobPosition
        exclude = ('business',)

class CreateEmployee(forms.ModelForm):
    position = forms.ModelChoiceField(label="Должность", queryset=JobPosition.objects.all()) #Надо как-то найти бизнес_айди
    worker = forms.ModelChoiceField(label="Имя сотрудника", queryset=Citizen.objects.all())

    class Meta:
        model = Employee
        exclude = ('business', 'hire_date')

class AskLoanForm(forms.ModelForm):
    interest_rate = forms.ModelChoiceField(queryset=InterestRate.objects.all(), label="Тип займа")
    amount = forms.IntegerField(min_value=100, label="Сумма в рублях")
    period = forms.IntegerField(min_value=1, label="Срок выплаты в днях")
    class Meta:
        model = AskLoan
        exclude = ('loaner', 'capital', 'start_date', 'payback_date', 'payback_sum')

class CreateService(forms.ModelForm):
    name = forms.CharField(label="Название")
    price = forms.IntegerField(min_value=10, label="Цена в рублях")
    service_type = forms.ChoiceField(label="Товар или услуга", choices=[('товар', "Товар"),("услуга", "Услуга")])
    class Meta:
        model = Service
        exclude = ('owner',)

class MakeOrder(forms.ModelForm):
    amount = forms.IntegerField(min_value=1, label="Количество")
    class Meta:
        model = Order
        fields = ('amount',)