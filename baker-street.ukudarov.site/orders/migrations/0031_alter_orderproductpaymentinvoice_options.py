# Generated by Django 4.0.2 on 2022-04-06 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0030_remove_paymentinvoice_order_paymentinvoice_qty_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderproductpaymentinvoice',
            options={'verbose_name': 'Счет на оплату (Товар в заказе)', 'verbose_name_plural': 'Счет на оплату (Товары в заказе)'},
        ),
    ]
