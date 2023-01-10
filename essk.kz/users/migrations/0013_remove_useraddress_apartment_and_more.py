# Generated by Django 4.0.2 on 2022-10-26 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_remove_categoryrequisite_pe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='apartment',
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='street',
            field=models.CharField(blank=True, max_length=200, verbose_name='Улица, дом, квартира'),
        ),
    ]