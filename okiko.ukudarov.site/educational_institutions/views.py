from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View, TemplateView
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import *
from .forms import *
from users.models import *
from .filters import *
from users.mixins import *


class SearchUnivView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        universities = University.objects.all()
        query_search = self.request.GET.get('search')
        form = SearchUnivForm(self.request.POST or None)
        if query_search:
            universities = University.objects.filter(Q(title__icontains=query_search))
            context = {
                'universities': universities,
                'query_search': query_search,
                'admin': self.admin,
                'student': self.student,
                'form': form
                }
            return render(request, 'educational_institutions/search_univ.html', context)

        context = {
            'universities': universities,
            'query_search': query_search,
            'admin': self.admin,
            'student': self.student,
            'form': form
            }
        return render(request, 'educational_institutions/search_univ.html', context)


class UnivDetailView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        university = University.objects.get(id=kwargs.get('id'))
        educational_programs = EducationalPrograms.objects.filter(university=university)
        university_specializations = UniversitySpecializations.objects.filter(university=university)
        context = {
            'educational_programs': educational_programs,
            'university_specializations': university_specializations,
            'university': university,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/univ_detail.html', context)


class AllByTypeView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        type_university = TypeUniversity.objects.all()
        university = University.objects.order_by('-id')

        context = {
            'university': university,
            'type_university': type_university,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/search_by_type.html', context)


class SearchByTypeView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        type_university = TypeUniversity.objects.all()
        result_type_university = TypeUniversity.objects.get(id=kwargs.get('id'))
        university = University.objects.filter(type=result_type_university)

        context = {
            'university': university,
            'type_university': type_university,
            'result_type_university': result_type_university,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/search_by_type.html', context)


class AllByCategoryView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        category_university = CategoryUniversity.objects.all()
        university = University.objects.order_by('-id')

        context = {
            'university': university,
            'category_university': category_university,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/search_by_category.html', context)


class SearchByCategoryView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        category_university = CategoryUniversity.objects.all()
        result_category_university = CategoryUniversity.objects.get(id=kwargs.get('id'))
        university = University.objects.filter(category=result_category_university)

        context = {
            'university': university,
            'category_university': category_university,
            'result_category_university': result_category_university,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/search_by_category.html', context)


class AllByRegionView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        region = Region.objects.all()
        university = University.objects.order_by('-id')

        context = {
            'university': university,
            'region': region,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/search_by_region.html', context)


class SearchByRegionView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        region = Region.objects.all()
        result_city = City.objects.get(id=kwargs.get('id'))
        university = University.objects.filter(city=result_city)

        context = {
            'university': university,
            'result_city': result_city,
            'region': region,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/search_by_region.html', context)


class AllByCodeView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        university = University.objects.order_by('code')

        context = {
            'university': university,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/search_by_code.html', context)


class AllSpecializationsView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        scientific_degrees = ScientificDegrees.objects.all()
        specializations = Specializations.objects.all()

        context = {
            'scientific_degrees': scientific_degrees,
            'specializations': specializations,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/specializations.html', context)


class SpecializationsView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        scientific_degrees = ScientificDegrees.objects.all()
        scientific_degrees_result = ScientificDegrees.objects.get(id=kwargs.get('id'))
        specializations = Specializations.objects.filter(scientific_degrees=scientific_degrees_result)

        context = {
            'scientific_degrees': scientific_degrees,
            'scientific_degrees_result': scientific_degrees_result,
            'specializations': specializations,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/specializations.html', context)


class SpecializationsDetailView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        specializations = Specializations.objects.get(id=kwargs.get('id'))

        context = {
            'specializations': specializations,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/specializations_detail.html', context)


class AllAreasOfEducationView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        scientific_degrees = ScientificDegrees.objects.all()
        areas_of_education = AreasOfEducation.objects.all()

        context = {
            'scientific_degrees': scientific_degrees,
            'areas_of_education': areas_of_education,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/areas_of_education.html', context)


class AreasOfEducationView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        scientific_degrees = ScientificDegrees.objects.all()
        scientific_degrees_result = ScientificDegrees.objects.get(id=kwargs.get('id'))
        areas_of_education = AreasOfEducation.objects.filter(scientific_degrees=scientific_degrees_result)

        context = {
            'scientific_degrees': scientific_degrees,
            'scientific_degrees_result': scientific_degrees_result,
            'areas_of_education': areas_of_education,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/areas_of_education.html', context)


class AreasOfEducationDetailView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        areas_of_education = AreasOfEducation.objects.get(id=kwargs.get('id'))
        areas_of_training = AreasOfTraining.objects.filter(areas_of_education=areas_of_education)

        context = {
            'areas_of_training': areas_of_training,
            'areas_of_education': areas_of_education,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/areas_of_education_detail.html', context)


class AllAreasOfTrainingView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        scientific_degrees = ScientificDegrees.objects.all()
        areas_of_training = AreasOfTraining.objects.all()

        context = {
            'scientific_degrees': scientific_degrees,
            'areas_of_training': areas_of_training,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/areas_of_training.html', context)


class AreasOfTrainingView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        scientific_degrees = ScientificDegrees.objects.all()
        scientific_degrees_result = ScientificDegrees.objects.get(id=kwargs.get('id'))
        areas_of_training = AreasOfTraining.objects.filter(scientific_degrees=scientific_degrees_result)

        context = {
            'scientific_degrees': scientific_degrees,
            'scientific_degrees_result': scientific_degrees_result,
            'areas_of_training': areas_of_training,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/areas_of_training.html', context)


class AreasOfTrainingDetailView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        areas_of_training = AreasOfTraining.objects.get(id=kwargs.get('id'))
        groups_of_educational_programs = GroupsOfEducationalPrograms.objects.filter(areas_of_training=areas_of_training)

        context = {
            'areas_of_training': areas_of_training,
            'groups_of_educational_programs': groups_of_educational_programs,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/areas_of_training_detail.html', context)


class AllGroupsOfEducationalProgramsView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        scientific_degrees = ScientificDegrees.objects.all()
        groups_of_educational_programs = GroupsOfEducationalPrograms.objects.all()

        context = {
            'scientific_degrees': scientific_degrees,
            'groups_of_educational_programs': groups_of_educational_programs,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/groups_of_educational_programs.html', context)


class GroupsOfEducationalProgramsView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        scientific_degrees = ScientificDegrees.objects.all()
        scientific_degrees_result = ScientificDegrees.objects.get(id=kwargs.get('id'))
        groups_of_educational_programs = GroupsOfEducationalPrograms.objects.filter(scientific_degrees=scientific_degrees_result)

        context = {
            'scientific_degrees': scientific_degrees,
            'scientific_degrees_result': scientific_degrees_result,
            'groups_of_educational_programs': groups_of_educational_programs,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/groups_of_educational_programs.html', context)


class GroupsOfEducationalProgramsDetailView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        groups_of_educational_programs = GroupsOfEducationalPrograms.objects.get(id=kwargs.get('id'))
        educational_programs = EducationalPrograms.objects.filter(groups_of_educational_programs=groups_of_educational_programs)

        context = {
            'groups_of_educational_programs': groups_of_educational_programs,
            'educational_programs': educational_programs,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/groups_of_educational_programs_detail.html', context)


class EducationalProgramsDetailView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        educational_programs = EducationalPrograms.objects.get(id=kwargs.get('id'))

        context = {
            'educational_programs': educational_programs,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/educational_programs_detail.html', context)


class ProfileSubjectsView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        profile_subjects = UNTSubjects.objects.all()

        context = {
            'profile_subjects': profile_subjects,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/profile_subjects.html', context)


class SearchByProfileSubjectsView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        profile_subjects_result = UNTSubjects.objects.get(id=kwargs.get('id'))
        groups_of_educational_programs = GroupsOfEducationalPrograms.objects.filter(unt_subjects=profile_subjects_result)

        context = {
            'profile_subjects_result': profile_subjects_result,
            'groups_of_educational_programs': groups_of_educational_programs,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/profile_subjects.html', context)


class AllProgramsView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        educational_programs = EducationalPrograms.objects.all()

        context = {
            'educational_programs': educational_programs,
            'admin': self.admin,
            'student': self.student
        }
        return render(request, 'educational_institutions/all_programs.html', context)


class ApplicationsForAdmissionView(StudentMixin, AdminMixin, View):

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        educational_programs = EducationalPrograms.objects.get(id=kwargs.get('id'))
        category_document = DocumentCategory.objects.filter(for_graduates=True)
        student_document = StudentDocument.objects.filter(student=student)
        list_category_document = []
        list_student_document = []
        for item in category_document:
            list_category_document.append(item.id)
        for item in student_document:
            list_student_document.append(item.document_category.id)
        result=list(set(list_category_document) & set(list_student_document))
        if len(list_category_document) == len(result):
            ApplicationsForAdmission.objects.create(
                university=educational_programs.university,
                student=student,
                program=educational_programs
            )
            messages.add_message(request, messages.INFO, "Заявка была отправлена!")
            return redirect("profile")
        else:
            messages.add_message(request, messages.INFO, "Добавьте обязательные документы!")
            return redirect("profile")
