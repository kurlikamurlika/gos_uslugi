from django.urls import path
from . import views
app_name = 'bank'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('send/', views.send, name='send'),
    path('about_us/', views.about_us, name='about_us'),
    path('citizen/', views.citizen, name='citizen'),
    path('bank_result/', views.bank_result, name='bank_result'),
    path('send_result/', views.send_result, name='send_result'),
    path('jobs/', views.jobs, name='jobs'),
    path('get_citizenship/', views.get_citizenship, name='get_citizenship'),
    path('business_management/', views.business_management, name='business_management'),
    path('business_management/loan/', views.loan, name='loan'),
    path('business_management/fiscal_info/', views.fiscal_info, name='fiscal_info'),
]