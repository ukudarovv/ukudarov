# Generated by Django 4.0.2 on 2022-02-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_shopbuyer_kaspi_name'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryman',
            name='shops',
            field=models.ManyToManyField(blank=True, related_name='related_shops', to='shops.ShopBuyer', verbose_name='Магазины'),
        ),
    ]