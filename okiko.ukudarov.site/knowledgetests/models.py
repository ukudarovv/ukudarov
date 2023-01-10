from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from educational_institutions.models import *

User = get_user_model()


class KnowledgeTest(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название теста', null=True, blank=True)
    unt_subjects = models.ForeignKey(UNTSubjects, verbose_name='Профильные предметы на ЕНТ', on_delete=models.CASCADE, null=True, blank=True)
    all_question = models.PositiveIntegerField(default=0, verbose_name='Всего вопросов', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания теста')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return "Тест: {}".format(self.title)

    def get_absolute_url(self):
        return reverse('run_test', kwargs={'id': self.id})


class TestQuestions(models.Model):
    knowledge_test = models.ForeignKey(KnowledgeTest, verbose_name='Тест', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Вопрос', null=True, blank=True)
    position = models.PositiveIntegerField(default=0, verbose_name='Позиция')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return "Вопрос: {}".format(self.title)


class QuestionAnswers(models.Model):
    test_question = models.ForeignKey(TestQuestions, verbose_name='Вопрос', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Ответ', null=True, blank=True)
    correct = models.BooleanField("Правильный?", blank=True, default=False)
    position = models.PositiveIntegerField(default=0, verbose_name='Позиция')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return "Ответ: {}".format(self.title)


class UserTest(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    knowledge_test = models.ForeignKey(KnowledgeTest, verbose_name='Тест', on_delete=models.CASCADE)
    user_answer = models.ManyToManyField('UserAnswersForTest', verbose_name='Ответы', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    finish = models.BooleanField("Завершен?", blank=True, default=False)
    all_question = models.PositiveIntegerField(default=0, verbose_name='Всего вопросов', blank=True, null=True)
    finish_question = models.PositiveIntegerField(default=0, verbose_name='Правильно отвечены', blank=True, null=True)
    wrong_question = models.PositiveIntegerField(default=0, verbose_name='Неправильно отвечены', blank=True, null=True)

    class Meta:
        verbose_name = 'Тест (для пользователя)'
        verbose_name_plural = 'Тесты (для пользователя)'

    def __str__(self):
        return "Тест: {} для {}".format(self.knowledge_test.title, self.user.username)


class UserAnswersForTest(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    user_test = models.ForeignKey(UserTest, verbose_name='Пользователь', on_delete=models.CASCADE)
    user_test_question = models.ForeignKey(TestQuestions, verbose_name='Вопрос', on_delete=models.CASCADE, blank=True, null=True)
    user_test_answer = models.ForeignKey(QuestionAnswers, verbose_name='Ответ', on_delete=models.CASCADE, blank=True, null=True)
    correct_answer = models.BooleanField("Правильно ответил?", blank=True, default=False)
    isnt_answer = models.BooleanField("Не ответил?", blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)

    class Meta:
        verbose_name = 'Тест (для пользователя)'
        verbose_name_plural = 'Тесты (для пользователя)'

    def __str__(self):
        return "Результат пользователя: {}".format(self.user_test.user.username)
