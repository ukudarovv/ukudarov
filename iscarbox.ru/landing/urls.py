from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('develiry/', develiry, name='develiry'),
    path('payment_methods/', paymentmethods, name='paymentmethods'),
    path('purchase_returns/', purchasereturns, name='purchasereturns'),
    path('site_policy/', sitepolicy, name='sitepolicy'),
]
