from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *


urlpatterns = [
    path('', SearchUnivView.as_view(), name='search_univ'),
    path('university/<int:id>/', UnivDetailView.as_view(), name='univ_detail'),
    path('search_by_type/', AllByTypeView.as_view(), name='search_by_type'),
    path('search_by_type/<int:id>/', SearchByTypeView.as_view(), name='type_university'),
    path('search_by_category/', AllByCategoryView.as_view(), name='search_by_category'),
    path('search_by_category/<int:id>/', SearchByCategoryView.as_view(), name='category_university'),
    path('search_by_region/', AllByRegionView.as_view(), name='search_by_region'),
    path('search_by_region/<int:id>/', SearchByRegionView.as_view(), name='city'),
    path('search_by_code/', AllByCodeView.as_view(), name='search_by_code'),
    path('specializations/<int:id>/', SpecializationsDetailView.as_view(), name='specializations'),
    path('all_specializations/', AllSpecializationsView.as_view(), name='all_specializations'),
    path('all_specializations/<int:id>/', SpecializationsView.as_view(), name='scientific_degrees_1'),
    path('areas_of_education/<int:id>/', AreasOfEducationDetailView.as_view(), name='areas_of_education'),
    path('all_areas_of_education/', AllAreasOfEducationView.as_view(), name='all_areas_of_education'),
    path('all_areas_of_education/<int:id>/', AreasOfEducationView.as_view(), name='scientific_degrees_2'),
    path('areas_of_training/<int:id>/', AreasOfTrainingDetailView.as_view(), name='areas_of_training'),
    path('all_areas_of_training/', AllAreasOfTrainingView.as_view(), name='all_areas_of_training'),
    path('all_areas_of_training/<int:id>/', AreasOfTrainingView.as_view(), name='scientific_degrees_3'),
    path('all_groups_of_educational_programs/', AllGroupsOfEducationalProgramsView.as_view(), name='all_groups_of_educational_programs'),
    path('all_groups_of_educational_programs/<int:id>/', GroupsOfEducationalProgramsView.as_view(), name='scientific_degrees_4'),
    path('groups_of_educational_programs/<int:id>/', GroupsOfEducationalProgramsDetailView.as_view(), name='groups_of_educational_programs'),
    path('educational_programs/<int:id>/', EducationalProgramsDetailView.as_view(), name='educational_programs'),
    path('profile_subjects/', ProfileSubjectsView.as_view(), name='profile_subjects'),
    path('profile_subjects/<int:id>/', SearchByProfileSubjectsView.as_view(), name='unt_subjects'),
    path('all_programs/', AllProgramsView.as_view(), name='all_programs'),
    path('applications_for_admission/<int:id>/', ApplicationsForAdmissionView.as_view(), name='applications_for_admission'),
]
