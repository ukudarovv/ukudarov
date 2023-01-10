from django.contrib import admin
from .models import *


class ProductMaterialColorInline(admin.TabularInline):
    model = ProductMaterialColor
    extra = 0


class ProductThreadColorInline(admin.TabularInline):
    model = ProductThreadColor
    extra = 0


class ProductBorderColorInline(admin.TabularInline):
    model = ProductBorderColor
    extra = 0


class ProductAccessoryInline(admin.TabularInline):
    model = ProductAccessory
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    list_display_links = ('id', 'name')
    list_editable = ('price', 'price_old')
    list_filter = ['available', 'created', 'updated']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductMaterialColorInline, ProductThreadColorInline, ProductBorderColorInline, ProductAccessoryInline]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


class ProductMaterialColorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductMaterialColor._meta.fields]
    list_display_links = ('id', 'color_title')
    list_editable = ('product', 'available',)
    class Meta:
        model = ProductMaterialColor

admin.site.register(ProductMaterialColor, ProductMaterialColorAdmin)


class ProductThreadColorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductThreadColor._meta.fields]
    list_display_links = ('id', 'color_title')
    list_editable = ('product', 'available',)

    class Meta:
        model = ProductThreadColor

admin.site.register(ProductThreadColor, ProductThreadColorAdmin)


class ProductBorderColorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductBorderColor._meta.fields]
    list_display_links = ('id', 'color_title')
    list_editable = ('product', 'available',)

    class Meta:
        model = ProductBorderColor

admin.site.register(ProductBorderColor, ProductBorderColorAdmin)


class CategoryProductAccessoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CategoryProductAccessory._meta.fields]
    list_display_links = ('id', 'title')

    class Meta:
        model = CategoryProductAccessory

admin.site.register(CategoryProductAccessory, CategoryProductAccessoryAdmin)


class ProductAccessoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductAccessory._meta.fields]
    list_display_links = ('id', 'accessory_title')
    list_editable = ('product', 'available',)

    class Meta:
        model = ProductAccessory

admin.site.register(ProductAccessory, ProductAccessoryAdmin)
