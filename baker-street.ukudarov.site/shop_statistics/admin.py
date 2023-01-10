from django.contrib import admin
from .models import *


class ForDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    list_display_links = ('id', 'created_at')
    list_filter = ['created_at']

admin.site.register(ForDay, ForDayAdmin)
