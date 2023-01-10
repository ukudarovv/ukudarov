from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('basket_adding/', basket_adding, name='basket_adding'),
    path('', cart, name='cart'),
    path('order_create/', order_create, name='order_create'),
]
