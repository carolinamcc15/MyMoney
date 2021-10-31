from django import forms
from django.contrib.auth.models import AbstractUser
import re

class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        required = True, 
        max_length= 15,
        widget=forms.TextInput())

    email = forms.EmailField(
        required = True)

    password = forms.CharField(
        required = True,
        widget = forms.PasswordInput())

    confirmpassword = forms.CharField(
        required = True,
        widget = forms.PasswordInput())

    class Meta:
        model = AbstractUser
        fields = [
            'username',
            'email',
            'password'
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) != 5:
            raise forms.ValidationError("Nombre de usuario malo")
        return username
        # email = self.cleaned_data.get("email")
        # password = self.cleaned_data.get("password")
        # confirmpassword = self.cleaned_data.get("confirmpassword")
        
