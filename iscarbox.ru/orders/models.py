from django.db import models
from shop.models import *
from django.db.models.signals import post_save


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None, verbose_name='Название статуса')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class PaymentMethod(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None, verbose_name='Способ оплаты')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'


class Region(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True, verbose_name='Название региона')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class City(models.Model):
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Название региона')
    name = models.CharField(max_length=40, blank=True, null=True, verbose_name='Название города')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма', help_text="Цена в рублях")
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL, verbose_name='Регион')
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL, verbose_name='Город')
    first_name = models.CharField(max_length=50, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, null=True, verbose_name='Фамилия')
    email = models.EmailField(null=True, verbose_name='Email')
    phone = models.CharField(max_length=48, null=True, verbose_name='Номер телефона')
    postal_code = models.CharField(max_length=20, null=True, verbose_name='Индекс')
    street = models.CharField(max_length=250, null=True, verbose_name='Улица')
    house = models.CharField(max_length=250, null=True, verbose_name='Дом')
    apartment = models.CharField(max_length=250, null=True, verbose_name='Номер квартиры')
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL, verbose_name='Статус заказа')
    payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL, verbose_name='Способ оплаты')
    message = models.TextField(max_length=500, blank=True, null=True, verbose_name='Комментарий к заказу')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL, related_name='order_items', verbose_name='Заказа')
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL, related_name='order_items', verbose_name='Товар')
    product_material = models.ForeignKey(ProductMaterialColor, blank=True, null=True, on_delete=models.SET_NULL, related_name='order_items', verbose_name='Цвет материала товара')
    product_thread = models.ForeignKey(ProductThreadColor, blank=True, null=True, on_delete=models.SET_NULL, related_name='order_items', verbose_name='Цвет нити товара')
    product_border = models.ForeignKey(ProductBorderColor, blank=True, null=True, on_delete=models.SET_NULL, related_name='order_items', verbose_name='Цвет окантовки товара')
    product_accessory = models.ForeignKey(ProductAccessory, blank=True, null=True, on_delete=models.SET_NULL, related_name='order_items', verbose_name='Аксессуар товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Цена в рублях", blank=True, null=True, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма')
    is_active = models.BooleanField(default=True, verbose_name='Доступный?')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return '{}'.format(self.id)


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL, related_name='basket_items', verbose_name='Товар')
    product_material = models.ForeignKey(ProductMaterialColor, blank=True, null=True, on_delete=models.SET_NULL, related_name='basket_items', verbose_name='Цвет материала товара')
    product_thread = models.ForeignKey(ProductThreadColor, blank=True, null=True, on_delete=models.SET_NULL, related_name='basket_items', verbose_name='Цвет нити товара')
    product_border = models.ForeignKey(ProductBorderColor, blank=True, null=True, on_delete=models.SET_NULL, related_name='basket_items', verbose_name='Цвет окантовки товара')
    product_accessory = models.ForeignKey(ProductAccessory, blank=True, null=True, on_delete=models.SET_NULL, related_name='basket_items', verbose_name='Аксессуар товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Цена в рублях", blank=True, null=True, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма')
    is_active = models.BooleanField(default=True, verbose_name='Доступный?')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return '{}'.format(self.id)

    def save(self, *args, **kwargs):
        price = self.product.price
        self.price = price
        self.total_price = int(self.quantity) * price
        super(ProductInBasket, self).save(*args, **kwargs)
