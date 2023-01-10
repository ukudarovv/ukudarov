from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from shops.models import *
from users.models import *
from products.models import *


User = get_user_model()


class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='cart_product', blank=True)
    product = models.ForeignKey("products.Product", verbose_name='Товар', on_delete=models.CASCADE, blank=True)
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество', blank=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0, blank=True)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзинах'

    def __str__(self):
        return "{}".format(self.product.title)


class Cart(models.Model):
    CUSTOMER = 'customer'
    DELIVERYMAN = 'deliveryman'
    SHOP_ADMINISTRATOR = 'shop_administrator'

    ROLE_CHOICES = (
        (CUSTOMER, 'Покупатель'),
        (DELIVERYMAN, 'Доставщик'),
        (SHOP_ADMINISTRATOR, 'Администратор')
    )

    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True)
    role = models.CharField(
        max_length=100,
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default=CUSTOMER,
        blank=True
    )
    for_anonymous_user = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0, blank=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return "Корзина № {}".format(self.id)
