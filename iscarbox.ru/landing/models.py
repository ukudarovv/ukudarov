from django.db import models



class SEO(models.Model):
    description = models.TextField(blank=True, verbose_name='Description')
    keywords = models.TextField(blank=True, verbose_name='Keywords')
    site_icon = models.ImageField("Иконка сайта", upload_to="image/logo/", blank=True, null=True)
    google_analytics = models.TextField(blank=True, null=True, verbose_name='Google Analytics')


    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "SEO сайта"
        verbose_name_plural = "SEO сайта"


class Carousel(models.Model):
    photo = models.ImageField(upload_to='carousel/photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Контент')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'


class Contacts(models.Model):
    numder_phone = models.CharField(max_length=20,verbose_name='Номер телефона')
    instagram_name = models.CharField(max_length=200, verbose_name='Название инстаграмм аккаунта')
    instagram_url = models.URLField(max_length=200, verbose_name='Ссылка на инстаграмм')
    email = models.EmailField(max_length=254, verbose_name='Email')
    about = models.TextField(blank=True, verbose_name='О нас')

    def __str__(self):
        return self.instagram_name

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


class ContactForm(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    phone_number = models.CharField(max_length=25, verbose_name='Номер телефона')
    message = models.TextField(max_length=500, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Контактная форма'
        verbose_name_plural = 'Контактная форма'


class Develiry(models.Model):
    content = models.TextField(blank=True, verbose_name='Контент')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Страница доставки'
        verbose_name_plural = 'Страница доставки'


class Paymentmethods(models.Model):
    content = models.TextField(blank=True, verbose_name='Контент')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Страница cпособы оплаты'
        verbose_name_plural = 'Страница cпособы оплаты'


class Purchasereturns(models.Model):
    content = models.TextField(blank=True, verbose_name='Контент')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Страница возврата товара'
        verbose_name_plural = 'Страница возврата товара'


class Sitepolicy(models.Model):
    content = models.TextField(blank=True, verbose_name='Контент')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Страница политики сайта'
        verbose_name_plural = 'Страница политики сайта'
