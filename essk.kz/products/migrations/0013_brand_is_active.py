# Generated by Django 4.0.2 on 2022-11-28 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_brand_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Доступен'),
        ),
    ]
