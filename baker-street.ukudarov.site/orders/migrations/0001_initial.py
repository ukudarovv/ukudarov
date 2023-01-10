# Generated by Django 4.0.2 on 2022-02-11 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '__first__'),
        ('products', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, choices=[('customer', 'Покупатель'), ('deliveryman', 'Доставщик'), ('shop_administrator', 'Администратор')], default='customer', max_length=100, verbose_name='Роль')),
                ('for_anonymous_user', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('phone', models.CharField(max_length=11, verbose_name='Телефон')),
                ('address', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Адрес')),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата получения заказа')),
                ('status', models.CharField(choices=[('new', 'Новый заказ'), ('in_progress', 'Заказ в обработке'), ('is_cancelled', 'Заказ отменен'), ('completed', 'Заказ выполнен')], default='new', max_length=100, verbose_name='Статус заказ')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, verbose_name='Итоговая сумма')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('buyer_shop', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_shop', to='shops.shopbuyer', verbose_name='Закупщик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderProductRemainder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Итоговая сумма')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product_remainder', to='orders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Остаток от заказа',
                'verbose_name_plural': 'Остатки от заказов',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Итоговая сумма')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='orders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='order_products', to='orders.OrderProduct', verbose_name='Товары'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]