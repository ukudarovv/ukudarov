# Generated by Django 4.0.2 on 2022-10-27 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(blank=True, default=0, verbose_name='Общая сумма'),
        ),
    ]
