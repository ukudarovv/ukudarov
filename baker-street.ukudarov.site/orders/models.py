from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from users.models import *
from shops.models import *
from products.models import *


class OrderProduct(models.Model):
    number = models.PositiveIntegerField(default=1, verbose_name='Нумерация')
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_product')
    product = models.ForeignKey("products.Product", verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return "{}".format(self.product.title)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class OrderProductRemainder(models.Model):
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_product_remainder')
    product = models.ForeignKey('products.Product', verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0)

    class Meta:
        verbose_name = 'Остаток от заказа'
        verbose_name_plural = 'Остатки от заказов'

    def __str__(self):
        return "{}".format(self.order.id)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_CANCELLED = 'is_cancelled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_CANCELLED, 'Заказ отменен'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    CUSTOMER = 'customer'
    DELIVERYMAN = 'deliveryman'
    SHOP_ADMINISTRATOR = 'shop_administrator'

    ROLE_CHOICES = (
        (CUSTOMER, 'Покупатель'),
        (DELIVERYMAN, 'Доставщик'),
        (SHOP_ADMINISTRATOR, 'Администратор')
    )


    KASPI = 'kaspi'
    CASH = 'cash'

    PAY_CHOICES = (
        (KASPI, 'Каспи'),
        (CASH, 'Наличными')
    )

    SIMPLE = 'simple'
    REALIZATION = 'realization'

    BUYING_TYPE_CHOICES = (
        (SIMPLE, 'Обычный'),
        (REALIZATION, 'Под реализацию')
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True)
    role = models.CharField(
        max_length=100,
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default=CUSTOMER,
        blank=True
    )
    for_anonymous_user = models.BooleanField(default=False, blank=True)
    buyer_shop = models.ForeignKey('shops.ShopBuyer', verbose_name='Закупщик', on_delete=models.CASCADE, related_name='order_shop', blank=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя', blank=True)
    phone = models.CharField(max_length=11, verbose_name='Телефон', blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    order_date = models.DateTimeField(verbose_name='Дата получения заказа', default=timezone.now, blank=True)
    finish_making = models.BooleanField(verbose_name='Завершение оформления', default=False, blank=True)
    paid = models.BooleanField(verbose_name='Оплатил', default=False, blank=True)

    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        blank=True
    )

    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        blank=False
    )

    pay = models.CharField(
        max_length=100,
        verbose_name='Оплата',
        choices=PAY_CHOICES,
        blank=False
    )

    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0, blank=True)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания заказа', blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "{}".format(self.id)

    def save(self, *args, **kwargs):
        products = OrderProduct.objects.filter(order=self)
        number_i = 0
        for item in products:
            number_i = number_i + 1
            item.number = number_i
            item.save()
        super().save(*args, **kwargs)


