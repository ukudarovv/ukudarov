# Generated by Django 4.0.2 on 2022-02-21 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_order_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(blank=True, choices=[('simple', 'Обычный'), ('realization', 'Под реализацию')], max_length=100, verbose_name='Тип заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pay',
            field=models.CharField(blank=True, choices=[('kaspi', 'Каспи'), ('cash', 'Наличными')], max_length=100, verbose_name='Оплата'),
        ),
    ]
