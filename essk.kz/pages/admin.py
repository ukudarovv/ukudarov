from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *


class CertificatesAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Certificates
        fields = '__all__'


class CertificatesAdmin(admin.ModelAdmin):
    form = CertificatesAdminForm
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')

admin.site.register(Certificates, CertificatesAdmin)


class PartnersAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Partners
        fields = '__all__'


class PartnersAdmin(admin.ModelAdmin):
    form = PartnersAdminForm
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')

admin.site.register(Partners, PartnersAdmin)


class RefundAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Refund
        fields = '__all__'


class RefundAdmin(admin.ModelAdmin):
    form = RefundAdminForm
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')

admin.site.register(Refund, RefundAdmin)
