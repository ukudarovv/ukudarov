# Generated by Django 4.0.2 on 2022-10-22 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_category_p'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='product/%Y/%m/%d/', verbose_name='Изображение'),
        ),
    ]
