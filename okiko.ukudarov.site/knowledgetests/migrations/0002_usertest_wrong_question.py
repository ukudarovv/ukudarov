# Generated by Django 3.1.6 on 2021-12-07 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgetests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertest',
            name='wrong_question',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Неправильно отвечены'),
        ),
    ]
