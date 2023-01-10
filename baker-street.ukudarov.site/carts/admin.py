from django.contrib import admin
from .models import *



class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 0


class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product')
    list_display_links = ('id', 'cart')
    list_filter = ['cart']

admin.site.register(CartProduct, CartProductAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'role', 'for_anonymous_user')
    list_display_links = ('id', 'user')
    list_filter = ['for_anonymous_user', 'role']
    inlines = [CartProductInline]

admin.site.register(Cart, CartAdmin)
