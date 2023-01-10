from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from slugify import slugify

User = get_user_model()


class UserPassword(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, blank=True)
    password = models.CharField(max_length=1000, verbose_name='Password', blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=True)

    class Meta:
        verbose_name = 'Секретно'
        verbose_name_plural = 'Секретно'

    def __str__(self):
        return self.user.username


class Slider(models.Model):
    name = models.CharField(db_index=True, max_length=255, verbose_name='Название', blank=True)
    image = models.ImageField(upload_to='slider/', verbose_name='Изображение', blank=True)
    link = models.URLField(db_index=True, max_length=255, verbose_name='Ссылка', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.name


class ParentCategory(models.Model):
    image = models.CharField(max_length=1000, verbose_name='Изображение', blank=True)
    name = models.CharField(db_index=True, max_length=255, verbose_name='Имя категории')
    service = models.BooleanField("Это услуга?", blank=True, default=False)
    slug = models.SlugField(db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории 1 уровень'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('parent_category_detail', kwargs={'slug': self.slug})


class MiddleCategory(models.Model):
    image = models.CharField(max_length=1000, verbose_name='Изображение', blank=True)
    parent_category = models.ForeignKey(ParentCategory, verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField(db_index=True, max_length=255, verbose_name='Имя категории')
    service = models.BooleanField("Это услуга?", blank=True, default=False)
    slug = models.SlugField(db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории 2 уровень'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('middle_category_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    image = models.CharField(max_length=1000, verbose_name='Изображение', blank=True)
    middle_category = models.ForeignKey(MiddleCategory, verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField(db_index=True, max_length=255, verbose_name='Имя категории')
    service = models.BooleanField("Это услуга?", blank=True, default=False)
    slug = models.SlugField(db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории 3 уровень'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Customer(models.Model):
    SEX = (
        ('MEN', 'Мужчина'),
        ('WOMEN', 'Женщина')
    )

    JOB = (
        ('DIRECTOR', 'Директор'),
        ('SELLER', 'Продавец'),
        ('REPAIRER', 'Ремонтник'),
        ('ACCOUNTANT', 'Бухгалтер')
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True, blank=True)
    sex = models.CharField("Пол", blank=True, max_length=30, choices=SEX,
                           default="Нет")
    email = models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order', blank=True)
    job = models.CharField("Должность", blank=True, max_length=30, choices=JOB)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания профиля')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Product(models.Model):
    ON_VERIFICATION = 'На проверке'
    STATUS = (
        ('ON_VERIFICATION', 'На проверке'),
        ('ACTIVE', 'Активный'),
        ('NO_ACTIVE', 'Не активный'),
    )

    IN_STOCK = 'В наличии'
    STATUS_PRODUCT = (
        ('IN_STOCK', 'В наличии'),
        ('OUT_OF_STOCK', 'Не в наличии'),
        ('WILL_BE_SOON', 'Скоро будет'),
    )

    title = models.CharField(db_index=True, max_length=100, verbose_name='Наименование')
    shop = models.ForeignKey('Shop', verbose_name='Товары магазина', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    status = models.CharField("Статус", max_length=30, choices=STATUS, default=ON_VERIFICATION)
    status_product = models.CharField("В наличии", max_length=30, choices=STATUS_PRODUCT, default=IN_STOCK, blank=True)
    slug = models.SlugField(db_index=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Изображение 1', blank=True)
    image_2 = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Изображение 2', blank=True)
    image_3 = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Изображение 3', blank=True)
    image_4 = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Изображение 4', blank=True)
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    contractual_price = models.BooleanField("Договорная цена", blank=True, default=False)
    service = models.BooleanField("Это услуга?", blank=True, default=False)
    order_qty = models.PositiveIntegerField(default=0)
    features = models.ManyToManyField("specs.ProductFeatures", blank=True, related_name='features_for_product')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + "_" + self.shop.slug)
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_features(self):
        return {f.feature.feature_name: ' '.join([f.value, f.feature.unit or ""]) for f in self.features.all()}


class Reviews(models.Model):
    rating = models.DecimalField("Оценка", max_digits=9, decimal_places=0)
    product = models.ForeignKey('Product', verbose_name='Товар', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Сообщение')
    created_at_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return "Отзыв: от {}".format(self.customer.first_name)


class Rating(models.Model):
    product = models.ForeignKey('Product', verbose_name='Товар', on_delete=models.CASCADE)
    one = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Оценка единица')
    two = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Оценка двойка')
    three = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Оценка тройка')
    four = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Оценка четверка')
    five = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Оценка пятерка')
    average_rating = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Средняя оценка')

    class Meta:
        verbose_name = 'Рейтинг товара'
        verbose_name_plural = 'Рейтинги товаров'

    def __str__(self):
        return "Товар {}".format(self.product.title)


class Shop(models.Model):
    ON_VERIFICATION = 'На проверке'
    STATUS = (
        ('ON_VERIFICATION', 'На проверке'),
        ('ACTIVE', 'Активный'),
        ('NO_ACTIVE', 'Не активный'),
    )
    shop_name = models.CharField(db_index=True, max_length=20, verbose_name='Название магазина')
    customer = models.ManyToManyField('Customer', verbose_name='Администраторы магазина', blank=True)
    category = models.ManyToManyField('ParentCategory', verbose_name='Категории магазина', blank=True)
    status = models.CharField("Статус", max_length=30, choices=STATUS, default=ON_VERIFICATION)
    shop_image = models.ImageField(verbose_name='Логотип магазина', upload_to='shop/logo/', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True)
    slug = models.SlugField(db_index=True)
    shop_address = models.CharField(max_length=255, verbose_name='Адрес магазина')
    shop_email = models.EmailField(max_length=254, verbose_name='Email магазина')
    shop_phone = models.CharField(max_length=12, verbose_name='Номер телефона магазина')
    instagram = models.CharField(max_length=250, verbose_name='Имя пользователя в Instagram', blank=True)
    vk = models.CharField(max_length=250, verbose_name='Имя пользователя в VK', blank=True)
    facebook = models.CharField(max_length=250, verbose_name='Имя пользователя в Facebook', blank=True)
    whatsapp = models.CharField(max_length=12, verbose_name='Номер телефона WhatsApp', blank=True)
    telegram = models.CharField(max_length=255, verbose_name='Имя пользователя в Telegram', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания магазина')
    end_time = models.DateTimeField(default=timezone.now, verbose_name='Дата окончания срока магазина')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.shop_name)
        return super(Shop, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.shop_name)

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'slug': self.slug})


class RequestToWork(models.Model):
    YES_OR_NO = (
        ('YES', 'Да'),
        ('NO', 'Нет')
    )

    shop = models.ForeignKey('Shop', verbose_name='От кого', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', verbose_name='Кому', on_delete=models.CASCADE)
    job = models.CharField("Должность", max_length=30)
    yes_or_no = models.CharField("Ответ", blank=True, max_length=30, choices=YES_OR_NO)
    active = models.BooleanField("Активный", blank=True, default=False)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания запроса')

    class Meta:
        verbose_name = 'Запрос на работу'
        verbose_name_plural = 'Запросы на работу'

    def __str__(self):
        return "Запрос: от {} к {}".format(self.shop.shop_name, self.customer.first_name)


class CartProduct(models.Model):
    #Попробывать сделать вывод и изменение статуса товара через эту модель
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзинах'

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return str(self.id)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_CANCELLED = 'is_cancelled'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_CANCELLED, 'Заказ отменен'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=11, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', related_name='cart', on_delete=models.CASCADE,
                             null=True, blank=True)
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='order_shop', blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "Заказ: №{} ".format(self.id)


class OrderProduct(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_CANCELLED = 'is_cancelled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый'),
        (STATUS_IN_PROGRESS, 'В обработке'),
        (STATUS_CANCELLED, 'Отменен'),
        (STATUS_COMPLETED, 'Выполнен')
    )
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )

    class Meta:
        verbose_name = 'Товар (для заказа)'
        verbose_name_plural = 'Товары (для заказа)'

    def __str__(self):
        return "Заказ №{}, Товар: {} (для заказа)".format(self.order.id, self.product.title)


class OrderForShop(models.Model):
    STATUS_CHOICES = (
        ('STATUS_NEW', 'Новый заказ'),
        ('STATUS_IN_PROGRESS', 'Заказ в обработке'),
        ('STATUS_CANCELLED', 'Заказ отменен'),
        ('STATUS_COMPLETED', 'Заказ выполнен')
    )

    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE, blank=True)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', on_delete=models.CASCADE, blank=True)
    product = models.ManyToManyField(OrderProduct, verbose_name='Товары', blank=True)
    total_products = models.PositiveIntegerField(default=0, blank=True)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default='STATUS_NEW'
    )

    class Meta:
        verbose_name = 'Заказ (для продавца)'
        verbose_name_plural = 'Заказы (для продавца)'

    def __str__(self):
        return "Заказ №{}: {} (для продавца)".format(self.order.id, self.shop.shop_name)


class Complaints(models.Model):

    TYPE_OF_REQUEST = (
        ('QUALITY_OF_SERVICE', 'Качество обслуживания'),
        ('LONG_SERVICE_LIFE', 'Долгое обслуживание'),
        ('DEFECTIVE_PRODUCT', 'Бракованный товар'),
        ('LATE_DELIVERY', 'Несвоевременная доставка'),
        ('NON_CORRECT_PRODUCT_DESCRIPTION', 'Неккоректное описание товара'),
        ('THE_QUALITY_OF_THE_PRODUCT', 'Качество товара')
    )

    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='complaint_order', on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, verbose_name='Пользователь', related_name='related_complaints',
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, verbose_name='Телефон')
    type_of_request = models.CharField(
        max_length=100,
        verbose_name='Тип обращения',
        choices=TYPE_OF_REQUEST
    )
    comment = models.TextField(verbose_name='Комментарий к жалобе')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'

    def __str__(self):
        return "Жалоба: №{} ".format(self.id)


class SupportService(models.Model):

    TYPE_OF_REQUEST = (
        ('QUALITY_OF_SERVICE', 'Качество обслуживания'),
        ('LONG_SERVICE_LIFE', 'Долгое обслуживание'),
        ('DEFECTIVE_PRODUCT', 'Бракованный товар'),
        ('LATE_DELIVERY', 'Несвоевременная доставка'),
        ('NON_CORRECT_PRODUCT_DESCRIPTION', 'Неккоректное описание товара'),
        ('THE_QUALITY_OF_THE_PRODUCT', 'Качество товара')
    )

    user = models.ForeignKey(Customer, verbose_name='Пользователь', related_name='related_support',
                             on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, verbose_name='Email')
    type_of_request = models.CharField(
        max_length=100,
        verbose_name='Тип обращения',
        choices=TYPE_OF_REQUEST
    )
    comment = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Служба поддержки'
        verbose_name_plural = 'Служба поддержки'

    def __str__(self):
        return "Жалоба: №{} ".format(self.id)


class AboutDina(models.Model):

    content = models.TextField(verbose_name='Контент')

    class Meta:
        verbose_name = 'Страница о Дине'
        verbose_name_plural = 'Страница о Дине'

    def __str__(self):
        return self.content



class AboutUs(models.Model):

    content = models.TextField(verbose_name='Контент')

    class Meta:
        verbose_name = 'Страница о нас'
        verbose_name_plural = 'Страница о нас'

    def __str__(self):
        return self.content


class News(models.Model):

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_blog',
                                 on_delete=models.CASCADE)
    title = models.CharField(db_index=True, max_length=100, verbose_name='Наименование')
    image = models.ImageField(verbose_name='Фото', upload_to='news/img/')
    slug = models.SlugField(db_index=True)
    content = models.TextField(verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})


