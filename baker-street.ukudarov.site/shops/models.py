from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from users.models import *


class ShopBuyer(models.Model):
    title = models.CharField(db_index=True, max_length=20, verbose_name='Название магазина', blank=True)
    kaspi_name = models.CharField(db_index=True, max_length=20, verbose_name='Имя каспи переводящего', blank=True)
    customer = models.ForeignKey('users.ShopAdministrator', verbose_name='Администратор магазина', on_delete=models.SET_NULL, blank=True, null=True)
    deliveryman = models.ForeignKey('users.Deliveryman', verbose_name='Доставщик', on_delete=models.SET_NULL, blank=True, null=True)
    iin_bin = models.CharField(max_length=12, verbose_name='ИИН/БИН Магазина', blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес магазина', blank=True)
    gis_link = models.URLField(verbose_name='Ссылка в 2GIS адреса магазина', max_length=1000, blank=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона магазина', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания магазина', blank=True)

    class Meta:
        verbose_name = 'Закупщик'
        verbose_name_plural = 'Закупщики'

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'id': self.id})
