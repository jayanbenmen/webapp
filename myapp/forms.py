from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import calendar
from datetime import datetime


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

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget = forms.PasswordInput(), label = "Old Password:")
    new_password1 = forms.CharField(widget = forms.PasswordInput(), label = "New Password:")
    new_password2 = forms.CharField(widget = forms.PasswordInput(), label = "Confirm New Password:")

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class CalendarForm(forms.Form):
    month = forms.ChoiceField(choices=[(str(i), calendar.month_name[i]) for i in range(1, 13)], initial=str(datetime.now().month), label='Month')

class DateForm(forms.Form):
    day_date = forms.DateField(widget = forms.DateInput(attrs = {'type': 'date'}), label = "Date")

