from django import forms
from django.forms import TextInput
from .models import *
from educational_institutions.models import *

User = get_user_model()


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'prompt srch_explore'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'prompt srch_explore'}))

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
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'prompt srch_explore','title':'Логин', 'placeholder':"Логин"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'prompt srch_explore','title':'Подтвердите пароль', 'placeholder':"Подтвердите пароль"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'prompt srch_explore','title':'Пароль', 'placeholder':"Пароль"}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'prompt srch_explore','title':'Электронная почта', 'placeholder':"Электронная почта"}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'prompt srch_explore','title':'Имя', 'placeholder':"Имя"}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'prompt srch_explore','title':'Фамилия', 'placeholder':"Фамилия"}))

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
        if Student.objects.filter(email=email).exists():
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


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=TextInput(attrs={'class':'prompt srch_explore',
                                                                        'autocomplete': 'off',
                                                                        'title':'Имя',
                                                                        'placeholder':"Имя"}))
    last_name = forms.CharField(required=False, widget=TextInput(attrs={'class':'prompt srch_explore',
                                                                        'autocomplete': 'off',
                                                                        'title':'Фамилия',
                                                                        'placeholder':"Фамилия"}))
    iin = forms.CharField(required=False, widget=TextInput(attrs={'class':'prompt srch_explore',
                                                                  'autocomplete': 'off',
                                                                  'title':'ИИН',
                                                                  'placeholder':"ИИН"}))

    city = forms.ModelChoiceField(required=False, queryset=City.objects.all(), widget=forms.Select(attrs={'class':'ui fluid search selection dropdown focus mt-30 cntry152',
                                                                                      'autocomplete': 'off',
                                                                                      'title':'Регион',
                                                                                      'placeholder':"Регион"}))

    residence_address = forms.CharField(required=False, widget=TextInput(attrs={'class':'prompt srch_explore',
                                                                              'autocomplete': 'off',
                                                                              'title':'Адрес прописки',
                                                                              'placeholder':"Адрес прописки"}))

    residential_address = forms.CharField(required=False, widget=TextInput(attrs={'class':'prompt srch_explore',
                                                                              'autocomplete': 'off',
                                                                              'title':'Адрес проживания',
                                                                              'placeholder':"Адрес проживания"}))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'prompt srch_explore',
                                                                            'placeholder':"Email"}))

    phone = forms.CharField(required=False, widget=TextInput(attrs={'class':'prompt srch_explore',
                                                                    'type':"tel",
                                                                    'autocomplete': 'off',
                                                                    'title':'Введите номер телефона',
                                                                    'placeholder':"87071231234"}))

    birth_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class':'prompt srch_explore',
                                                                                'type': 'date',
                                                                                'title':'Дата рождения'}))

    core_competence = forms.CharField(required=False, widget=TextInput(attrs={'class':'prompt srch_explore',
                                                                              'autocomplete': 'off',
                                                                              'title':'Основная компетенция',
                                                                              'placeholder':"Основная компетенция"}))

    about = forms.CharField(required=False, widget=forms.Textarea(attrs={ 'title':'Биография',
                                                                          'placeholder':"О вас"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'profile_picture', 'iin', 'city', 'residence_address', 'residential_address', 'email', 'phone', 'birth_date', 'core_competence', 'about']


class EditAdminProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=TextInput(attrs={'class':'prompt srch_explore',
                                                                        'autocomplete': 'off',
                                                                        'title':'Имя'}))
    last_name = forms.CharField(required=False)
    phone = forms.CharField(required=False, widget=TextInput(attrs={'class':'prompt srch_explore',
                                                                    'type':"tel",
                                                                    'autocomplete': 'off',
                                                                    'pattern':"{1}[0-9]{11}",
                                                                    'title':'Введите номер телефона',
                                                                    'placeholder':"87071231234"}))
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = UniversityAdministrator
        fields = ['first_name', 'last_name', 'email', 'phone']


class AddDocumentForm(forms.ModelForm):
    document_category = forms.ModelChoiceField(required=False, queryset=DocumentCategory.objects.all(), widget=forms.Select(attrs={'class':'ui fluid search selection dropdown focus mt-30 cntry152',
                                                                                                                                  'autocomplete': 'off',
                                                                                                                                  'title':'Категория документа',
                                                                                                                                  'placeholder':"Категория документа"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = StudentDocument
        fields = ['document_category', 'document']


class EditUnivDetailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = University
        fields = ['logo']


class EditUnivContactlForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = UniversityContact
        fields = ['website', 'email', 'phone', 'location']
