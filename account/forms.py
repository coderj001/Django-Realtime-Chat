from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255, help_text="Required. Add valid email address")

    class Meta:
        model = Account
        fields = (
            'email',
            'username',
            'password1',
            'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(
            'Username "%s" is already in use.' % username)