from django.contrib import admin
from .models import *


class ShopDeliveryForDayInline(admin.TabularInline):
    model = ShopDeliveryForDay
    extra = 0


class ShopDeliveryForDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery', 'shop', 'delivered', 'created_at')
    list_display_links = ('id', 'delivery')
    list_filter = ['shop', 'delivered', 'created_at']

admin.site.register(ShopDeliveryForDay, ShopDeliveryForDayAdmin)


class DeliveryForDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ['created_at']
    inlines = [ShopDeliveryForDayInline]

admin.site.register(DeliveryForDay, DeliveryForDayAdmin)
