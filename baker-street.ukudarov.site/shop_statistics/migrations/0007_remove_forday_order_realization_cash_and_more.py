# Generated by Django 4.0.2 on 2022-03-03 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_statistics', '0006_remove_forday_order_realization_debt_cash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forday',
            name='order_realization_cash',
        ),
        migrations.RemoveField(
            model_name='forday',
            name='order_realization_debt_kaspi',
        ),
        migrations.RemoveField(
            model_name='forday',
            name='order_realization_kaspi',
        ),
    ]
