from django.contrib import admin
from .models import *


class ShopBuyerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'customer', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ['created_at']

admin.site.register(ShopBuyer, ShopBuyerAdmin)
