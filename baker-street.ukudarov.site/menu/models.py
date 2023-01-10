from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from users.models import *
from shops.models import *
from products.models import *


class IngredientCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название', blank=True)

    class Meta:
        verbose_name = 'Категория ингредиента'
        verbose_name_plural = 'Категории ингредиентов'

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

    title = models.CharField(max_length=255, verbose_name='Название', blank=True)
    category = models.ForeignKey('IngredientCategory', verbose_name='Категория ингредиента', on_delete=models.SET_NULL, blank=True, null=True, related_name='ingredient_category')
    qty = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Количество', default=0.0, blank=True)
    unit_of_measurement = models.CharField(
        max_length=100,
        verbose_name='Ед. измерения',
        choices=LIST_UN_MEASUREMENT,
        default=KG,
        blank=True
    )
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена', default=0.0, blank=True)
    cost_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Себестоимость', default=0.0, blank=True)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return "{}".format(self.title)

    def save(self, *args, **kwargs):
        products = UnderIngredient.objects.filter(product=self)
        cost_price = 0
        for item in products:
            cost_price += item.cost_price
        self.cost_price = cost_price
        super().save(*args, **kwargs)


class UnderIngredient(models.Model):
    PC = 'pc'
    GR = 'gr'
    ML = 'ml'

    LIST_UN_MEASUREMENT = (
        (GR, 'гр'),
        (PC, 'шт'),
        (ML, 'мл'),
    )

    product = models.ForeignKey('Ingredient', verbose_name='Продукт',  on_delete=models.SET_NULL, blank=True, null=True, related_name='under_ingredient_product')
    ingredient = models.ForeignKey('Ingredient', verbose_name='Ингредиент',  on_delete=models.SET_NULL, blank=True, null=True, related_name='under_ingredient_ingredient')
    gross = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Брутто', default=0.0, blank=True)
    unit_of_measurement = models.CharField(
        max_length=100,
        verbose_name='Ед. измерения',
        choices=LIST_UN_MEASUREMENT,
        default=GR,
        blank=True
    )
    cost_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Себестоимость', default=0.0, blank=True)

    class Meta:
        verbose_name = 'Подингредиенты продукта'
        verbose_name_plural = 'Подингредиенты продуктов'

    def __str__(self):
        return "{}".format(self.product.title)

    def save(self, *args, **kwargs):
        if self.ingredient.unit_of_measurement == 'kg':
            self.unit_of_measurement = 'gr'
            qty = self.ingredient.qty * 1000
            price = self.ingredient.price / qty
            self.cost_price = self.gross * price

        elif self.ingredient.unit_of_measurement == 'gr':
            self.unit_of_measurement = 'gr'
            price = self.ingredient.price / self.ingredient.qty
            self.cost_price = self.gross * price

        elif self.ingredient.unit_of_measurement == 'l':
            self.unit_of_measurement = 'ml'
            qty = self.ingredient.qty * 1000
            price = self.ingredient.price / qty
            self.cost_price = self.gross * price

        elif self.ingredient.unit_of_measurement == 'ml':
            self.unit_of_measurement = 'ml'
            price = self.ingredient.price / self.ingredient.qty
            self.cost_price = self.gross * price

        super().save(*args, **kwargs)


class TechCard(models.Model):
    product = models.ForeignKey('products.Product', verbose_name='Товар',  on_delete=models.SET_NULL, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Себестоимость', default=0.0)

    class Meta:
        verbose_name = 'Тех. карта продукта'
        verbose_name_plural = 'Тех. карты продуктов'

    def __str__(self):
        return "{}".format(self.product.title)

    def save(self, *args, **kwargs):
        products = TechCardIngredient.objects.filter(product=self)
        cost_price = 0
        for item in products:
            cost_price += item.cost_price
        self.cost_price = cost_price
        super().save(*args, **kwargs)


class TechCardIngredient(models.Model):
    PC = 'pc'
    GR = 'gr'
    ML = 'ml'

    LIST_UN_MEASUREMENT = (
        (GR, 'гр'),
        (PC, 'шт'),
        (ML, 'мл'),
    )

    product = models.ForeignKey('TechCard', verbose_name='Продукт',  on_delete=models.SET_NULL, blank=True, null=True)
    ingredient = models.ForeignKey('Ingredient', verbose_name='Ингредиент',  on_delete=models.SET_NULL, blank=True, null=True)
    gross = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Брутто', default=0.0)
    unit_of_measurement = models.CharField(
        max_length=100,
        verbose_name='Ед. измерения',
        choices=LIST_UN_MEASUREMENT,
        default=GR,
        blank=True
    )
    cost_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Себестоимость', default=0.0)

    class Meta:
        verbose_name = 'Ингредиенты продукта'
        verbose_name_plural = 'Ингредиенты продуктов'

    def __str__(self):
        return "{}".format(self.product.product.title)

    def save(self, *args, **kwargs):
        if self.ingredient.unit_of_measurement == 'kg':
            self.unit_of_measurement = 'gr'
            qty = self.ingredient.qty * 1000
            price = self.ingredient.price / qty
            self.cost_price = self.gross * price

        elif self.ingredient.unit_of_measurement == 'gr':
            self.unit_of_measurement = 'gr'
            price = self.ingredient.price / self.ingredient.qty
            self.cost_price = self.gross * price

        elif self.ingredient.unit_of_measurement == 'l':
            self.unit_of_measurement = 'ml'
            qty = self.ingredient.qty * 1000
            price = self.ingredient.price / qty
            self.cost_price = self.gross * price

        elif self.ingredient.unit_of_measurement == 'ml':
            self.unit_of_measurement = 'ml'
            price = self.ingredient.price / self.ingredient.qty
            self.cost_price = self.gross * price

        super().save(*args, **kwargs)
