from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='bank_account')
    name = models.CharField(max_length=10, unique=True)
    balance = models.IntegerField(default=0)
    account_type = models.CharField(max_length=20, default='personal')
    def __str__(self):
        return f'{self.name}_{self.user.username}_{self.account_type}'
    class Meta:
        ordering = ['user']


class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']


class Transaction(models.Model):
    sender = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True, related_name='account_sender')
    receiver = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True, related_name='account_receiver')
    amount = models.IntegerField(default=0)
    pub_time = models.DateTimeField('Publication time', default=timezone.now)
    def __str__(self):
        return f'{self.sender.name}_{self.receiver.name}_{self.amount}'



class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='citizen')
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True, related_name='citizen')
    role = models.ManyToManyField(Role)
    discord_name = models.CharField(max_length=50, default='no')
    minecraft_name = models.CharField(max_length=16, default='no')
    country = CountryField(default="no")
    def __str__(self):
        return self.user.username
    class Meta:
        ordering = ['user']

class AskCitizenship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ask_citizenship')
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True)
    discord_name = models.CharField(max_length=50)
    minecraft_name = models.CharField(max_length=16)
    country = CountryField(default="ru")
    def __str__(self):
        return self.user.username

class Property(models.Model):
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, blank=True, null=True, related_name='properties')
    property_type = models.CharField(max_length=50)
    market_price = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return f'{self.citizen.user.username} владеет {self.property_type} ({self.name}) за {self.market_price} рублей'
    class Meta:
        ordering = ['-market_price']

class JobOffer(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_offers')
    job_name = models.CharField(max_length=50)
    salary = models.IntegerField(default=0)
    location = models.CharField(max_length=100, default='Черногорск')
    description = models.TextField()
    pub_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.job_name}_{self.employer.username}_{self.salary}'
    class Meta:
        ordering = ['-pub_time']

class Business(models.Model):
    owner = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='business')
    def __str__(self):
        return f'{self.name}_{self.bank_account.name}_{self.owner.user.username}'
    class Meta:
        ordering = ['name']

class JobPosition(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='job_positions')
    name = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.IntegerField(default=100)
    def __str__(self):
        return f'{self.name}'
    class Meta:
        ordering = ['-salary']

class Employee(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='employees')
    position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, related_name='employees')
    worker = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='employees')
    hire_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.worker.user.username}_{self.position.name}_{self.business.name}_{self.position.salary}'
    class Meta:
        ordering = ['-position']

class Service(models.Model):
    owner = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=500)
    price = models.IntegerField(default=0)
    SERVICE_TYPE_CHOICES = [
        ('товар', "Товар"),
        ("услуга", "Услуга"),
    ]
    service_type = models.CharField(max_length=100, default=SERVICE_TYPE_CHOICES[0][0], choices=SERVICE_TYPE_CHOICES) #подписка или разовая покупка
    def __str__(self):
        return f'{self.name}_{self.price}_{self.service_type}_{self.owner.name}'
    class Meta:
        ordering = ['-price']

class InterestRate(models.Model):
    service_type = models.CharField(max_length=50)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.service_type}. Ставка: {self.rate}% дневных'

class AskLoan(models.Model):
    loaner = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    interest_rate = models.ForeignKey(InterestRate, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    capital = models.IntegerField(default=0)
    period = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    payback_date = models.DateTimeField(default= timezone.now)
    payback_sum = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.loaner.user.username}_{self.interest_rate.rate}_{self.capital}_{self.payback_sum}_{self.payback_date}'

class Loan(models.Model):
    loaner = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='loans')
    interest_rate = models.ForeignKey(InterestRate, on_delete=models.CASCADE, related_name='loans')
    amount = models.IntegerField(default=0)
    capital = models.IntegerField(default=0)
    period = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    payback_date = models.DateTimeField(default=timezone.now)
    payback_sum = models.IntegerField(default=0)
    remained_sum = models.IntegerField(default=0)
    paid_sum = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.loaner.user.username}_{self.interest_rate.rate}_{self.capital}_{self.payback_sum}_{self.payback_date}'
    class Meta:
        ordering = ['-remained_sum']

class Order(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='orders')
    amount = models.IntegerField(default=1)
    total_cost = models.IntegerField(default=0)
    buy_date = models.DateTimeField(default=timezone.now)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='orders')
    def __str__(self):
        return f'{self.service.name}_{self.amount}_{self.total_cost} рублей'
    class Meta:
        ordering = ['-buy_date']

class ExchangeRate(models.Model):
    resource = models.CharField(max_length=100)
    rate = models.IntegerField(default=1)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Курс {self.resource} к CHR {self.rate} рублей.'

class Car(models.Model):
    registration_plate = models.CharField(max_length=8, primary_key=True)
    owner = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='car')
    car_model = models.OneToOneField(Property, on_delete=models.CASCADE)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.owner.user.username} владеет {self.car_model.name} с номером {self.registration_plate}'
