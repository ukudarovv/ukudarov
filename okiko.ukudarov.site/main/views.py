from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View, TemplateView
from django.shortcuts import get_list_or_404, get_object_or_404

from educational_institutions.models import *
from users.models import *
from users.mixins import *


class MainView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        type_university = TypeUniversity.objects.all()
        category_university = CategoryUniversity.objects.all()
        university = University.objects.order_by('-id')[:10]

        context = {
            'university': university,
            'type_university': type_university,
            'category_university': category_university,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'base.html', context)
