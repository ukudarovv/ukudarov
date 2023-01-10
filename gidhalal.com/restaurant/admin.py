from django.contrib import admin
from .models import *


class RestaurantUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'is_active', 'created_at')
    list_display_links = ('id', 'user')
    list_editable = ['is_active']

admin.site.register(RestaurantUser, RestaurantUserAdmin)


class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_display_links = ('id', 'title')
    list_editable = ['is_active']

admin.site.register(CategoryProduct, CategoryProductAdmin)


class RestaurantProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'title', 'category', 'price', 'is_active', 'created_at')
    list_display_links = ('id', 'restaurant', 'title')
    list_filter = ['category', 'restaurant', 'is_active']
    list_editable = ['is_active']

admin.site.register(RestaurantProduct, RestaurantProductAdmin)


class LinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant')
    list_display_links = ('id', 'restaurant')
    list_filter = ['restaurant']

admin.site.register(Links, LinksAdmin)


class OpenningTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'weekday')
    list_display_links = ('id', 'restaurant')
    list_filter = ['restaurant']

admin.site.register(OpenningTime, OpenningTimeAdmin)
