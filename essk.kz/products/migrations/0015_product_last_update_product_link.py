# Generated by Django 4.0.2 on 2022-12-28 20:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_remove_productfeedback_title_productfeedback_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_update',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.URLField(blank=True, verbose_name='Ссылка'),
        ),
    ]
