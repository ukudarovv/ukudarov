# Generated by Django 4.0.2 on 2022-02-23 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_deliveryman_first_name_alter_deliveryman_shops'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryman',
            name='shops',
        ),
    ]
