# Generated by Django 3.1 on 2020-08-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_productinbasket_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='session_key',
        ),
        migrations.AddField(
            model_name='productinbasket',
            name='session_key',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
    ]