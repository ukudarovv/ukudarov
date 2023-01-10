# Generated by Django 4.0.2 on 2022-02-21 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0004_shopbuyer_kaspi_name'),
        ('products', '0001_initial'),
        ('orders', '0018_alter_order_buying_type_alter_order_pay'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, verbose_name='Итоговая сумма')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('finish_making', models.BooleanField(blank=True, default=False, verbose_name='Завершение оформления')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('buyer_shop', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocks_shop', to='shops.shopbuyer', verbose_name='Закупщик')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
            },
        ),
        migrations.CreateModel(
            name='StocksProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Итоговая сумма')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Товар')),
                ('stocks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_product', to='orders.stocks', verbose_name='Акция')),
            ],
            options={
                'verbose_name': 'Товар (Акция)',
                'verbose_name_plural': 'Товары (Акция)',
            },
        ),
    ]
