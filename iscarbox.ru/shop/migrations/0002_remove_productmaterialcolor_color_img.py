# Generated by Django 3.1 on 2020-08-09 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmaterialcolor',
            name='color_img',
        ),
    ]
