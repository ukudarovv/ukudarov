# Generated by Django 3.1 on 2020-08-09 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20200809_1508'),
        ('orders', '0004_auto_20200808_2126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('name',), 'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('name',), 'verbose_name': 'Регион', 'verbose_name_plural': 'Регионы'},
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='orders.order', verbose_name='Заказа'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Цена в рублях', max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='shop.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_border',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='shop.productbordercolor', verbose_name='Цвет оконтовки товара'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='shop.productmaterialcolor', verbose_name='Цвет материала товара'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='shop.productthreadcolor', verbose_name='Цвет нити товара'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.CreateModel(
            name='ProductInBasket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, help_text='Цена в рублях', max_digits=10, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Общая сумма')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='basket_items', to='orders.order', verbose_name='Заказа')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='basket_items', to='shop.product', verbose_name='Товар')),
                ('product_border', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='basket_items', to='shop.productbordercolor', verbose_name='Цвет оконтовки товара')),
                ('product_material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='basket_items', to='shop.productmaterialcolor', verbose_name='Цвет материала товара')),
                ('product_thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='basket_items', to='shop.productthreadcolor', verbose_name='Цвет нити товара')),
            ],
            options={
                'verbose_name': 'Товар в корзине',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
    ]