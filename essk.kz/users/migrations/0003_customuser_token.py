# Generated by Django 4.0.2 on 2022-05-20 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='token',
            field=models.CharField(blank=True, max_length=255, verbose_name='CSRF Token'),
        ),
    ]
