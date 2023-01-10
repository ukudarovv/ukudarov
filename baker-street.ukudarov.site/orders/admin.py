from django.contrib import admin
from .models import *


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product')
    list_display_links = ('id', 'order')
    list_filter = ['product']

admin.site.register(OrderProduct, OrderProductAdmin)


class OrderProductRemainderInline(admin.TabularInline):
    model = OrderProductRemainder
    extra = 0


class OrderProductRemainderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product')
    list_display_links = ('id', 'order')
    list_filter = ['order']

admin.site.register(OrderProductRemainder, OrderProductRemainderAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'buyer_shop', 'role', 'status', 'buying_type', 'pay', 'finish_making')
    list_display_links = ('id', 'user', 'buyer_shop')
    list_filter = ['user', 'buyer_shop', 'for_anonymous_user', 'role', 'status', 'buying_type', 'pay', 'finish_making']
    inlines = [OrderProductInline, OrderProductRemainderInline]

admin.site.register(Order, OrderAdmin)


class RefundProductInline(admin.TabularInline):
    model = RefundProduct
    extra = 0


class RefundProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'refund', 'product', 'qty', 'total_price')
    list_display_links = ('id', 'refund')
    list_filter = ['refund']

admin.site.register(RefundProduct, RefundProductAdmin)


class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'buyer_shop', 'total_price', 'finish_making', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ['buyer_shop', 'finish_making', 'created_at']
    inlines = [RefundProductInline]

admin.site.register(Refund, RefundAdmin)


class StocksProductInline(admin.TabularInline):
    model = StocksProduct
    extra = 0


class StocksProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'stocks', 'product', 'qty', 'total_price')
    list_display_links = ('id', 'stocks')
    list_filter = ['stocks']

admin.site.register(StocksProduct, StocksProductAdmin)


class StocksAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'buyer_shop', 'total_price', 'finish_making', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ['buyer_shop', 'finish_making', 'created_at']
    inlines = [StocksProductInline]

admin.site.register(Stocks, StocksAdmin)


class PreparedProductInline(admin.TabularInline):
    model = PreparedProduct
    extra = 0


class PreparedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'prepared_products_p_d', 'product', 'qty')
    list_display_links = ('id', 'prepared_products_p_d')
    list_filter = ['prepared_products_p_d']

admin.site.register(PreparedProduct, PreparedProductAdmin)


class PreparedProductsPerDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    list_display_links = ('id', 'created_at')
    list_filter = ['created_at']
    inlines = [PreparedProductInline]

admin.site.register(PreparedProductsPerDay, PreparedProductsPerDayAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'shop', 'number', 'created_at')
    list_display_links = ('id', 'order')
    list_filter = ['shop', 'created_at']

admin.site.register(Invoice, InvoiceAdmin)


class OrdersPaymentInvoiceInline(admin.TabularInline):
    model = OrdersPaymentInvoice
    extra = 0


class OrdersPaymentInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'pay_invoice', 'order')
    list_display_links = ('id', 'pay_invoice')
    list_filter = ['pay_invoice']

admin.site.register(OrdersPaymentInvoice, OrdersPaymentInvoiceAdmin)


class OrderProductPaymentInvoiceInline(admin.TabularInline):
    model = OrderProductPaymentInvoice
    extra = 0


class OrderProductPaymentInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'pay_invoice', 'product')
    list_display_links = ('id', 'pay_invoice')
    list_filter = ['pay_invoice']

admin.site.register(OrderProductPaymentInvoice, OrderProductPaymentInvoiceAdmin)


class PaymentInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'number', 'created_at')
    list_display_links = ('id', 'shop')
    list_filter = ['shop', 'created_at']
    inlines = [OrdersPaymentInvoiceInline, OrderProductPaymentInvoiceInline]

admin.site.register(PaymentInvoice, PaymentInvoiceAdmin)
