# Generated by Django 4.0.2 on 2022-02-21 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_alter_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания заказа'),
        ),
    ]