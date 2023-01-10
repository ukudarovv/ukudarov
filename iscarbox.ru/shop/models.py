from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Название товара')
    slug = models.SlugField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена товара', help_text="Цена в рублях")
    price_old = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Старая цена товара', help_text="Цена в рублях")
    image = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Фото товара', blank=True, default='default/img_p.png')
    available = models.BooleanField(default=True, verbose_name='Доступный?')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                        args=[self.id, self.slug])

    class Meta:
        ordering = ['created']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class ProductMaterialColor(models.Model):
    color_title = models.CharField(max_length=150, verbose_name='Название цвета')
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Товар')
    color_img = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Фото товара', blank=True, default='default/img_p.png')
    product_img = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Фото товара', blank=True, default='default/img_p.png')
    available = models.BooleanField(default=True, verbose_name='Доступный?')

    def model_name(self):
        return 'Цвет материала'

    def __str__(self):
        return self.color_title

    class Meta:
        verbose_name = 'Цвет материала товара'
        verbose_name_plural = 'Цвета материала товара'


class ProductThreadColor(models.Model):
    color_title = models.CharField(max_length=150, verbose_name='Название цвета')
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Товар')
    color_img = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Фото товара', blank=True, default='default/img_p.png')
    product_img = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Фото товара', blank=True, default='default/img_p.png')
    available = models.BooleanField(default=True, verbose_name='Доступный?')

    def model_name(self):
        return 'Цвет нити'

    def __str__(self):
        return self.color_title

    class Meta:
        verbose_name = 'Цвет нити товара'
        verbose_name_plural = 'Цвета нити товара'


class ProductBorderColor(models.Model):
    color_title = models.CharField(max_length=150, verbose_name='Название цвета')
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Товар')
    color_img = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Фото товара', blank=True, default='default/img_p.png')
    product_img = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Фото товара', blank=True, default='default/img_p.png')
    available = models.BooleanField(default=True, verbose_name='Доступный?')

    def model_name(self):
        return 'Цвет окантовки'

    def __str__(self):
        return self.color_title

    class Meta:
        verbose_name = 'Цвет окантовки товара'
        verbose_name_plural = 'Цвета окантовки товара'


class CategoryProductAccessory(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Название категории для аксессуара товара')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория для аксессуара товара'
        verbose_name_plural = 'Категории для аксессуара товара'


class ProductAccessory(models.Model):
    accessory_title = models.CharField(max_length=150, verbose_name='Название аксессуара')
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Товар')
    accessory_price = models.IntegerField(verbose_name='Цена')
    accessory_img = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Фото аксессуара', blank=True)
    product_img = models.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Фото аксессуара на товаре', blank=True, default='default/img_p.png')
    category = models.ForeignKey('CategoryProductAccessory', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Категория аксессуара')
    available = models.BooleanField(default=True, verbose_name='Доступный?')

    def model_name(self):
        return 'Аксессуары'

    def __str__(self):
        return self.accessory_title

    class Meta:
        verbose_name = 'Аксессуар товара'
        verbose_name_plural = 'Аксессуары товара'
