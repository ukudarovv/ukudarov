from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('<int:id>/<slug>', product_detail, name='product_detail'),
]
