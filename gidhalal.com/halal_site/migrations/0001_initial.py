# Generated by Django 4.0.2 on 2022-10-08 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Наименование')),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, db_index=True, max_length=20, verbose_name='Название заведения')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('work_schedule', models.CharField(blank=True, max_length=255, verbose_name='График работы')),
                ('gis_link', models.URLField(blank=True, max_length=1000, verbose_name='Ссылка в 2GIS адреса')),
                ('phone', models.CharField(blank=True, max_length=12, verbose_name='Номер телефона')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Заведение',
                'verbose_name_plural': 'Заведения',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='Номер телефона')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Продавец',
                'verbose_name_plural': 'Продавецы',
            },
        ),
        migrations.CreateModel(
            name='ProductSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='halal_site.product', verbose_name='Товар')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='halal_site.supplier', verbose_name='Продавец')),
            ],
            options={
                'verbose_name': 'Товар (Продавец)',
                'verbose_name_plural': 'Товары (Продавец)',
            },
        ),
        migrations.CreateModel(
            name='ProductRestaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='halal_site.product', verbose_name='Товар')),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='halal_site.restaurant', verbose_name='Заведение')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='halal_site.supplier', verbose_name='Продавец')),
            ],
            options={
                'verbose_name': 'Товар (Заведение)',
                'verbose_name_plural': 'Товары (Заведение)',
            },
        ),
    ]