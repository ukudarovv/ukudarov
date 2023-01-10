from django import forms
from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin, ImportExportMixin


class BannerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_display_links = ('id', 'title')
    list_filter = ['is_active']
    list_editable = ['is_active']

admin.site.register(Banner, BannerAdmin)


class CategoryPublicationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_display_links = ('id', 'title')
    list_filter = ['is_active']
    list_editable = ['is_active']

admin.site.register(CategoryPublication, CategoryPublicationAdmin)


class PublicationAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].label = 'Текст'

    class Meta:
        model = Publication
        fields = '__all__'


class PublicationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_active')
    list_display_links = ('id', 'title')
    list_filter = ['category', 'is_active']
    list_editable = ['is_active']
    form = PublicationAdminForm

admin.site.register(Publication, PublicationAdmin)