class RequestFromShop(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_CANCELLED = 'is_cancelled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заявка'),
        (STATUS_IN_PROGRESS, 'Заявка в обработке'),
        (STATUS_CANCELLED, 'Заявка отменен'),
        (STATUS_COMPLETED, 'Заявка выполнен')
    )
    customer = models.ForeignKey(Customer, verbose_name='Пользователь', related_name='related_req_f_sh',
                                 on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    shop_name = models.CharField(db_index=True, max_length=20, verbose_name='Название магазина')
    shop_address = models.CharField(max_length=255, verbose_name='Адрес магазина')
    shop_email = models.EmailField(max_length=254, verbose_name='Email магазина')
    shop_phone = models.CharField(max_length=15, verbose_name='Номер телефона магазина')
    category = models.ManyToManyField('ParentCategory', verbose_name='Категории магазина', blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заявки',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )

    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')

    class Meta:
        verbose_name = 'Заявка на регистрацию'
        verbose_name_plural = 'Заявки на регистрацию'

    def __str__(self):
        return "Заявка №{} ".format(self.id)


class RequestServiceToShop(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_CANCELLED = 'is_cancelled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новая заявка'),
        (STATUS_IN_PROGRESS, 'Заявка в обработке'),
        (STATUS_CANCELLED, 'Заявка отменена'),
        (STATUS_COMPLETED, 'Заявка выполнена')
    )

    customer = models.ForeignKey(Customer, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', on_delete=models.CASCADE, blank=True)
    service = models.ForeignKey(Product, verbose_name='Услуга', on_delete=models.CASCADE, blank=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=11, verbose_name='Телефон')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')

    class Meta:
        verbose_name = 'Заявка на услугу для магазина'
        verbose_name_plural = 'Заявки на услуги для магазина'

    def __str__(self):
        return "Заявка на услугу: {}".format(self.customer.first_name)
