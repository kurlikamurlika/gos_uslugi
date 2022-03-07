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
        bank_acc = BankAccount.objects.filter(user_id=user_id).get(account_type='personal')
        no_account = False
        transaction_get = Transaction.objects.filter(receiver_id=bank_acc.id)
        transaction_send = Transaction.objects.filter(sender_id=bank_acc.id)
    except:
        no_account = True
    return render(request, 'bank/profile.html', context={'no_account': no_account, 'bank_acc': bank_acc, 'user_profile': user_profile, 'trans_get': transaction_get, 'trans_send': transaction_send})

def bank_result(request):
    name = 'PER' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
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
        bank_account = BankAccount.objects.filter(user_id=request.user.id).get(account_type='personal')
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
        bank_account = BankAccount.objects.filter(user_id=request.user.id).get(account_type='personal')
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
        job_offer.pub_time = timezone.now()
        job_offer.save()
        return HttpResponseRedirect(reverse('bank:index'))
    return render(request, 'bank/jobs.html', context=jobs_dict)

def business_management(request):
    form = CreateBusinessForm(request.POST or None)
    has_bank = ''
    personal_bank_acc = ''
    has_citizenship = ''
    citizenship = ''
    not_enough_money = False
    has_business = False
    try:
        personal_bank_acc = BankAccount.objects.filter(user_id=request.user.id).get(account_type='personal')
        has_bank = True
    except:
        has_bank = False
    try:
        citizenship = Citizen.objects.get(user_id=request.user.id)
        has_citizenship = True
    except:
        has_citizenship = False
    user_business = Business.objects.filter(owner_id=citizenship.id)
    if len(user_business) > 0:
        has_business = True
    else:
        has_business = False
    if form.is_valid():
        business = form.save(commit=False)
        if personal_bank_acc.balance >= 1000:
            business.owner = citizenship
            business.creation_date = timezone.now()
            name = 'BIZ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            biz_bank_acc = BankAccount(user_id=request.user.id, name=name, balance=1000, account_type='business')
            biz_bank_acc.save()
            business.bank_account = biz_bank_acc
            business.save()
            print('works!!!')
            personal_bank_acc.balance -= 1000
            personal_bank_acc.save()
        else:
            not_enough_money = True
    business_dict = {
        'form': form,
        'has_bank': has_bank,
        'has_citizenship': has_citizenship,
        'not_enough_money': not_enough_money,
        'has_business': has_business,
        'businesses': user_business,
    }
    return render(request, 'bank/business_management.html', context=business_dict)

def loan(request):
    return render(request, 'bank/loan.html')
def fiscal_info(request):
    return render(request, 'bank/fiscal_info.html')
def business_detail(request, business_id):
    business = Business.objects.get(id=business_id)
    send_money = SendMoney(request.POST or None)
    bank_account = business.bank_account
    works = True
    not_enough_money = False

    if send_money.is_valid():
        receiver = send_money.cleaned_data.get("receiver")
        amount = int(send_money.cleaned_data.get('amount'))
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
    income_trans = Transaction.objects.filter(receiver_id=bank_account.id)
    revenue = 0
    costs = 0
    for trans in income_trans:
        revenue += trans.amount
    outcome_trans = Transaction.objects.filter(sender_id=bank_account.id)
    for trans in outcome_trans:
        costs += trans.amount
    profit = revenue - costs
    create_job_position = CreateJobPosition(request.POST or None)
    if create_job_position.is_valid():
        job_position = create_job_position.save(commit=False)
        job_position.business = business
        job_position.save()
    create_employee = CreateEmployee(request.POST or None)
    create_employee.fields['position'].queryset = JobPosition.objects.filter(business_id=business.id)
    position_list = JobPosition.objects.filter(business_id=business.id)
    emp_list = Employee.objects.filter(business_id=business.id)

    if create_employee.is_valid():
        employee = create_employee.save(commit=False)
        employee.business = business
        employee.save()
    business_dict = {
        'business': business,
        'send_money': send_money,
        'works': works,
        'not_enough_money': not_enough_money,
        'revenue': revenue,
        'costs': costs,
        'profit': profit,
        'create_job_position': create_job_position,
        'create_employee': create_employee,
        'position_list': position_list,
        'emp_list': emp_list,
    }
    return render(request, 'bank/business_detail.html', context=business_dict)

def delete_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    name = employee.worker.user.username
    employee.delete()
    return render(request, 'bank/delete_employee.html', context={'name': name})