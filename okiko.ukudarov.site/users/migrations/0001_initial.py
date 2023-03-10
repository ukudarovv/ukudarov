# Generated by Django 3.1.6 on 2021-12-04 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('educational_institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название категории')),
                ('for_graduates', models.BooleanField(blank=True, default=False, verbose_name='Для выпускников')),
                ('magistracy', models.BooleanField(blank=True, default=False, verbose_name='Магистратура')),
                ('doctorate', models.BooleanField(blank=True, default=False, verbose_name='Докторантура')),
            ],
            options={
                'verbose_name': 'Категория документа',
                'verbose_name_plural': 'Категории документов',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия')),
                ('iin', models.CharField(blank=True, max_length=15, null=True, verbose_name='ИИН')),
                ('residence_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес прописки')),
                ('residential_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес проживания')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='Номер телефона')),
                ('birth_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата рождения')),
                ('core_competence', models.CharField(blank=True, max_length=250, null=True, verbose_name='Основная компетенция')),
                ('about', models.TextField(blank=True, null=True, verbose_name='Биография')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='image/about/', verbose_name='Картинка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.city', verbose_name='Регион')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
            },
        ),
        migrations.CreateModel(
            name='UniversityAdministrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='Номер телефона')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Администратор университета',
                'verbose_name_plural': 'Администраторы университетов',
            },
        ),
        migrations.CreateModel(
            name='StudentDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ImageField(blank=True, null=True, upload_to='documents/%Y/%m/%d/', verbose_name='Документ')),
                ('document_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.documentcategory', verbose_name='Категория документа')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student', verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Документы студента',
                'verbose_name_plural': 'Документы студентов',
            },
        ),
    ]
