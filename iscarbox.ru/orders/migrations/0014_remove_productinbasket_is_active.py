# Generated by Django 3.1 on 2020-08-11 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_productinbasket_product_accessory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinbasket',
            name='is_active',
        ),
    ]
