from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        min_length = 11,
        max_length = 11,
        required=True,
        label = "ID Number",
        error_messages = {
            'required': 'Please follow the format e.g. 202100111',
        }
    )
    first_name = forms.CharField(
        required=True,
        label = "First Name"
    )
    last_name = forms.CharField(
        required=True,
        label = "Last Name"
    )
    email = forms.EmailField(
        required=True,
        label = "Gbox"
    )
    password1 = forms.CharField(
        widget = forms.PasswordInput,
        min_length = 8,
        required = True,
        label = "Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, min_length=8,
        required=True,
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class AdminCreationForm(UserCreationForm):
    username = forms.CharField(
        min_length = 9,
        max_length = 9,
        required=True,
        label = "User Name",
        error_messages = {
            'required': 'Please follow the format e.g. 202100111',
        }
    )
    first_name = forms.CharField(
        required=True,
        label = "First Name"
    )
    last_name = forms.CharField(
        required=True,
        label = "Last Name"
    )
    email = forms.EmailField(
        required=True,
        label = "Email"
    )
    password1 = forms.CharField(
        widget = forms.PasswordInput,
        min_length = 8,
        required = True,
        label = "Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, min_length=8,
        required=True,
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

