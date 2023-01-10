from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *


admin.site.site_header = "Администрирование сайта 'Dina Atyrau by Kudarov™'"


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(News, NewsAdmin)


admin.site.register(RequestFromShop)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'rating', 'created_at')
    list_display_links = ('id', 'product')
    list_filter = ['product', 'rating', 'created_at']

admin.site.register(Reviews, ReviewsAdmin)


class AboutUsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = AboutUs
        fields = '__all__'


class AboutUsAdmin(admin.ModelAdmin):
    form = AboutUsAdminForm
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')

admin.site.register(AboutUs, AboutUsAdmin)


class AboutDinaAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = AboutDina
        fields = '__all__'


class AboutDinaAdmin(admin.ModelAdmin):
    form = AboutDinaAdminForm
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')

admin.site.register(AboutDina, AboutDinaAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'average_rating')
    list_display_links = ('id', 'product')
    list_filter = ['average_rating', 'product']

admin.site.register(Rating, RatingAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'status', 'price', 'service')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    list_filter = ['status', 'service', 'shop', 'category']
    change_form_template = 'custom_admin/change_form.html'


class ParentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


class MiddleCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_category')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['parent_category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'middle_category')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['middle_category']


class ShopAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Shop._meta.fields]
    list_display_links = ('id', 'shop_name')
    list_filter = ['status', 'created_at', 'end_time']
    list_editable = ['status']
    prepopulated_fields = {'slug': ('shop_name',)}

    class Meta:
        model = Shop


class RequestToWorkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RequestToWork._meta.fields]
    list_display_links = ('id', 'shop')
    list_filter = ['yes_or_no', 'created_at']

    class Meta:
        model = RequestToWork


class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields]
    list_display_links = ('id', 'user')
    list_filter = ['sex', 'created_at']

    class Meta:
        model = Customer


class ComplaintsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Complaints._meta.fields]
    list_display_links = ('id', 'order')
    list_filter = ['type_of_request', 'created_at']

    class Meta:
        model = Complaints


class SupportServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SupportService._meta.fields]
    list_display_links = ('id', 'user')
    list_filter = ['type_of_request', 'created_at']

    class Meta:
        model = SupportService


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    list_display_links = ('id', 'customer')
    list_filter = ['status', 'created_at']

    class Meta:
        model = Order

class UserPasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ['created_at']

admin.site.register(UserPassword, UserPasswordAdmin)


class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ['created_at']

admin.site.register(Slider, SliderAdmin)


class RequestServiceToShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone', 'status', 'created_at')
    list_display_links = ('id', 'first_name')
    list_filter = ['phone', 'status', 'created_at']

admin.site.register(RequestServiceToShop, RequestServiceToShopAdmin)


admin.site.register(Shop, ShopAdmin)
admin.site.register(RequestToWork, RequestToWorkAdmin)
admin.site.register(ParentCategory, ParentCategoryAdmin)
admin.site.register(MiddleCategory, MiddleCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartProduct)
admin.site.register(OrderProduct)
admin.site.register(OrderForShop)
admin.site.register(Cart)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Complaints, ComplaintsAdmin)
admin.site.register(SupportService, SupportServiceAdmin)
