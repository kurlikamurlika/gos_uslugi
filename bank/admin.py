from django.contrib import admin
from .models import User, BankAccount, Role, Property, Citizen, Transaction, AskCitizenship, JobOffer, Service
# Register your models here.

admin.site.register(Citizen)
admin.site.register(BankAccount)
admin.site.register(Role)
admin.site.register(Property)
admin.site.register(Transaction)
admin.site.register(AskCitizenship)
admin.site.register(JobOffer)
admin.site.register(Service)
