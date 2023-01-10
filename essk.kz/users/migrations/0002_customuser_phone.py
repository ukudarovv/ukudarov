# Generated by Django 4.0.2 on 2022-05-20 21:43

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
    ]
