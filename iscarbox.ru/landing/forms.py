from django import forms
from .models import *


class ContactsFrom(forms.ModelForm):

    class Meta(object):
        model = ContactForm
        fields = ('__all__')
        exclude = ["created_at"]
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'phone_number': forms.TextInput(attrs={"class": "form-control"}),
            'message': forms.Textarea(attrs={"class": "form-control"})
        }
