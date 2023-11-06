from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин:',
                               widget=forms.TextInput(attrs={'class': 'form-control item', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(
        attrs={'class': 'form-control item', 'placeholder': 'Пароль'}))
