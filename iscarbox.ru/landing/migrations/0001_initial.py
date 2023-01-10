# Generated by Django 3.1 on 2020-08-05 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='carousel/photos/%Y/%m/%d/', verbose_name='Фото')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
            ],
            options={
                'verbose_name': 'Слайд',
                'verbose_name_plural': 'Слайды',
            },
        ),
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('phone_number', models.CharField(max_length=25, verbose_name='Номер телефона')),
                ('message', models.TextField(null=True, verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Контактная форма',
                'verbose_name_plural': 'Контактная форма',
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numder_phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('instagram_name', models.CharField(max_length=200, verbose_name='Название инстаграмм аккаунта')),
                ('instagram_url', models.URLField(verbose_name='Ссылка на инстаграмм')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('about', models.TextField(blank=True, verbose_name='О нас')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='Develiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
            ],
            options={
                'verbose_name': 'Страница доставки',
                'verbose_name_plural': 'Страница доставки',
            },
        ),
        migrations.CreateModel(
            name='Paymentmethods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
            ],
            options={
                'verbose_name': 'Страница cпособы оплаты',
                'verbose_name_plural': 'Страница cпособы оплаты',
            },
        ),
        migrations.CreateModel(
            name='Purchasereturns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
            ],
            options={
                'verbose_name': 'Страница возврата товара',
                'verbose_name_plural': 'Страница возврата товара',
            },
        ),
        migrations.CreateModel(
            name='Sitepolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
            ],
            options={
                'verbose_name': 'Страница политики сайта',
                'verbose_name_plural': 'Страница политики сайта',
            },
        ),
    ]
