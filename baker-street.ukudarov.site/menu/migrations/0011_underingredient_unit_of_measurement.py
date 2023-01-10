# Generated by Django 4.0.2 on 2022-04-18 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0010_alter_underingredient_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='underingredient',
            name='unit_of_measurement',
            field=models.CharField(blank=True, choices=[('kg', 'кг'), ('gr', 'гр'), ('pc', 'шт'), ('l', 'л'), ('ml', 'мл')], default='kg', max_length=100, verbose_name='Ед. измерения'),
        ),
    ]