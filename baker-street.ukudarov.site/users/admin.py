from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'email', 'phone', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ['created_at']

admin.site.register(Customer, CustomerAdmin)


class DeliverymanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'email', 'phone', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ['created_at']

admin.site.register(Deliveryman, DeliverymanAdmin)


class ShopAdministratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'email', 'phone', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ['created_at']

admin.site.register(ShopAdministrator, ShopAdministratorAdmin)
