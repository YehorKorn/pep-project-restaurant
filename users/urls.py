from django.urls import path, include

from users.views import (
    UserCreateView,
    UserLoginView,
    UserLogoutView,
    UserUpdateView,
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path('registration/', UserCreateView.as_view(), name="registration"),
    path('update-data/<int:pk>/', UserUpdateView.as_view(), name="update-data"),
]

app_name = "users"
