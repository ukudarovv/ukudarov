# Generated by Django 4.0.2 on 2022-11-16 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_category_all'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/', verbose_name='Изображение'),
        ),
    ]
