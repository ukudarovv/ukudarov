# Generated by Django 3.1 on 2020-08-09 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20200809_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinbasket',
            name='quantity',
            field=models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Количество'),
        ),
    ]
