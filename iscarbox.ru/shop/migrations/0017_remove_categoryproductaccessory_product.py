# Generated by Django 3.1 on 2020-08-14 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20200815_0055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryproductaccessory',
            name='product',
        ),
    ]
