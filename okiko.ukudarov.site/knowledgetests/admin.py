from django.contrib import admin
from .models import *


class TestQuestionsInline(admin.TabularInline):
    model = TestQuestions
    extra = 0


class QuestionAnswersInline(admin.TabularInline):
    model = QuestionAnswers
    extra = 0


class UserAnswersForTestInline(admin.TabularInline):
    model = UserAnswersForTest
    extra = 0


class KnowledgeTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'all_question', 'unt_subjects', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ['unt_subjects', 'created_at']
    inlines = [TestQuestionsInline]

    class Meta:
        model = KnowledgeTest

admin.site.register(KnowledgeTest, KnowledgeTestAdmin)


class TestQuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'knowledge_test')
    list_display_links = ('id', 'title')
    list_filter = ['knowledge_test']
    inlines = [QuestionAnswersInline]

    class Meta:
        model = TestQuestions

admin.site.register(TestQuestions, TestQuestionsAdmin)


class UserTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'knowledge_test', 'user', 'created_at')
    list_display_links = ('id', 'knowledge_test')
    list_filter = ['created_at']

    inlines = [UserAnswersForTestInline]

    class Meta:
        model = UserTest

admin.site.register(UserTest, UserTestAdmin)
