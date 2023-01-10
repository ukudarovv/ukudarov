from django.contrib import admin
from .models import *


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'address')
    list_display_links = ('id', 'title')
    inlines = [IngredientInline, ProductInline]

admin.site.register(Warehouse, WarehouseAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse', 'product', 'qty', 'unit_of_measurement', 'price')
    list_display_links = ('id', 'warehouse', 'product')
    list_filter = ['warehouse']

admin.site.register(Ingredient, IngredientAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse', 'product', 'qty', 'price')
    list_display_links = ('id', 'warehouse', 'product')
    list_filter = ['warehouse']

admin.site.register(Product, ProductAdmin)
