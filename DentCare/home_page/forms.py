# forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    phone_number = forms.CharField(max_length=10, label='Phone Number', min_length=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password', 'confirm_password']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
