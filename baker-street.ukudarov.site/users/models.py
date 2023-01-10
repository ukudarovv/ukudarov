from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from shops.models import *

User = get_user_model()


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.username, self.user.first_name)



class Deliveryman(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True, blank=True)
    email = models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='Номер телефона', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')

    class Meta:
        verbose_name = 'Доставщик'
        verbose_name_plural = 'Доставщики'

    def __str__(self):
        return "Доставщик: {} {}".format(self.user.username, self.user.first_name)


class ShopAdministrator(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='Номер телефона', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')

    class Meta:
        verbose_name = 'Администратор магазина'
        verbose_name_plural = 'Администраторы магазинов'

    def __str__(self):
        return "Администратор магазина: {} {}".format(self.user.username, self.user.first_name)
