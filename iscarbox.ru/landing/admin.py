from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'numder_phone', 'email')
    list_display_links = ('id', 'numder_phone')

admin.site.register(Contacts, ContactsAdmin)


class ContactformAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone_number', 'created_at')
    list_display_links = ('id', 'first_name')
    list_filter = ('phone_number', 'created_at',)
    readonly_fields = ['created_at']

admin.site.register(ContactForm, ContactformAdmin)


class DeveliryAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Develiry
        fields = '__all__'


class DeveliryAdmin(admin.ModelAdmin):
    form = DeveliryAdminForm
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')

admin.site.register(Develiry, DeveliryAdmin)


class PaymentmethodsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Paymentmethods
        fields = '__all__'


class PaymentmethodsAdmin(admin.ModelAdmin):
    form = PaymentmethodsAdminForm
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')

admin.site.register(Paymentmethods, PaymentmethodsAdmin)


class PurchasereturnsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Purchasereturns
        fields = '__all__'


class PurchasereturnsAdmin(admin.ModelAdmin):
    form = PurchasereturnsAdminForm
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')

admin.site.register(Purchasereturns, PurchasereturnsAdmin)


class SitepolicyAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Sitepolicy
        fields = '__all__'


class SitepolicyAdmin(admin.ModelAdmin):
    form = SitepolicyAdminForm
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')

admin.site.register(Sitepolicy, SitepolicyAdmin)


class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(Carousel, CarouselAdmin)


class SEOAdminForm(forms.ModelForm):
    google_analytics = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = SEO
        fields = '__all__'

class SEOAdmin(admin.ModelAdmin):
    form = SEOAdminForm
    list_display = ('id', 'description')
    list_display_links = ('id', 'description')

admin.site.register(SEO, SEOAdmin)
