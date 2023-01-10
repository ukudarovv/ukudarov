from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name='Наименование', blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена', blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title
