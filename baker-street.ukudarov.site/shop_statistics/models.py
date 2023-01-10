from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from users.models import *
from shops.models import *


class ForDay(models.Model):
    created_at = models.DateField(verbose_name='Дата создания', blank=True, default=timezone.now)

    order = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая сумма (Заказы)', default=0.0)
    order_cash = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма наличными (Заказы)', default=0.0)
    order_kaspi = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма каспи (Заказы)', default=0.0)
    order_debt = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая сумма долга (Заказы)', default=0.0)
    order_debt_cash = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма наличными долга (Заказы)', default=0.0)
    order_debt_kaspi = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма каспи долга (Заказы)', default=0.0)

    order_realization = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая сумма (Заказы под реализацию)', default=0.0)
    order_realization_debt = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая сумма долга (Заказы под реализацию)', default=0.0)

    refund = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая сумма (Возврат)', default=0.0)
    stocks = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая сумма (Акции)', default=0.0)
    order_qty = models.PositiveIntegerField(default=0, verbose_name='Количество (Заказы)')
    order_realization_qty = models.PositiveIntegerField(default=0, verbose_name='Количество (Заказы под реализацию)')
    refund_qty = models.PositiveIntegerField(default=0, verbose_name='Количество (Возврат)')
    stocks_qty = models.PositiveIntegerField(default=0, verbose_name='Количество (Акции)')

    class Meta:
        verbose_name = 'Статистика за день'
        verbose_name_plural = 'Статистика за день'

    def __str__(self):
        return "{}".format(self.created_at)
