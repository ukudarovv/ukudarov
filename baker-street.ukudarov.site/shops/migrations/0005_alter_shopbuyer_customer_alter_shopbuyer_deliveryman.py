# Generated by Django 4.0.2 on 2022-02-22 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_deliveryman_shops'),
        ('shops', '0004_shopbuyer_kaspi_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopbuyer',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.shopadministrator', verbose_name='Администратор магазина'),
        ),
        migrations.AlterField(
            model_name='shopbuyer',
            name='deliveryman',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.deliveryman', verbose_name='Доставщик'),
        ),
    ]
