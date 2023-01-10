from django import forms
from django.forms import TextInput
from django.contrib.auth import login, authenticate, get_user_model
from .models import *
from orders.models import *
from users.models import *
from products.models import *
from shops.models import *
from menu.models import *

User = get_user_model()


class AdminLoginForm(forms.ModelForm):

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


class EditPreparedProductForm(forms.ModelForm):

    CHOICES = (
        ('PLUS', 'Прибавить'),
        ('MINUS', 'Отнять'),
    )

    action = forms.RadioSelect(choices=CHOICES, attrs={'required': False})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action'].label = 'Действие'
        self.fields['prepared_qty'].label = 'Количество'

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = PreparedProduct
        fields = ['action', 'product', 'prepared_qty']


class AddPreparedProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = PreparedProduct
        fields = ['product', 'prepared_qty']


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Category
        fields = ['title']


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Product
        fields = ['category', 'title', 'image', 'price']


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['email'].label = 'Электронная почта'

    def clean_email(self):
        email = self.cleaned_data['email']
        # domain = email.split('.')[-1]
        # if domain in ['com', 'net']:
        #     raise forms.ValidationError(
        #         f'Регистрация для домена {domain} невозможна'
        #     )
        if ShopAdministrator.objects.filter(email=email).exists():
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
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name']


class DeliverymanForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Deliveryman
        fields = ['phone']


class EditDeliverymanForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Deliveryman
        fields = ['first_name', 'phone', 'email']


class EditShopContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = ShopBuyer
        fields = ['customer', 'deliveryman', 'title', 'kaspi_name', 'iin_bin', 'address', 'gis_link', 'phone']


class EditShopAdminContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = ShopAdministrator
        fields = ['first_name', 'email', 'phone']


class EditInvoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Invoice
        fields = ['number', 'created_at']


class EditPaymentInvoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = PaymentInvoice
        fields = ['number', 'number_2', 'created_at']


class IngredientCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = IngredientCategory
        fields = ['title']


class IngredientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Ingredient
        fields = ['title', 'category', 'qty', 'unit_of_measurement', 'price', 'cost_price']


class UnderIngredientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = UnderIngredient
        fields = ['ingredient', 'gross', 'cost_price']


class TechCardForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = TechCard
        fields = ['product', 'cost_price']


class TechCardIngredientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = TechCardIngredient
        fields = ['ingredient', 'gross', 'unit_of_measurement', 'cost_price']
