from django import forms

from frontend.general_site_settings import BaseForm


class LoginForm(BaseForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)