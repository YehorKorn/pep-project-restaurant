from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
                "placeholder": "Username",
                "class": "form-control",
                "autofocus": True,
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
                "placeholder": "Password",
                "class": "form-control",
                "autocomplete": "current-password",
        }))


class UserForm(UserCreationForm):
    first_name = forms.CharField(
        error_messages={
            "required": "*"
        },
        widget=forms.TextInput(attrs={
            "placeholder": "First name",
            "class": "form-control",
            "autofocus": True,
        }))
    last_name = forms.CharField(
        error_messages={
            "required": "*"
        },
        widget=forms.TextInput(attrs={
            "placeholder": "Last name",
            "class": "form-control",
        }))
    email = forms.CharField(
        error_messages={
            "required": "*",
            "invalid": "*Enter a valid email address: example@example.com",
        },
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "class": "form-control",
        }))
    username = forms.CharField(
        error_messages={
            "required": "*",
            "unique": "*User with that username already exists."
        },
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "form-control",
        }))
    password1 = forms.CharField(
        error_messages={
            "required": "*",
        },
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "form-control",
        }))
    password2 = forms.CharField(
        error_messages={
            "required": "*",
        },
        widget=forms.PasswordInput(attrs={
            "placeholder": "Сonfirm password",
            "class": "form-control",
        }))

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        )
