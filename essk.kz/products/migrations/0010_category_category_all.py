# Generated by Django 4.0.2 on 2022-11-17 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_all',
            field=models.ManyToManyField(blank=True, related_name='related_category', to='products.Category', verbose_name='Категории'),
        ),
    ]
