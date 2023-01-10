from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone

from users.models import *


class CategoryUniversity(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория ВУЗа'
        verbose_name_plural = '01) Категории ВУЗа'

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('category_university', kwargs={'id': self.id})


class TypeUniversity(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название типа')

    class Meta:
        verbose_name = 'Тип ВУЗа'
        verbose_name_plural = '02) Типы ВУЗа'

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('type_university', kwargs={'id': self.id})


class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название области')
    city = models.ManyToManyField('City', verbose_name='Города', blank=True, related_name='related_city')

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = '03) Области'

    def __str__(self):
        return "{}".format(self.name)


class City(models.Model):
    region = models.ForeignKey(Region, verbose_name='Область', on_delete=models.CASCADE, null=True, blank=True, related_name='related_region')
    name = models.CharField(max_length=255, verbose_name='Название города')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = '04) Города'

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('city', kwargs={'id': self.id})


class University(models.Model):
    administrator = models.ForeignKey('users.UniversityAdministrator', verbose_name='Администратор', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название', null=True, blank=True)
    abbreviation = models.CharField(max_length=255, verbose_name='Аббревиатура', null=True, blank=True)
    code = models.CharField(max_length=255, verbose_name='Код ВУЗа', null=True, blank=True)
    threshold_score = models.CharField(max_length=255, verbose_name='Пороговый балл для поступления', null=True, blank=True)
    city = models.ForeignKey(City, verbose_name='Регион', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(CategoryUniversity, verbose_name='Категория ВУЗа', on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey(TypeUniversity, verbose_name='Тип ВУЗа', on_delete=models.CASCADE, null=True, blank=True)
    qty_dormitories = models.CharField(max_length=255, verbose_name='Количество общежитий', null=True, blank=True)
    old_title = models.CharField(max_length=255, verbose_name='Старые названия', null=True, blank=True)
    logo = models.ImageField("Логотип", upload_to="image/university/logo/", blank=True, null=True)
    background = models.ImageField("Фон", upload_to="image/university/background/", blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)
    scientific_degrees_educational_programs = models.ManyToManyField('ScientificDegrees', verbose_name='Академические степени для образовательных программ', blank=True, related_name='related_scientific_degrees')
    scientific_degrees_specializations = models.ManyToManyField('ScientificDegrees', verbose_name='Академические степени для специальности', blank=True, related_name='related_specializations')

    class Meta:
        verbose_name = 'ВУЗ'
        verbose_name_plural = '05) ВУЗы'

    def __str__(self):
        return "ВУЗ: {}".format(self.title)

    def get_absolute_url(self):
        return reverse('univ_detail', kwargs={'id': self.id})


class UniversityContact(models.Model):
    university = models.ForeignKey(University, verbose_name='Университет', on_delete=models.CASCADE)
    website = models.URLField(max_length=200, verbose_name='Сайт', null=True, blank=True)
    email = models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name='Номер телефона 1', null=True, blank=True)
    phone_2 = models.CharField(max_length=15, verbose_name='Номер телефона 2', null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name='Местоположение', null=True, blank=True)

    class Meta:
        verbose_name = 'Контакты университета'
        verbose_name_plural = 'Контакты университетов'

    def __str__(self):
        return "Контакты университета: {}".format(self.university.title)


class UniversityGallery(models.Model):
    university = models.ForeignKey(University, verbose_name='Университет', on_delete=models.CASCADE)
    image = models.ImageField("Картинка", upload_to="image/university/photo/", blank=True, null=True)

    class Meta:
        verbose_name = 'Фотография университета'
        verbose_name_plural = 'Фотографии университетов'

    def __str__(self):
        return "Фотография университета: {}".format(self.university.title, self.image)


class UniversityNews(models.Model):
    university = models.ForeignKey(University, verbose_name='Университет', on_delete=models.CASCADE)
    image = models.ImageField("Картинка", upload_to="image/university/news/photo/", blank=True, null=True)
    description = models.TextField("Текст", blank=True, null=True)

    class Meta:
        verbose_name = 'Новость университета'
        verbose_name_plural = 'Новости университетов'

    def __str__(self):
        return "Новость университета: {}".format(self.university.title)


class ScientificDegrees(models.Model):
    title = models.CharField(max_length=255, verbose_name='Академическая степень', null=True, blank=True)

    class Meta:
        verbose_name = 'Академическая степень'
        verbose_name_plural = '06) Академические степени'

    def __str__(self):
        return "Академическая степень: {}".format(self.title)

    def get_absolute_url(self):
        return reverse('scientific_degrees', kwargs={'id': self.id})


class UNTSubjects(models.Model):
    title = models.CharField(max_length=255, verbose_name='Названия предметов')

    class Meta:
        verbose_name = 'Профильные предметы на ЕНТ'
        verbose_name_plural = '07) Профильные предметы на ЕНТ'

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('unt_subjects', kwargs={'id': self.id})


class Specializations(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название специальности', null=True, blank=True)
    scientific_degrees = models.ForeignKey(ScientificDegrees, verbose_name='Академическая степень', on_delete=models.CASCADE, null=True, blank=True)
    groups_of_educational_programs = models.ForeignKey('GroupsOfEducationalPrograms', verbose_name='Группа образовательных программ', on_delete=models.CASCADE, null=True, blank=True)
    unt_subjects = models.ForeignKey(UNTSubjects, verbose_name='Профильные предметы на ЕНТ', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=255, verbose_name='Код специальности', null=True, blank=True)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = '08) Специальности'

    def __str__(self):
        return "Специальность: {} {}".format(self.code, self.title)

    def get_absolute_url(self):
        return reverse('specializations', kwargs={'id': self.id})


class AreasOfEducation(models.Model):
    code = models.CharField(max_length=255, verbose_name='Код специальности', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название области образования', null=True, blank=True)
    scientific_degrees = models.ForeignKey(ScientificDegrees, verbose_name='Академическая степень', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Область образования'
        verbose_name_plural = '09) Области образования'

    def __str__(self):
        return "Область образования: {} {}".format(self.code, self.title)

    def get_absolute_url(self):
        return reverse('areas_of_education', kwargs={'id': self.id})


class AreasOfTraining(models.Model):
    areas_of_education = models.ForeignKey(AreasOfEducation, verbose_name='Область образования', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=255, verbose_name='Код специальности', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название направления подготовки', null=True, blank=True)
    scientific_degrees = models.ForeignKey(ScientificDegrees, verbose_name='Академическая степень', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Направление подготовки'
        verbose_name_plural = '10) Направления подготовки'

    def __str__(self):
        return "Направление подготовки: {} {}".format(self.code, self.title)

    def get_absolute_url(self):
        return reverse('areas_of_training', kwargs={'id': self.id})


class GroupsOfEducationalPrograms(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название группы образовательных программ', null=True, blank=True)
    code = models.CharField(max_length=255, verbose_name='Код специальности', null=True, blank=True)
    scientific_degrees = models.ForeignKey(ScientificDegrees, verbose_name='Академическая степень', on_delete=models.CASCADE, null=True, blank=True)
    unt_subjects = models.ForeignKey(UNTSubjects, verbose_name='Профильные предметы на ЕНТ', on_delete=models.CASCADE, null=True, blank=True)
    areas_of_education = models.ForeignKey(AreasOfEducation, verbose_name='Область образования', on_delete=models.CASCADE, null=True, blank=True)
    areas_of_training = models.ForeignKey(AreasOfTraining, verbose_name='Направление подготовки', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Группа образовательной программы'
        verbose_name_plural = '11) Группы образовательных программ'

    def __str__(self):
        return "Группа образовательной программы:  {} {}".format(self.code, self.title)

    def get_absolute_url(self):
        return reverse('groups_of_educational_programs', kwargs={'id': self.id})


class EducationalPrograms(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название образовательной программы', null=True, blank=True)
    code = models.CharField(max_length=255, verbose_name='Код специальности', null=True, blank=True)
    description = models.TextField("Цель образовательной программы", blank=True, null=True)
    scientific_degrees = models.ForeignKey(ScientificDegrees, verbose_name='Академическая степень', on_delete=models.CASCADE, null=True, blank=True)
    languages_of_instruction = models.CharField(max_length=255, verbose_name='Языки обучения', null=True, blank=True)
    university = models.ForeignKey(University, verbose_name='ВУЗ', on_delete=models.CASCADE, null=True, blank=True)
    duration_of_training = models.CharField(max_length=255, verbose_name='Срок обучения', null=True, blank=True)
    volume_of_loans = models.CharField(max_length=255, verbose_name='Объем кредитов', null=True, blank=True)
    groups_of_educational_programs = models.ForeignKey(GroupsOfEducationalPrograms, verbose_name='Группа образовательных программ', on_delete=models.CASCADE, null=True, blank=True)
    unt_subjects = models.ForeignKey(UNTSubjects, verbose_name='Профильные предметы на ЕНТ', on_delete=models.CASCADE, null=True, blank=True)
    areas_of_education = models.ForeignKey(AreasOfEducation, verbose_name='Область образования', on_delete=models.CASCADE, null=True, blank=True)
    areas_of_training = models.ForeignKey(AreasOfTraining, verbose_name='Направление подготовки', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена за год', null=True, blank=True)

    class Meta:
        verbose_name = 'Образовательная программа'
        verbose_name_plural = '12) Образовательные программы'

    def __str__(self):
        return "Образовательная программа:  {} {}".format(self.code, self.title)

    def get_absolute_url(self):
        return reverse('educational_programs', kwargs={'id': self.id})


class UniversitySpecializations(models.Model):
    university = models.ForeignKey(University, verbose_name='ВУЗ', on_delete=models.CASCADE, null=True, blank=True)
    specializations = models.ForeignKey(Specializations, verbose_name='Специальность', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Специальность университета'
        verbose_name_plural = '13) Специальности университетов'

    def __str__(self):
        return "Специальность: {} {}".format(self.specializations.code, self.specializations.title)


class ApplicationsForAdmission(models.Model):
    university = models.ForeignKey(University, verbose_name='ВУЗ', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('users.Student', verbose_name='Студент', on_delete=models.CASCADE, null=True, blank=True)
    program = models.ForeignKey(EducationalPrograms, verbose_name='Образовательная программа', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')

    class Meta:
        verbose_name = 'Заявка на поступление'
        verbose_name_plural = '14) Заявки на поступления'

    def __str__(self):
        return "Заявка: {}".format(self.student.first_name)
