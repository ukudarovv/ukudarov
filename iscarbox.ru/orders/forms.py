from django import forms
from .models import Order, Region, City, PaymentMethod


class OrderCreateForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Выберите регион", widget=forms.Select(attrs={'class': 'form-control mb-4'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Выберите город", widget=forms.Select(attrs={'class': 'form-control mb-4'}))
    payment_method = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), empty_label="Выберите способ оплаты", widget=forms.RadioSelect(attrs={'class': 'form-check-input with-gap'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone', 'region', 'city', 'postal_code', 'street', 'house', 'apartment', 'message', 'payment_method')

        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control mb-4", 'placeholder': 'youremail@mail.ru'}),
            'phone': forms.TextInput(attrs={"class": "form-control mb-4", 'placeholder': '+71234567890'}),
            'street': forms.TextInput(attrs={"class": "form-control mb-4", 'placeholder': 'Пушкина 1'}),
            'house': forms.TextInput(attrs={"class": "form-control mb-4", 'placeholder': '1'}),
            'apartment': forms.TextInput(attrs={"class": "form-control mb-4", 'placeholder': '1'}),
            'postal_code': forms.TextInput(attrs={"class": "form-control mb-4", 'placeholder': '010000'}),
            'message': forms.Textarea(attrs={"class": "form-control mb-4", }),
        }


class ProductQuantityUpdate(forms.Form):
    id = forms.IntegerField()
    product = forms.IntegerField()
    quantity = forms.IntegerField()


class ProductIsActiveUpdate(forms.Form):
    id = forms.IntegerField()
    product = forms.IntegerField()
    product_material = forms.IntegerField()
    product_thread = forms.IntegerField()
    product_border = forms.IntegerField()
    product_accessory = forms.IntegerField()


class ProductAddBasket(forms.Form):
    id = forms.IntegerField()
    quantity = forms.IntegerField()
    product = forms.IntegerField()
    product_material = forms.IntegerField()
    product_thread = forms.IntegerField()
    product_border = forms.IntegerField()
    product_accessory = forms.IntegerField()
