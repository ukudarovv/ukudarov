from django.contrib import admin
from .models import *


class StudentDocumentInline(admin.TabularInline):
    model = StudentDocument
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Student._meta.fields]
    list_display_links = ('id', 'user', 'first_name')
    list_filter = ['core_competence', 'email', 'phone', 'created_at']
    inlines = [StudentDocumentInline]

    class Meta:
        model = Student

admin.site.register(Student, StudentAdmin)


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DocumentCategory._meta.fields]
    list_display_links = ('id', 'title')

    class Meta:
        model = DocumentCategory

admin.site.register(DocumentCategory, DocumentCategoryAdmin)


class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student']
    list_display_links = ('id', 'student')

    class Meta:
        model = StudentDocument

admin.site.register(StudentDocument, StudentDocumentAdmin)


class UniversityAdministratorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UniversityAdministrator._meta.fields]
    list_display_links = ('id', 'user')

    class Meta:
        model = UniversityAdministrator

admin.site.register(UniversityAdministrator, UniversityAdministratorAdmin)
