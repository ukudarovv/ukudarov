# Generated by Django 4.0.2 on 2022-02-22 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_statistics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forday',
            name='order_debt',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Общая сумма долга (Заказы)'),
        ),
        migrations.AddField(
            model_name='forday',
            name='order_realization_debt',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Общая сумма долга (Заказы под реализацию)'),
        ),
    ]
