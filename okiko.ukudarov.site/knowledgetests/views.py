from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View, TemplateView
from django.shortcuts import get_list_or_404, get_object_or_404

from .forms import *
from educational_institutions.models import *
from users.models import *
from users.mixins import *
from .models import *


class AllTestsView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        knowledge_tests = KnowledgeTest.objects.all()
        unt_subjects = UNTSubjects.objects.all()
        context = {
            'unt_subjects': unt_subjects,
            'knowledge_tests': knowledge_tests,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'knowledgetests/all_tests.html', context)


class TestsView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        unt_subjects = UNTSubjects.objects.all()
        unt_subjects_result = UNTSubjects.objects.get(id=kwargs.get('id'))
        knowledge_tests = KnowledgeTest.objects.filter(unt_subjects=unt_subjects_result)
        context = {
            'unt_subjects': unt_subjects,
            'unt_subjects_result': unt_subjects_result,
            'knowledge_tests': knowledge_tests,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'knowledgetests/all_tests.html', context)


class StartTestView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        position = kwargs.get('position')
        if request.user.is_authenticated:
            if UniversityAdministrator.objects.filter(user=request.user):
                admin = True
            else:
                admin = False
        else:
            admin = False
        knowledge_test = KnowledgeTest.objects.get(id=kwargs.get('id'))
        session_id = request.session.session_key
        if UserTest.objects.filter(user=request.user, knowledge_test=knowledge_test, finish=False):
            user_test = UserTest.objects.filter(user=request.user, knowledge_test=knowledge_test, finish=False).order_by('-id').first()
        else:
            user_test = UserTest.objects.create(user=request.user, knowledge_test=knowledge_test, finish=False)
        test_question = TestQuestions.objects.get(knowledge_test=knowledge_test, position=position)
        question_answer = QuestionAnswers.objects.filter(test_question=test_question)
        form = TestAnswerForm(request.POST or None)

        context = {
            'form': form,
            'admin': self.admin,
            'student': self.student,
            'knowledge_test': knowledge_test,
            'test_question': test_question,
            'question_answer': question_answer
        }
        return render(request, 'knowledgetests/run_test.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UniversityAdministrator.objects.filter(user=request.user):
                admin = True
            else:
                admin = False
        else:
            admin = False
        knowledge_test = KnowledgeTest.objects.get(id=kwargs.get('id'))
        position = kwargs.get('position')
        test_question = TestQuestions.objects.get(knowledge_test=knowledge_test, position=position)
        question_answer = QuestionAnswers.objects.filter(test_question=test_question)
        form = TestAnswerForm(request.POST or None)
        if form.is_valid():
            user_test = UserTest.objects.filter(user=request.user, knowledge_test=knowledge_test, finish=False).order_by('-id').first()
            question_id = int(form.cleaned_data['user_test_question_id'])
            test_question = TestQuestions.objects.get(id=question_id)
            position_number = int(form.cleaned_data['user_test_answer_id'])

            if position_number == 0:
                answer = QuestionAnswers.objects.get(test_question=test_question, position=1)
                if answer.correct == True:
                    correct_answer = True
                else:
                    correct_answer = False
                UserAnswersForTest.objects.create(user=request.user, user_test=user_test, user_test_question=test_question, user_test_answer=answer, correct_answer=correct_answer, isnt_answer=True)
            else:
                answer = QuestionAnswers.objects.get(test_question=test_question, position=position_number)
                if answer.correct == True:
                    correct_answer = True
                else:
                    correct_answer = False
                if not UserAnswersForTest.objects.filter(user_test=user_test, user_test_question=test_question):
                    UserAnswersForTest.objects.create(user=request.user, user_test=user_test, user_test_question=test_question, user_test_answer=answer, correct_answer=correct_answer)
                else:
                    UserAnswersForTest.objects.filter(user_test=user_test, user_test_question=test_question).update(user_test_answer=answer, correct_answer=correct_answer)

            next_test_question = TestQuestions.objects.filter(knowledge_test=knowledge_test).order_by('-id').first()
            position_s = position + 1
            if next_test_question.position < position_s:
                user_id = UserTest.objects.get(user=request.user, knowledge_test=knowledge_test, finish=False)
                user_answers = UserAnswersForTest.objects.filter(user=request.user, user_test=user_id)
                for item in user_answers:
                    user_id.user_answer.add(item)
                user_id.save()
                all_question = UserAnswersForTest.objects.filter(user=request.user, user_test=user_id).count()
                finish_question = UserAnswersForTest.objects.filter(user=request.user, user_test=user_id, correct_answer=True, isnt_answer=False).count()
                wrong_question = UserAnswersForTest.objects.filter(user=request.user, user_test=user_id, correct_answer=False, isnt_answer=False).count()
                user_test = UserTest.objects.filter(id=user_id.id, user=request.user, knowledge_test=knowledge_test, finish=False).update(finish=True, all_question=all_question, finish_question=finish_question, wrong_question=wrong_question)
                id = user_id.id
                return redirect("end_test", id)
            else:
                position += 1
                id = kwargs.get('id')
                return redirect("run_test", id, position)
        context = {
            'form': form,
            'admin': self.admin,
            'student': self.student,
            'knowledge_test': knowledge_test,
            'test_question': test_question,
            'question_answer': question_answer
            }
        return render(request, 'knowledgetests/run_test.html', context)


class EndTestView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        user_test = UserTest.objects.get(id=id)
        user_answer = UserAnswersForTest.objects.filter(user_test=user_test)

        context = {
            'user_test': user_test,
            'user_answer': user_answer,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'knowledgetests/end_test.html', context)
