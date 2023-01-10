from django import forms
from django.forms import TextInput
from .models import *

User = get_user_model()


class SearchUnivForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hostel'].label = 'Общежитие:'
        self.fields['governmental'].label = 'Государственный:'

    hostel = forms.BooleanField(required=False)
    governmental = forms.BooleanField(required=False)
