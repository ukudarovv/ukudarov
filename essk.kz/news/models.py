from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone


class Banner(models.Model):
    title = models.CharField(max_length=64, verbose_name='Название', blank=True)
    image = models.ImageField(upload_to='banner/', verbose_name='Изображение', blank=True)
    url = models.URLField(verbose_name='Ссылка', max_length=1000, blank=True)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.title


class CategoryPublication(models.Model):
    title = models.CharField(max_length=64, verbose_name='Категория', unique=True)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('publication_category', kwargs={'id': self.id})


class Publication(models.Model):
    category = models.ForeignKey(CategoryPublication, verbose_name='Категория', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name='Заголовок', unique=False, blank=True)
    image = models.ImageField(upload_to='publication/', verbose_name='Изображение', blank=True)
    image_2 = models.ImageField(upload_to='publication/', verbose_name='Изображение 2', blank=True)
    description = models.TextField(verbose_name='Текст', null=True, blank=True)
    created_at_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    is_active = models.BooleanField(verbose_name='Показывать', default=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('publication_detail', kwargs={'id': self.id})
