# Generated by Django 4.0.2 on 2022-10-25 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_initial'),
        ('orders', '0004_alter_order_address_alter_order_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carts.cart', verbose_name='Корзина'),
        ),
    ]
