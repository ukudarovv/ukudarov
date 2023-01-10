from django.contrib import admin
from .models import *


class IngredientCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(IngredientCategory, IngredientCategoryAdmin)


class UnderIngredientInline(admin.TabularInline):
    model = UnderIngredient
    fk_name = "product"
    extra = 0


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'qty', 'unit_of_measurement', 'price', 'cost_price')
    list_display_links = ('id', 'title')
    list_filter = ['category', 'unit_of_measurement']
    inlines = [UnderIngredientInline]

admin.site.register(Ingredient, IngredientAdmin)


class UnderIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'ingredient', 'gross', 'unit_of_measurement', 'cost_price')
    list_display_links = ('id', 'product')
    list_filter = ['product']

admin.site.register(UnderIngredient, UnderIngredientAdmin)


class TechCardIngredientInline(admin.TabularInline):
    model = TechCardIngredient
    extra = 0


class TechCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'cost_price')
    list_display_links = ('id', 'product')
    list_filter = ['product']
    inlines = [TechCardIngredientInline]

admin.site.register(TechCard, TechCardAdmin)


class TechCardIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'ingredient', 'gross', 'cost_price')
    list_display_links = ('id', 'product')
    list_filter = ['product']

admin.site.register(TechCardIngredient, TechCardIngredientAdmin)
