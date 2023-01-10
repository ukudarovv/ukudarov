from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from products.models import *
from users.models import *
from addition.models import *
from carts.models import *

User = get_user_model()


class PaymentType(models.Model):
    title = models.CharField(max_length=64, verbose_name='Вид', unique=True)

    class Meta:
        verbose_name = 'Вид оплаты'
        verbose_name_plural = 'Виды оплаты'

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_CANCELLED = 'is_cancelled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_CANCELLED, 'Заказ отменен'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    LE = 'le'
    PE = 'pe'

    TYPE_CHOICES = (
        (LE, 'Юр. лицо'),
        (PE, 'Физ. лицо')
    )

    token = models.CharField(max_length=255, verbose_name='CSRF Token', blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey('users.Company', verbose_name='Компания', on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(
        max_length=100,
        verbose_name='Тип плательщика',
        choices=TYPE_CHOICES,
        default=PE,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        blank=True,
        null=True
    )
    payment = models.ForeignKey(PaymentType, verbose_name='Тип оплаты', on_delete=models.SET_NULL, null=True)
    person = models.CharField(max_length=250, verbose_name='Контактное лицо', null=True)
    phone = models.CharField(max_length=15, verbose_name='Моб. телефон', null=True)
    email = models.EmailField(verbose_name='Эл. почта', null=True)
    country = models.ForeignKey('addition.Country', verbose_name='Страна', on_delete=models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey('addition.Area', verbose_name='Область (Регион)', on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey('addition.City', verbose_name='Город', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250, verbose_name='Улица, Дом (Квартира)', null=True)
    total_products = models.PositiveIntegerField(verbose_name='Количество товаров', default=0, blank=True, null=True)
    total_price = models.DecimalField(max_digits=15, default=0, decimal_places=2, verbose_name='Общая сумма', blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа', blank=True, null=True)
    for_anonymous_user = models.BooleanField(verbose_name='Анонимный пользователь', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "Покупатель: {} ".format(self.id)

    def save(self, *args, **kwargs):
        total_price = 0
        total_products = 0
        products = OrderProduct.objects.filter(order=self)
        for item in products:
            total_products += 1
            total_price += item.total_price
        self.total_price = total_price
        self.total_products = total_products
        super().save(*args, **kwargs)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.PositiveIntegerField(verbose_name='Количество', default=0, blank=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Общая сумма', blank=True)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return "Продукт: {} (для заказа)".format(self.product.title)

    def save(self, *args, **kwargs):
        if self.product.new_price != 0:
            self.total_price = self.qty * self.product.new_price
        else:
            self.total_price = self.qty * self.product.price
        super().save(*args, **kwargs)
