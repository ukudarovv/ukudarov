# Generated by Django 4.0.2 on 2022-11-26 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Показывать'),
        ),
    ]
