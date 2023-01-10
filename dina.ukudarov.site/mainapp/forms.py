from django import forms
from django.forms import TextInput
from specs.models import ProductFeatures
from .models import *

User = get_user_model()


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином "{username} не найден в системе')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль")
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Электронная почта'

    def clean_email(self):
        email = self.cleaned_data['email']
        # domain = email.split('.')[-1]
        # if domain in ['com', 'net']:
        #     raise forms.ValidationError(
        #         f'Регистрация для домена {domain} невозможна'
        #     )
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f'Данный почтовый адрес уже зарегистрирован в системе'
            )
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                f'Имя {username} занято'
            )
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    SEX = (
        ('MEN', 'Мужчина'),
        ('WOMEN', 'Женщина'),
    )

    sex = forms.RadioSelect(choices=SEX)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone = forms.CharField(required=False, widget=TextInput(attrs={'class':'form-control',
                                                                    'type':"tel",
                                                                    'autocomplete': 'off',
                                                                    'pattern':"{1}[0-9]{11}",
                                                                    'title':'Введите номер телефона',
                                                                    'placeholder':"87071231234"}))
    address = forms.CharField(required=False, widget=TextInput(attrs={'class':'form-control',
                                                                      'autocomplete': 'off',
                                                                      'title':'Введите ваш адрес',
                                                                      'placeholder':"Улица, дом, квартира"}))
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя:'
        self.fields['last_name'].label = 'Фамилия:'
        self.fields['sex'].label = 'Пол:'
        self.fields['phone'].label = 'Номер телефона:'
        self.fields['address'].label = 'Адрес:'
        self.fields['email'].label = 'Электронная почта:'

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'phone', 'email', 'sex']


class AddProductForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.filter(service=False))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = 'Категория:'
        self.fields['title'].label = 'Название:'
        self.fields['image'].label = 'Фото №1:'
        self.fields['image_2'].label = 'Фото №2:'
        self.fields['image_3'].label = 'Фото №3:'
        self.fields['image_4'].label = 'Фото №4:'
        self.fields['description'].label = 'Описание:'
        self.fields['price'].label = 'Цена:'


    class Meta:
        model = Product
        fields = ['category', 'title', 'image', 'image_2', 'image_3', 'image_4', 'description', 'price']


class AddServiceForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.filter(service=True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = 'Категория:'
        self.fields['title'].label = 'Название:'
        self.fields['image'].label = 'Фото №1:'
        self.fields['image_2'].label = 'Фото №2:'
        self.fields['image_3'].label = 'Фото №3:'
        self.fields['image_4'].label = 'Фото №4:'
        self.fields['description'].label = 'Описание:'
        self.fields['price'].label = 'Цена:'
        self.fields['contractual_price'].label = 'Договорная цена?'


    class Meta:
        model = Product
        fields = ['category', 'title', 'image', 'image_2', 'image_3', 'image_4', 'description', 'price', 'contractual_price']


class EditProductForm(forms.ModelForm):

    image = forms.ImageField(required=False)
    image_2 = forms.ImageField(required=False)
    image_3 = forms.ImageField(required=False)
    image_4 = forms.ImageField(required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)
    price = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'Фото №1:'
        self.fields['image_2'].label = 'Фото №2:'
        self.fields['image_3'].label = 'Фото №3:'
        self.fields['image_4'].label = 'Фото №4:'
        self.fields['status_product'].label = 'Статус товара:'
        self.fields['description'].label = 'Описание:'
        self.fields['price'].label = 'Цена:'

    class Meta:
        model = Product
        fields = ['image', 'image_2', 'image_3', 'image_4', 'status_product', 'description', 'price']


class EditServiceForm(forms.ModelForm):

    image = forms.ImageField(required=False)
    image_2 = forms.ImageField(required=False)
    image_3 = forms.ImageField(required=False)
    image_4 = forms.ImageField(required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)
    price = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'Фото №1:'
        self.fields['image_2'].label = 'Фото №2:'
        self.fields['image_3'].label = 'Фото №3:'
        self.fields['image_4'].label = 'Фото №4:'
        self.fields['description'].label = 'Описание:'
        self.fields['price'].label = 'Цена:'
        self.fields['contractual_price'].label = 'Договорная цена?'


    class Meta:
        model = Product
        fields = ['image', 'image_2', 'image_3', 'image_4', 'description', 'price', 'contractual_price']


class CreateShopForm(forms.ModelForm):

    shop_phone = forms.CharField(required=True, widget=TextInput(attrs={'class':'form-control',
                                                                        'type':"tel",
                                                                        'autocomplete': 'off',
                                                                        'pattern':"{1}[0-9]{11}",
                                                                        'title':'Введите номер телефона',
                                                                        'placeholder':"87071231234"}))
    shop_address = forms.CharField(required=True, widget=TextInput(attrs={'class':'form-control',
                                                                          'autocomplete': 'off',
                                                                          'title':'Введите ваш адрес',
                                                                          'placeholder':"Главное здание, второй этаж, 32 бутик"}))
    shop_email = forms.EmailField(required=True)

    category = forms.ModelMultipleChoiceField(
        queryset=ParentCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shop_name'].label = 'Название магазина:'
        self.fields['category'].label = 'Категория магазина:'
        self.fields['shop_image'].label = 'Логотип магазина:'
        self.fields['shop_address'].label = 'Адрес магазина:'
        self.fields['shop_email'].label = 'Email магазина:'
        self.fields['shop_phone'].label = 'Номер телефона магазина:'

    def clean_shop_name(self):
        shop_name = self.cleaned_data['shop_name']

        if self.cleaned_data['shop_name'] != "":
            shop_name = self.cleaned_data['shop_name']
            if Shop.objects.filter(shop_name=shop_name).exists():
                raise forms.ValidationError(
                    f'Данное название магазина уже зарегистрирован в системе'
                )
            return shop_name
        return shop_name

    class Meta:
        model = Shop
        fields = ['shop_name', 'category', 'shop_image', 'shop_address', 'shop_email', 'shop_phone', 'instagram', 'vk', 'facebook']


class SearchUserForm(forms.Form):
    JOB = (
        ('Продавец', 'Продавец'),
        ('Ремонтник', 'Ремонтник'),
        ('Бухгалтер', 'Бухгалтер')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Ник пользователя:'
        self.fields['job'].label = 'Должность пользователя:'

    q = forms.CharField(label='Ник пользователя', max_length=150)
    job = forms.ChoiceField(required=True, choices=JOB)


class AnswerRequestToWorkForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['yes_or_no'].label = ''

    class Meta:
        model = RequestToWork
        fields = ['yes_or_no']


class ComplaintsForm(forms.ModelForm):
    phone = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                   'type': "tel",
                                                                   'autocomplete': 'off',
                                                                   'pattern': "{1}[0-9]{11}",
                                                                   'title': 'Введите номер телефона',
                                                                   'placeholder': "87071231234"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].label = 'Выберите заказ'
        self.fields['phone'].label = 'Введите номер телефона'
        self.fields['type_of_request'].label = 'Выберите тип обращения'
        self.fields['comment'].label = 'Оставьте комментарий к заказу'

    class Meta:
        model = Complaints
        fields = ['order', 'phone', 'type_of_request', 'comment']


class ShopDetailUpdateForm(forms.ModelForm):

    shop_phone = forms.CharField(required=False, widget=TextInput(attrs={'class':'form-control',
                                                                         'type':"tel",
                                                                         'autocomplete': 'off',
                                                                         'pattern':"[+][7]{1}[0-9]{10}",
                                                                         'title':'Введите номер телефона',
                                                                         'placeholder':"+77071231234"}))

    whatsapp = forms.CharField(required=False, widget=TextInput(attrs={'class':'form-control',
                                                                         'type':"tel",
                                                                         'autocomplete': 'off',
                                                                         'pattern':"[+][7]{1}[0-9]{10}",
                                                                         'title':'Введите номер телефона',
                                                                         'placeholder':"+77071231234"}))

    description = forms.CharField(required=False, widget=forms.Textarea)
    shop_email = forms.EmailField(required=False)

    category = forms.ModelMultipleChoiceField(
        required=False,
        queryset=ParentCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = 'Категория магазина:'
        self.fields['description'].label = 'Описание магазина:'
        self.fields['shop_image'].label = 'Логотип магазина:'
        self.fields['shop_email'].label = 'Email магазина:'
        self.fields['shop_phone'].label = 'Номер телефона магазина:'

    class Meta:
        model = Shop
        fields = ['category', 'description', 'shop_image', 'shop_email', 'shop_phone', 'instagram', 'vk', 'facebook', 'whatsapp', 'telegram']


class SupportServiceForm(forms.ModelForm):

    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Введите Email'
        self.fields['type_of_request'].label = 'Выберите тип обращения'
        self.fields['comment'].label = 'Сообщение'

    class Meta:
        model = SupportService
        fields = ['email', 'type_of_request', 'comment']


class ReviewsForm(forms.ModelForm):

    rating = forms.DecimalField(min_value=1, max_value=5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].label = 'Ваш отзыв'

    class Meta:
        model = Reviews
        fields = ['rating', 'comment']


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )


class RequestFromShopForm(forms.ModelForm):
    phone = forms.CharField(required=True, widget=TextInput(attrs={'class':'form-control',
                                                                         'type':"tel",
                                                                         'autocomplete': 'off',
                                                                         'pattern':"[+][7]{1}[0-9]{10}",
                                                                         'title':'Введите номер телефона',
                                                                         'placeholder':"+77071231234"}))
    shop_phone = forms.CharField(required=True, widget=TextInput(attrs={'class':'form-control',
                                                                         'type':"tel",
                                                                         'autocomplete': 'off',
                                                                         'pattern':"[+][7]{1}[0-9]{10}",
                                                                         'title':'Введите номер телефона',
                                                                         'placeholder':"+77071231234"}))
    shop_address = forms.CharField(required=True, widget=TextInput(attrs={'class':'form-control',
                                                                          'autocomplete': 'off',
                                                                          'title':'Введите ваш адрес',
                                                                          'placeholder':"Главное здание, второй этаж, 32 бутик"}))
    shop_email = forms.EmailField(required=True)

    category = forms.ModelMultipleChoiceField(
        queryset=ParentCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = 'Категория магазина:'
        self.fields['shop_email'].label = 'Email магазина:'
        self.fields['shop_phone'].label = 'Номер телефона магазина:'
        self.fields['shop_address'].label = 'Местонахождения магазина:'
        self.fields['phone'].label = 'Номер телефона:'

    def clean_shop_name(self):
        shop_name = self.cleaned_data['shop_name']

        if self.cleaned_data['shop_name'] != "":
            shop_name = self.cleaned_data['shop_name']
            if Shop.objects.filter(shop_name=shop_name).exists():
                raise forms.ValidationError(
                    f'Данное название магазина уже зарегистрирован в системе'
                )
            return shop_name
        return shop_name

    class Meta:
        model = RequestFromShop
        fields = (
            'first_name', 'last_name', 'phone', 'shop_name', 'shop_address', 'shop_email', 'shop_phone', 'category', 'comment'
        )



class RequestServiceToShopForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = RequestServiceToShop
        fields = (
            'first_name', 'phone', 'comment'
        )
