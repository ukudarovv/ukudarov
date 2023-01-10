from django.db import models
from django.contrib.auth import get_user_model
from products.models import *


User = get_user_model()


class Cart(models.Model):
    token = models.CharField(max_length=255, verbose_name='CSRF Token', blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True)
    total_products = models.PositiveIntegerField(verbose_name='Количество товаров', default=0, blank=True)
    total_price = models.IntegerField(default=0,  verbose_name='Общая сумма', blank=True)
    for_anonymous_user = models.BooleanField(verbose_name='Анонимный пользователь', default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return "Покупатель: {} ".format(self.id)

    def save(self, *args, **kwargs):
        total_price = 0
        total_products = 0
        products = CartProduct.objects.filter(cart=self)
        for item in products:
            total_products += 1
            total_price += item.total_price
        self.total_price = total_price
        self.total_products = total_products
        super().save(*args, **kwargs)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.PositiveIntegerField(verbose_name='Количество', default=0, blank=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Общая сумма', blank=True)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзинах'

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.product.price
        super().save(*args, **kwargs)
