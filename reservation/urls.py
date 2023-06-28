from django.urls import path
from reservation.views import (
    ReservationCreateView,
    ReservationListView,
    # ReservationDetailView,
)


urlpatterns = [
    path("", ReservationCreateView.as_view(), name="reservation"),
    path("list/", ReservationListView.as_view(), name="reservation-list"),
]

app_name = "reservation"
