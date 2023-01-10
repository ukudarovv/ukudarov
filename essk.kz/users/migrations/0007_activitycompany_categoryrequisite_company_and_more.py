# Generated by Django 4.0.2 on 2022-05-21 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('addition', '0001_initial'),
        ('users', '0006_useraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Сфера деятельности',
                'verbose_name_plural': '2.3) Сферы деятельности',
            },
        ),
        migrations.CreateModel(
            name='CategoryRequisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='Наименование')),
                ('ie', models.BooleanField(blank=True, default=False, verbose_name='ИП')),
                ('le', models.BooleanField(blank=True, default=False, verbose_name='Юр. лицо')),
                ('pe', models.BooleanField(blank=True, default=False, verbose_name='Физ. лицо')),
            ],
            options={
                'verbose_name': 'Категория (Реквезиты)',
                'verbose_name_plural': '3) Категории (Реквезиты)',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='Наименование')),
                ('logo', models.ImageField(blank=True, upload_to='images/logo/%Y/%m/%d/', verbose_name='Логотип')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Номер телефона')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('web_site', models.URLField(blank=True, verbose_name='Сайт')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.activitycompany', verbose_name='Сфера деятельности')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': '2.1) Компании',
            },
        ),
        migrations.CreateModel(
            name='CompanyRequisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('ie', 'ИП'), ('le', 'Юр. лицо'), ('pe', 'Физ. лицо')], default='ie', max_length=100, verbose_name='Шаблон')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Реквизит компании',
                'verbose_name_plural': '2.7) Реквизиты компании',
            },
        ),
        migrations.CreateModel(
            name='TypeCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Тип компании',
                'verbose_name_plural': '2.2) Типы компаний',
            },
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': '1.1) Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='useraddress',
            options={'verbose_name': 'Адрес пользователя', 'verbose_name_plural': '1.2) Адреса пользователей'},
        ),
        migrations.CreateModel(
            name='RequisiteField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=200, verbose_name='Значение')),
                ('key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.categoryrequisite', verbose_name='Категория (Реквезиты)')),
                ('requisite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.companyrequisite', verbose_name='Реквизит компании')),
            ],
            options={
                'verbose_name': 'Реквизит компании (поле)',
                'verbose_name_plural': '2.8) Реквизиты компании (поле)',
            },
        ),
        migrations.CreateModel(
            name='CompanyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.company', verbose_name='Компания')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Контакт компании',
                'verbose_name_plural': '2.5) Контакты компаний',
            },
        ),
        migrations.CreateModel(
            name='CompanyBankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='Название')),
                ('bank_title', models.CharField(blank=True, max_length=200, verbose_name='Наименование банка')),
                ('bik', models.CharField(blank=True, max_length=200, verbose_name='БИК')),
                ('iik', models.CharField(blank=True, max_length=200, verbose_name='ИИК')),
                ('rnn', models.CharField(blank=True, max_length=200, verbose_name='ИИК')),
                ('bin', models.CharField(blank=True, max_length=200, verbose_name='ИИК')),
                ('cor_acc', models.CharField(blank=True, max_length=200, verbose_name='Кор/сч')),
                ('acc_currency', models.CharField(blank=True, max_length=200, verbose_name='Валюта счёта')),
                ('bank_address', models.CharField(blank=True, max_length=200, verbose_name='Адрес банка')),
                ('swift', models.CharField(blank=True, max_length=200, verbose_name='SWIFT')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Банковские реквизиты компании',
                'verbose_name_plural': '2.6) Банковские реквизиты компании',
            },
        ),
        migrations.CreateModel(
            name='CompanyAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=200, verbose_name='Улица')),
                ('apartment', models.CharField(blank=True, max_length=200, verbose_name='Дом, квартира')),
                ('index', models.CharField(blank=True, max_length=200, verbose_name='Индекс')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='addition.area', verbose_name='Область (Регион)')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='addition.city', verbose_name='Город')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.company', verbose_name='Компания')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='addition.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Адрес компании',
                'verbose_name_plural': '2.4) Адреса компаний',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.typecompany', verbose_name='Тип компании'),
        ),
    ]
