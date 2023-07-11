from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from users.forms import UserLoginForm, UserForm

URL_LOGIN = reverse("users:login")
URL_REGISTRATION = reverse("users:registration")
URL_UPDATE_DATA = "users:update-data"
URL_INDEX = reverse("index")


class UserLoginViewTest(TestCase):
    def test_login_view_success_status_code(self):
        response = self.client.get(URL_LOGIN)
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        response = self.client.get(URL_LOGIN)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_view_uses_correct_form(self):
        response = self.client.get(URL_LOGIN)
        self.assertIsInstance(response.context["form"], UserLoginForm)

    def test_login_view_redirects_on_successful_login(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        data = {
            "username": "testuser",
            "password": "testpassword"
        }

        response = self.client.post(URL_LOGIN, data)
        self.assertRedirects(response, URL_INDEX)


class UserCreateViewTest(TestCase):
    def test_registration_view_success_status_code(self):
        response = self.client.get(URL_REGISTRATION)
        self.assertEqual(response.status_code, 200)

    def test_registration_view_uses_correct_template(self):
        response = self.client.get(URL_REGISTRATION)
        self.assertTemplateUsed(response, "users/user_form.html")

    def test_registration_view_uses_correct_form(self):
        response = self.client.get(URL_REGISTRATION)
        self.assertIsInstance(response.context["form"], UserForm)

    def test_registration_view_redirects_on_successful_creation(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
        }
        response = self.client.post(URL_REGISTRATION, form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.email, form_data["email"])
        self.assertRedirects(response, URL_LOGIN)


class UserUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )

    def test_update_view_success_status_code(self):
        url = reverse(URL_UPDATE_DATA, args=[self.user.pk])
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        url = reverse(URL_UPDATE_DATA, args=[self.user.pk])
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "users/user_form.html")

    def test_update_view_uses_correct_form(self):
        url = reverse(URL_UPDATE_DATA, args=[self.user.pk])
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(url)
        self.assertIsInstance(response.context["form"], UserForm)

    def test_update_view_redirects_on_successful_update(self):
        form_data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated@example.com",
            "username": "testuser2",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = UserForm(data=form_data, instance=self.user)
        url = reverse(URL_UPDATE_DATA, args=[self.user.pk])

        self.assertTrue(form.is_valid())
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.post(url, form_data)
        self.assertRedirects(response, URL_INDEX)
