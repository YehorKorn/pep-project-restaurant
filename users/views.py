from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from users.forms import UserLoginForm, UserForm


class UserLoginView(views.LoginView):
    form_class = UserLoginForm
    success_url = reverse_lazy("index")


class UserLogoutView(views.LogoutView):
    ...


class UserCreateView(generic.CreateView):
    model = get_user_model()
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:login")


class UserUpdateView(generic.UpdateView):
    model = get_user_model()
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("index")
