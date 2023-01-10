from django import forms
from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin, ImportExportMixin


admin.site.site_header = "Администрирование сайта 'ESSK'"


class CategoryProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(CategoryProduct, CategoryProductAdmin)


class CategoryResource(resources.ModelResource):

    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget = widgets.ForeignKeyWidget(Category, 'title'))

    class Meta:
        model = Category
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('title',)
        fields = ('id', 'parent','title','category_all','lft','rght','tree_id','level')


class CategoryMPTTModelAdmin(ImportExportModelAdmin, MPTTModelAdmin):
    resource_class = CategoryResource

admin.site.register(Category, CategoryMPTTModelAdmin)


class BrandAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(Brand, BrandAdmin)


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].label = 'Описание'

    class Meta:
        model = Product
        fields = '__all__'


class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 0


class ProductFeedbackInline(admin.TabularInline):
    model = ProductFeedback
    extra = 0



class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        skip_unchanged = True
        report_skipped = True


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource
    exclude = ['id']
    form = ProductAdminForm
    fields = ('category','category_p', 'category_all','brand','title','image','article', 'code', 'price', 'new_price', 'discount', 'm_description', 'description', 'is_active')
    list_display = ('title', 'category', 'brand', 'is_active')
    list_display_links = ('title',)
    list_filter = ['category', 'brand', 'category_p']
    list_editable = ['category', 'brand', 'is_active']
    inlines = [ProductPhotoInline, ProductFeedbackInline]

admin.site.register(Product, ProductAdmin)


class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')
    list_display_links = ('id', 'product')

admin.site.register(ProductPhoto, ProductPhotoAdmin)


class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 0


class CategoryFeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')
    list_display_links = ('id', 'title')
    list_filter = ['category']
    inlines = [FeatureValueInline]

admin.site.register(CategoryFeature, CategoryFeatureAdmin)


class ValueKeyInline(admin.TabularInline):
    model = ValueKey
    extra = 0


class FeatureValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category_feature')
    list_display_links = ('id', 'title')
    list_filter = ['category_feature']
    inlines = [ValueKeyInline]

admin.site.register(FeatureValue, FeatureValueAdmin)


class ValueKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'feature_value')
    list_display_links = ('id', 'title')
    list_filter = ['feature_value']

admin.site.register(ValueKey, ValueKeyAdmin)


class ProductFeatureValueInline(admin.TabularInline):
    model = ProductFeatureValue
    extra = 0


class ProductFeaturesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'category_feature')
    list_display_links = ('id', 'product')
    list_filter = ['product', 'category_feature']
    inlines = [ProductFeatureValueInline]

admin.site.register(ProductFeatures, ProductFeaturesAdmin)


class ProductFeatureValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_features', 'feature_value', 'value_key')
    list_display_links = ('id', 'product_features')
    list_filter = ['product_features']

admin.site.register(ProductFeatureValue, ProductFeatureValueAdmin)


class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'first_name', 'email', 'point', 'for_anonymous_user')
    list_display_links = ('id', 'product')
    list_filter = ['email', 'for_anonymous_user']

admin.site.register(ProductFeedback, ProductFeedbackAdmin)
