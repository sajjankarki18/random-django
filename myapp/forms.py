from typing import Any
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs).__init__(self, *args, **kwargs)    
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder': 'Enter your username'})
        self.fields['password1'].widget.attrs.update({'class':'form-control', 'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update({'class':'form-control', 'placeholder': 'confirm password'})