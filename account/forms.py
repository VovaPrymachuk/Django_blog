from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']