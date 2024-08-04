from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('initiate/', views.initiate_payment, name='initiate_payment'),
    path('verify/', views.verify_payment, name='verify_payment'),
    path('success/', views.payment_success, name='success'),
    path('failure/', views.payment_failure, name='failure'),
]