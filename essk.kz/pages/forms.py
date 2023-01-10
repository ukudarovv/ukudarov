from django import forms
from django.forms import TextInput
from .models import *
from carts.models import *
from orders.models import *
from users.models import *

User = get_user_model()


class OrderUserForm(forms.ModelForm):

    phone = forms.CharField(required=True, widget=TextInput(attrs={ 'type':"tel",
                                                                    'autocomplete': 'off',
                                                                    'pattern':"{1}[0-9]{14}",
                                                                    'title':'Введите номер телефона',
                                                                    'placeholder':"87071231234"}))

    address = forms.CharField(required=True, widget=TextInput(attrs={ 'autocomplete': 'off',
                                                                      'title':'Введите ваш адрес',
                                                                      'placeholder':"Улица, дом, квартира"}))

    email = forms.EmailField(required=True)

    payment = forms.ModelChoiceField(required=True, queryset=PaymentType.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].label = 'Моб. телефон'

    class Meta:
        model = Order
        fields = (
            'person', 'phone', 'email', 'city', 'address', 'comment', 'payment',
        )


class OrderCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = (
            'title', 'address', 'iin_bin',
        )


class OrderBankCompanyForm(forms.ModelForm):

    class Meta:
        model = CompanyBankDetails
        fields = (
            'bank_title', 'bik', 'iik',
        )


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователь с данным почтовым адресом "{email}" не найден в системе')
        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль")
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone = forms.CharField(required=False, widget=TextInput(attrs={ 'type':"tel",
                                                                    'autocomplete': 'off',
                                                                    'pattern':"{1}[0-9]{14}",
                                                                    'title':'Введите номер телефона',
                                                                    'placeholder':"87071231234"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Электронная почта'
        self.fields['phone'].label = 'Номер телефона'

    def clean_email(self):
        email = self.cleaned_data['email']
        # domain = email.split('.')[-1]
        # if domain in ['com', 'net']:
        #     raise forms.ValidationError(
        #         f'Регистрация для домена {domain} невозможна'
        #     )
        if User.objects.filter(email=email).exists():
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
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'phone']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'


class UserAddressForm(forms.ModelForm):
    street = forms.CharField(required=False, widget=TextInput(attrs={ 'autocomplete': 'off',
                                                                      'title':'Введите ваш адрес',
                                                                      'placeholder':"Улица, дом, квартира"}))
    index = forms.CharField(required=False)

    class Meta:
        model = UserAddress
        fields = ['city', 'street', 'index']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].label = 'Город'
        self.fields['street'].label = 'Улица, дом, квартира'
        self.fields['index'].label = 'Индекс'


class ProductFeedbackForm(forms.ModelForm):

    class Meta:
        model = ProductFeedback
        fields = ['first_name', 'email', 'text', 'point']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
