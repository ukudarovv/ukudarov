from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View, TemplateView
from django.shortcuts import get_list_or_404, get_object_or_404

from .forms import *
from educational_institutions.models import *
from knowledgetests.models import *
from users.mixins import *


class LoginView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'users/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'users/login.html', context)


class RegistrationView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'users/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            student = Student.objects.create(
                user=new_user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            Student.objects.create(
                student=student
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'users/registration.html', context)


class ProfileView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        user = Student.objects.get(user=request.user)
        student_document = StudentDocument.objects.filter(student=user)
        user_test = UserTest.objects.filter(user=request.user).order_by('-id')
        user_answer = UserAnswersForTest.objects.filter(user=request.user).order_by('-id')

        context = {
            'user_test': user_test,
            'user_answer': user_answer,
            'student_document': student_document,
            'admin': self.admin,
            'student': self.student,
            'user': user
        }
        return render(request, 'users/profile.html', context)


class EditProfileView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        form = EditProfileForm(request.POST or None, instance=student)

        context = {
            'form': form,
            'admin': self.admin,
            'student': self.student,
        }
        return render(request, 'users/edit_profile.html', context)

    def post(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        form = EditProfileForm(request.POST or None, instance=student)

        if form.is_valid():
            form.save()
            return redirect("profile")

        context = {
            'form': form,
            'admin': self.admin,
            'student': self.student,
        }
        return render(request, 'users/edit_profile.html', context)


class EditDocumentView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        student_document = StudentDocument.objects.filter(student=student)

        context = {
            'student_document': student_document,
            'admin': self.admin,
            'student': self.student,
        }
        return render(request, 'users/edit_document.html', context)


class AddDocumentView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        form = AddDocumentForm(request.POST or None)

        context = {
            'form': form,
            'admin': self.admin,
            'student': self.student,
        }
        return render(request, 'users/add_document.html', context)

    def post(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        form = AddDocumentForm(request.POST or None)

        if form.is_valid():
            new_document = form.save(commit=False)
            new_document.student = student
            new_document.document = request.FILES['document']
            new_document.save()
            messages.add_message(request, messages.INFO, "Документ был добавлен!")
            return redirect("edit_document")

        context = {
            'form': form,
            'admin': self.admin,
            'student': self.student,
        }
        return render(request, 'users/add_document.html', context)


class DeleteDocumentView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        student_document = StudentDocument.objects.get(id=kwargs.get('id'), student=student)
        student_document.delete()
        context = {
            'admin': self.admin,
            'student': self.student,
        }
        return redirect("edit_document")


class AdminProfileView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UniversityAdministrator.objects.filter(user=request.user):
                admin = True
            else:
                admin = False
        else:
            admin = False
        user = UniversityAdministrator.objects.get(user=request.user)
        university = University.objects.get(administrator=user)
        contact = UniversityContact.objects.get(university=university)
        context = {
            'user': user,
            'university': university,
            'admin': admin,
            'contact': contact
        }
        return render(request, 'users/admin_profile.html', context)


class EditAdminProfileView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UniversityAdministrator.objects.filter(user=request.user):
                admin = True
            else:
                admin = False
        else:
            admin = False
        user = UniversityAdministrator.objects.get(user=request.user)
        form = EditAdminProfileForm(request.POST or None, instance=user)
        context = {
            'form': form,
            'admin': admin,
            'user': user
        }
        return render(request, 'users/edit_admin_profile.html', context)

    def post(self, request, *args, **kwargs):
        user = UniversityAdministrator.objects.get(user=request.user)
        form = EditAdminProfileForm(request.POST or None, instance=user)

        if form.is_valid():
            form.save()
            return redirect("admin_profile")
        context = {
            'form': form,
            'admin': admin
        }
        return render(request, 'users/edit_admin_profile.html', context)


class EditUnivDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UniversityAdministrator.objects.filter(user=request.user):
                admin = True
            else:
                admin = False
        else:
            admin = False
        user = UniversityAdministrator.objects.get(user=request.user)
        university = University.objects.get(administrator=user)
        university_contact = UniversityContact.objects.get(university=university)
        form = EditUnivDetailForm(request.POST or None, instance=university)
        context = {
            'university': university,
            'form': form,
            'admin': admin,
            'user': user
        }
        return render(request, 'users/edit_univ_detail.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UniversityAdministrator.objects.filter(user=request.user):
                admin = True
            else:
                admin = False
        else:
            admin = False
        user = UniversityAdministrator.objects.get(user=request.user)
        university = University.objects.get(administrator=user)
        university_contact = UniversityContact.objects.get(university=university)
        form = EditUnivDetailForm(request.POST or None, instance=university)

        if form.is_valid():
            form.save()
            return redirect("admin_profile")

        context = {
            'university': university,
            'form': form,
            'admin': admin,
            'user': user
        }
        return render(request, 'users/edit_univ_detail.html', context)


class EditUnivContactView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UniversityAdministrator.objects.filter(user=request.user):
                admin = True
            else:
                admin = False
        else:
            admin = False
        user = UniversityAdministrator.objects.get(user=request.user)
        university = University.objects.get(administrator=user)
        university_contact = UniversityContact.objects.get(university=university)
        form = EditUnivContactlForm(request.POST or None, instance=university_contact)
        context = {
            'university': university,
            'form': form,
            'admin': admin,
            'user': user
        }
        return render(request, 'users/edit_univ_contact.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UniversityAdministrator.objects.filter(user=request.user):
                admin = True
            else:
                admin = False
        else:
            admin = False
        user = UniversityAdministrator.objects.get(user=request.user)
        university = University.objects.get(administrator=user)
        university_contact = UniversityContact.objects.get(university=university)
        form = EditUnivContactlForm(request.POST or None, instance=university_contact)

        if form.is_valid():
            form.save()
            return redirect("admin_profile")

        context = {
            'university': university,
            'form': form,
            'admin': admin,
            'user': user
        }
        return render(request, 'users/edit_univ_contact.html', context)
