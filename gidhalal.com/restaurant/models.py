from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from halal_site.models import *

User = get_user_model()


class RestaurantUser(models.Model):
    restaurant = models.ForeignKey('halal_site.Restaurant', verbose_name='Заведение', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')
    is_active = models.BooleanField(verbose_name='Активность', default=True, blank=True)

    class Meta:
        verbose_name = 'Администратор заведения'
        verbose_name_plural = 'Администраторы заведений'

    def __str__(self):
        return "Администратор заведения: {} {}".format(self.restaurant.title, self.first_name)


class CategoryProduct(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    is_active = models.BooleanField(verbose_name='Показывать?', default=False, blank=True)

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.title


class RestaurantProduct(models.Model):
    restaurant = models.ForeignKey('halal_site.Restaurant', verbose_name='Заведение', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(CategoryProduct, verbose_name='Категория', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(db_index=True, max_length=100, verbose_name='Наименование', blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(verbose_name='Показывать?', default=False, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class Links(models.Model):
    restaurant = models.ForeignKey('halal_site.Restaurant', verbose_name='Заведение', on_delete=models.SET_NULL, null=True, blank=True)
    gis = models.URLField(verbose_name='Ссылка в 2GIS ', max_length=1000, blank=True)
    googlemaps = models.URLField(verbose_name='Ссылка в Google карта', max_length=1000, blank=True)
    yandexmaps = models.URLField(verbose_name='Ссылка в Yandex карта', max_length=1000, blank=True)
    applemaps = models.URLField(verbose_name='Ссылка в Apple карта', max_length=1000, blank=True)
    instagram = models.URLField(verbose_name='Ссылка в Instagram', max_length=1000, blank=True)
    facebook = models.URLField(verbose_name='Ссылка в Facebook', max_length=1000, blank=True)
    own_site = models.URLField(verbose_name='Ссылка на личный сайт', max_length=1000, blank=True)

    class Meta:
        verbose_name = 'Ссылки заведения'
        verbose_name_plural = 'Ссылки заведений'

    def __str__(self):
        return self.restaurant.title


class OpenningTime(models.Model):

    WEEKDAYS = (
        ('MONDAY', 'Понедельник'),
        ('TUESDAY', 'Вторник'),
        ('WEDNESDAY', 'Среда'),
        ('THURSDAY', 'Четверг'),
        ('FRIDAY', 'Пятница'),
        ('SATURDAY', 'Суббота'),
        ('SUNDAY', 'Воскресенье'),

    )

    restaurant = models.ForeignKey('halal_site.Restaurant', verbose_name='Заведение', on_delete=models.SET_NULL, null=True, blank=True)
    weekday = models.CharField("День", max_length=30, choices=WEEKDAYS, default='Не выбрано', blank=True)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'Графики работы'

    def __str__(self):
        return self.restaurant.title
