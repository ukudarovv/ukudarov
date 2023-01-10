from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from users.models import *
from shops.models import *
from products.models import *
from menu.models import *


class Warehouse(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название склада', blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес склада', blank=True)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return "{}".format(self.title)


class Ingredient(models.Model):

    KG = 'kg'
    PC = 'pc'
    L = 'l'
    GR = 'gr'
    ML = 'ml'

    LIST_UN_MEASUREMENT = (
        (KG, 'кг'),
        (GR, 'гр'),
        (PC, 'шт'),
        (L, 'л'),
        (ML, 'мл'),
    )

    warehouse = models.ForeignKey('Warehouse', verbose_name='Склад', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey('menu.Ingredient', verbose_name='Ингредиент', on_delete=models.SET_NULL, blank=True, null=True)
    qty = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Количество', default=0.0, blank=True)
    unit_of_measurement = models.CharField(
        max_length=100,
        verbose_name='Ед. измерения',
        choices=LIST_UN_MEASUREMENT,
        default=KG,
        blank=True
    )
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итого', default=0.0, blank=True)

    class Meta:
        verbose_name = 'Ингредиент (Склад)'
        verbose_name_plural = 'Ингредиенты (Склад)'

    def __str__(self):
        return "{}".format(self.title)

    def save(self, *args, **kwargs):
        self.price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Product(models.Model):

    warehouse = models.ForeignKey('Warehouse', verbose_name='Склад', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey('products.Product', verbose_name='Продукт', on_delete=models.SET_NULL, blank=True, null=True)
    qty = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Количество', default=0.0, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итого', default=0.0, blank=True)

    class Meta:
        verbose_name = 'Продукт (Склад)'
        verbose_name_plural = 'Продукты (Склад)'

    def __str__(self):
        return "{}".format(self.title)

    def save(self, *args, **kwargs):
        self.price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Supplier(models.Model):

    title = models.CharField(max_length=255, verbose_name='Наименование', blank=True)

    class Meta:
        verbose_name = 'Поставщик (Склад)'
        verbose_name_plural = 'Поставщики (Склад)'

    def __str__(self):
        return "{}".format(self.title)
