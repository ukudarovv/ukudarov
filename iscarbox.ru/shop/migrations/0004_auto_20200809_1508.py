# Generated by Django 3.1 on 2020-08-09 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200809_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbordercolor',
            name='color_img',
            field=models.ImageField(blank=True, upload_to='product/%Y/%m/%d/', verbose_name='Фото товара'),
        ),
        migrations.AddField(
            model_name='productmaterialcolor',
            name='color_img',
            field=models.ImageField(blank=True, upload_to='product/%Y/%m/%d/', verbose_name='Фото товара'),
        ),
        migrations.AddField(
            model_name='productthreadcolor',
            name='color_img',
            field=models.ImageField(blank=True, upload_to='product/%Y/%m/%d/', verbose_name='Фото товара'),
        ),
    ]