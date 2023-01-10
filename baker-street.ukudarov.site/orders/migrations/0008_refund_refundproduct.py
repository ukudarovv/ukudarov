# Generated by Django 4.0.2 on 2022-02-15 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0002_remove_shopbuyer_email_shopbuyer_iin_bin_and_more'),
        ('orders', '0007_order_buying_type_alter_order_order_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, verbose_name='Итоговая сумма')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('buyer_shop', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='refund_shop', to='shops.shopbuyer', verbose_name='Закупщик')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Возврат',
                'verbose_name_plural': 'Возвраты',
            },
        ),
        migrations.CreateModel(
            name='RefundProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Итоговая сумма')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Товар')),
                ('refund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refund_product', to='orders.refund', verbose_name='Возврат')),
            ],
            options={
                'verbose_name': 'Товар (Возврат)',
                'verbose_name_plural': 'Товары (Возврат)',
            },
        ),
    ]
