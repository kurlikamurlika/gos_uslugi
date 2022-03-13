from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=10, unique=True)
    balance = models.IntegerField(default=0)
    account_type = models.CharField(max_length=20, default='personal')

    def __str__(self):
        return f'{self.name}_{self.user.username}_{self.account_type}'


class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    sender = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True, related_name='account_sender')
    receiver = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True, related_name='account_receiver')
    amount = models.IntegerField(default=0)
    pub_time = models.DateTimeField('Publication time', default=timezone.now)

    def __str__(self):
        return f'{self.sender.name}_{self.receiver.name}_{self.amount}'


class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ManyToManyField(Role)
    discord_name = models.CharField(max_length=50, default='no')
    minecraft_name = models.CharField(max_length=16, default='no')
    country = CountryField(default="no")

    def __str__(self):
        return self.user.username

class AskCitizenship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, blank=True, null=True)
    discord_name = models.CharField(max_length=50)
    minecraft_name = models.CharField(max_length=16)
    country = CountryField(default="no")

    def __str__(self):
        return self.user.username

class Property(models.Model):
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, blank=True, null=True)
    property_type = models.CharField(max_length=50)
    market_price = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'{self.citizen.user.username}_{self.property_type}_{self.market_price}'

class JobOffer(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=50)
    salary = models.IntegerField(default=0)
    location = models.CharField(max_length=100, default='Черногорск')
    description = models.TextField()
    pub_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.job_name}_{self.employer.username}_{self.salary}'

class Business(models.Model):
    owner = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}_{self.bank_account.name}_{self.owner.user.username}'

class JobPosition(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.IntegerField(default=100)

    def __str__(self):
        return f'{self.name}'

class Employee(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    worker = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    hire_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.worker.user.username}_{self.position.name}_{self.business.name}_{self.position.salary}'

class Service(models.Model):
    owner = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    price = models.IntegerField(default=0)
    SERVICE_TYPE_CHOICES = [
        ('товар', "Товар"),
        ("услуга", "Услуга"),
    ]
    service_type = models.CharField(max_length=100, default=SERVICE_TYPE_CHOICES[0][0], choices=SERVICE_TYPE_CHOICES) #подписка или разовая покупка

    def __str__(self):
        return f'{self.name}_{self.price}_{self.service_type}_{self.owner.name}'

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
    loaner = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    interest_rate = models.ForeignKey(InterestRate, on_delete=models.CASCADE)
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

class Order(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    total_cost = models.IntegerField(default=0)
    buy_date = models.DateTimeField(default=timezone.now)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.service.name}_{self.amount}_{self.total_cost} рублей'

class ExchangeRate(models.Model):
    resource = models.CharField(max_length=100)
    rate = models.IntegerField(default=1)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Курс {self.resource} к CHR {self.rate} рублей.'