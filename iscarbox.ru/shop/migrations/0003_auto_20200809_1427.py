# Generated by Django 3.1 on 2020-08-09 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_productmaterialcolor_color_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productbordercolor',
            name='color_img',
        ),
        migrations.RemoveField(
            model_name='productthreadcolor',
            name='color_img',
        ),
    ]
