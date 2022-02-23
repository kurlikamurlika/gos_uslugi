from .forms import *
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
import random, string
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'bank/index.html')

def profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)
    bank_acc = ''
    transaction_get = ''
    transaction_send = ''
    try:
        bank_acc = BankAccount.objects.get(user_id=user_id)
        no_account = False
        transaction_get = Transaction.objects.filter(receiver_id=bank_acc.id)
        transaction_send = Transaction.objects.filter(sender_id=bank_acc.id)
    except:
        no_account = True
    return render(request, 'bank/profile.html', context={'no_account': no_account, 'bank_acc': bank_acc, 'user_profile': user_profile, 'trans_get': transaction_get, 'trans_send': transaction_send})

def bank_result(request):
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    bank = BankAccount(user_id=request.user.id, name=name, balance=0)
    bank.save()
    return HttpResponseRedirect(reverse('bank:profile', args=(request.user.id,)))

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('bank:index')
    else:
        form = SignUpForm()
    return render(request, 'bank/register.html', {'form': form})

def send(request):
    works = True
    bank_account = ''
    not_enough_money = False
    try:
        bank_account = BankAccount.objects.get(user_id=request.user.id)
        has_bank = True
    except:
        has_bank = False
    form = SendMoney(request.POST or None)

    if form.is_valid():
        receiver = form.cleaned_data.get("receiver")
        amount = int(form.cleaned_data.get('amount'))
        if bank_account.balance >= amount:
            try:
                receiver_object = BankAccount.objects.get(name=receiver)
                receiver_id = receiver_object.id
                trans = Transaction(sender_id=bank_account.id, receiver_id=receiver_id, amount=amount, pub_time=timezone.now())
                bank_account.balance -= amount
                receiver_object.balance += amount

                bank_account.save()
                receiver_object.save()
                trans.save()

                works = True
            except:
                works = False
        else:
            not_enough_money = True

    send_dict = {
        'has_bank': has_bank,
        'bank_account': bank_account,
        'form': form,
        'works': works,
        'not_enough_money': not_enough_money,
    }
    return render(request, 'bank/send.html', context=send_dict)

def send_result(request):

    return HttpResponseRedirect(reverse('bank:send'))

def about_us(request):
    return render(request, 'bank/about_us.html')

def citizen(request):
    has_citizenship = False
    citizenship = ''
    bank_account = ''
    property_list = []
    try:
        bank_account = BankAccount.objects.get(user_id=request.user.id)
        has_bank = True
    except:
        has_bank = False

    try:
        citizenship = Citizen.objects.get(user_id=request.user.id)
        has_citizenship = True
        property_list = Property.objects.filter(citizen_id=citizenship.id)
    except:
        has_citizenship = False
    form = getCitizenShip(request.POST or None)
    form_property = RegisterProperty(request.POST or None)
    citizen_dict = {
        'has_citizenship': has_citizenship,
        'citizenship': citizenship,
        'form': form,
        'has_bank': has_bank,
        'form_property': form_property,
        'property_list': property_list,
    }

    if form.is_valid():
        minecraft_username = form.cleaned_data.get("minecraft_username")
        discord_username = form.cleaned_data.get("discord_username")
        country = form.cleaned_data.get('country')
        askCitizenship = AskCitizenship(user_id=request.user.id, bank_account=bank_account, discord_name=discord_username, minecraft_name=minecraft_username, country=country)
        askCitizenship.save()
        return HttpResponseRedirect(reverse('bank:get_citizenship'))
    if form_property.is_valid():
        citizen_property = form_property.save(commit=False)
        citizen_property.citizen = citizenship
        citizen_property.save()
    return render(request, 'bank/citizen.html', context=citizen_dict)

def get_citizenship(request):
    return render(request, 'bank/get_citizenship.html')

def jobs(request):
    form = JobOfferForm(request.POST or None)
    job_list = JobOffer.objects.order_by('-pub_time')
    jobs_dict = {
        'form': form,
        'job_list': job_list,
    }
    if form.is_valid():
        job_offer = form.save(commit=False)
        job_offer.employer = request.user
        job_offer.save()
        return HttpResponseRedirect(reverse('bank:index'))
    return render(request, 'bank/jobs.html', context=jobs_dict)