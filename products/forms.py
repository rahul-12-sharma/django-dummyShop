from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class SimpleUserCreationForm(UserCreationForm):
    username = forms.CharField(
        min_length=5,
        max_length=10,
        help_text="5–10 characters only",
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Type your password (can be easy)"
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text="Repeat password for verification"
    )

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Try another one.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2
