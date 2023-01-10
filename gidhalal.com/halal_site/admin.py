from django.contrib import admin
from .models import *
from restaurant.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_display_links = ('id', 'title')
    list_editable = ['is_active']

admin.site.register(Product, ProductAdmin)


class ProductSupplierInline(admin.TabularInline):
    model = ProductSupplier
    extra = 0


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_active', 'created_at')
    list_display_links = ('id', 'user', 'created_at')
    inlines = [ProductSupplierInline]
    list_editable = ['is_active']

admin.site.register(Supplier, SupplierAdmin)


class ProductSupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'supplier', 'is_active')
    list_display_links = ('id', 'product', 'supplier')
    list_filter = ['supplier', 'is_active']
    list_editable = ['is_active']

admin.site.register(ProductSupplier, ProductSupplierAdmin)


class CategoryRestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_display_links = ('id', 'title')
    list_editable = ['is_active']

admin.site.register(CategoryRestaurant, CategoryRestaurantAdmin)


class ProductRestaurantInline(admin.TabularInline):
    model = ProductRestaurant
    extra = 0


class RestaurantProductInline(admin.TabularInline):
    model = RestaurantProduct
    extra = 0


class LinksInline(admin.TabularInline):
    model = Links
    extra = 0


class OpenningTimeInline(admin.TabularInline):
    model = OpenningTime
    extra = 0


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_active', 'created_at')
    list_display_links = ('id', 'title', 'category', 'created_at')
    list_filter = ['category', 'is_active']
    list_editable = ['is_active']
    inlines = [ProductRestaurantInline, RestaurantProductInline, LinksInline, OpenningTimeInline]

admin.site.register(Restaurant, RestaurantAdmin)


class ProductRestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'product', 'supplier', 'is_active')
    list_display_links = ('id', 'restaurant', 'product', 'supplier')
    list_filter = ['restaurant', 'supplier', 'is_active']
    list_editable = ['is_active']

admin.site.register(ProductRestaurant, ProductRestaurantAdmin)
