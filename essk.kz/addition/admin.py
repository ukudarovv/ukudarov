from django.contrib import admin
from .models import *


class AreaInline(admin.TabularInline):
    model = Area
    extra = 0


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    inlines = [AreaInline]

admin.site.register(Country, CountryAdmin)


class CityInline(admin.TabularInline):
    model = City
    extra = 0


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country')
    list_display_links = ('id', 'title')
    list_filter = ['country']
    inlines = [CityInline]

admin.site.register(Area, AreaAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'area')
    list_display_links = ('id', 'title')
    list_filter = ['area']

admin.site.register(City, CityAdmin)
