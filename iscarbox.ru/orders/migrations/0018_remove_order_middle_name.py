# Generated by Django 3.1 on 2020-08-12 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_productinorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='middle_name',
        ),
    ]