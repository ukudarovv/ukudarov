# Generated by Django 4.0.2 on 2022-11-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_category_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category_all',
            field=models.ManyToManyField(blank=True, related_name='related_category_all', to='products.Category', verbose_name='Категории'),
        ),
    ]