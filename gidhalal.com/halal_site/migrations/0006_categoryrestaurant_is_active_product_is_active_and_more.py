# Generated by Django 4.0.2 on 2022-10-16 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halal_site', '0005_remove_restaurant_gis_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryrestaurant',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, verbose_name='Показывать?'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, verbose_name='Показывать?'),
        ),
        migrations.AddField(
            model_name='productrestaurant',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, verbose_name='Показывать?'),
        ),
        migrations.AddField(
            model_name='productsupplier',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, verbose_name='Показывать?'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, verbose_name='Показывать?'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, verbose_name='Показывать?'),
        ),
    ]