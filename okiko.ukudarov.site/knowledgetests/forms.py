from django import forms
from django.forms import TextInput
from .models import *

User = get_user_model()


class TestAnswerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_test_question_id'].label = 'Вопрос:'
        self.fields['user_test_answer_id'].label = 'Ответ:'

    user_test_question_id = forms.DecimalField(required=False, widget=TextInput(attrs={'readonly':'readonly'}))
    user_test_answer_id = forms.DecimalField(required=False, widget=TextInput(attrs={'readonly':'readonly'}))
