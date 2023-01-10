from django.contrib import admin
from .models import *


class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token', 'for_anonymous_user')
    list_display_links = ('id', 'user', 'token')
    list_filter = ['for_anonymous_user']
    inlines = [CartProductInline]

admin.site.register(Cart, CartAdmin)


class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'qty', 'total_price')
    list_display_links = ('id', 'cart')

admin.site.register(CartProduct, CartProductAdmin)
