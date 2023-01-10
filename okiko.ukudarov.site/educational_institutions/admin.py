from django.contrib import admin
from .models import *

class UniversityContactInline(admin.TabularInline):
    model = UniversityContact
    extra = 0


class UniversityGalleryInline(admin.TabularInline):
    model = UniversityGallery
    extra = 0


class UniversityNewsInline(admin.TabularInline):
    model = UniversityNews
    extra = 0


class UniversitySpecializationsInline(admin.TabularInline):
    model = UniversitySpecializations
    extra = 0


class EducationalProgramsInline(admin.TabularInline):
    model = EducationalPrograms
    extra = 0


class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'abbreviation', 'code', 'city', 'category', 'type']
    list_display_links = ('id', 'title')
    list_filter = ['city', 'category', 'type']
    inlines = [UniversitySpecializationsInline, EducationalProgramsInline, UniversityContactInline, UniversityGalleryInline, UniversityNewsInline]

    class Meta:
        model = University

admin.site.register(University, UniversityAdmin)


class CategoryUniversityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CategoryUniversity._meta.fields]
    list_display_links = ('id', 'name')

    class Meta:
        model = CategoryUniversity

admin.site.register(CategoryUniversity, CategoryUniversityAdmin)


class TypeUniversityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TypeUniversity._meta.fields]
    list_display_links = ('id', 'name')

    class Meta:
        model = TypeUniversity

admin.site.register(TypeUniversity, TypeUniversityAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]
    list_display_links = ('id', 'name')
    list_filter = ['region']

    class Meta:
        model = City

admin.site.register(City, CityAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Region._meta.fields]
    list_display_links = ('id', 'name')

    class Meta:
        model = Region

admin.site.register(Region, RegionAdmin)


class ScientificDegreesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScientificDegrees._meta.fields]
    list_display_links = ('id', 'title')

    class Meta:
        model = ScientificDegrees

admin.site.register(ScientificDegrees, ScientificDegreesAdmin)


class SpecializationsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Specializations._meta.fields]
    list_display_links = ('id', 'title')
    list_filter = ['scientific_degrees', 'unt_subjects', 'groups_of_educational_programs']

    class Meta:
        model = Specializations

admin.site.register(Specializations, SpecializationsAdmin)


class UNTSubjectsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UNTSubjects._meta.fields]
    list_display_links = ('id', 'title')

    class Meta:
        model = UNTSubjects

admin.site.register(UNTSubjects, UNTSubjectsAdmin)


class AreasOfEducationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AreasOfEducation._meta.fields]
    list_display_links = ('id', 'title')
    list_filter = ['scientific_degrees']

    class Meta:
        model = AreasOfEducation

admin.site.register(AreasOfEducation, AreasOfEducationAdmin)


class AreasOfTrainingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AreasOfTraining._meta.fields]
    list_display_links = ('id', 'title')
    list_filter = ['scientific_degrees', 'areas_of_education']

    class Meta:
        model = AreasOfTraining

admin.site.register(AreasOfTraining, AreasOfTrainingAdmin)


class GroupsOfEducationalProgramsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GroupsOfEducationalPrograms._meta.fields]
    list_display_links = ('id', 'title')
    list_filter = ['scientific_degrees', 'unt_subjects', 'areas_of_education', 'areas_of_training']

    class Meta:
        model = GroupsOfEducationalPrograms

admin.site.register(GroupsOfEducationalPrograms, GroupsOfEducationalProgramsAdmin)


class EducationalProgramsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EducationalPrograms._meta.fields]
    list_display_links = ('id', 'title')
    list_filter = ['university', 'scientific_degrees', 'groups_of_educational_programs', 'unt_subjects', 'areas_of_education', 'areas_of_training']

    class Meta:
        model = EducationalPrograms

admin.site.register(EducationalPrograms, EducationalProgramsAdmin)


class UniversitySpecializationsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UniversitySpecializations._meta.fields]
    list_display_links = ('id', 'university')

    class Meta:
        model = UniversitySpecializations

admin.site.register(UniversitySpecializations, UniversitySpecializationsAdmin)


class ApplicationsForAdmissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ApplicationsForAdmission._meta.fields]
    list_display_links = ('id', 'university')

    class Meta:
        model = ApplicationsForAdmission

admin.site.register(ApplicationsForAdmission, ApplicationsForAdmissionAdmin)
