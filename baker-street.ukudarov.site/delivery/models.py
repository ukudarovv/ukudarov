from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from users.models import *
from shops.models import *


class DeliveryForDay(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата доставки')

    class Meta:
        verbose_name = 'Доставка за день'
        verbose_name_plural = 'Доставки за день'

    def __str__(self):
        return "{}".format(self.user.username)


class ShopDeliveryForDay(models.Model):
    delivery = models.ForeignKey('DeliveryForDay', verbose_name='Доставка', on_delete=models.CASCADE, blank=True)
    shop = models.ForeignKey('shops.ShopBuyer', verbose_name='Закупщик', on_delete=models.CASCADE, blank=True)
    delivered = models.BooleanField(verbose_name='Доставлено', default=False)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата доставки')

    class Meta:
        verbose_name = 'Закупщик'
        verbose_name_plural = 'Закупщики'

    def __str__(self):
        return "{}".format(self.shop.title)
