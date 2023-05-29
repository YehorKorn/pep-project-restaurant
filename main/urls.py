from django.urls import path, include

from main.views import UserCreateView

urlpatterns = [
    # path('registration/', UserCreateView.as_view(), name="registration"),
    # path('login/', login_view, name="login"),
]

app_name = "main"
