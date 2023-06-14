from django.urls import path
from meal.views import (
    MealListView,
    MealDetailView,
    MealUpdateView,
    MealCreateView,
    MealDeleteView,
    index,
    about,
    booking,
    CookListView,
    contact,
)


urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("booking/", booking, name="booking"),
    path("team/", CookListView.as_view(), name="team"),
    path("contact/", contact, name="contact"),
    path("menu/", MealListView.as_view(), name="menu"),
    path("create/", MealCreateView.as_view(), name="meal-create"),
    path("<slug:slug>/", MealDetailView.as_view(), name="meal-detail"),
    path("<slug:slug>/update/", MealUpdateView.as_view(), name="meal-update"),
    path("<slug:slug>/delete/", MealDeleteView.as_view(), name="meal-delete"),
]

app_name = "meal"
