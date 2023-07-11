from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import datetime, timedelta

from reservation.forms import ReservationForm, ReservationSearchForm
from reservation.models import Reservation

URL_RESERVATION_CREATE = reverse("reservation:reservation")
URL_RESERVATION_LIST = reverse("reservation:reservation-list")


class ReservationCreateViewTest(TestCase):
    def setUp(self):
        self.form_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "1234567890",
            "date_time": datetime.now().strftime("%m/%d/%Y %I:%M %p"),
            "number_of_people": 2,
            "special_request": "Special requests",
        }

    def test_reservation_create_view_should_return_200_for_all_users(self):
        response = self.client.get(URL_RESERVATION_CREATE)
        self.assertEqual(response.status_code, 200)

    def test_reservation_create_view_after_send_form_should_redirect_to_home_page(self):
        response = self.client.post(URL_RESERVATION_CREATE, data=self.form_data)
        self.assertRedirects(response, reverse("index"))

    def test_reservation_with_valid_data(self):
        response = self.client.post(URL_RESERVATION_CREATE, data=self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.name, self.form_data["name"])
        self.assertEqual(reservation.email, self.form_data["email"])
        self.assertEqual(reservation.phone, self.form_data["phone"])
        self.assertEqual(reservation.date_time.strftime("%m/%d/%Y %I:%M %p"), self.form_data["date_time"])
        self.assertEqual(reservation.number_of_people, self.form_data["number_of_people"])
        self.assertEqual(reservation.special_request, self.form_data["special_request"])

    def test_reservation_create_form_validation_date_time(self):
        self.form_data["date_time"] = (datetime.now() - timedelta(minutes=1)).strftime("%m/%d/%Y %I:%M %p")

        form = ReservationForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class ReservationListViewTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(username="Adminuser", password="testpassword")
        self.other_user = get_user_model().objects.create_user(username="Otheruser", password="testpassword")

        # Create some reservations for testing
        self.reservation1 = Reservation.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            phone="1234567890",
            date_time=datetime.now() + timedelta(hours=2),
            number_of_people=2,
            special_request="Special request 1",
        )
        self.reservation2 = Reservation.objects.create(
            name="Jane Smith",
            email="janesmith@example.com",
            phone="0987654321",
            date_time=datetime.now() + timedelta(hours=1),
            number_of_people=4,
            special_request="Special request 2",
        )

    def test_reservation_list_view_should_return_200_for_authenticated_superuser(self):
        self.client.login(username="Adminuser", password="testpassword")
        response = self.client.get(URL_RESERVATION_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.reservation1.name)
        self.assertContains(response, self.reservation2.name)

    def test_reservation_list_view_should_return_302_for_anonymous_user(self):
        response = self.client.get(URL_RESERVATION_LIST)
        self.assertEqual(response.status_code, 302)

    def test_reservation_list_view_should_return_403_for_is_not_superuser(self):
        self.client.login(username="Otheruser", password="testpassword")
        response = self.client.get(URL_RESERVATION_LIST)
        self.assertEqual(response.status_code, 403)

    def test_reservation_search_by_name(self):
        self.client.login(username="Adminuser", password="testpassword")
        response = self.client.get(URL_RESERVATION_LIST, data={"name": "John"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.reservation1.name)
        self.assertNotContains(response, self.reservation2.name)

        response = self.client.get(URL_RESERVATION_LIST, data={"name": "Jane"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.reservation1.name)
        self.assertContains(response, self.reservation2.name)
