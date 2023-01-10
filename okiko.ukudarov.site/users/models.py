from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from educational_institutions.models import *
from .validators import validate_file_extension

User = get_user_model()


class Student(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True, blank=True)
    iin = models.CharField(max_length=15, verbose_name='ИИН', null=True, blank=True)
    city = models.ForeignKey(City, verbose_name='Регион', on_delete=models.CASCADE, null=True, blank=True)
    residence_address = models.CharField(max_length=255, verbose_name='Адрес прописки', null=True, blank=True)
    residential_address = models.CharField(max_length=255, verbose_name='Адрес проживания', null=True, blank=True)
    email = models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='Номер телефона', null=True, blank=True)
    birth_date = models.DateField("Дата рождения", blank=True, default=timezone.now, null=True)
    core_competence = models.CharField("Основная компетенция", max_length=250, null=True, blank=True)
    about = models.TextField("Биография", null=True, blank=True)
    profile_picture = models.ImageField("Картинка", upload_to="image/about/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return "Студент: {} {}".format(self.first_name, self.last_name)


class DocumentCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории', null=True, blank=True)
    for_graduates = models.BooleanField("Для выпускников", blank=True, default=False)
    magistracy = models.BooleanField("Магистратура", blank=True, default=False)
    doctorate = models.BooleanField("Докторантура", blank=True, default=False)

    class Meta:
        verbose_name = 'Категория документа'
        verbose_name_plural = 'Категории документов'

    def __str__(self):
        return "{}".format(self.title)


class StudentDocument(models.Model):
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE)
    document_category = models.ForeignKey(DocumentCategory, verbose_name='Категория документа', on_delete=models.CASCADE)
    document = models.ImageField("Документ", upload_to="documents/%Y/%m/%d/", blank=True, null=True)

    class Meta:
        verbose_name = 'Документы студента'
        verbose_name_plural = 'Документы студентов'

    def __str__(self):
        return "Документы студента: {} {}".format(self.student.first_name, self.student.last_name)


class UniversityAdministrator(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True, blank=True)
    email = models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='Номер телефона', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')

    class Meta:
        verbose_name = 'Администратор университета'
        verbose_name_plural = 'Администраторы университетов'

    def __str__(self):
        return "Администратор университета: {} {}".format(self.first_name, self.last_name)
