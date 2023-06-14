from django.urls import path
from meal.views import (
    MealListView,
    MealDetailView,
    MealUpdateView,
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
    path("menu/<slug:slug>/", MealDetailView.as_view(), name="meal-detail"),
    path("menu/update/<slug:slug>/", MealUpdateView.as_view(), name="meal-update"),
]

app_name = "meal"
