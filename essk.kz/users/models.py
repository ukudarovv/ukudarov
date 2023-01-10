from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from addition.models import *


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, verbose_name='Моб. телефон', blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '1.1) Пользователи'

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey('addition.Country', verbose_name='Страна', on_delete=models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey('addition.Area', verbose_name='Область (Регион)', on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey('addition.City', verbose_name='Город', on_delete=models.SET_NULL, blank=True, null=True)
    street = models.CharField(max_length=200, verbose_name='Улица, дом, квартира', blank=True)
    index = models.CharField(max_length=200, verbose_name='Индекс', blank=True)

    class Meta:
        verbose_name = 'Адрес пользователя'
        verbose_name_plural = '1.2) Адреса пользователей'

    def __str__(self):
        return self.user.username


class TypeCompany(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)

    class Meta:
        verbose_name = 'Тип компании'
        verbose_name_plural = '2.2) Типы компаний'

    def __str__(self):
        return self.title


class ActivityCompany(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)

    class Meta:
        verbose_name = 'Сфера деятельности'
        verbose_name_plural = '2.3) Сферы деятельности'

    def __str__(self):
        return self.title


class Company(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    logo = models.ImageField(upload_to='images/logo/%Y/%m/%d/', verbose_name='Логотип', blank=True)
    type = models.ForeignKey(TypeCompany, verbose_name='Тип компании', on_delete=models.SET_NULL, blank=True, null=True)
    activity = models.ForeignKey(ActivityCompany, verbose_name='Сфера деятельности', on_delete=models.SET_NULL, blank=True, null=True)
    phone = models.CharField(max_length=15, verbose_name='Моб. телефон', null=True)
    email = models.EmailField(verbose_name='E-mail', blank=True)
    web_site = models.URLField(verbose_name='Сайт', blank=True)
    iin_bin = models.CharField(max_length=200, verbose_name='БИН/ИИН')
    address = models.CharField(max_length=200, verbose_name='Юридический адрес')
    kbe = models.CharField(max_length=200, verbose_name='КБе', blank=True)
    nds = models.CharField(max_length=200, verbose_name='НДС', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = '2.1) Компании'

    def __str__(self):
        return self.title


class CompanyAddress(models.Model):
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey('addition.Country', verbose_name='Страна', on_delete=models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey('addition.Area', verbose_name='Область (Регион)', on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey('addition.City', verbose_name='Город', on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, verbose_name='Улица, дом, квартира', blank=True)
    index = models.CharField(max_length=200, verbose_name='Индекс', blank=True)

    class Meta:
        verbose_name = 'Адрес компании'
        verbose_name_plural = '2.4) Адреса компаний'

    def __str__(self):
        return self.company.title


class CompanyContact(models.Model):
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.SET_NULL, blank=True, null=True)
    person = models.CharField(max_length=250, verbose_name='Контактное лицо', blank=True)
    phone = models.CharField(max_length=15, verbose_name='Моб. телефон', null=True)
    email = models.EmailField(verbose_name='E-mail', blank=True)
    for_anonymous_user = models.BooleanField(verbose_name='Анонимный пользователь', default=False)

    class Meta:
        verbose_name = 'Контакт компании'
        verbose_name_plural = '2.5) Контакты компаний'

    def __str__(self):
        return self.company.title


class CompanyBankDetails(models.Model):
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.SET_NULL, blank=True, null=True)
    bank_title = models.CharField(max_length=200, verbose_name='Наименование банка')
    bik = models.CharField(max_length=200, verbose_name='БИК')
    iik = models.CharField(max_length=200, verbose_name='ИИК')
    bank_address = models.CharField(max_length=200, verbose_name='Адрес банка', blank=True)

    class Meta:
        verbose_name = 'Банковские реквизиты компании'
        verbose_name_plural = '2.6) Банковские реквизиты компании'

    def __str__(self):
        return self.company.title


class CategoryRequisite(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)
    ie = models.BooleanField(verbose_name='ИП', default=False, blank=True)
    le = models.BooleanField(verbose_name='Юр. лицо', default=False, blank=True)

    class Meta:
        verbose_name = 'Категория (Реквезиты)'
        verbose_name_plural = '3) Категории (Реквезиты)'

    def __str__(self):
        return self.title


class CompanyRequisite(models.Model):
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.SET_NULL, blank=True, null=True)
    key = models.ForeignKey(CategoryRequisite, verbose_name='Категория (Реквезиты)', on_delete=models.SET_NULL, blank=True, null=True)
    value = models.CharField(max_length=200, verbose_name='Значение', blank=True)

    class Meta:
        verbose_name = 'Реквизит компании'
        verbose_name_plural = '2.8) Реквизиты компании'

    def __str__(self):
        return self.company.title
