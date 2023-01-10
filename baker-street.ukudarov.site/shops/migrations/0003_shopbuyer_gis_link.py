# Generated by Django 4.0.2 on 2022-02-19 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_remove_shopbuyer_email_shopbuyer_iin_bin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopbuyer',
            name='gis_link',
            field=models.URLField(blank=True, max_length=1000, verbose_name='Ссылка в 2GIS адреса магазина'),
        ),
    ]
