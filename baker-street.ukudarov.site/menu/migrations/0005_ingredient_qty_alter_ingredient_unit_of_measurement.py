# Generated by Django 4.0.2 on 2022-04-17 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_ingredient_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='qty',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit_of_measurement',
            field=models.CharField(blank=True, choices=[('kg', 'кг'), ('gr', 'гр'), ('pc', 'шт'), ('l', 'л')], default='kg', max_length=100, verbose_name='Ед. измерения'),
        ),
    ]
