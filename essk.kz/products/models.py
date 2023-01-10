from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class CategoryProduct(models.Model):
    title = models.CharField(max_length=64, verbose_name='Категория', unique=True)

    class Meta:
        verbose_name = 'Вид товара'
        verbose_name_plural = '8) Виды товаров'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_p_detail', kwargs={'id': self.id})


class Category(MPTTModel):
    title = models.CharField(max_length=64, verbose_name='Категория', unique=False)
    parent = TreeForeignKey('self', verbose_name='Родитель', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    category_all = models.ManyToManyField('self', verbose_name='Категории', related_name='related_category_cat', blank=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = '1) Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'id': self.id})


class Brand(models.Model):
    image = models.ImageField(upload_to='brands/', verbose_name='Изображение', blank=True)
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Доступен', default=False)

    class Meta:
        verbose_name = 'Фирма'
        verbose_name_plural = '2) Фирмы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'id': self.id})


class Product(models.Model):
    link = models.URLField(verbose_name='Ссылка', blank=True)
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Дата создания', blank=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, blank=True, null=True)
    category_p = models.ManyToManyField(CategoryProduct, verbose_name='Вид товара', related_name='related_category_p', blank=True)
    category_all = models.ManyToManyField(Category, verbose_name='Категории', related_name='related_category_all', blank=True)
    brand = models.ForeignKey(Brand, verbose_name='Фирма', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True)
    article = models.CharField(max_length=50, verbose_name='Артикул', blank=True, null=True)
    code = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Код товара', blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена', blank=True, null=True)
    new_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Новая цена', blank=True, null=True)
    discount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Скидка (в процентах)', blank=True, null=True)
    m_description = models.TextField(verbose_name='Небольшое описание', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Доступен', default=False)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = '3) Товары'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'id': self.id})


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Изображение', blank=True)

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = '4) Фото товаров'

    def __str__(self):
        return self.product.title


class CategoryFeature(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать в фильтрации', default=False)

    class Meta:
        verbose_name = 'Категория характеристики'
        verbose_name_plural = '5.1) Категории характеристики'

    def __str__(self):
        return self.title


class FeatureValue(models.Model):
    category_feature = models.ForeignKey(CategoryFeature, verbose_name='Категория характеристики', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать в фильтрации', default=False)

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = '5.2) Значения характеристик'

    def __str__(self):
        return self.title


class ValueKey(models.Model):
    feature_value = models.ForeignKey(FeatureValue, verbose_name='Значение характеристики', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='Наименование', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать в фильтрации', default=False)

    class Meta:
        verbose_name = 'Ключ к значению характеристики'
        verbose_name_plural = '5.3) Ключи к значениям характеристик'

    def __str__(self):
        return self.title


class ProductFeatures(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, blank=True, null=True)
    category_feature = models.ForeignKey(CategoryFeature, verbose_name='Категория характеристики', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Характеристики товара'
        verbose_name_plural = '6.1) Характеристики товаров'

    def __str__(self):
        return "Товар {}: {} - {}".format(self.product.title)


class ProductFeatureValue(models.Model):
    product_features = models.ForeignKey(ProductFeatures, verbose_name='Характеристики товара', on_delete=models.SET_NULL, blank=True, null=True)
    feature_value = models.ForeignKey(FeatureValue, verbose_name='Значение', on_delete=models.SET_NULL, blank=True, null=True)
    value_key = models.ForeignKey(ValueKey, verbose_name='Ключ к значению', on_delete=models.SET_NULL, blank=True, null=True)


    class Meta:
        verbose_name = 'Значение и ключ к товару'
        verbose_name_plural = '6.2) Значения и ключи к товару'

    def __str__(self):
        return "Товар {}: {} - {}".format(self.product_features.product.title, self.feature_value.title, self.value_key.title)


class ProductFeedback(models.Model):
    for_anonymous_user = models.BooleanField(verbose_name='Анонимный пользователь', default=False)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=200, verbose_name='Имя', blank=True)
    email = models.EmailField(verbose_name='Эл. почта', null=True)
    text = models.TextField(verbose_name='Текст', null=True, blank=True)
    point = models.PositiveIntegerField(verbose_name='Оценка', default=0)


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = '7) Отзывы'

    def __str__(self):
        return self.product.title
