import pytest as pytest
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadhandler import MemoryFileUploadHandler
from django.test import TestCase, TransactionTestCase, override_settings
from django.urls import reverse

from meal.forms import MealForm
from meal.models import Meal, Cook, Category


class MealListViewTest(TestCase):
    def test_meal_list_view_should_return_200(self):
        response = self.client.get(reverse("meal:menu"))
        self.assertEqual(response.status_code, 200)

    def test_meal_list_view_should_contain_meal_list_in_context(self):
        category = Category.objects.create(name="LUNCH")
        meal = Meal.objects.create(
            name="Pizza",
            description="The pizza from Italia and is very delicious.",
            people=2,
            price=10,
            preparation_time=15,
            image="meal/pizza.jpg",
            category_id=category.id,
            slug="pizza"
        )
        response = self.client.get(reverse("meal:menu"))
        self.assertContains(response, meal)
        self.assertIn("meal_list", response.context)


class MealDetailViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="LUNCH")
        self.meal = Meal.objects.create(
            name="Pizza",
            description="The pizza from Italia and is very delicious.",
            people=2,
            price=10,
            preparation_time=15,
            image="meal/pizza.jpg",
            category_id=category.id,
            slug="pizza"
        )

    def test_meal_detail_view_should_return_200(self):
        response = self.client.get(reverse("meal:meal-detail", args=[self.meal.slug]))
        self.assertEqual(response.status_code, 200)

    def test_meal_detail_view_should_contain_meal_in_context(self):
        response = self.client.get(reverse("meal:meal-detail", args=[self.meal.slug]))
        self.assertContains(response, self.meal)
        self.assertIn("meal", response.context)


class MealUpdateViewTest(TransactionTestCase):
    def setUp(self):
        category = Category.objects.create(name="LUNCH")

        self.meal = Meal.objects.create(
            name="Pizza",
            description="The pizza from Italia and is very delicious.",
            people="2",
            price="10.00",
            preparation_time="15",
            image="meal/pizza.jpg",
            category_id=category.id,
            slug="pizza"
        )

        self.admin_user = get_user_model().objects.create_superuser(username="Adminuser", password="testpassword")
        self.other_user = get_user_model().objects.create_user(username="Otheruser", password="testpassword")

    def test_meal_update_view_should_return_302_for_anonymous_user(self):
        response = self.client.get(reverse("meal:meal-update", args=[self.meal.slug]))
        self.assertEqual(response.status_code, 302)

    def test_meal_update_view_should_return_403_for_is_not_superuser(self):
        self.client.login(username="Otheruser", password="testpassword")
        response = self.client.get(reverse("meal:meal-update", args=[self.meal.slug]))
        self.assertEqual(response.status_code, 403)

    def test_meal_update_view_should_return_200_for_authenticated_superuser(self):
        self.client.login(username="Adminuser", password="testpassword")
        response = self.client.get(reverse("meal:meal-update", args=[self.meal.slug]))
        self.assertEqual(response.status_code, 200)

    @pytest.fixture(scope="session")
    def image_file(tmpdir_factory):
        img = Image.new("RGB", (640, 480))
        fn = tmpdir_factory.mktemp("data").join("img.jpg")
        img.save(str(fn))
        return fn

    def test_upload_image(self, client, image_file, settings, tmpdir):
        settings.MEDIA_ROOT = tmpdir
        with open(image_file, "rb") as fp:
            response = client.post("meal:meal-update", {"image": fp})
        assert response.status_code == 200

    def test_meal_update_view_should_update_meal_for_authenticated_superuser(self):
        self.client.login(username="Adminuser", password="testpassword")

        image_path = "media/test_image.png"

        self.client.handler_class = MemoryFileUploadHandler

        image_file = SimpleUploadedFile(name="meal/test_image.png", content=open(image_path, "rb").read(),
                                        content_type="image/jpeg")

        new_name = "Pizza_updated"
        form_data = {
            "name": new_name,
            "description": self.meal.description,
            "people": "2",
            "price": "10.00",
            "preparation_time": "15",
            "category": str(self.meal.category.id),
            "slug": self.meal.slug,
        }

        # Инициализация формы с обновленным файлом изображения
        form = MealForm(form_data, instance=self.meal, files={"image": image_file})

        response = self.client.post(
            reverse("meal:meal-update", args=[self.meal.slug]),
            data=form.data,
            files=form.files,
        )
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        # self.client.handler_class = ClientHandler
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("meal:meal-detail", args=[self.meal.slug]))
        self.meal.refresh_from_db()
        self.assertEqual(self.meal.name, new_name)

        # Проверка, что файл изображения был обновлен
        self.assertEqual(self.meal.image.name, "meal/test_image.png")
        self.assertEqual(self.meal.image.name, image_file.name)


# class MealCreateViewTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="testpassword")
#
#     def test_meal_create_view_should_return_302_for_anonymous_user(self):
#         response = self.client.get(reverse("meal:create"))
#         self.assertEqual(response.status_code, 302)
#
#     def test_meal_create_view_should_return_200_for_authenticated_user(self):
#         self.client.login(username="testuser", password="testpassword")
#         response = self.client.get(reverse("meal:create"))
#         self.assertEqual(response.status_code, 200)
#
#     def test_meal_create_view_should_redirect_to_login_for_anonymous_user(self):
#         response = self.client.post(reverse("meal:create"), {})
#         self.assertRedirects(response, reverse("login") + "?next=" + reverse("meal:create"))
#
#     def test_meal_create_view_should_create_meal_for_authenticated_user(self):
#         self.client.login(username="testuser", password="testpassword")
#         meal_name = "New Meal"
#         response = self.client.post(reverse("meal:create"), {"name": meal_name})
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(Meal.objects.filter(name=meal_name).exists())
#
#
# class MealDeleteViewTest(TestCase):
#     def setUp(self):
#         self.meal = Meal.objects.create(name="Test Meal")
#         self.user = User.objects.create_user(username="testuser", password="testpassword")
#
#     def test_meal_delete_view_should_return_302_for_anonymous_user(self):
#         response = self.client.get(reverse("meal:delete", args=[self.meal.pk]))
#         self.assertEqual(response.status_code, 302)
#
#     def test_meal_delete_view_should_return_200_for_authenticated_user(self):
#         self.client.login(username="testuser", password="testpassword")
#         response = self.client.get(reverse("meal:delete", args=[self.meal.pk]))
#         self.assertEqual(response.status_code, 200)
#
#     def test_meal_delete_view_should_redirect_to_login_for_anonymous_user(self):
#         response = self.client.post(reverse("meal:delete", args=[self.meal.pk]), {})
#         self.assertRedirects(response, reverse("login") + "?next=" + reverse("meal:delete", args=[self.meal.pk]))
#
#     def test_meal_delete_view_should_delete_meal_for_authenticated_user(self):
#         self.client.login(username="testuser", password="testpassword")
#         response = self.client.post(reverse("meal:delete", args=[self.meal.pk]), {})
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(Meal.objects.filter(pk=self.meal.pk).exists())
#
#
# class CookListViewTest(TestCase):
#     def test_cook_list_view_should_return_200(self):
#         response = self.client.get(reverse("cook:list"))
#         self.assertEqual(response.status_code, 200)
#
#     def test_cook_list_view_should_contain_cook_list_in_context(self):
#         cook = Cook.objects.create(name="Test Cook")
#         response = self.client.get(reverse("cook:list"))
#         self.assertContains(response, cook.name)
#         self.assertIn("cook_list", response.context)