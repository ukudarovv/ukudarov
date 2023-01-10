from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class UserAddressInline(admin.TabularInline):
    model = UserAddress
    extra = 0


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email']
    list_display_links = ('username', 'email')
    inlines = [UserAddressInline]

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Доп. данные',
            {
                'fields': (
                    'phone',
                )
            }
        )
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Доп. данные',
            {
                'fields': (
                    'phone',
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')

admin.site.register(UserAddress, UserAddressAdmin)


class TypeCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(TypeCompany, TypeCompanyAdmin)


class ActivityCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(ActivityCompany, ActivityCompanyAdmin)


class CompanyAddressInline(admin.TabularInline):
    model = CompanyAddress
    extra = 0


class CompanyContactInline(admin.TabularInline):
    model = CompanyContact
    extra = 0


class CompanyBankDetailsInline(admin.TabularInline):
    model = CompanyBankDetails
    extra = 0


class CompanyRequisiteInline(admin.TabularInline):
    model = CompanyRequisite
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'activity', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ['type', 'activity']
    inlines = [CompanyAddressInline, CompanyContactInline, CompanyBankDetailsInline, CompanyRequisiteInline]

admin.site.register(Company, CompanyAdmin)


class CompanyAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'country', 'area', 'city')
    list_display_links = ('id', 'company')
    list_filter = ['company', 'country', 'area', 'city']

admin.site.register(CompanyAddress, CompanyAddressAdmin)


class CompanyContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'user')
    list_display_links = ('id', 'company')
    list_filter = ['company']

admin.site.register(CompanyContact, CompanyContactAdmin)


class CompanyBankDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'company')
    list_display_links = ('id', 'company')
    list_filter = ['company']

admin.site.register(CompanyBankDetails, CompanyBankDetailsAdmin)


class CategoryRequisiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ie', 'le')
    list_display_links = ('id', 'title')
    list_filter = ['ie', 'le']

admin.site.register(CategoryRequisite, CategoryRequisiteAdmin)


class CompanyRequisiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'company')
    list_display_links = ('id', 'company')
    list_filter = ['company']

admin.site.register(CompanyRequisite, CompanyRequisiteAdmin)
