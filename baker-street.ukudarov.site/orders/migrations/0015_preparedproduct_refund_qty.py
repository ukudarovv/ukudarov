# Generated by Django 4.0.2 on 2022-02-19 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_preparedproduct_sale_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='preparedproduct',
            name='refund_qty',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество возвращенного'),
        ),
    ]
