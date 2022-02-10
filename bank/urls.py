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
    path('workspace/', views.workspace, name='workspace'),
    path('get_citizenship/', views.get_citizenship, name='get_citizenship')
]