# Generated by Django 4.0.2 on 2022-02-15 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_refund_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='refund',
            name='finish_making',
            field=models.BooleanField(blank=True, default=False, verbose_name='Завершение оформления'),
        ),
    ]
