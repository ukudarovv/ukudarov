from django.db import models


class Country(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = '1) Страны'

    def __str__(self):
        return self.title


class Area(models.Model):
    country = models.ForeignKey(Country, verbose_name='Страна', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)

    class Meta:
        verbose_name = 'Область (Регион)'
        verbose_name_plural = '2) Областя (Регионы)'

    def __str__(self):
        return self.title


class City(models.Model):
    area = models.ForeignKey(Area, verbose_name='Область (Регион)', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = '3) Города'

    def __str__(self):
        return self.title
