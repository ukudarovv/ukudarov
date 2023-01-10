from django.contrib import admin
from .models import *


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(PaymentType, PaymentTypeAdmin)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ['type', 'created_at']
    inlines = [OrderProductInline]

admin.site.register(Order, OrderAdmin)


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'qty', 'total_price')
    list_display_links = ('id', 'order')

admin.site.register(OrderProduct, OrderProductAdmin)
