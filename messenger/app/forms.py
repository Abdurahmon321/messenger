from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import UserProfile
from .validators import CustomPasswordValidator
import re


class CustomUserCreationForm(UserCreationForm):
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 is None or len(password1) < 8:
            raise ValidationError(_('Parol kamida 8 ta belgidan iborat bo\'lishi kerak.'))
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')
        if password2 is None or len(password2) < 8 and password2 == password1:
            raise ValidationError(_('Parol kamida 8 ta belgidan iborat bo\'lishi kerak.'))
        return password2

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'address', 'phone_number', 'date_of_birth']