class Refund(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True)
    buyer_shop = models.ForeignKey('shops.ShopBuyer', verbose_name='Закупщик', on_delete=models.CASCADE, related_name='refund_shop', blank=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0, blank=True)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    finish_making = models.BooleanField(verbose_name='Завершение оформления', default=False, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания заказа', blank=True)

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'

    def __str__(self):
        return "{}".format(self.id)


class RefundProduct(models.Model):
    refund = models.ForeignKey('Refund', verbose_name='Возврат', on_delete=models.CASCADE, related_name='refund_product')
    product = models.ForeignKey('products.Product', verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0)

    class Meta:
        verbose_name = 'Товар (Возврат)'
        verbose_name_plural = 'Товары (Возврат)'

    def __str__(self):
        return "{}".format(self.refund.id)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Stocks(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True)
    buyer_shop = models.ForeignKey('shops.ShopBuyer', verbose_name='Закупщик', on_delete=models.CASCADE, related_name='stocks_shop', blank=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0, blank=True)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    finish_making = models.BooleanField(verbose_name='Завершение оформления', default=False, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания заказа', blank=True)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return "{}".format(self.id)


class StocksProduct(models.Model):
    stocks = models.ForeignKey('Stocks', verbose_name='Акция', on_delete=models.CASCADE, related_name='stock_product')
    product = models.ForeignKey('products.Product', verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0)

    class Meta:
        verbose_name = 'Товар (Акция)'
        verbose_name_plural = 'Товары (Акция)'

    def __str__(self):
        return "{}".format(self.stocks.id)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class PreparedProductsPerDay(models.Model):
    prepared_qty = models.PositiveIntegerField(default=1, verbose_name='Общее количество заготовленных товаров')
    created_at = models.DateField(verbose_name='Дата изготовления', blank=True, default=timezone.now)

    class Meta:
        verbose_name = 'Заготовленный товар'
        verbose_name_plural = 'Заготовленные товары'

    def __str__(self):
        return "{}".format(self.created_at)


class PreparedProduct(models.Model):

    PLUS = 'plus'
    MINUS = 'minus'

    CHOICES = (
        (PLUS, 'Прибавить'),
        (MINUS, 'Отнять')
    )

    action = models.CharField(
        max_length=100,
        verbose_name='Действие',
        choices=CHOICES,
        blank=True,
        null=True
    )
    prepared_products_p_d = models.ForeignKey('PreparedProductsPerDay', verbose_name='Заготовленные товары', on_delete=models.CASCADE, related_name='prepared_product')
    product = models.ForeignKey('products.Product', verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name='Остаток не проданного')
    sale_qty = models.PositiveIntegerField(default=0, verbose_name='Количество проданного')
    stocks_qty = models.PositiveIntegerField(default=0, verbose_name='Количество товаров по акции')
    refund_qty = models.PositiveIntegerField(default=0, verbose_name='Количество возвращенного')
    prepared_qty = models.PositiveIntegerField(default=1, verbose_name='Количество заготовленных')

    class Meta:
        verbose_name = 'Товар (Заготовленный товар)'
        verbose_name_plural = 'Товары (Заготовленный товар)'

    def __str__(self):
        return "{}".format(self.product.title)


class Invoice(models.Model):
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_invoice', blank=True)
    shop = models.ForeignKey('shops.ShopBuyer', verbose_name='Закупщик', on_delete=models.CASCADE, related_name='shop_invoice', blank=True)
    number = models.PositiveIntegerField(default=1, verbose_name='Номер')
    created_at = models.DateField(verbose_name='Дата', blank=True, default=timezone.now)

    class Meta:
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'

    def __str__(self):
        return "{}".format(self.number)


class PaymentInvoice(models.Model):
    shop = models.ForeignKey('shops.ShopBuyer', verbose_name='Закупщик', on_delete=models.CASCADE, related_name='shop_pay_invoice', blank=True)
    number = models.PositiveIntegerField(default=0, verbose_name='Номер', blank=True)
    number_2 = models.CharField(max_length=1024, verbose_name='Номер договора', null=True, blank=True)
    created_at = models.DateField(verbose_name='Дата', blank=True, default=timezone.now)
    qty = models.PositiveIntegerField(default=0, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0)
    finish_making = models.BooleanField(verbose_name='Завершение оформления', default=False, blank=True)


    class Meta:
        verbose_name = 'Счет на оплату'
        verbose_name_plural = 'Счет на оплату'

    def __str__(self):
        return "{}".format(self.number)

    def save(self, *args, **kwargs):
        products = OrderProductPaymentInvoice.objects.filter(pay_invoice=self)
        number_i = 0
        qty = 0
        total_price = 0
        for item in products:
            number_i = number_i + 1
            item.number = number_i
            qty = qty + 1
            total_price += item.total_price
            item.save()
        self.total_price = total_price
        self.qty = qty
        super().save(*args, **kwargs)


class OrdersPaymentInvoice(models.Model):
    pay_invoice = models.ForeignKey('PaymentInvoice', verbose_name='Счет на оплату', on_delete=models.CASCADE, related_name='pay_invoice', blank=True)
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_pay_invoice', blank=True)

    class Meta:
        verbose_name = 'Счет на оплату (Заказы)'
        verbose_name_plural = 'Счет на оплату (Заказы)'

    def __str__(self):
        return "{}".format(self.order.id)


class OrderProductPaymentInvoice(models.Model):
    pay_invoice = models.ForeignKey('PaymentInvoice', verbose_name='Счет на оплату', on_delete=models.CASCADE, related_name='product_pay_invoice', blank=True)
    number = models.PositiveIntegerField(default=1, verbose_name='Нумерация', blank=True)
    product = models.ForeignKey("products.Product", verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая сумма', default=0.0)

    class Meta:
        verbose_name = 'Счет на оплату (Товар в заказе)'
        verbose_name_plural = 'Счет на оплату (Товары в заказе)'

    def __str__(self):
        return "{}".format(self.product.title)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.product.price
        super().save(*args, **kwargs)
