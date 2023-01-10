from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование', blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать?', default=False, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class Supplier(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='Номер телефона', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')
    is_active = models.BooleanField(verbose_name='Показывать?', default=False, blank=True)

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return "Продавец: {} {}".format(self.user.username, self.user.first_name)


class ProductSupplier(models.Model):
    supplier = models.ForeignKey(Supplier, verbose_name='Продавец', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Показывать?', default=False, blank=True)

    class Meta:
        verbose_name = 'Товар (Продавец)'
        verbose_name_plural = 'Товары (Продавец)'

    def __str__(self):
        return "Товар (Продавец): {} {}".format(self.product.title, self.supplier.user.username)


class CategoryRestaurant(models.Model):
    title = models.CharField(db_index=True, max_length=40, verbose_name='Название категории', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать?', default=False, blank=True)

    class Meta:
        verbose_name = 'Категория (Заведение)'
        verbose_name_plural = 'Категории (Заведение)'

    def __str__(self):
        return "Категория (Заведение): {}".format(self.title)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'id': self.id})


class Restaurant(models.Model):
    category = models.ForeignKey(CategoryRestaurant, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(db_index=True, max_length=20, verbose_name='Название заведения', blank=True)
    image = models.ImageField(upload_to='restaurant/logo/', verbose_name='Изображение', blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать?', default=False, blank=True)

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('restaurant_detail', kwargs={'id': self.id})


class ProductRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, verbose_name='Заведение', on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, verbose_name='Продавец', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Показывать?', default=False, blank=True)

    class Meta:
        verbose_name = 'Товар (Заведение)'
        verbose_name_plural = 'Товары (Заведение)'

    def __str__(self):
        return "Товар (Заведение): {} {} {}".format(self.restaurant.title, self.product.title, self.supplier.user.username)
