from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone


class Certificates(models.Model):

    content = models.TextField(verbose_name='Контент')

    class Meta:
        verbose_name = 'Сертификаты компании'
        verbose_name_plural = 'Сертификаты компании'

    def __str__(self):
        return self.content


class Partners(models.Model):

    content = models.TextField(verbose_name='Контент')

    class Meta:
        verbose_name = 'Партнеры компании'
        verbose_name_plural = 'Партнеры компании'

    def __str__(self):
        return self.content


class Refund(models.Model):

    content = models.TextField(verbose_name='Контент')

    class Meta:
        verbose_name = 'Возврат (Покупателям)'
        verbose_name_plural = 'Возврат (Покупателям)'

    def __str__(self):
        return self.content
