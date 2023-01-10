from django.contrib import admin
from .models import *
import csv
import datetime
from django.http import HttpResponse


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    raw_id_fields = ['product']
    extra = 0


class StatusAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]

    class Meta:
        model = Status

admin.site.register(Status, StatusAdmin)

class PaymentMethodAdmin (admin.ModelAdmin):
    list_display = [field.name for field in PaymentMethod._meta.fields]

    class Meta:
        model = PaymentMethod

admin.site.register(PaymentMethod, PaymentMethodAdmin)

class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]
    list_display_links = ('id', 'product')

    class Meta:
        model = ProductInOrder

admin.site.register(ProductInOrder, ProductInOrderAdmin)


class ProductInBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]
    list_display_links = ('id', 'session_key')
    readonly_fields = ['created', 'updated']

    class Meta:
        model = ProductInBasket

admin.site.register(ProductInBasket, ProductInBasketAdmin)


class RegionAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Region._meta.fields]

    class Meta:
        model = Region

admin.site.register(Region, RegionAdmin)


class CityAdmin (admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]

    class Meta:
        model = City

admin.site.register(City, CityAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'phone', 'region', 'city', 'status',
                    'created', 'updated']
    list_display_links = ('id', 'first_name')
    list_editable = ['status']
    list_filter = ['status', 'created', 'updated']
    inlines = [ProductInOrderInline]
    actions = [export_to_csv]
    readonly_fields = ['created', 'updated']

admin.site.register(Order, OrderAdmin)
